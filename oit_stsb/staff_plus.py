import pandas as pd

from oit_stsb.load_cfg import conn_string, table_name
from oit_stsb import load_data


def difficult_levels(mark, month, year):
    if not mark:
        return pd.DataFrame()

    df = load_data(table=table_name,
                   connection_string=conn_string,
                   month=month,
                   year=year)
    df.analytics = df.analytics.fillna('')
    df.analytics = df.analytics.apply(lambda x: x.split(','))

    if mark == 'difficult':
        df[mark] = df.analytics.apply(lambda row: [item for item in row if item.strip().isdigit()])
        df[mark] = df[mark].apply(lambda x: [x[i].strip() for i in range(len(x))])
        df[mark] = df[mark].apply(lambda x: x[len(x) - 1] if len(x) > 0 else 'Не указано')
    else:
        df[mark] = df.analytics.apply(lambda row: [item for item in row if not item.strip().isdigit()])
        df[mark] = df[mark].apply(lambda x: [x[i].strip() for i in range(len(x))])
        df[mark] = df[mark].apply(lambda x: ', '.join(x))
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


def mean_difficult(df):
    if len(df) == 0:
        return 0

    list_of_difficult_levels = []
    for difficult_level in df:
        if difficult_level.isdigit():
            list_of_difficult_levels.append(int(difficult_level))
    if len(list_of_difficult_levels) > 0:
        return str(round(sum(list_of_difficult_levels)/len(list_of_difficult_levels), 2))
    return 0
