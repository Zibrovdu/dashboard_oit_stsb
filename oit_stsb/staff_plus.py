import pandas as pd

from oit_stsb.load_cfg import conn_string, table_name
from oit_stsb import load_data


def difficult_levels(mark):
    if not mark:
        return pd.DataFrame()

    df = load_data(table=table_name,
                   connection_string=conn_string, )
    df.analytics = df.analytics.fillna('')
    df.analytics = df.analytics.apply(lambda x: x.split(','))

    def get_difficult_level_and_categories(row, marks):
        difficult_list = []
        categories_list = []
        for analytics_list in row:
            if analytics_list.strip().isdigit():
                difficult_list.append(analytics_list.strip())
            else:
                categories_list.append(analytics_list.strip())
        if marks == 'difficult':
            return difficult_list
        else:
            return categories_list

    df[mark] = df.analytics.apply(lambda row: get_difficult_level_and_categories(row=row, marks=mark))

    df[mark] = df[mark].apply(lambda x: ','.join(x))
    df[mark] = df[mark].apply(lambda x: 'Не указано' if x == '' else x)

    df_result = pd.DataFrame(df.groupby(['specialist', mark])[mark].count())
    df_result = df_result.rename(columns={mark: 'counts'}).reset_index()

    return df_result


def set_difficult_levels_columns():
    columns = [
        dict(name=['Сложность'], id='difficult'),
        dict(name=['Количество обращений, шт.'], id='counts'),
    ]
    return columns


def set_categories_columns():
    columns = [
        dict(name=['Категории'], id='categories'),
        dict(name=['Количество обращений, шт.'], id='counts'),
    ]
    return columns
