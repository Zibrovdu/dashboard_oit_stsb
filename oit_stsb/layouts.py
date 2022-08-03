from dash import dcc, html
# import dash_html_components as html
# import dash_table.Format
# from dash.dash_table.Format import Group

import oit_stsb
# from oit_stsb.params import region_style, staff_style, tooltips
from oit_stsb.load_cfg import table_name, conn_string, colors, staff_table_name
import oit_stsb.tabs

filter_options = [{'label': item, 'value': i + 1} for i, item in enumerate(['ФИО сотрудника', 'Регион'])]


def serve_layout():
    # filter_options = [{'label': item, 'value': i + 1} for i, item in enumerate(['ФИО сотрудника', 'Регион'])]

    # staff_oit_stsb_df = oit_stsb.load_staff(
    #     connection_string=conn_string
    # )

    filter_query_region = oit_stsb.get_filter_options(df=oit_stsb.load_staff(connection_string=conn_string,
                                                                             table=staff_table_name,
                                                                             update='update'),
                                                      filter_name='region')

    filter_query_work = oit_stsb.get_filter_options(df=oit_stsb.load_staff(connection_string=conn_string,
                                                                           table=staff_table_name,
                                                                           update='update'),
                                                    filter_name='state')

    filter_query_task = oit_stsb.get_filter_options(df=oit_stsb.load_staff(connection_string=conn_string,
                                                                           table=staff_table_name,
                                                                           update='update'),
                                                    filter_name='works_w_tasks')

    subs_options = [{'label': i, "value": i} for i in ['ПУНФА/ПУИО', 'ПУОТ', 'Администрирование', 'Командирование']]

    data_df = oit_stsb.load_data(table=table_name,
                                 connection_string=conn_string
                                 )
    end_month = oit_stsb.set_periods(df=data_df)

    # colors = [dict(label=f'Цветовая схема № {i + 1}', value=j) for i, j in enumerate(oit_stsb.load_cfg.color_schemes)]

    layout = html.Div([
        dcc.Location(
            id='url',
            refresh=True
        ),
        html.Div([
            html.H2(
                'Отдел информационно-технического сопровождения централизованной бухгалтерии'
            ),
            html.A([
                html.Img(
                    src="assets/logo.png"
                )
            ],
                href='#modal-1',
                className='js-modal-open link'
            )
        ],
            className='banner'
        ),
        html.Div([
            html.Div([
                html.Div([
                    html.Label(
                        'Выберите период: '
                    )
                ],
                    className='wrapper-dropdown-4'
                )
            ],
                className='bblock'
            ),
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='month_dd',
                        options=end_month,
                        value=end_month[0]['value'],
                        clearable=False,
                        searchable=False
                    )
                ],
                    className='wrapper-dropdown-3'
                ),
            ],
                className='bblock'
            ),
            html.Div([
                html.Div([
                    html.Label(
                        'Цветовая схема: '
                    ),
                ],
                    className='label_colorscheme'
                )
            ],
                className='bblock'
            ),
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='choose_colorscheme',
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
            style=dict(background='#b1d5fa',
                       height='55px')
        ),
        html.Br(),
        html.Br(),
        html.Div([
            dcc.Tabs(
                id='main_tabs',
                value='regions',
                children=oit_stsb.tabs.not_admin_tabs_list,
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
                    ],
                        className='modal__dialog-header-content'
                    ),
                    html.Div([
                        html.Button([
                            html.Span(
                                'x'
                            )
                        ],
                            className='js-modal-close modal__dialog-header-close-btn'
                        )
                    ],
                        className='modal__dialog-header-close'
                    )
                ],
                    className='modal__dialog-header'
                ),
                html.Div([
                    html.Br(),
                    html.Div([
                        dcc.Textarea(
                            value=oit_stsb.read_history_data(),
                            readOnly=True,
                            className='frame-history'
                        )
                    ]),
                    html.Br(),
                ],
                    className='modal__dialog-body'
                ),
                html.Div([
                    html.Button(
                        'Close',
                        className='js-modal-close modal__dialog-footer-close-btn'
                    )
                ],
                    className='modal__dialog-footer'
                )
            ],
                className='modal__dialog'
            )
        ],
            id='modal-1',
            className='modal_history modal--l'
        ),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        'Добавление нового сотрудника'
                    ],
                        className='modal__dialog-header-content'
                    ),
                    html.Div([
                        html.Button([
                            html.Span('x')

                        ],
                            className='js-modal-close modal__dialog-header-close-btn button_load_staff',
                            style=dict(padding='0px 15px')
                        )
                    ],
                        className='modal__dialog-header-close'
                    )
                ],
                    className='modal__dialog-header'
                ),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Label('Введите ФИО сотрудника'),
                            dcc.Input(id='new_staff_fio',
                                      style=dict(width='350px',
                                                 fontSize='16px')
                                      ),
                        ]),
                        html.Br(),
                        html.Div([
                            html.Label('Введите должность сотрудника'),
                            dcc.Input(id='new_staff_pos',
                                      style=dict(width='350px',
                                                 fontSize='16px')
                                      ),
                        ]),
                        html.Br(),
                        # html.Br(),
                        html.Div([
                            html.Label('Выберите регион сотрудника'),
                            dcc.Dropdown(
                                id='add_new_staff_region',
                                # options=filter_query_region[1:],
                                # value=filter_query_region[1]['value'],
                                clearable=False,
                                placeholder='Выберите регион',
                                style=dict(width='350px',
                                           fontSize='16px'))
                        ]),
                        html.Br(),
                        # html.Br(),
                        html.Div([
                            html.Label('Статус сотрудника'),
                            dcc.Dropdown(id='add_new_staff_work',
                                         # options=filter_query_work[1:],
                                         # value=filter_query_work[1]['value'],
                                         clearable=False,
                                         placeholder='Укажите статус сотрудинка',
                                         style=dict(width='350px',
                                                    fontSize='16px')
                                         )

                        ]),
                        html.Br(),
                        # html.Br(),
                        html.Div([
                            html.Label('Участие в рейтинге'),
                            dcc.Dropdown(
                                id='add_new_staff_task',
                                # options=filter_query_task[1:],
                                # value=filter_query_task[2]['value'],
                                clearable=False,
                                placeholder='Участвует ли сотрудинк в рейтинге',
                                style=dict(width='350px',
                                           fontSize='16px')
                            )
                        ]),
                        # html.Br(),
                        html.Br(),
                        html.Div([
                            html.Label('Подсистема с которой работает сотрудник'),
                            dcc.Dropdown(
                                id='add_new_staff_subs',
                                # options=subs_options,
                                # value=filter_query_task[2]['value'],
                                clearable=False,
                                placeholder='Выберите подсистему',
                                style=dict(width='350px',
                                           fontSize='16px')
                            )
                        ]),
                        html.Div([
                            html.Div([
                                html.Span(id='load_state')
                            ])
                        ])

                    ]),

                ],
                    className='modal__dialog-body'
                ),
                html.Div([
                    html.Div([
                        html.Button(
                            'Сохранить',
                            id='load_staff_to_db',
                            className='button_load_staff spec_style_btn_save',
                        ),
                    ],
                        style=dict(display='inline-block')
                    ),
                    html.Div([
                        html.Button(
                            'Отменить',
                            className='js-modal-close modal__dialog-footer-close-btn button_load_staff '
                                      'spec_style_btn_cancel',
                        )
                    ],
                        style=dict(display='inline-block')
                    ),
                ],
                    className='modal__dialog-footer'
                )
            ],
                className='modal__dialog'
            )
        ],
            id='modal-2',
            className='modal_history modal--z'
        ),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        'Изменение данных по сотруднику'
                    ],
                        className='modal__dialog-header-content'
                    ),
                    html.Div([
                        html.Button([
                            html.Span('x')
                        ],
                            className='js-modal-close modal__dialog-header-close-btn button_load_staff',
                            style=dict(padding='0px 15px')

                        )
                    ],
                        className='modal__dialog-header-close'
                    )
                ],
                    className='modal__dialog-header'
                ),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Label('Выберите сотрудника'),
                            dcc.Dropdown(id='list_staff_fio_modify',
                                         # options=filter_query_fio[1:],
                                         value='',
                                         clearable=False,
                                         searchable=False,
                                         style=dict(width='350px',
                                                    fontSize='16px')
                                         ),
                        ]),
                        html.Br(),
                        html.Div([
                            html.Label('Введите ФИО сотрудника'),
                            dcc.Input(id='modify_staff_fio',
                                      style=dict(width='350px',
                                                 fontSize='16px')
                                      ),
                        ]),
                        html.Br(),
                        html.Div([
                            html.Label('Введите должность сотрудника'),
                            dcc.Input(id='modify_staff_pos',
                                      style=dict(width='350px',
                                                 fontSize='16px')
                                      ),
                        ]),
                        html.Br(),
                        html.Div([
                            html.Label('Выберите регион сотрудника'),
                            dcc.Dropdown(
                                id='modify_staff_region',
                                options=filter_query_region[1:],
                                value='',
                                clearable=False,
                                style=dict(width='350px',
                                           fontSize='16px'))
                        ]),
                        html.Br(),
                        html.Div([
                            html.Label('Статус сотрудника'),
                            dcc.Dropdown(id='modify_staff_work',
                                         options=filter_query_work[1:],
                                         value='',
                                         clearable=False,
                                         style=dict(width='350px',
                                                    fontSize='16px')
                                         )

                        ]),
                        html.Br(),
                        html.Div([
                            html.Label('Участие в рейтинге'),
                            dcc.Dropdown(
                                id='modify_staff_task',
                                options=filter_query_task[1:],
                                value='',
                                clearable=False,
                                style=dict(width='350px',
                                           fontSize='16px')
                            )
                        ]),
                        html.Br(),
                        html.Div([
                            html.Label('Подсистема с которой работает сотрудник'),
                            dcc.Dropdown(
                                id='modify_staff_subs',
                                options=subs_options,
                                value='',
                                clearable=False,
                                style=dict(width='350px',
                                           fontSize='16px')
                            )
                        ]),
                        html.Div([
                            html.Div([
                                html.Span(id='modify_state')
                            ])
                        ])

                    ]),

                ],
                    className='modal__dialog-body'
                ),
                html.Div([
                    html.Div([
                        html.Button(
                            'Сохранить',
                            id='modify_staff_to_db',
                            className='button_load_staff spec_style_btn_save',
                        ),
                    ],
                        style=dict(display='inline-block')
                    ),
                    html.Div([
                        html.Button(
                            'Отменить',
                            className='js-modal-close modal__dialog-footer-close-btn button_load_staff '
                                      'spec_style_btn_cancel',
                        )
                    ],
                        style=dict(display='inline-block')
                    ),
                ],
                    className='modal__dialog-footer'
                )
            ],
                className='modal__dialog'
            )
        ],
            id='modal-3',
            className='modal_history modal--z'
        ),
        html.Script(
            src='assets/js/main.js'
        ),
    ],
        style=dict(background='#ebecf1')
    )
    return layout
