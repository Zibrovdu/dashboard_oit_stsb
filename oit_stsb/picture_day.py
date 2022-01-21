import base64
import io

import pandas as pd

import oit_stsb.log_writer as lw
from oit_stsb.staff_plus import parse_analytics


def no_data():
    df = pd.DataFrame(columns=['Регион', 'Взято в работу', 'Решено на 2Л', 'В работе', 'Сотрудники', 'Возвраты',
                               'Среднее кол-во заявок/сотрудник'])
    return df


def parse_load_file(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        content_df = pd.read_excel(io.BytesIO(decoded), skiprows=7)

        lw.log_writer(log_msg=f'Файл "{filename}" успешно загружен!')

        return content_df
    except Exception as e:
        lw.log_writer(log_msg=f'При загрузки файла "{filename}" возникла ошибка: {e}')
        content_df = no_data()

        return content_df


def data_table(data_df, filename):
    try:
        data_df.drop(['Unnamed: 0', '№ п/п', 'Приоритет', 'Причина Ожидания', '№ Обращения - Источника эскалации',
                      'Функциональная Область', 'Функция', 'Код Решения Заявки', 'Ошибка ППО Инцидента',
                      'Время Решения Инцидента (план) (MSK)', 'Кем Последний раз переоткрывался Инцидент',
                      'Место оказания услуг', 'Расположение Заявителя Инцидента', 'Описание Инцидента',
                      'Резолюция Решения Инцидента', 'Количество постановок Инцидента в Ожидание'],
                     axis=1,
                     inplace=True)

        if 'Аналитические Признаки Инцидента' not in data_df.columns:
            data_df['analitycs'] = '-'

        data_df.columns = ['task_number', 'reg_date', 'status', 'it-service', 'assign_group', 'solve_date',
                           'specialist', 'solve_date_2', 'is_sla', 'count_of_returns', 'work_time_solve',
                           'count_escalation_tasks', 'analytics']
        data_df.drop(0, inplace=True)
        data_df.reset_index(inplace=True)
        data_df.drop('index', inplace=True, axis=1)
        lw.log_writer(log_msg=f'Файл "{filename}" успешно обработан')

        return data_df, 'Файл успешно загружен'
    except Exception as e:
        lw.log_writer(log_msg=f'Ошибка при обработке файла: "{filename}": {e}')
        lw.log_writer(log_msg=f'Неверный формат файла "{filename}"')
        data_df = no_data()

        return data_df, "Ошибка при обработке файла"


def make_table(content_df, staff_df):
    staff_df.loc[len(staff_df)] = 'Не определено', 'Не определено', 'y', 'y', '', '', '', ''

    merged_df = content_df.merge(staff_df[['fio', 'region', 'works_w_tasks']],
                                 how='left',
                                 left_on='specialist',
                                 right_on='fio')

    merged_df = merged_df[merged_df.assign_group == 'ЦА 1С_Группа сопровождения (ПУНФА, ПУиО, ПУК)']
    merged_df.drop('fio', axis=1, inplace=True)

    if len(merged_df) == 0:
        return pd.DataFrame(columns=[
            'Регион', 'Количество поступивших обращений', 'Из них, решенных на 2Л', 'Из них, в работе',
            'Количество сотрудников', 'Количество возвратов', 'Среднее кол-во обращений на 1 сотрудника'
        ])

    merged_df = parse_analytics(df=merged_df, pic_day=True)

    picture_day_df = merged_df.pivot_table(
        index='region',
        columns='Subsystem',
        values='task_number',
        aggfunc='count',
        fill_value=0,
        observed=True
    )

    picture_day_df = picture_day_df.merge(
        staff_df[(staff_df['works_w_tasks'] == 'y') & (staff_df['state'] == 'y')].pivot_table(
            index='region',
            values=['bgu', 'zkgu', 'admin', 'command'],
            aggfunc='count'
        ).reset_index(),
        on='region')

    if 'Командирование' not in picture_day_df.columns:
        picture_day_df['Командирование'] = 0

    if 'Администрирование' not in picture_day_df.columns:
        picture_day_df['Администрирование'] = 0

    if 'ПУНФА‚ ПУиО' not in picture_day_df.columns:
        picture_day_df['ПУНФА‚ ПУиО'] = 0

    if 'ПУОТ' not in picture_day_df.columns:
        picture_day_df['ПУОТ'] = 0

    if len(picture_day_df.columns) > 6:
        picture_day_df = picture_day_df[['region', 'ПУНФА‚ ПУиО', 'bgu', 'ПУОТ', 'zkgu', 'Администрирование', 'admin',
                                         'Командирование', 'command', 'Прочие']]
    else:
        picture_day_df = picture_day_df[['region', 'bgu', 'zkgu', 'admin', 'command', 'Прочие']]

    picture_day_df = picture_day_df.merge(merged_df.groupby('region')['task_number'].count(), how='outer', on='region')

    picture_day_df = picture_day_df.merge(merged_df.groupby('region')['specialist'].nunique(), how='outer', on='region')

    picture_day_df['delta'] = round(picture_day_df['task_number'] / picture_day_df['specialist'], 1)

    picture_day_df = picture_day_df[['region', 'task_number', 'specialist', 'delta', 'ПУНФА‚ ПУиО', 'bgu', 'ПУОТ',
                                     'zkgu', 'Администрирование', 'admin', 'Командирование', 'command', 'Прочие', ]]

    picture_day_df.columns = [column for column in range(len(picture_day_df.columns))]

    return picture_day_df


def set_picture_day_columns():
    columns = [
        dict(name=['', 'Регион'], id=0),
        dict(name=['Количество', 'обращений'], id=1),
        dict(name=['Количество', 'сотрудников'], id=2),
        dict(name=['Среднее кол-во', 'обращений на сотрудника'], id=3),
        dict(name=['ПУНФА‚ ПУиО', 'Обращения'], id=4),
        dict(name=['ПУНФА‚ ПУиО', 'Сотрудники'], id=5),
        dict(name=['ПУОТ', 'Обращения'], id=6),
        dict(name=['ПУОТ', 'Сотрудники'], id=7),
        dict(name=['Администрирование', 'Обращения'], id=8),
        dict(name=['Администрирование', 'Сотрудники'], id=9),
        dict(name=['Командирование', 'Обращения'], id=10),
        dict(name=['Командирование', 'Сотрудники'], id=11),
        dict(name=['', 'Прочие'], id=12),

    ]
    return columns


def set_picture_day_columns_old():
    columns = [
        dict(name=['Регион', ''], id=0),
        dict(name=['ПУНФА‚ ПУиО', 'Сотрудники'], id=1),
        dict(name=['ПУОТ', 'Сотрудники'], id=2),
        dict(name=['Администрирование', 'Сотрудники'], id=3),
        dict(name=['Командирование', 'Сотрудники'], id=4),
        dict(name=['Прочие', ''], id=5),
        dict(name=['Количество', 'обращений'], id=6),
        dict(name=['Количество', 'сотрудников'], id=7),
        dict(name=['Среднее кол-во', 'обращений на сотрудника'], id=8)
    ]
    return columns


def set_styles(msg):
    if 'Ошибка'.lower() in str(msg).lower():
        style = dict(color='red', fontWeight='bold')
    else:
        style = dict(color='green', fontWeight='bold')
    return style


def load_day_df(connection_string):
    return pd.read_sql(
        """
        SELECT * 
        FROM picture_day 
        WHERE assign_group = 'ЦА 1С_Группа сопровождения (ПУНФА, ПУиО, ПУК)'
        """,
        con=connection_string)
