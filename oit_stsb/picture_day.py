import base64
import io

import numpy as np
import pandas as pd

import oit_stsb.log_writer as lw


def no_data():
    df = pd.DataFrame(columns=['Регион', 'Взято в работу', 'Решено на 2Л', 'В работе', 'Сотрудники', 'Возвраты',
                               'Среднее кол-во заявок/сотрудник'])
    return df


def parse_load_file(contents, filename):
    content_type, content_string = contents.split(',')
    with open('content.txt', 'w') as f:
        f.write(contents)
        f.close()
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
        data_df.columns = ['task_number', 'reg_date', 'status', 'it-service', 'assign_group', 'solve_date',
                           'specialist',
                           'solve_date_2', 'is_sla', 'count_of_returns', 'work_time_solve', 'count_escalation_tasks']
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
    staff_df.loc[105] = 'Не определено', 'Не определено', 'y', 'y'
    merged_df = content_df.merge(staff_df[['fio', 'region', 'works_w_tasks']],
                                 how='left',
                                 left_on='specialist',
                                 right_on='fio')
    merged_df = merged_df[merged_df.assign_group == 'ЦА 1С_Группа сопровождения (ПУНФА, ПУиО, ПУК)']
    merged_df.drop('fio', axis=1, inplace=True)

    if len(merged_df) == 0:
        return pd.DataFrame(columns=['Регион', 'Количество обращений, взятых в работу',
                                     'Количество обращений решенных на 2Л', 'Количество обращений в работе',
                                     'Количество сотрудников', 'Количество возвратов',
                                     'Среднее кол-во заявок на 1 сотрудника'])

    picture_day_df = merged_df.pivot_table(index='region', values='task_number', aggfunc='count').reset_index()

    if len(merged_df[merged_df.solve_date.notna()]) == 0:
        picture_day_df['solved_tasks'] = 0
    else:
        picture_day_df = picture_day_df.merge(merged_df[merged_df.solve_date.notna()].pivot_table(index='region',
                                                                                                  values='task_number',
                                                                                                  aggfunc='count').
                                              rename(columns={'task_number': 'solved_tasks'}).reset_index(),
                                              on='region',
                                              how='left')
    if len(merged_df[merged_df.solve_date.isna()]) == 0:
        picture_day_df['in_work_task'] = 0
    else:
        picture_day_df = picture_day_df.merge(merged_df[merged_df.solve_date.isna()].pivot_table(index='region',
                                                                                                 values='task_number',
                                                                                                 aggfunc='count').
                                              rename(columns={'task_number': 'in_work_task'}).reset_index(),
                                              on='region',
                                              how='left')
    picture_day_df = picture_day_df.merge(merged_df.pivot_table(index='region',
                                                                values='specialist',
                                                                aggfunc=pd.Series.nunique).reset_index(),
                                          on='region',
                                          how='left')
    if len(merged_df[merged_df.count_of_returns > 0]) == 0:
        picture_day_df['count_of_returns'] = 0
    else:
        picture_day_df = picture_day_df.merge(
            merged_df[merged_df.count_of_returns > 0].pivot_table(index='region',
                                                                  values='count_of_returns',
                                                                  aggfunc=np.sum).reset_index(),
            on='region',
            how='left')

    picture_day_df['average'] = round(picture_day_df['task_number'] / picture_day_df['specialist'], 2)

    picture_day_df.fillna(0, inplace=True)

    for column in [x for x in picture_day_df.columns if x != 'region' and x != 'average']:
        picture_day_df[column] = picture_day_df[column].astype(int)

    picture_day_df.columns = ['Регион', 'Количество обращений, взятых в работу', 'Количество обращений решенных на 2Л',
                              'Количество обращений в работе', 'Количество сотрудников', 'Количество возвратов',
                              'Среднее кол-во заявок на 1 сотрудника']
    return picture_day_df


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
