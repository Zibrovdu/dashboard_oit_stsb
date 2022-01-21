import dash
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
from flask import request

import oit_stsb
import oit_stsb.figures
import oit_stsb.staff
import oit_stsb.picture_day
import oit_stsb.staff_plus
import oit_stsb.tabs
import oit_stsb.log_writer as lw
# import oit_stsb.kpi as kpi
from oit_stsb.load_cfg import table_name, tasks_closed_wo_3l, conn_string


def register_callbacks(app):
    @app.callback(
        Output('main_tabs', 'children'),
        Input('month_dd', 'value')
    )
    def check_access_rights(value):
        username = request.authorization['username']
        if username == 'admin':
            lw.log_writer(f'Осуществлен вход под учетной записью {username}')
            return oit_stsb.tabs.admin_tabs_list
        else:
            lw.log_writer(f'Осуществлен вход под учетной записью {username}')
            return oit_stsb.tabs.not_admin_tabs_list

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
        Output('store_staff_df', 'data'),
        Output('meat_count_tasks_per_day_graph', 'figure'),
        Input('month_dd', 'value'),
        Input('choose_colorscheme', 'value')
    )
    def update_table(value, colors):

        month, year = value.split('_')

        month_work_days = oit_stsb.count_month_work_days(month=month,
                                                         year=year)

        data_df = oit_stsb.make_main_table(table_name=table_name,
                                           month=month,
                                           year=year,
                                           column='region',
                                           month_work_days=month_work_days)

        mean_count_tasks_df = oit_stsb.figures.get_meat_count_tasks_per_day_df(table_name=table_name,
                                                                               conn_string=conn_string,
                                                                               month=month,
                                                                               year=year)

        mean_count_tasks_graph = oit_stsb.figures.plot_meat_count_tasks_per_day(df=mean_count_tasks_df,
                                                                                colors=colors)

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
                                                        year=year,
                                                        month_work_days=month_work_days)

        staff_data_columns = oit_stsb.staff.set_staff_columns(mv=oit_stsb.staff.count_statistic(income_df=staff_data_df,
                                                                                                column=2))

        return (data_df.to_dict('records'), columns, total_task_pie_g, inc_close_wo_3l,
                inc_wo_sla_violation_graph, inc_back_work_graph, mean_time_solve_wo_waiting_graph,
                mean_count_tasks_per_empl_per_day_graph, staff_data_df.to_dict('records'), staff_data_columns,
                staff_data_df.to_dict('records'), mean_count_tasks_graph)

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
    )
    def fill_form(column, text, data_df):
        df = pd.DataFrame(data_df)
        mv = oit_stsb.staff.count_statistic(income_df=df,
                                            column='2')
        if column and text:
            df = df[df[str(column - 1)].isin(text)]
            div_staff_table_hidden = True
            div_single_staff = False
        else:
            div_staff_table_hidden = False
            div_single_staff = True

        df_columns = oit_stsb.staff.set_staff_columns(mv=mv)

        return df.to_dict('records'), df_columns, div_staff_table_hidden, div_single_staff

    @app.callback(
        Output('person', 'options'),
        Output('person_table', 'data'),
        Output('person_table', 'columns'),
        Output('categories', 'data'),
        Output('categories', 'columns'),
        Output('subsystems', 'data'),
        Output('subsystems', 'columns'),
        Input('store_staff_df', 'data'),
        Input('person', 'value'),
        Input('month_dd', 'value')
    )
    def fill_person(data, person, month_year):
        month, year = month_year.split('_')
        df = pd.DataFrame(data)

        mv = oit_stsb.staff.count_statistic(income_df=df,
                                            column='2')
        options = [{'label': item, 'value': item} for item in np.sort(df['0'].unique())]

        person_df = df[df['0'] == person][['1', '2', '3', '4', '5', '6', '7', '8', '9']]

        columns = oit_stsb.staff.set_staff_columns(mv=mv)[1:]

        categories_df = oit_stsb.staff_plus.build_category_table(month=month, year=year, person=person)
        categories_df_columns = [{'name': i, 'id': i} for i in categories_df.columns]

        if len(categories_df) > 0:
            subs_df = pd.DataFrame(categories_df.groupby('Подсистема')['Средний уровень сложности'].mean().round(2)
                                   ).reset_index()
        else:
            subs_df = pd.DataFrame(columns=['Подсистема', 'Средний уровень сложности'])
        subs_df_columns = [{'name': i, 'id': i} for i in subs_df.columns]

        return (options, person_df.to_dict('records'), columns, categories_df.to_dict('records'), categories_df_columns,
                subs_df.to_dict('records'), subs_df_columns
                )

    @app.callback(
        Output('load_data', 'children'),
        Output('store_main_data', 'data'),
        Output('div_load_btn', 'hidden'),
        Input('upload_total_file', 'contents'),
        Input('upload_total_file', 'filename')
    )
    def get_main_data(contents, filename):
        if contents is not None:
            incoming_df = oit_stsb.picture_day.parse_load_file(contents=contents,
                                                               filename=filename)
            msg = oit_stsb.picture_day.data_table(data_df=incoming_df, filename=filename)[1]

            if len(incoming_df) > 0:
                # data_df = oit_stsb.load_data_from_file(df=incoming_df)
                # print(data_df.dtypes)
                hide_button = False
            else:
                # data_df = oit_stsb.picture_day.no_data()
                hide_button = True
        else:
            incoming_df = oit_stsb.picture_day.no_data()
            msg = 'Нажмите кнопку "Загрузить файл с данными" и выберите файл для загрузки'
            hide_button = True

        return msg, incoming_df.to_dict('records'), hide_button

    @app.callback(
        Output('lbl_load_data', 'children'),
        Output("upd_load_main_data", "href"),
        Input('store_main_data', 'data'),
        Input('btn_load_main_data', 'n_clicks'),
        prevent_initial_call=True,
    )
    def write_data_to_db(data, click):
        if click and data:
            df = pd.DataFrame(data)
            data_df = oit_stsb.load_data_from_file(df=df)
            data_df.to_sql(table_name,
                           con=conn_string,
                           index=False,
                           if_exists='replace')
            return 'loading successful!!!', "/"
        return dash.no_update, dash.no_update

    @app.callback(
        Output('error_msg', 'children'),
        Output('error_msg', 'style'),
        Output('data_pic_day', 'children'),
        Input('upload_day_file', 'contents'),
        Input('upload_day_file', 'filename'))
    def get_picture_day_table(contents, filename):

        if contents is not None:
            incoming_df = oit_stsb.picture_day.parse_load_file(contents=contents,
                                                               filename=filename)
            msg = oit_stsb.picture_day.data_table(data_df=incoming_df, filename=filename)[1]

            if len(incoming_df) > 0:
                incoming_df.to_sql('picture_day', con=conn_string, if_exists='replace', index=False)

                style = oit_stsb.picture_day.set_styles(msg=msg)
                date_picture_day = oit_stsb.save_date(df=incoming_df, connection_string=conn_string)

                return msg, style, date_picture_day

            msg = oit_stsb.picture_day.data_table(data_df=incoming_df, filename=filename)[1]

            style = oit_stsb.picture_day.set_styles(msg=msg)

            return msg, style, dash.no_update

        else:
            return dash.no_update, dash.no_update, dash.no_update

    @app.callback(
        Output('picture_day_table', 'data'),
        Output('picture_day_table', 'columns'),
        Output('data_pic_day_label', 'children'),
        Output('div_update_day_graph', 'style'),
        Output('update_day', 'figure'),
        Input('db_load_data', 'n_clicks'),
        Input('choose_colorscheme_day', 'value')
    )
    def load_table_data(n_click, color_scheme):
        if n_click:
            incoming_df = oit_stsb.picture_day.load_day_df(connection_string=conn_string)
            staff_df = oit_stsb.load_staff(connection_string=conn_string)
            picture_day_df = oit_stsb.picture_day.make_table(content_df=incoming_df,
                                                             staff_df=staff_df)

            if len(picture_day_df.columns) > 6:
                picture_day_df_columns = oit_stsb.picture_day.set_picture_day_columns()
            else:
                picture_day_df_columns = oit_stsb.picture_day.set_picture_day_columns_old()

            mean_count_tasks_df = oit_stsb.figures.meat_count_tasks_per_day(df=incoming_df)

            picture_day_date = oit_stsb.load_date(connection_string=conn_string)
            div_style = dict(opacity='1')
            mean_count_tasks_graph = oit_stsb.figures.plot_meat_count_tasks_per_day(df=mean_count_tasks_df,
                                                                                    colors=color_scheme,
                                                                                    legend=True)

            return (picture_day_df.to_dict('records'), picture_day_df_columns, picture_day_date, div_style,
                    mean_count_tasks_graph)

        div_style = dict(opacity='0')
        return dash.no_update, dash.no_update, dash.no_update, div_style, dash.no_update

    # @app.callback(
    #     Output('kpi_table', 'data'),
    #     Output('kpi_table', 'columns'),
    #     Output('kpi_small', 'data'),
    #     Output('kpi_small', 'columns'),
    #     Input('month_dd', 'value'),
    # )
    # def build_kpi_table(value):
    #
    #     month, year = value.split('_')
    #
    #     kpi_df = kpi.kpi_table(month=month, year=year, small=False)
    #
    #     kpi_df_columns = kpi.set_kpi_columns_big()
    #
    #     kpi_small_df = kpi.kpi_table(month=month, year=year, small=True)
    #
    #     kpi_small_df_columns = kpi.set_kpi_columns()
    #
    #     return (
    #         kpi_df.to_dict('records'), kpi_df_columns, kpi_small_df.to_dict('records'), kpi_small_df_columns
    #             )
