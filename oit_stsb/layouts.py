from dash import dcc, html
# import dash_html_components as html
# import dash_table.Format
# from dash.dash_table.Format import Group

import oit_stsb
# from oit_stsb.params import region_style, staff_style, tooltips
from oit_stsb.load_cfg import table_name, conn_string, colors
import oit_stsb.tabs

filter_options = [{'label': item, 'value': i + 1} for i, item in enumerate(['ФИО сотрудника', 'Регион'])]


def serve_layout():
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
        html.Script(
            src='assets/js/main.js'
        ),
    ],
        style=dict(background='#ebecf1')
    )
    return layout
