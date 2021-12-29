import pandas as pd
from oit_stsb import load_data, load_staff
from oit_stsb.load_cfg import conn_string, table_name
from oit_stsb.staff_plus import parse_analytics


def create_kpi_table(month, year, small=True):
    df = load_data(table=table_name,
                   connection_string=conn_string,
                   month=month,
                   year=year)

    df = parse_analytics(df=df)

    if small:
        main_table = df.pivot_table(index=['Subsystem'],
                                    values=['work_time_solve', 'difficult'],
                                    aggfunc='mean').reset_index() \
            .rename(columns={'Subsystem': 'Категория',
                             'difficult': 'Средняя сложность',
                             'work_time_solve': 'Среднее время решения'}
                    )
        table_wo_3l = df[df['count_escalation_tasks'] == 0].pivot_table(index=['Subsystem'],
                                                                        values='task_number',
                                                                        aggfunc='count') \
            .reset_index().rename(columns={'Subsystem': 'Категория',
                                           'task_number': 'Количество обращений закрытые без участия 3Л'}
                                  )
    else:
        main_table = df.pivot_table(index=['categories'],
                                    values=['work_time_solve', 'difficult'],
                                    aggfunc='mean').reset_index() \
            .rename(columns={'categories': 'Категория',
                             'difficult': 'Средняя сложность',
                             'work_time_solve': 'Среднее время решения'}
                    )
        table_wo_3l = df[df['count_escalation_tasks'] == 0].pivot_table(index=['categories'],
                                                                        values='task_number',
                                                                        aggfunc='count') \
            .reset_index().rename(columns={'categories': 'Категория',
                                           'task_number': 'Количество обращений закрытые без участия 3Л'}
                                  )

    result_df = main_table.merge(table_wo_3l, how='outer', on='Категория')

    for column in ['Средняя сложность', 'Среднее время решения']:
        result_df[column] = result_df[column].round(2)

    return result_df


def kpi_table(month, year, small=True):
    df = load_data(table=table_name,
                   connection_string=conn_string,
                   month=month,
                   year=year,
                   enq_field='solve_date')

    df = df.merge(load_staff(connection_string=conn_string),
                  left_on='specialist',
                  right_on='fio',
                  how='left')
    df.drop('fio', axis=1, inplace=True)
    df.reset_index(inplace=True)

    df = parse_analytics(df=df)

    if small:
        merged_df = pd.DataFrame(columns=['Subsystem'])
        for region in df.region.unique():
            merged_df = merged_df.merge(
                df[(df['count_escalation_tasks'] == 0) & (df.region == region)].pivot_table(
                    index=['Subsystem'], values='task_number', aggfunc='count').reset_index(),
                how='outer',
                on=['Subsystem']
            )
            merged_df = merged_df.merge(
                df[df.region == region].pivot_table(
                    index=['Subsystem'], values=['work_time_solve'], aggfunc='mean').reset_index(),
                how='outer',
                on=['Subsystem'])

    else:
        merged_df = pd.DataFrame(columns=['Subsystem', 'categories'])
        for region in df.region.unique():
            merged_df = merged_df.merge(df[(df['count_escalation_tasks'] == 0) &
                                           (df.region == region)].pivot_table(
                index=['Subsystem', 'categories'], values='task_number', aggfunc='count').reset_index().rename(
                columns={'task_number': f'3l_task_{region}'}),
                how='outer',
                on=['Subsystem', 'categories'])

            merged_df = merged_df.merge(df[df.region == region].pivot_table(index=['Subsystem', 'categories'],
                                                                            values=['task_number', 'work_time_solve',
                                                                                    'difficult'],
                                                                            aggfunc={'task_number': 'count',
                                                                                     'work_time_solve': 'mean',
                                                                                     'difficult': 'mean'}
                                                                            ).reset_index().rename(
                columns={'task_number': f'task_{region}',
                         'work_time_solve': f'work_{region}',
                         'difficult': f'dif_{region}'}),
                how='outer',
                on=['Subsystem', 'categories'])
        merged_df = merged_df[
                ['Subsystem', 'categories', 'task_Москва', '3l_task_Москва', 'work_Москва', 'dif_Москва',
                 'task_Владимир', '3l_task_Владимир', 'work_Владимир', 'dif_Владимир',
                 'task_Нижний Новгород', '3l_task_Нижний Новгород', 'work_Нижний Новгород', 'dif_Нижний Новгород',
                 'task_Новосибирск', '3l_task_Новосибирск', 'work_Новосибирск', 'dif_Новосибирск',
                 'task_Владивосток', '3l_task_Владивосток', 'work_Владивосток', 'dif_Владивосток'
                 ]
            ]

    merged_df['id'] = 0
    merged_df.loc[merged_df[merged_df.Subsystem == 'ПУНФА‚ ПУиО'].index, 'id'] = 1
    merged_df.loc[merged_df[merged_df.Subsystem == 'ПУОТ'].index, 'id'] = 2
    merged_df.loc[merged_df[merged_df.Subsystem == 'Командирование'].index, 'id'] = 3
    merged_df.loc[merged_df[merged_df.Subsystem == 'Администрирование'].index, 'id'] = 4
    merged_df.loc[merged_df[merged_df.Subsystem == 'Прочие'].index, 'id'] = 5
    merged_df = merged_df.sort_values('id')
    merged_df.drop('id', axis=1, inplace=True)

    merged_df = merged_df.round(2)
    merged_df = merged_df.fillna(0)
    merged_df.columns = [i for i in range(len(merged_df.columns))]

    return merged_df


def set_kpi_columns():
    kpi_columns = [
        dict(name=['Подсистема/Регион', ''], id=0),
        dict(name=['Москва', 'Решено без 3Л'], id=1),
        dict(name=['Москва', 'Время решения'], id=2),
        dict(name=['Владимир', 'Решено без 3Л'], id=3),
        dict(name=['Владимир', 'Время решения'], id=4),
        dict(name=['Нижний Новгород', 'Решено без 3Л'], id=5),
        dict(name=['Нижний Новгород', 'Время решения'], id=6),
        dict(name=['Новосибирск', 'Решено без 3Л'], id=7),
        dict(name=['Новосибирск', 'Время решения'], id=8),
        dict(name=['Владивосток', 'Решено без 3Л'], id=9),
        dict(name=['Владивосток', 'Время решения'], id=10)
    ]
    return kpi_columns


def set_kpi_columns_big():
    kpi_columns = [
        dict(name=['Подсистема', 'Подсистема'], id=0),
        dict(name=['Категория', 'Категория'], id=1),
        dict(name=['Москва', 'Решено'], id=2),
        dict(name=['Москва', 'Решено без 3Л'], id=3),
        dict(name=['Москва', 'Время решения'], id=4),
        dict(name=['Москва', 'Сложность'], id=5),

        dict(name=['Владимир', 'Решено'], id=6),
        dict(name=['Владимир', 'Решено без 3Л'], id=7),
        dict(name=['Владимир', 'Время решения'], id=8),
        dict(name=['Владимир', 'Сложность'], id=9),

        dict(name=['Нижний Новгород', 'Решено'], id=10),
        dict(name=['Нижний Новгород', 'Решено без 3Л'], id=11),
        dict(name=['Нижний Новгород', 'Время решения'], id=12),
        dict(name=['Нижний Новгород', 'Сложность'], id=13),

        dict(name=['Новосибирск', 'Решено'], id=14),
        dict(name=['Новосибирск', 'Решено без 3Л'], id=15),
        dict(name=['Новосибирск', 'Время решения'], id=16),
        dict(name=['Новосибирск', 'Сложность'], id=17),

        dict(name=['Владивосток', 'Решено'], id=18),
        dict(name=['Владивосток', 'Решено без 3Л'], id=19),
        dict(name=['Владивосток', 'Время решения'], id=20),
        dict(name=['Владивосток', 'Сложность'], id=21),

    ]
    return kpi_columns
