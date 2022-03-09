import pandas as pd
from functools import reduce

from oit_stsb.load_cfg import conn_string, table_name
from oit_stsb import load_data, bound_replace
import oit_stsb.category_lists as category_lists


def mean_difficult(df):
    if len(df) == 0:
        return 0

    list_of_difficult_levels = []
    for difficult_level in df:
        if difficult_level.isdigit():
            list_of_difficult_levels.append(int(difficult_level))
    if len(list_of_difficult_levels) > 0:
        return str(round(sum(list_of_difficult_levels) / len(list_of_difficult_levels), 2))
    return 0


def parse_analytics(df, pic_day=False):
    df.analytics = df.analytics.fillna('')

    if pic_day:
        df.analytics = df.analytics.apply(
            lambda x: reduce(bound_replace, ['>', '<', 'Сложность: ', 'Категория обращения: '], x))
        df.analytics = df.analytics.apply(lambda x: x.replace(';', ', '))

    df.analytics = df.analytics.apply(lambda x: x.split(','))

    df['difficult'] = df.analytics.apply(lambda row: [item for item in row if item.strip().isdigit()])
    df['difficult'] = df['difficult'].apply(lambda x: [x[i].strip() for i in range(len(x))])
    df['difficult'] = df['difficult'].apply(lambda x: x[len(x) - 1] if len(x) > 0 else 0)
    df['difficult'] = df['difficult'].astype(int)

    df['categories'] = df.analytics.apply(lambda row: [item for item in row if not item.strip().isdigit()])
    df['categories'] = df['categories'].apply(lambda x: [x[i].strip() for i in range(len(x))])
    df['categories'] = df['categories'].apply(lambda x: x[0] if len(x) > 0 else x)
    df['categories'] = df['categories'].apply(lambda x: '' if x == [] else x)
    df['categories'] = df['categories'].apply(lambda x: 'Не указано/Неверно указано' if x == '' else x)

    df['Subsystem'] = ''
    df.loc[df[df['categories'].isin(category_lists.zkgu_list)].index, 'Subsystem'] = 'ПУОТ'
    df.loc[df[df['categories'].isin(category_lists.bgu_list)].index, 'Subsystem'] = 'ПУНФА‚ ПУиО'
    df.loc[df[df['categories'].isin(category_lists.com_list)].index, 'Subsystem'] = 'Командирование'
    df.loc[df[df['categories'].isin(category_lists.admin_list)].index, 'Subsystem'] = 'Администрирование'
    df.loc[df[df['Subsystem'] == ''].index, 'Subsystem'] = 'Прочие'

    return df


def build_category_table(month, year, person):
    df = load_data(table=table_name,
                   connection_string=conn_string,
                   month=month,
                   year=year)

    df = parse_analytics(df=df)

    if len(df[df['specialist'] == person]) > 0:
        cat_df = df[df['specialist'] == person].pivot_table(
            index=['specialist', 'Subsystem', 'categories'],
            values='difficult',
            aggfunc='mean').reset_index()
        cat_df['difficult'] = cat_df['difficult'].round(2)
        cat_df = cat_df.merge(pd.DataFrame(
            df[df['specialist'] == person].groupby(['categories']).size()).reset_index().rename(
            columns={0: 'cat_count'}), on='categories')
        cat_df['cat_persent'] = round(cat_df['cat_count'] / cat_df['cat_count'].sum() * 100, 2)
        cat_df.columns = ['ФИО', 'Подсистема', 'Категория', 'Средний уровень сложности', 'Количество',
                          'в % от от общего количества']
    else:
        cat_df = pd.DataFrame(columns=['ФИО', 'Подсистема', 'Категория', 'Средний уровень сложности', 'Количество',
                                       'в % от от общего количества'])
    return cat_df
