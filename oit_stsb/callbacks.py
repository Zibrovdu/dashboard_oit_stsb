import dash
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

import oit_stsb
import oit_stsb.figures
import oit_stsb.staff
from oit_stsb.load_cfg import table_name, tasks_closed_wo_3l


def register_callbacks(app):
    @app.callback(
        Output('main_table', 'data'),
        Output('main_table', 'columns'),
        Output('total_task_pie', 'figure'),
        Output('inc_close_wo_3l', 'figure'),
        Output('inc_wo_sla_violation', 'figure'),
        Output('inc_back_work', 'figure'),
        Output('mean_time_solve_wo_waiting', 'figure'),
        Output('mean_count_tasks_per_empl_per_day', 'figure'),
        Output('staff_table', 'data'),
        Output('staff_table', 'columns'),
        Input('month_dd', 'value'),
        Input('choose_colorscheme', 'value'),
        # Input('filter_btn', 'n_clicks'),
        # State('form_filter', 'children')
    )
    def update_table(value, colors):

        month, year = value.split('_')

        data_df = oit_stsb.make_main_table(table_name=table_name,
                                           month=month,
                                           year=year,
                                           column='region')

        columns = oit_stsb.set_columns()

        total_task_pie_g = oit_stsb.figures.total_tasks_pie(df=data_df.loc[:len(data_df) - 2],
                                                            colors=colors)

        inc_close_wo_3l = oit_stsb.figures.make_bars(df=data_df.loc[:len(data_df) - 2],
                                                     column=4,
                                                     norma=tasks_closed_wo_3l,
                                                     colors=colors,
                                                     name=oit_stsb.load_cfg.tasks_closed_wo_3l_name,
                                                     title=oit_stsb.load_cfg.tasks_closed_wo_3l_title)

        inc_wo_sla_violation_graph = oit_stsb.figures.make_bars(df=data_df.loc[:len(data_df) - 2],
                                                                column=6,
                                                                norma=oit_stsb.load_cfg.tasks_wo_sla_violation,
                                                                colors=colors,
                                                                name=oit_stsb.load_cfg.tasks_wo_sla_violation_name,
                                                                title=oit_stsb.load_cfg.tasks_wo_sla_violation_title)

        inc_back_work_graph = oit_stsb.figures.make_bars(df=data_df.loc[:len(data_df) - 2],
                                                         column=8,
                                                         norma=oit_stsb.load_cfg.tasks_back_work,
                                                         colors=colors,
                                                         name=oit_stsb.load_cfg.tasks_back_work_name,
                                                         title=oit_stsb.load_cfg.tasks_back_work_title)

        mean_time_solve_wo_waiting_graph = oit_stsb.figures.make_bars(df=data_df.loc[:len(data_df) - 2],
                                                                      column=9,
                                                                      norma=oit_stsb.load_cfg.
                                                                      mean_time_solve_wo_waiting,
                                                                      colors=colors,
                                                                      name=oit_stsb.load_cfg.
                                                                      mean_time_solve_wo_waiting_name,
                                                                      title=oit_stsb.load_cfg.
                                                                      mean_time_solve_wo_waiting_title)

        mean_count_tasks_per_empl_per_day_graph = oit_stsb.figures.make_bars(df=data_df.loc[:len(data_df) - 2],
                                                                             column=12,
                                                                             norma=oit_stsb.load_cfg.
                                                                             mean_count_tasks_per_empl_per_day,
                                                                             colors=colors,
                                                                             name=oit_stsb.load_cfg.
                                                                             mean_count_tasks_per_empl_per_day_name,
                                                                             title=oit_stsb.load_cfg.
                                                                             mean_count_tasks_per_empl_per_day_title)

        staff_data_df = oit_stsb.staff.make_staff_table(table_name=table_name,
                                                        month=month,
                                                        year=year)
        staff_data_columns = oit_stsb.staff.set_staff_columns(mv=oit_stsb.staff.count_statistic(income_df=staff_data_df,
                                                                                                column=2))

        return (data_df.to_dict('records'), columns, total_task_pie_g, inc_close_wo_3l, inc_wo_sla_violation_graph,
                inc_back_work_graph, mean_time_solve_wo_waiting_graph, mean_count_tasks_per_empl_per_day_graph,
                staff_data_df.to_dict('records'), staff_data_columns
                )

    @app.callback(
        Output('sub_filter', 'options'),
        Input('main_filter', 'value'),
        Input('staff_table', 'data')
    )
    def fill_sub_filter(column, data):
        staff_data_df = pd.DataFrame(data)
        staff_data_df.columns = [i for i in range(1, len(staff_data_df.columns) + 1)]
        if column:
            sub_filter_options = [{'label': item, 'value': item} for item in np.sort(staff_data_df[column].unique())]
            return sub_filter_options

        return dash.no_update

    @app.callback(
        Output('single_staff', 'data'),
        Output('single_staff', 'columns'),
        Output('div_staff_table', 'hidden'),
        Output('div_single_staff', 'hidden'),
        Input('main_filter', 'value'),
        Input('sub_filter', 'value'),
        Input('staff_table', 'data'),
        Input('filter_btn', 'n_clicks')
    )
    def fill_form(column, text, data_df, click):
        df = pd.DataFrame(data_df)
        mv = oit_stsb.staff.count_statistic(income_df=df,
                                            column='2')
        if click:
            if column and text:
                df = df[df[str(column-1)].isin(text)]
                div_staff_table_hidden = True
                div_single_staff = False
            else:
                div_staff_table_hidden = False
                div_single_staff = True
        else:
            div_staff_table_hidden = False
            div_single_staff = True

        df_columns = oit_stsb.staff.set_staff_columns(mv=mv)

        return df.to_dict('records'), df_columns, div_staff_table_hidden, div_single_staff
