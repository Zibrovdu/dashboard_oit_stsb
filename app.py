import dash

from oit_stsb.callbacks import register_callbacks
from oit_stsb.layouts import serve_layout

app = dash.Dash(__name__,
                suppress_callback_exceptions=True,
                title='Отдел информационно-технического сопровождения центральной бухгалтерии')
server = app.server

app.layout = serve_layout
register_callbacks(app)

if __name__ == '__main__':
    app.run_server()
