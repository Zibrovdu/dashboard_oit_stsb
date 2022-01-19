from dash import dcc, html, dash_table

from oit_stsb.params import region_style, staff_style, tooltips, kpi_style_big
from oit_stsb.load_cfg import colors

tab_selected_style = dict(backgroundColor='#ebecf1',
                          fontWeight='bold')

filter_options = [{'label': item, 'value': i + 1} for i, item in enumerate(['ФИО сотрудника', 'Регион'])]

region_tab = dcc.Tab(
    label='Регионы',
    value='regions',
    children=[
        html.Div([
            dcc.Loading(
                id="loading_main_table",
                fullscreen=False,
                children=[
                    html.Div([
                        dash_table.DataTable(id='main_table',
                                             merge_duplicate_headers=True,
                                             style_cell={
                                                 'whiteSpace': 'normal',
                                                 'height': 'auto',
                                                 'textAlign': 'center',
                                                 'backgroundColor': '#f0f8ff'
                                             },
                                             style_data_conditional=region_style,
                                             export_format='xlsx')
                    ], style=dict(width='95%',
                                  padding='0 2.5%')
                    )
                ]
            )
        ]
        ),
        html.Div([
            # html.Div([
            #     html.Div([
            #         dash_table.DataTable(
            #             id='kpi_small',
            #             merge_duplicate_headers=True,
            #             style_cell={
            #                 'whiteSpace': 'normal',
            #                 'height': 'auto',
            #                 'textAlign': 'center',
            #                 'backgroundColor': '#f0f8ff'
            #             },
            #             style_cell_conditional=[kpi_style],
            #             style_header={'textAlign': 'center'},
            #             export_format='xlsx'
            #         )
            #
            #     ],
            #         className='dash_tables'
            #     )
            # ],
            #     className='line_block_kpi_table',
            #     # style=dict(height='290px', margin='95px 21px')
            # ),
            html.Div([
                dcc.Graph(
                    id='total_task_pie'
                )
            ],
                className='line_block',
            ),

        ],
            style=dict(backgroundColor='#ebecf1')
        ),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='meat_count_tasks_per_day_graph'
                )
            ],
                className='line_block',
            ),
            html.Div([
                dcc.Graph(
                    id='inc_close_wo_3l'
                )
            ],
                className='line_block',
            )
        ],
            style=dict(backgroundColor='#ebecf1')
        ),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='inc_wo_sla_violation'
                )
            ],
                className='line_block',
            ),
            html.Div([
                dcc.Graph(
                    id='inc_back_work'
                )
            ],
                className='line_block',
            ),
        ],
            style=dict(backgroundColor='#ebecf1')
        ),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='mean_time_solve_wo_waiting'
                )
            ],
                className='line_block',
            ),
            html.Div([
                dcc.Graph(
                    id='mean_count_tasks_per_empl_per_day'
                )
            ],
                className='line_block',
            ),
        ],
            style=dict(backgroundColor='#ebecf1')
        ),
    ],
    selected_style=tab_selected_style
)

staff_tab = dcc.Tab(
    label='Сотрудники',
    value='staff',
    children=[
        html.Div([
            html.Div([
                html.Label(
                    'Столбец для фильтрации'
                )
            ],
                className='bblock'
            ),
            html.Div([
                dcc.Dropdown(
                    id='main_filter',
                    options=filter_options,
                    clearable=False,
                    searchable=False,
                    placeholder="Выберите столбец",
                    style=dict(width='200px',
                               fontSize='16px')
                )
            ],
                className='bblock'
            ),
            html.Div([
                dcc.Dropdown(
                    id='sub_filter',
                    multi=True,
                    clearable=True,
                    searchable=True,
                    placeholder='< Сначала выберите столбец для фильтрации',
                    style=dict(width='800px',
                               fontSize='14px')
                )
            ],
                className='bblock'
            ),
        ]
        ),
        html.Div([
            dcc.Loading(
                id='load_staff',
                fullscreen=False,
                children=[
                    html.Div([
                        html.Div([
                            dash_table.DataTable(
                                id='staff_table',
                                style_cell={
                                    'whiteSpace': 'normal',
                                    'height': 'auto',
                                    'textAlign': 'center',
                                    'backgroundColor': '#f0f8ff'
                                },
                                style_data_conditional=staff_style,
                                tooltip_header={
                                    3: {'value': tooltips['3_column'],
                                        'type': 'markdown'}
                                },
                                tooltip_duration=None,
                                sort_action='native',
                                export_format='xlsx',
                            )
                        ],
                            className='dash_tables',
                            id='div_staff_table',
                        ),
                        html.Div([
                            dash_table.DataTable(
                                id='single_staff',
                                style_cell={
                                    'whiteSpace': 'normal',
                                    'height': 'auto',
                                    'textAlign': 'center',
                                    'backgroundColor': '#f0f8ff'
                                },
                                style_data_conditional=staff_style,
                                tooltip_header={
                                    3: {'value': tooltips['3_column'],
                                        'type': 'markdown'}
                                },
                                tooltip_duration=None,
                                export_format='xlsx',
                            )
                        ],
                            className='dash_tables',
                            id='div_single_staff'
                        )
                    ]),
                ]
            )
        ])
    ],
    selected_style=tab_selected_style
)

staff_plus_tab = dcc.Tab(
    label='Сотрудники +',
    value='employee',
    children=[
        html.Div([
            dcc.Store(
                id='store_staff_df'
            )
        ]
        ),
        html.Div([
            dcc.Dropdown(
                id='person',
                clearable=False,
                searchable=True,
                placeholder='Выберите сотрудника'
            )
        ],
            style=dict(width='300px',
                       fontSize='14px', padding='1%')
        ),
        html.Div([
            dcc.Loading(
                id='person_table_loading',
                fullscreen=False,
                children=[
                    html.Div([
                        dash_table.DataTable(
                            id='person_table',
                            style_cell={
                                'whiteSpace': 'normal',
                                'height': 'auto',
                                'textAlign': 'center',
                                'backgroundColor': '#f0f8ff'
                            },
                            style_data_conditional=staff_style,
                            tooltip_header={
                                3: {'value': tooltips['3_column'],
                                    'type': 'markdown'}
                            },
                            tooltip_duration=None,
                        )
                    ],
                        className='dash_tables'
                    ),
                ])
        ]),
        html.Div([
            html.Div([
                dash_table.DataTable(
                    id='categories',
                    style_cell={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'textAlign': 'left',
                        'backgroundColor': '#f0f8ff'
                    },
                    style_cell_conditional=[
                        {
                            'if':
                                {
                                    'column_id': ['Средний уровень сложности',
                                                  'Количество',
                                                  'в % от от общего количества']
                                },
                            'textAlign': 'center'
                        }
                    ],
                    style_header={
                        'textAlign': 'center'
                    },
                    export_format='xlsx'
                )
            ],
                className='table_categories_levels'
            )
        ],
            className='bblock'
        ),
        html.Div([
            html.Div([
                dash_table.DataTable(
                    id='subsystems',
                    style_cell={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'textAlign': 'left',
                        'backgroundColor': '#f0f8ff'
                    },
                    style_cell_conditional=[
                        {
                            'if':
                                {
                                    'column_id': 'Средний уровень сложности'
                                },
                            'textAlign': 'center'
                        }
                    ],
                    style_header={
                        'textAlign': 'center'
                    }
                )
            ],
                className='table_subs_levels'
            )
        ],
            className='bblock'
        )
    ],
    selected_style=tab_selected_style
)

picture_day_tab = dcc.Tab(
    label='Картина дня',
    value='picture_day',
    children=[
        html.Div([
            html.Br(),
            html.Div([
                html.Div([
                    html.Button(
                        'Обновить',
                        id='db_load_data'
                    )
                ],
                    className='btn_load'
                ),
            ],
                className='bblock'
            ),
            html.Div([
                html.Div([
                    html.Label(
                        'Актуализация данных'
                    ),
                ],
                    className='bblock'
                ),
                html.Div([
                    html.Label(
                        id='data_pic_day_label'
                    )
                ],
                    className='bblock'
                ),
            ],
                className='bblock'
            ),
            html.Div([
                html.Div([
                    html.Div([
                        html.Label(
                            'Цветовая схема: '
                        ),
                    ],
                        className='label_colorscheme',
                        style=dict(backgroundColor="#ebecf1")
                    )
                ],
                    className='bblock'
                ),
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id='choose_colorscheme_day',
                            options=colors,
                            value=colors[0]['value'],
                            clearable=False,
                            searchable=False
                        )
                    ],
                        className='colorscheme_dropdown'
                    ),
                ],
                    className='bblock'
                )
            ],
                className='bblock'
            ),
            html.Br(),
            html.Div([
                dcc.Loading(
                    id='load_picture_day_table',
                    children=[
                        html.Div([
                            dash_table.DataTable(
                                id='picture_day_table',
                                style_cell={
                                    'whiteSpace': 'normal',
                                    'height': 'auto',
                                    'textAlign': 'center',
                                    'backgroundColor': '#f0f8ff'
                                },
                                tooltip_header={
                                    'Количество поступивших обращений': {'value': tooltips['3_column'],
                                                                         'type': 'markdown'}
                                },
                                export_format='xlsx'
                            )
                        ],
                            className='dash_tables'
                        )
                    ])
            ]),
            html.Div([
                dcc.Graph(
                    id='update_day'
                )
            ],
                id='div_update_day_graph',
                style=dict(opacity='0',
                           width='90%')
            ),
            html.Div([
                dcc.Upload(
                    html.Button(
                        'Загрузить файл с данными'
                    ),
                    id='upload_day_file',
                    className='btn_load'
                ),
            ]),
            html.Br(),
            html.Div([
                html.Div([
                    html.Label(
                        'Дата'
                    ),
                ],
                    className='bblock'
                ),
                html.Div([
                    html.Label(
                        id='data_pic_day'
                    )
                ],
                    className='bblock'
                ),
                html.Div([
                    html.Span(
                        id='error_msg',
                        className='labels_encrypt'
                    ),
                ],
                    className='bblock'
                ),
            ]),
        ])
    ],
    selected_style=tab_selected_style
)

load_data_tab = dcc.Tab(
    label='Загрузка и обновление данных',
    value='load_data',
    children=[
        html.Div([
            dcc.Tabs(
                id='tab_load_data',
                value='data',
                children=[
                    dcc.Tab(
                        label='Обновление данных',
                        value='data',
                        children=[
                            html.Div([
                                html.Div([
                                    html.Div([
                                        dcc.Upload(
                                            html.Button(
                                                'Загрузить файл с данными'
                                            ),
                                            id='upload_total_file',
                                            className='btn_load', style=dict(margin='70px 0px')
                                        ),
                                    ]),
                                    html.Div([
                                        dcc.Loading(
                                            html.Label(id='load_data')
                                        )
                                    ]),
                                    html.Div([
                                        dcc.Store(id='store_main_data')
                                    ])
                                ]),
                                html.Div([
                                    html.Div([
                                        html.Button('Загрузить данные в базу',
                                                    id='btn_load_main_data',
                                                    className='btn_save_data_to_db')
                                    ])
                                ])

                            ])
                        ],
                        selected_style=tab_selected_style
                    ),
                    dcc.Tab(
                        label='Обновление базы сотрудников',
                        value='staff',
                        children=[],
                        selected_style=tab_selected_style
                    )
                ],
                colors=dict(border='#ebecf1',
                            primary='#222780',
                            background='#33ccff')
            )
        ], style=dict(backgroundColor='#ebecf1')
        ),

    ],
    selected_style=tab_selected_style
)

kpi_tab = dcc.Tab(
    label='KPI',
    value='kpi',
    children=[
        html.Div([
            html.Div([
                dcc.Loading(
                    id='load_kpi_table',
                    children=[
                        html.Div([
                            dash_table.DataTable(
                                id='kpi_table',
                                merge_duplicate_headers=True,
                                style_cell={
                                    'whiteSpace': 'normal',
                                    'height': 'auto',
                                    'textAlign': 'center',
                                    'backgroundColor': '#f0f8ff'
                                },
                                style_cell_conditional=[kpi_style_big],
                                style_header={'textAlign': 'center'},
                                export_format='xlsx'
                            )
                        ],
                            className='dash_tables'
                        )
                    ]
                ),
            ])
        ])
    ],
    selected_style=tab_selected_style
)

admin_tabs_list = [region_tab, staff_tab, staff_plus_tab, picture_day_tab, load_data_tab]

not_admin_tabs_list = [region_tab, staff_tab, staff_plus_tab, picture_day_tab]
