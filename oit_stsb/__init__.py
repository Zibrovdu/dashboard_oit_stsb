import pandas as pd

from oit_stsb.load_cfg import engine

df_staff = pd.read_excel(r'assets/Список сотрудников ОИТСЦБ.xlsx')


def load_data(table, **kwargs):
    """
    Синтаксис:
    ----------

    **load_etsp_data** ()

    Описание:
    ---------
    Функция загружает из базы данных информацию об обращениях по техподдержке ЕЦП

    Returns:
    -------
        **DataFrame**
    """
    if not kwargs:
        df = pd.read_sql(f"""
                    SELECT * 
                    FROM {table}
                    WHERE assign_group = 'ЦА 1С_Группа сопровождения (ПУНФА, ПУиО, ПУК)'
                """, con=engine)
        return df
    if len(kwargs) == 2:
        df = pd.read_sql(f"""
                    SELECT * 
                    FROM {table}
                    WHERE assign_group = 'ЦА 1С_Группа сопровождения (ПУНФА, ПУиО, ПУК)'
                    AND closed_month = {kwargs['month']}
                    AND closed_year = {kwargs['year']}
                """, con=engine)
        return df


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
    start_period = [{"label": f'{get_period_month(year=df["solve_date"].min().year, month=i)}',
                     "value": str(i) + '_' + str(df["solve_date"].min().year)}
                    for i in range(df["solve_date"].min().month, 13)]
    end_period = [{"label": f'{get_period_month(year=df["solve_date"].max().year, month=i)}',
                   "value": str(i) + '_' + str(df["solve_date"].max().year)}
                  for i in range(1, df["solve_date"].max().month + 1)]
    if df["solve_date"].max().year - df["solve_date"].min().year <= 1:
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


def make_main_table(table_name, month, year):
    df = load_data(table=table_name, month=month, year=year)
    merged_df = df.merge(df_staff,
                         left_on='specialist',
                         right_on='ФИО',
                         how='left')
    merged_df.drop('ФИО', axis=1, inplace=True)
    merged_df.reset_index(inplace=True)

    result = merged_df.pivot_table(index='Регион',
                                   values='task_number',
                                   aggfunc='count').reset_index()
    result.columns = ['Регион', 'num']
    result['persent'] = result.num.apply(lambda x: round(x / result.num.sum() * 100, 1))

    pt = merged_df[merged_df.count_escalation_tasks == 0].pivot_table(index='Регион',
                                                                      values='task_number',
                                                                      aggfunc='count').reset_index()
    pt.columns = ['Регион', 'num2']
    result = result.merge(pt, on='Регион')
    result['persent2'] = result.apply(lambda x: round(x.num2 / x.num * 100, 1), axis=1)

    pt = merged_df[(merged_df.count_escalation_tasks == 0) &
                   (merged_df.is_sla == 'Нет')].pivot_table(index='Регион',
                                                            values='task_number',
                                                            aggfunc='count').reset_index()
    pt.columns = ['Регион', 'num3']
    result = result.merge(pt, on='Регион')
    result['persent3'] = result.apply(lambda x: round(x.num3 / x.num2 * 100, 1), axis=1)

    pt = merged_df[(merged_df.count_escalation_tasks == 0) &
                   (merged_df.count_of_returns > 0)].pivot_table(index='Регион',
                                                                 values='task_number',
                                                                 aggfunc='count').reset_index()
    pt.columns = ['Регион', 'num4']
    result = result.merge(pt, on='Регион')
    result['persent4'] = result.apply(lambda x: round(x.num4 / x.num2 * 100, 1), axis=1)

    pt = merged_df[merged_df.count_escalation_tasks > 0].pivot_table(index='Регион', values='work_time_solve',
                                                                     aggfunc='mean').reset_index()
    pt.columns = ['Регион', 'num5']
    result = result.merge(pt, on='Регион')

    result.loc[len(result)] = 'Итог:', result.num.sum(), round(result.persent.sum()), result.num2.sum(), \
                              round(result.num2.sum() / result.num.sum() * 100, 1), result.num3.sum(), \
                              round(result.num3.sum() / result.num2.sum() * 100, 1), result.num4.sum(), \
                              round(result.num4.sum() / result.num2.sum() * 100, 1), \
                              (result.num2 * result.num5).sum() / result.num2.sum()

    result.num5 = pd.to_datetime(result.num5, unit='h').dt.strftime('%H:%M:%S')
    result.columns = [i for i in range(10)]

    # result.columns = ([['Регион', 'Инциденты, закрытые группой, из всего потока на 2Л',
    #                     'Инциденты, закрытые группой, из всего потока на 2Л',
    #                     'Из них (п.1) Иниденты, закрытые без участия 3Л',
    #                     'Из них (п.1) Иниденты, закрытые без участия 3Л',
    #                     'Из них (п.2) Инциденты, без нарушение SLA', 'Из них (п.2) Инциденты, без нарушение SLA',
    #                     'Из них (п.2) Инциденты, вернувшиеся на доработку',
    #                     'Из них (п.2) Инциденты, вернувшиеся на доработку'],
    #                    ['', 'шт.', '%', 'шт.', '%', 'шт.', '%', 'шт.', '%']
    #                    ])
    return result


def set_columns():
    columns = [{'name': ['Регион', ''], 'id': 0},
               {'name': ['Инциденты, закрытые группой, из всего потока на 2Л', 'шт.', ''],
                'id': 1},
               {'name': ['Инциденты, закрытые группой, из всего потока на 2Л', '%', ''],
                'id': 2},
               {'name': ['Из них (п.1) Иниденты, закрытые без участия 3Л', 'шт.', 'Не менее 70%'], 'id': 3},
               {'name': ['Из них (п.1) Иниденты, закрытые без участия 3Л', '%', 'Не менее 70%'], 'id': 4},
               {'name': ['Из них (п.2) Инциденты, без нарушение SLA', 'шт.', 'не менее 85%'], 'id': 5},
               {'name': ['Из них (п.2) Инциденты, без нарушение SLA', '%', 'не менее 85%'], 'id': 6},
               {'name': ['Из них (п.2) Инциденты, вернувшиеся на доработку', 'шт.', 'Не более 10%'],
                'id': 7},
               {'name': ['Из них (п.2) Инциденты, вернувшиеся на доработку', '%', 'Не более 10%'], 'id': 8},
               {'name': ['Из них (п.2) Среднее время решения без учета ожидания', 'чч:мм:сс', 'Не более 24ч'], 'id': 9,
                'type': 'datetime'}]
    return columns
