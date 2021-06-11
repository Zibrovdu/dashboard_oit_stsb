import dash_html_components as html
import dash_core_components as dcc
import dash_table.Format

import oit_stsb

from oit_stsb.load_cfg import table_name


def serve_layout():
    data_df = oit_stsb.load_data(table=table_name)
    end_month = oit_stsb.set_periods(df=data_df)

    layout = html.Div([
        html.Div([
            html.H2('Отдел информационно-технического сопровождения центральной бухгалтерии'),
            html.Img(src='assets/logo.png')
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

        ], style=dict(background='#b1d5fa', height='55px')),
        html.Br(),
        html.Br(),
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
                                             'textAlign': 'center'
                                         },
                                         style_data_conditional=[
                                             {'if': {'filter_query': f'{{4}} > 60 && {{4}} < 70', 'column_id': 4},
                                              'backgroundColor': '#fcb500'},
                                             {'if': {'filter_query': f'{{4}} < 60', 'column_id': 4},
                                              'backgroundColor': 'tomato', 'color': 'white'},
                                             {'if': {'filter_query': f'{{4}} > 70', 'column_id': 4},
                                              'backgroundColor': '#c4fbdb'},
                                             {'if': {'filter_query': f'{{6}} > 75 && {{6}} < 85', 'column_id': 6},
                                              'backgroundColor': '#fcb500'},
                                             {'if': {'filter_query': f'{{6}} < 75', 'column_id': 6},
                                              'backgroundColor': 'tomato', 'color': 'white'},
                                             {'if': {'filter_query': f'{{6}} > 85', 'column_id': 6},
                                              'backgroundColor': '#c4fbdb'},
                                             {'if': {'filter_query': f'{{8}} > 10 && {{8}} < 15', 'column_id': 8},
                                              'backgroundColor': '#fcb500'},
                                             {'if': {'filter_query': f'{{8}} > 15', 'column_id': 8},
                                              'backgroundColor': 'tomato', 'color': 'white'},
                                             {'if': {'filter_query': f'{{8}} < 10', 'column_id': 8},
                                              'backgroundColor': '#c4fbdb'},
                                             {'if': {'filter_query': f'{{9}} > "07:" && {{9}} < "14:"', 'column_id': 9},
                                              'backgroundColor': '#fcb500'},
                                             {'if': {'filter_query': '{9} > "14:"', 'column_id': 9},
                                              'backgroundColor': '#c4fbdb'},
                                             {'if': {'filter_query': '{9} < "07"', 'column_id': 9},
                                              'backgroundColor': 'tomato', 'color': 'white'},

                                         ])
                ], style=dict(width='95%', padding='0 2.5%'))
            )
        ])
    ])
    return layout
