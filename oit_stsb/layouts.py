import dash_core_components as dcc
import dash_html_components as html
import dash_table.Format

import oit_stsb
from oit_stsb.load_cfg import table_name, conn_string

filter_options = [{'label': item, 'value': i + 1} for i, item in enumerate(['ФИО сотрудника', 'Регион'])]


def serve_layout():
    data_df = oit_stsb.load_data(table=table_name, connection_string=conn_string)
    end_month = oit_stsb.set_periods(df=data_df)

    tab_selected_style = dict(backgroundColor='#ebecf1',
                              fontWeight='bold')

    colors = [dict(label=f'Цветовая схема № {i + 1}', value=j) for i, j in enumerate(oit_stsb.load_cfg.color_schemes)]

    layout = html.Div([
        dcc.Location(id='url',
                     refresh=True),
        html.Div([
            html.H2('Отдел информационно-технического сопровождения центральной бухгалтерии'),
            html.A([
                html.Img(src="assets/logo.png")
            ], href='#modal-1', className='js-modal-open link')
        ], className='banner'),
        html.Div([
            html.Div([
                html.Div([
                    html.Label('Выберите период: ')
                ], className='wrapper-dropdown-4')
            ], className='bblock'),
            html.Div([
                html.Div([
                    dcc.Dropdown(id='month_dd',
                                 options=end_month,
                                 value=end_month[0]['value'],
                                 clearable=False,
                                 searchable=False)
                ], className='wrapper-dropdown-3',
                    style=dict(width='295px',
                               display='block')),
            ], className='bblock'),
            html.Div([
                html.Div([
                    html.Label('Цветовая схема: '),
                ], className='label_colorscheme')
            ], className='bblock'),
            html.Div([
                html.Div([
                    dcc.Dropdown(id='choose_colorscheme',
                                 options=colors,
                                 value=colors[0]['value'],
                                 clearable=False,
                                 searchable=False)
                ], className='colorscheme_dropdown'),
            ], className='bblock')

        ], style=dict(background='#b1d5fa', height='55px')),
        html.Br(),
        html.Br(),
        html.Div([
            dcc.Tabs(id='main_tabs',
                     value='regions',
                     children=[
                         dcc.Tab(label='Регионы',
                                 value='regions',
                                 children=[
                                     html.Div([
                                         dcc.Loading(
                                             id="loading-1",
                                             # type="cube",
                                             fullscreen=True,
                                             children=html.Div([
                                                 dash_table.DataTable(id='main_table',
                                                                      merge_duplicate_headers=True,
                                                                      style_cell={
                                                                          'whiteSpace': 'normal',
                                                                          'height': 'auto',
                                                                          'textAlign': 'center',
                                                                          'backgroundColor': '#f0f8ff'
                                                                      },
                                                                      style_data_conditional=[
                                                                          {'if': {
                                                                              'filter_query':
                                                                                  f'{{4}} > 60 && {{4}} < 70',
                                                                              'column_id': 4},
                                                                              'backgroundColor': '#fcb500'},
                                                                          {'if': {'filter_query': f'{{4}} < 60',
                                                                                  'column_id': 4},
                                                                           'backgroundColor': 'tomato',
                                                                           'color': 'white'},
                                                                          {'if': {'filter_query': f'{{4}} > 70',
                                                                                  'column_id': 4},
                                                                           'backgroundColor': '#c4fbdb'},
                                                                          {'if': {
                                                                              'filter_query':
                                                                                  f'{{6}} > 75 && {{6}} < 85',
                                                                              'column_id': 6},
                                                                              'backgroundColor': '#fcb500'},
                                                                          {'if': {'filter_query': f'{{6}} < 75',
                                                                                  'column_id': 6},
                                                                           'backgroundColor': 'tomato',
                                                                           'color': 'white'},
                                                                          {'if': {'filter_query': f'{{6}} > 85',
                                                                                  'column_id': 6},
                                                                           'backgroundColor': '#c4fbdb'},
                                                                          {'if': {
                                                                              'filter_query':
                                                                                  f'{{8}} > 10 && {{8}} < 15',
                                                                              'column_id': 8},
                                                                              'backgroundColor': '#fcb500'},
                                                                          {'if': {'filter_query': f'{{8}} > 15',
                                                                                  'column_id': 8},
                                                                           'backgroundColor': 'tomato',
                                                                           'color': 'white'},
                                                                          {'if': {'filter_query': f'{{8}} < 10',
                                                                                  'column_id': 8},
                                                                           'backgroundColor': '#c4fbdb'},
                                                                          {'if': {
                                                                              'filter_query':
                                                                                  f'{{9}} < "30:" && {{9}} > "24:"',
                                                                              'column_id': 9},
                                                                              'backgroundColor': '#fcb500'},
                                                                          {'if': {'filter_query': '{9} < "24:"',
                                                                                  'column_id': 9},
                                                                           'backgroundColor': '#c4fbdb'},
                                                                          {'if': {'filter_query': '{9} > "30"',
                                                                                  'column_id': 9},
                                                                           'backgroundColor': 'tomato',
                                                                           'color': 'white'},
                                                                          {'if': {'filter_query': f'{{12}} > 6',
                                                                                  'column_id': 12},
                                                                           'backgroundColor': '#c4fbdb'},
                                                                          {'if': {
                                                                              'filter_query':
                                                                                  f'{{12}} < 6 && {{12}} > 4',
                                                                              'column_id': 12},
                                                                              'backgroundColor': '#fcb500'},
                                                                          {'if': {'filter_query': f'{{12}} < 4',
                                                                                  'column_id': 12},
                                                                           'backgroundColor': 'tomato',
                                                                           'color': 'white'}
                                                                      ],
                                                                      export_format='xlsx')
                                             ], style=dict(width='95%', padding='0 2.5%'))
                                         )
                                     ]),
                                     html.Div([
                                         html.Div([
                                             dcc.Graph(id='total_task_pie')
                                         ], className='line_block', style=dict(width='40%')
                                         ),
                                         html.Div([
                                             dcc.Graph(id='inc_close_wo_3l')
                                         ], className='line_block', style=dict(width='58%')
                                         ),
                                     ], style=dict(backgroundColor='#ebecf1')),
                                     html.Div([
                                         html.Div([
                                             dcc.Graph(id='inc_wo_sla_violation')
                                         ], className='line_block', style=dict(width='48%')
                                         ),
                                         html.Div([
                                             dcc.Graph(id='inc_back_work')
                                         ], className='line_block', style=dict(width='48%')
                                         ),
                                     ], style=dict(backgroundColor='#ebecf1')),
                                     html.Div([
                                         html.Div([
                                             dcc.Graph(id='mean_time_solve_wo_waiting')
                                         ], className='line_block', style=dict(width='48%')
                                         ),
                                         html.Div([
                                             dcc.Graph(id='mean_count_tasks_per_empl_per_day')
                                         ], className='line_block', style=dict(width='48%')
                                         ),
                                     ], style=dict(backgroundColor='#ebecf1')),
                                 ],
                                 selected_style=tab_selected_style),
                         dcc.Tab(label='Сотрудники',
                                 value='staff',
                                 children=[
                                     html.Div([
                                         html.Div([
                                             html.Label('Столбец для фильтрации')
                                         ], className='bblock'),
                                         html.Div([
                                             dcc.Dropdown(id='main_filter',
                                                          options=filter_options,
                                                          clearable=False,
                                                          searchable=False,
                                                          placeholder="Выберите столбец",
                                                          style=dict(width='200px', fontSize='16px'))
                                         ], className='bblock'),
                                         html.Div([
                                             dcc.Dropdown(id='sub_filter',
                                                          multi=True,
                                                          clearable=False,
                                                          searchable=False,
                                                          style=dict(width='800px', fontSize='14px'))
                                         ], className='bblock'),
                                         html.Div([html.Span(id='form_filter', hidden=True)], className='bblock'),
                                         html.Div([
                                             html.Button('Применить фильтр', id='filter_btn')
                                         ], className='bblock'),
                                         html.Div([
                                             html.Button('Сбросить фильтр', id='reset_btn')
                                         ], className='bblock')

                                     ]),
                                     html.Div([
                                         dcc.Loading(
                                             id='load_staff',
                                             fullscreen=True,
                                             children=html.Div([
                                                 dash_table.DataTable(id='staff_table',
                                                                      style_cell={
                                                                          'whiteSpace': 'normal',
                                                                          'height': 'auto',
                                                                          'textAlign': 'center',
                                                                          'backgroundColor': '#f0f8ff'
                                                                      },
                                                                      sort_action='native',
                                                                      export_format='xlsx',
                                                                      filter_action='native',
                                                                      )
                                             ], style=dict(width='98%', padding='0 1%'))
                                         )
                                     ])
                                 ],
                                 selected_style=tab_selected_style)
                     ],
                     colors=dict(border='#ebecf1',
                                 primary='#222780',
                                 background='#33ccff')
                     ),

        ], style=dict(backgroundColor='#ebecf1')),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        'История изменений'
                    ], className='modal__dialog-header-content'),
                    html.Div([
                        html.Button([
                            html.Span('x')
                        ], className='js-modal-close modal__dialog-header-close-btn')
                    ], className='modal__dialog-header-close')
                ], className='modal__dialog-header'),
                html.Div([
                    html.Br(),
                    html.Div([
                        dcc.Textarea(value=oit_stsb.read_history_data(), readOnly=True, className='frame-history')
                    ]),
                    html.Br(),
                ], className='modal__dialog-body'),
                html.Div([
                    html.Button('Close', className='js-modal-close modal__dialog-footer-close-btn')
                ], className='modal__dialog-footer')
            ], className='modal__dialog')
        ], id='modal-1', className='modal_history modal--l'),
        html.Script(src='assets/js/main.js'),
    ], style=dict(background='#ebecf1'))
    return layout
