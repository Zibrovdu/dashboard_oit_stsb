import oit_stsb


def make_staff_table(table_name, month, year):
    df = oit_stsb.load_data(table=table_name,
                            month=month,
                            year=year,
                            enq_field='reg_date')
    df = df.groupby('specialist')['task_number'].count().reset_index()

    df1 = oit_stsb.load_data(table=table_name,
                             month=month,
                             year=year,
                             enq_field='solve_date')
    df1 = df1.groupby('specialist')['task_number'].count().reset_index()

    result = df.merge(df1,
                      how='outer',
                      on='specialist')
    result.columns = ['specialist', 'tasks_receive', 'task_solve']

    result = result.merge(oit_stsb.df_staff,
                          left_on='specialist',
                          right_on='ФИО',
                          how='left')
    result.drop(['ФИО', 'Статус'],
                axis=1,
                inplace=True)
    result.reset_index(inplace=True)
    result = result[['specialist', 'Регион', 'tasks_receive', 'task_solve']]

    df3 = oit_stsb.load_data(table=table_name)
    df3 = df3[df3.solve_date.isna()].groupby('specialist')['task_number'].count().reset_index()
    result = result.merge(df3,
                          on='specialist',
                          how='left')
    result[['tasks_receive', 'task_solve', 'task_number']] = result[['tasks_receive', 'task_solve', 'task_number']].fillna(0)
    result['Регион'] = result['Регион'].fillna('Не определен')
    for col in [col for col in result.columns if col != 'specialist' and col != 'Регион']:
        result[col] = result[col].astype(int)

    df2 = oit_stsb.make_main_table(table_name=table_name,
                                   month=month,
                                   year=year,
                                   column='specialist').drop([10, 11, 12], axis=1)
    df2 = df2.drop(len(df2) - 1)
    result = result.merge(df2,
                          left_on='specialist',
                          right_on=0,
                          how='outer')
    result.drop(0, axis=1, inplace=True)
    result = result.fillna(0)
    result.columns = [i for i in range(14)]

    return result


def set_staff_columns():
    columns = [{'name': ['ФИО сотрудника', ''], 'id': 0},
               {'name': ['Регион', ''], 'id': 1},
               {'name': ['Поступило', ''], 'id': 2},
               {'name': ['Решено', ''], 'id': 3},
               {'name': ['В работе', ''], 'id': 4},
               {'name': ['Инциденты, закрытые группой, из всего потока на 2Л', 'шт.', ''], 'id': 5},
               {'name': ['Инциденты, закрытые группой, из всего потока на 2Л', '%', ''], 'id': 6},
               {'name': ['Из них (п.1) Иниденты, закрытые без участия 3Л', 'шт.', 'Не менее 70%'], 'id': 7},
               {'name': ['Из них (п.1) Иниденты, закрытые без участия 3Л', '%', 'Не менее 70%'], 'id': 8},
               {'name': ['Из них (п.2) Инциденты, без нарушение SLA', 'шт.', 'не менее 85%'], 'id': 9},
               {'name': ['Из них (п.2) Инциденты, без нарушение SLA', '%', 'не менее 85%'], 'id': 10},
               {'name': ['Из них (п.2) Инциденты, вернувшиеся на доработку', 'шт.', 'Не более 10%'], 'id': 11},
               {'name': ['Из них (п.2) Инциденты, вернувшиеся на доработку', '%', 'Не более 10%'], 'id': 12},
               {'name': ['Из них (п.2) Среднее время решения без учета ожидания', 'чч:мм:сс', 'Не более 24ч'],
                'id': 13}]
    return columns
