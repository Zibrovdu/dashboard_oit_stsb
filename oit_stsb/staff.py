import pandas as pd

import oit_stsb
from oit_stsb.load_cfg import conn_string


def count_statistic(income_df, column):
    df = pd.DataFrame(income_df[column])
    df.sort_values(column, inplace=True)

    irq = df[column].iloc[int(len(df[column]) / 2):].median() - df[column].iloc[:int(len(df[column]) / 2)].median()

    outlier_low = (df[column].iloc[:int(len(df[column]) / 2)].median()) - (1.5 * irq)
    outlier_high = (df[column].iloc[int(len(df[column]) / 2):].median()) + (1.5 * irq)

    return int(df[(df[column] > outlier_low) & (df[column] < outlier_high)].median().iloc[0])


def make_staff_table(table_name, month, year, month_work_days):
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
                                   column='specialist',
                                   month_work_days=month_work_days).drop([10, 11, 12], axis=1)
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

    for col in [col for col in df.columns if col not in ['specialist', 'region', 9, 'works_w_tasks', 'position']]:
        df[col] = df[col].fillna(0)
        df[col] = df[col].astype(int)
    df['region'] = df['region'].fillna('Не определен')
    df[9] = df[9].fillna('00:00:00')
    df['specialist'] = df['specialist'].apply(lambda x: x.title())

    df = df[df['works_w_tasks'] == 'y']

    df = df.sort_values(1, ascending=False)

    df['mean'] = df[1].apply(lambda x: x - count_statistic(income_df=df,
                                                           column=1))

    df = df[['specialist', 'position', 'region', 1, 'mean', 'tasks_receive', 'task_number', 4, 6, 8, 9]]

    df.columns = [i for i in range(11)]

    return df


def set_staff_columns(mv):
    columns = [
        dict(name=['ФИО сотрудника', ''], id=0),
        dict(name=['Должность', ''], id=1),
        dict(name=['Регион', ''], id=2),
        dict(name=['Решено', 'шт.'], id=3),
        dict(name=['Отклонение', f'(Среднее {mv})'], id=4),
        dict(name=['В работе', 'шт.'], id=5),
        dict(name=['Поступило', 'шт.'], id=6),
        dict(name=['Иниденты, закрытые без участия 3Л, %', 'Не менее 70%'], id=7),
        dict(name=['Инциденты, без нарушение SLA, %', 'не менее 85%'], id=8),
        dict(name=['Инциденты, вернувшиеся на доработку, %', 'Не более 10%'], id=9),
        dict(name=['Среднее время решения без учета ожидания', 'чч:мм:сс, Не более 24ч'], id=10)
    ]

    return columns
