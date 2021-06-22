import oit_stsb


def make_staff_table(table_name, month, year):
    df = oit_stsb.load_data(table=table_name,
                            month=month,
                            year=year,
                            enq_field='reg_date')
    df = df.groupby('specialist')['task_number'].count().reset_index()
    df.columns = ['specialist', 'tasks_receive']

    # df = df.merge(oit_stsb.df_staff,
    #               left_on='specialist',
    #               right_on='ФИО',
    #               how='left')
    # df.drop(['ФИО', 'Статус'],
    #         axis=1,
    #         inplace=True)
    # df.reset_index(inplace=True)
    # df = df[['specialist', 'Регион', 'tasks_receive']]

    df3 = oit_stsb.load_data(table=table_name)
    df3 = df3[df3.solve_date.isna()].groupby('specialist')['task_number'].count().reset_index()
    df = df.merge(df3,
                  on='specialist',
                  how='left')
    df[['tasks_receive', 'task_number']] = df[['tasks_receive', 'task_number']].fillna(0)
    # df['Регион'] = df['Регион'].fillna('Не определен')
    # for col in [col for col in df.columns if col != 'specialist' and col != 'Регион']:
    #     df[col] = df[col].fillna(0)
    #     df[col] = df[col].astype(int)

    df2 = oit_stsb.make_main_table(table_name=table_name,
                                   month=month,
                                   year=year,
                                   column='specialist').drop([10, 11, 12], axis=1)
    df2 = df2.drop(len(df2) - 1)
    df = df.merge(df2,
                  left_on='specialist',
                  right_on=0,
                  how='outer')
    df.drop(0, axis=1, inplace=True)
    df = df.merge(oit_stsb.df_staff, left_on='specialist', right_on='ФИО', how='left')
    df.drop(['ФИО', 'Статус'], axis=1, inplace=True)
    df.reset_index(inplace=True)

    for col in [col for col in df.columns if col != 'specialist' and col != 'Регион' and col != 9]:
        df[col] = df[col].fillna(0)
        df[col] = df[col].astype(int)
    df['Регион'] = df['Регион'].fillna('Не определен')
    df[9] = df[9].fillna('00:00:00')

    # df = df.fillna(0)

    for i in range(2, 9, 2):
        df[10 + i] = df.apply(lambda row: "".join([str(row[i]), " (", str(row[i - 1]), ")"]), axis=1)
        df.drop([i, i - 1], axis=1, inplace=True)
    df = df[['specialist', 'Регион', 'tasks_receive', 'task_number', 12, 14, 16, 18, 9]]
    df.columns = [i for i in range(9)]

    return df


def set_staff_columns():
    columns = [{'name': ['ФИО сотрудника', ''], 'id': 0},
               {'name': ['Регион', ''], 'id': 1},
               {'name': ['Поступило', ''], 'id': 2},
               {'name': ['В работе', ''], 'id': 3},
               {'name': ['Инциденты, закрытые сотрудником, из всего потока на 2Л', '% (шт.)', ''], 'id': 4},
               {'name': ['Из них (п.1) Иниденты, закрытые без участия 3Л', '% (шт.)', 'Не менее 70%'], 'id': 5},
               {'name': ['Из них (п.2) Инциденты, без нарушение SLA', '% (шт.)', 'не менее 85%'], 'id': 6},
               {'name': ['Из них (п.2) Инциденты, вернувшиеся на доработку', '% (шт.)', 'Не более 10%'], 'id': 7},
               {'name': ['Из них (п.2) Среднее время решения без учета ожидания', 'чч:мм:сс', 'Не более 24ч'],
                'id': 8}
               ]

    return columns
