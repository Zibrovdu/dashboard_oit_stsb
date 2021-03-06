import pandas as pd
import numpy as np
import datetime
from functools import reduce

from oit_stsb.calendar_data import count_month_work_days
from oit_stsb.load_cfg import conn_string, staff_table_name


def bound_replace(string, old):
    """
    Описание:
    ---------
    Функция необходима для корректной обработки файла с данными в части разделения аналитических призканов
    (колонка analytics)

    Returns:
    -------
        **String**
    """
    return string.replace(old, '')


def load_data(table, connection_string, **kwargs):
    """
    Синтаксис:
    ----------

    **load_data** ()

    Описание:
    ---------
    Функция загружает из базы данных информацию об обращениях

    Returns:
    -------
        **DataFrame**
    """
    if not kwargs:
        df = pd.read_sql(f"""
                    SELECT * 
                    FROM {table}
                    WHERE assign_group = 'ЦА 1С_Группа сопровождения (ПУНФА, ПУиО, ПУК)'
                """, con=connection_string)
        return df
    if len(kwargs) == 2:
        df = pd.read_sql(f"""
                    SELECT * 
                    FROM {table}
                    WHERE assign_group = 'ЦА 1С_Группа сопровождения (ПУНФА, ПУиО, ПУК)'
                    AND closed_month = {kwargs['month']}
                    AND closed_year = {kwargs['year']}
                """, con=connection_string)
        return df
    if 'enq_field' in kwargs.keys():
        df = pd.read_sql(f"""
                        SELECT * 
                        FROM {table}
                        WHERE assign_group = 'ЦА 1С_Группа сопровождения (ПУНФА, ПУиО, ПУК)'
                        AND extract(month from {kwargs['enq_field']}) = {kwargs['month']}
                        AND extract(year from {kwargs['enq_field']}) = {kwargs['year']}
                    """, con=connection_string)
        return df
    if 'person' in kwargs.keys():
        df = pd.read_sql(f"""
                    SELECT * 
                    FROM {table}
                    WHERE assign_group = 'ЦА 1С_Группа сопровождения (ПУНФА, ПУиО, ПУК)'
                    AND closed_month = {kwargs['month']}
                    AND closed_year = {kwargs['year']}
                    AND specialist = '{kwargs['person']}'
                """, con=connection_string)
        return df


def load_staff(connection_string, table, **kwargs):
    """
    Синтаксис:
    ----------
    **load_staff** (connection_string, **kwargs)
    Описание:
    ---------
    Функция загружает из базы данных информацию о сотрудниках
    Параметры:
    ----------
    **works** - отбирает только работающих сотрудников и учавствующих в рейтинге;
    **old_staff** - отбирает из базы сотрудников и их адреса электронной почты (требуется для старых данных до
    октября 2020 г., т.к. ранее в графе сотрудник указывалось не ФИО а электроннй адрес сотрудника)
    **update** - Выгрузка сотрудников из базы для картины дня и корректной работы вкладки обновление  
    Returns:
    -------
        **string** or **list of strings**
    """
    if 'works' in kwargs:
        return pd.read_sql(f"""SELECT * FROM {table} where works_w_tasks = 'y' and state = 'y'""",
                           con=connection_string)
    elif 'old_staff' in kwargs:
        return pd.read_sql('''SELECT * FROM old_staff''',
                           con=connection_string)
    elif 'update' in kwargs:
        df = pd.read_sql(f'''SELECT * FROM {table}''',
                         con=connection_string)
        df['state'] = df['state'].apply(lambda x: 'Работает' if x == 'y' else 'Уволен')
        df['works_w_tasks'] = df['works_w_tasks'].apply(lambda x: 'Да' if x == 'y' else 'Нет')
        df['bgu'] = df['bgu'].apply(lambda x: 'Да' if x == 1 else 'Нет')
        df['zkgu'] = df['zkgu'].apply(lambda x: 'Да' if x == 1 else 'Нет')
        df['admin'] = df['admin'].apply(lambda x: 'Да' if x == 1 else 'Нет')
        df['command'] = df['command'].apply(lambda x: 'Да' if x == 1 else 'Нет')

        df.sort_values(['fio'], ascending=True, inplace=True)
        return df
    else:
        return pd.read_sql(f'''SELECT * FROM {table}''',
                           con=connection_string)


def set_upd_staff_columns():
    """
    Синтаксис:
    ----------
    **set_staff_columns** ()
    Описание:
    ---------
    Функция отвечает за отображение названий столбцов в таблице сотрудинки на вкладке Загрузка и обновление данных ->
    Обновление базы сотрудников

    Returns:
    -------
        **Dict**
    """
    col_name_dict = dict(fio=['ФИО', ''], position=['Должность', ''], region=['Регион', ''], state=['Статус', ''],
                         works_w_tasks=['Участие в оценке', ''], bgu=['Подсистемы', 'ПУНФА/ПУИО'],
                         zkgu=['Подсистемы', 'ПУОТ'], admin=['Подсистемы', 'Администрирование'],
                         command=['Подсистемы', 'Командирование']
                         )

    columns = [{'name': name, 'id': index} for index, name in col_name_dict.items()]

    return columns


def get_period_month(year, month):
    """
    Синтаксис:
    ----------

    **get_period_month** (year, month)

    Описание:
    ----------
    Функция принимает на вход номер месяца и год. Возвращает строку 'Месяц год'.

    Параметры:
    ----------
        **year**: *int* - год

        **month**: *int* - номер месяца

    Returns:
    ----------
        **String**
    """
    months = ['', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь',
              'Ноябрь', 'Декабрь']
    period = ' '.join([str(months[month]), str(year)])

    return period


def set_periods(df):
    """
        Синтаксис:
        ----------

        **set_periods** (df)

        Описание:
        ----------
        Функция принимает на вход датафрейм с данными. Возвращает список уникальных значений "Месяц - Год"
        отсортированный по убыванию. Данный список загружается в выпадающий список, из которого пользователь производит
        выбор периода (компонент "month_dd")

        Returns:
        ----------
            **List**
        """
    start_period = [{'label': f"{get_period_month(year=df['solve_date'].min().year, month=i)}",
                     'value': str(i) + '_' + str(df['solve_date'].min().year)}
                    for i in range(df['solve_date'].min().month, 13)]
    end_period = [{'label': f"{get_period_month(year=df['solve_date'].max().year, month=i)}",
                   'value': str(i) + '_' + str(df['solve_date'].max().year)}
                  for i in range(1, df['solve_date'].max().month + 1)]
    if df['solve_date'].max().year - df['solve_date'].min().year <= 1:
        for item in end_period:
            start_period.append(item)
        start_period.reverse()

        return start_period

    else:
        years_list = []
        for count in range(1, (df["solve_date"].max().year -
                               df["solve_date"].min().year)):
            years_list.insert(count, df["solve_date"].min().year + count)

        addition_period = []
        for year in years_list:
            addition_period.append(
                [{"label": f'{get_period_month(year=year, month=i)}', "value": str(i) + '_' + str(year)} for i in
                 range(1, 13)])

    for period in addition_period:
        for item in period:
            start_period.append(item)
    for item in end_period:
        start_period.append(item)
    start_period.reverse()

    return start_period


def make_main_table(table_name, month, year, column, month_work_days):
    df = load_data(table=table_name,
                   connection_string=conn_string,
                   month=month,
                   year=year,
                   enq_field='solve_date')

    merged_df = df.merge(load_staff(connection_string=conn_string, table=staff_table_name, works='works'),
                         left_on='specialist',
                         right_on='fio',
                         how='left')

    merged_df.drop('fio', axis=1, inplace=True)
    merged_df.reset_index(inplace=True)
    merged_df['delta'] = merged_df['solve_date'] - merged_df['reg_date']

    result = merged_df.pivot_table(index=column,
                                   values='task_number',
                                   aggfunc='count').reset_index()

    result.columns = [column, 'num']
    result['persent'] = result['num'].apply(lambda num: round(num / result['num'].sum() * 100, 1))

    pt = merged_df[merged_df['count_escalation_tasks'] == 0].pivot_table(index=column,
                                                                         values='task_number',
                                                                         aggfunc='count').reset_index()
    pt.columns = [column, 'num2']
    result = result.merge(pt, on=column, how='outer')
    result['persent2'] = result.apply(lambda row: round(row['num2'] / row['num'] * 100, 1), axis=1)

    pt = merged_df[(merged_df['count_escalation_tasks'] == 0) &
                   (merged_df['is_sla'] == 'Нет')].pivot_table(index=column,
                                                               values='task_number',
                                                               aggfunc='count').reset_index()
    pt.columns = [column, 'num3']
    result = result.merge(pt, on=column, how='outer')
    result['persent3'] = result.apply(lambda row: round(row['num3'] / row['num2'] * 100, 1), axis=1)

    pt = merged_df[(merged_df['count_escalation_tasks'] == 0) &
                   (merged_df['count_of_returns'] > 0)].pivot_table(index=column,
                                                                    values='task_number',
                                                                    aggfunc='count').reset_index()
    pt.columns = [column, 'num4']
    result = result.merge(pt, on=column, how='outer')
    result['persent4'] = result.apply(lambda row: round(row['num4'] / row['num2'] * 100, 1), axis=1)

    pt = merged_df[merged_df['count_escalation_tasks'] == 0].pivot_table(index=column,
                                                                         values='work_time_solve',
                                                                         aggfunc='mean').reset_index()
    pt.columns = [column, 'num5']
    result = result.merge(pt, on=column, how='outer')

    result['delta'] = result[column].apply(lambda region: merged_df[merged_df[column] == region]['delta'].mean())
    result['delta'] = pd.to_timedelta(result['delta'].values.astype("timedelta64[s]"))

    result['staff'] = result[column].apply(
        lambda region: len(
            merged_df[merged_df[column] == region]['specialist'].unique()))

    result['task_count'] = result.apply(lambda row: round(row['num'] / row['staff'] / month_work_days, 2),
                                        axis=1)

    result.loc[len(result)] = 'Итог:', result['num'].sum(), round(result['persent'].sum()), result['num2'].sum(), \
                              round(result['num2'].sum() / result['num'].sum() * 100, 1), result['num3'].sum(), \
                              round(result['num3'].sum() / result['num2'].sum() * 100, 1), result['num4'].sum(), \
                              round(result['num4'].sum() / result['num2'].sum() * 100, 1), \
                              (result['num2'] * result['num5']).sum() / result['num2'].sum(), result['delta'].mean(), \
                              result['staff'].sum(), round(
        result['num'].sum() / result['staff'].sum() / month_work_days, 2)

    result['delta'] = result['delta'].astype(str).apply(lambda delta: delta.split('.')[0])
    result['num5'] = pd.to_datetime(result['num5'], unit='h').dt.strftime('%H:%M:%S')
    result.columns = [i for i in range(13)]

    return result


def set_main_table_columns():
    columns = [
        dict(name=['Регион', ''], id=0),
        dict(name=['Инциденты, закрытые сотрудником, из всего потока на 2Л', 'шт.', ''], id=1),
        dict(name=['Инциденты, закрытые сотрудником, из всего потока на 2Л', '%', ''], id=2),
        dict(name=['Из них (п.1) Иниденты, закрытые без участия 3Л', 'шт.', 'Не менее 70%'], id=3),
        dict(name=['Из них (п.1) Иниденты, закрытые без участия 3Л', '%', 'Не менее 70%'], id=4),
        dict(name=['Из них (п.2) Инциденты, без нарушение SLA', 'шт.', 'не менее 85%'], id=5),
        dict(name=['Из них (п.2) Инциденты, без нарушение SLA', '%', 'не менее 85%'], id=6),
        dict(name=['Из них (п.2) Инциденты, вернувшиеся на доработку', 'шт.', 'Не более 10%'], id=7),
        dict(name=['Из них (п.2) Инциденты, вернувшиеся на доработку', '%', 'Не более 10%'], id=8),
        dict(name=['Из них (п.2) Среднее время решения без учета ожидания', 'чч:мм:сс', 'Не более 24ч'], id=9,
             type='datetime'),
        dict(name=['Среднее время с момента регистрации обращения до момента выполнения',
                   '(разница между датой регистрации и датой решения)', ''], id=10),
        dict(name=['Количество сотрудников', ], id=11),
        dict(name=['Среднее кол-во Инцидентов на сотрудника в день', 'шт.', 'Не менее 6 шт'], id=12)]
    return columns


def read_history_data():
    history_data = ''
    with open('assets/history.txt', 'r', encoding="utf8") as history_text_file:
        for line in history_text_file:
            history_data += line
        return history_data


def save_date(df, connection_string):
    date_picture_day = pd.DataFrame([df['reg_date'].max().date().strftime("%d-%m-%Y")], columns=['update_date'])
    date_picture_day.to_sql('date_picture_day', con=connection_string, if_exists='replace', index=False)
    return date_picture_day.loc[0][0]


def load_date(connection_string):
    date_picture_day = pd.read_sql('date_picture_day', con=connection_string)
    return date_picture_day.loc[0][0]


def load_data_from_file(df):
    for col in ['reg_date', 'solve_date', 'solve_date_2']:
        df[col] = pd.to_datetime(df[col])
    df['closed_month'] = df['solve_date_2'].apply(lambda x: x.month)
    df['closed_year'] = df['solve_date_2'].apply(lambda x: x.year)
    df = df[(df.solve_date >= datetime.datetime(2020, 10, 1)) | (df.solve_date.isna())]
    df = df[df.assign_group == 'ЦА 1С_Группа сопровождения (ПУНФА, ПУиО, ПУК)']

    old_staff_df = load_staff(connection_string=conn_string, table=staff_table_name, old_staff='old_staff')
    for item in df[df['specialist'].str.contains('@')].specialist.unique():
        if item in old_staff_df[old_staff_df.mail.str.contains('@')].mail.unique():
            mask = df[df.specialist == item].index
            df.loc[mask, 'specialist'] = old_staff_df[old_staff_df.mail == item].fio.iloc[0]
    df['specialist'] = df['specialist'].fillna('Не определено')

    df.analytics = df.analytics.fillna('-')
    df.analytics = df.analytics.apply(
        lambda x: reduce(bound_replace, ['>', '<', 'Сложность: ', 'Категория обращения: '], x))
    df.analytics = df.analytics.apply(lambda x: x.replace(';', ', '))

    return df


def get_filter_options(df, filter_name):
    if filter_name == 'state':
        filter_query_options = [{'label': i, 'value': i} for i in df['state'].unique()]
    elif filter_name == 'works_w_tasks':
        filter_query_options = [{'label': i, 'value': i} for i in df['works_w_tasks'].unique()]
    elif filter_name == 'fio':
        filter_query_options = [{'label': i, 'value': i} for i in df['fio'].unique()]
    else:
        filter_query_options = [{'label': i, 'value': i} for i in df['region'].unique()]
    filter_query_options.insert(0, dict(label='Все', value='Все'))

    return filter_query_options


def make_row(fio, position, region, work, task, subs):
    if work == 'Работает':
        work = 'y'
    else:
        work = 'n'
    if task == 'Да':
        task = 'y'
    else:
        task = 'n'
    if subs == 'ПУНФА/ПУИО':
        row = [fio, position, region, work, task, 1, np.nan, np.nan, np.nan]
    elif subs == 'ПУОТ':
        row = [fio, position, region, work, task, np.nan, 1, np.nan, np.nan]
    elif subs == 'Администрирование':
        row = [fio, position, region, work, task, np.nan, np.nan, 1, np.nan]
    elif subs == 'Командирование':
        row = [fio, position, region, work, task, np.nan, np.nan, np.nan, 1]
    else:
        row = [fio, position, region, work, task, np.nan, np.nan, np.nan, np.nan]
    return row
