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
    fig.add_bar(x=df[0],
                y=df[column],
                marker_color=oit_stsb.load_cfg.color_schemes[colors][:len(df)],
                showlegend=False)
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
                    text=[str(x) + '%' for x in df[column]],
                    textposition='top center',
                    textfont=dict(color='black', size=20),
                    showlegend=False)
    fig.update_layout(paper_bgcolor='#ebecf1', title=title)

    return fig
