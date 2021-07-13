import plotly.graph_objects as go
import pandas as pd
import datetime

import oit_stsb.load_cfg


def total_tasks_pie(df, colors):
    pie_labels = df[0]
    pie_values = df[1]
    if not colors:
        colors = ['#09280a', '#446b04', '#e1c1b7', '#b05449', '#dbb238', 'tomato']

    total_task_pie = go.Figure(go.Pie(labels=pie_labels,
                                      values=pie_values,
                                      marker_colors=oit_stsb.load_cfg.color_schemes[colors][:len(df)]))

    total_task_pie.update_traces(hoverinfo="label+percent")

    total_task_pie.update_layout(paper_bgcolor='#ebecf1',
                                 showlegend=True,
                                 title='Инциденты, закрытые группой, из всего потока на 2-й линии')

    return total_task_pie


def make_bars(df, column, norma, colors, name, title):
    if not colors:
        colors = ['#09280a', '#446b04', '#e1c1b7', '#b05449', '#dbb238', 'tomato']

    fig = go.Figure()

    if column == 9:
        fig.add_bar(x=df[0],
                    y=df[column].apply(lambda time: round(int(time.split(':')[0]) +
                                                          int(time.split(':')[1]) / 60 +
                                                          int(time.split(':')[2]) / 3600, 2)),
                    marker_color=oit_stsb.load_cfg.color_schemes[colors][:len(df)],
                    showlegend=False,
                    name='')
        text_line = [str(data) for data in df[column]]
        font_params = dict(color=oit_stsb.load_cfg.color_schemes[colors][len(df)])
    else:
        fig.add_bar(x=df[0],
                    y=df[column],
                    marker_color=oit_stsb.load_cfg.color_schemes[colors][:len(df)],
                    showlegend=False,
                    name='')
        text_line = [str(data) + '%' for data in df[column]]
        font_params = dict(color=oit_stsb.load_cfg.color_schemes[colors][len(df)])

    if column == 12:
        text_line = [str(data) for data in df[column]]

    fig.add_scatter(x=df[0],
                    y=[norma] * len(df),
                    line=dict(width=3, color=oit_stsb.load_cfg.color_schemes[colors][len(df)]),
                    marker=dict(size=3),
                    name=name)

    fig.add_scatter(y=[0] * len(df),
                    x=df[0],
                    line=dict(width=1, color='black'),
                    marker=dict(size=1),
                    mode='lines+markers+text',
                    text=text_line,
                    textposition='top center',
                    textfont=font_params,
                    showlegend=False,
                    name='')

    fig.update_traces(hoverinfo="all")

    fig.update_layout(paper_bgcolor='#ebecf1',
                      title=title,
                      title_xref='paper')

    return fig


def get_meat_count_tasks_per_day_df(table_name, conn_string, month, year):
    count_month_days = oit_stsb.calendar_data.count_month_days(month=month, year=year)
    df = oit_stsb.load_data(table_name, conn_string, month=month, year=year)
    df.reg_date = pd.to_datetime(df.reg_date)
    df['hours'] = df.reg_date.dt.hour

    df = pd.DataFrame(df[(df.reg_date >= datetime.datetime(int(year), int(month), 1)) &
                         (df.reg_date <= datetime.datetime(int(year), int(month), count_month_days))].groupby('hours')
                      ['task_number'].count()).reset_index()

    mask = df[df.hours.isin([x for x in range(2, 7)])].index
    df.loc[mask, 'region'] = 'Владивосток'
    mask = df[df.hours.isin([x for x in range(10, 13)])].index
    df.loc[mask, 'region'] = 'Нижний новгород'
    mask = df[df.hours.isin([x for x in range(13, 16)])].index
    df.loc[mask, 'region'] = 'Владимир'
    mask = df[df.hours.isin([x for x in range(15, 17)])].index
    df.loc[mask, 'region'] = 'Москва'
    mask = df[df.region.isna()].index
    df.loc[mask, 'region'] = 'Новосибирск'

    return df


def plot_meat_count_tasks_per_day(df, colors):
    if not colors:
        colors = ['#09280a', '#446b04', '#e1c1b7', '#b05449', '#dbb238', 'tomato']

    regions_list = sorted(df.region.unique().tolist())

    fig = go.Figure()

    for num, region, in enumerate(regions_list):
        fig.add_bar(x=df[df.region == region].hours,
                    y=df[df.region == region]['task_number'],
                    marker_color=oit_stsb.load_cfg.color_schemes[colors][num],
                    text=df[df.region == region]['task_number'],
                    showlegend=False,
                    name='')
        fig.update_traces(textposition='outside',
                          hoverinfo="all")
        fig.update_layout(uniformtext_minsize=8,
                          uniformtext_mode='hide',
                          paper_bgcolor='#ebecf1',
                          title=oit_stsb.load_cfg.mean_count_tasks_per_day_title,
                          title_xref='paper')
    return fig
