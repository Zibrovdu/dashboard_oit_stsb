import dash
from dash.dependencies import Output, Input

import oit_stsb
from oit_stsb.load_cfg import table_name


def register_callbacks(app):
    @app.callback(
        Output('main_table', 'data'),
        Output('main_table', 'columns'),
        [Input('month_dd', 'value')]
    )
    def update_table(value):
        month, year = value.split('_')
        # data_df = oit_stsb.load_data(table=table_name, month=month, year=year)

        data_df = oit_stsb.make_main_table(table_name=table_name, month=month, year=year)

        columns = oit_stsb.set_columns()

        return data_df.to_dict('records'), columns


