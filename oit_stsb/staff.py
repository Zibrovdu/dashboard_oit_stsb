import pandas as pd

import oit_stsb
from oit_stsb.load_cfg import conn_string


def count_statistic(income_df, column):
    df = pd.DataFrame(income_df[column])
    df.sort_values(column, inplace=True)

    irq = df[column].loc[int(len(df[column]) / 2):].median() - df[column].loc[:int(len(df[column]) / 2)].median()

    outlier_low = (df[column].loc[:int(len(df[column]) / 2)].median()) - (1.5 * irq)
    outlier_high = (df[column].loc[int(len(df[column]) / 2):].median()) + (1.5 * irq)

    return int(df[(df[column] > outlier_low) & (df[column] < outlier_high)].median().iloc[0])


def make_staff_table(table_name, month, year):
    df = oit_stsb.load_data(table=table_name,
                            connection_string=conn_string,
                            month=month,
                            year=year,
                            enq_field='reg_date')
    df = df.groupby('specialist')['task_number'].count().reset_index()
    df.columns = ['specialist', 'tasks_receive']

    df3 = oit_stsb.load_data(table=table_name,
                             connection_string=conn_string)
    df3 = df3[df3.solve_date.isna()].groupby('specialist')['task_number'].count().reset_index()
    df = df.merge(df3,
                  on='specialist',
                  how='left')
    df[['tasks_receive', 'task_number']] = df[['tasks_receive', 'task_number']].fillna(0)

    df2 = oit_stsb.make_main_table(table_name=table_name,
                                   month=month,
                                   year=year,
                                   column='specialist').drop([10, 11, 12], axis=1)
    df2 = df2.drop(len(df2) - 1)
    df = df.merge(df2,
                  left_on='specialist',
                  right_on=0,
                  how='outer')
    df.drop(0,
            axis=1,
            inplace=True)
    df = df.merge(oit_stsb.load_staff(connection_string=conn_string),
                  left_on='specialist',
                  right_on='fio',
                  how='left')
    df.drop(['fio', 'state'],
            axis=1,
            inplace=True)
    df.reset_index(inplace=True)

    for col in [col for col in df.columns if col not in ['specialist', 'region', 9, 'works_w_tasks']]:
        df[col] = df[col].fillna(0)
        df[col] = df[col].astype(int)
    df['region'] = df['region'].fillna('Не определен')
    df[9] = df[9].fillna('00:00:00')
    df['specialist'] = df['specialist'].apply(lambda x: x.title())

    for i in range(4, 9, 2):
        df[10 + i] = df.apply(lambda row: "".join([str(row[i]), " (", str(row[i - 1]), ")"]),
                              axis=1)
        df.drop([i, i - 1],
                axis=1,
                inplace=True)
    df = df[df['works_w_tasks'] == 'y']
    df = df.sort_values(1, ascending=False)
    df['mean'] = df[1].apply(lambda x: x - count_statistic(income_df=df,
                                                           column=1))
    df = df[['specialist', 'region', 1, 'mean', 'tasks_receive', 'task_number', 14, 16, 18, 9]]

    df.columns = [i for i in range(10)]

    return df


def set_staff_columns(mv):
    columns = [{'name': ['ФИО сотрудника', ''], 'id': 0},
               {'name': ['Регион', ''], 'id': 1},
               {'name': ['Решено', 'шт.'], 'id': 2},
               {'name': ['Отклонение', f'(Среднее {mv})'], 'id': 3},
               {'name': ['В работе', 'шт.'], 'id': 4},
               {'name': ['Поступило', 'шт.'], 'id': 5},
               {'name': ['Иниденты, закрытые без участия 3Л', '% (шт.)', 'Не менее 70%'], 'id': 6},
               {'name': ['Инциденты, без нарушение SLA', '% (шт.)', 'не менее 85%'], 'id': 7},
               {'name': ['Инциденты, вернувшиеся на доработку', '% (шт.)', 'Не более 10%'], 'id': 8},
               {'name': ['Среднее время решения без учета ожидания', 'чч:мм:сс', 'Не более 24ч'],
                'id': 9}
               ]

    return columns