import plotly.graph_objects as go

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
                                                          int(time.split(':')[1])/60 +
                                                          int(time.split(':')[2])/3600, 2)),
                    marker_color=oit_stsb.load_cfg.color_schemes[colors][:len(df)],
                    showlegend=False)
        text_line = [str(data) for data in df[column]]
        font_params = dict(color='black', size=16)
    else:
        fig.add_bar(x=df[0],
                    y=df[column],
                    marker_color=oit_stsb.load_cfg.color_schemes[colors][:len(df)],
                    showlegend=False)
        text_line = [str(data) + '%' for data in df[column]]
        font_params = dict(color='black', size=20)

    if column == 12:
        text_line = [str(data) for data in df[column]]

    fig.add_scatter(x=df[0],
                    y=[norma for index in range(len(df))],
                    line=dict(width=3, color=oit_stsb.load_cfg.color_schemes[colors][len(df)]),
                    marker=dict(size=3),
                    name=name)

    fig.add_scatter(y=[0 for o in range(len(df))],
                    x=df[0],
                    line=dict(width=1, color='black'),
                    marker=dict(size=1),
                    mode='lines+markers+text',
                    text=text_line,
                    textposition='top center',
                    textfont=font_params,
                    showlegend=False)

    fig.update_layout(paper_bgcolor='#ebecf1',
                      title=title,
                      title_xref='paper')

    return fig
