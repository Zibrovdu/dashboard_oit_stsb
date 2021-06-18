from dash.dependencies import Output, Input

import oit_stsb
import oit_stsb.figures
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
        [Input('month_dd', 'value'),
         Input('choose_colorscheme', 'value')]
    )
    def update_table(value, colors):
        month, year = value.split('_')
        # data_df = oit_stsb.load_data(table=table_name, month=month, year=year)

        data_df = oit_stsb.make_main_table(table_name=table_name, month=month, year=year)

        columns = oit_stsb.set_columns()

        total_task_pie_g = oit_stsb.figures.total_tasks_pie(df=data_df.loc[:len(data_df) - 2], colors=colors)

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
                                                                      norma=oit_stsb.load_cfg.mean_time_solve_wo_waiting,
                                                                      colors=colors,
                                                                      name=oit_stsb.load_cfg.mean_time_solve_wo_waiting_name,
                                                                      title=oit_stsb.load_cfg.mean_time_solve_wo_waiting_title)

        mean_count_tasks_per_empl_per_day_graph = oit_stsb.figures.make_bars(df=data_df.loc[:len(data_df) - 2],
                                                                             column=12,
                                                                             norma=oit_stsb.load_cfg.mean_count_tasks_per_empl_per_day,
                                                                             colors=colors,
                                                                             name=oit_stsb.load_cfg.mean_count_tasks_per_empl_per_day_name,
                                                                             title=oit_stsb.load_cfg.mean_count_tasks_per_empl_per_day_title)

        return (data_df.to_dict('records'), columns, total_task_pie_g, inc_close_wo_3l, inc_wo_sla_violation_graph,
                inc_back_work_graph, mean_time_solve_wo_waiting_graph, mean_count_tasks_per_empl_per_day_graph)
