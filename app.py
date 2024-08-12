import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, State, callback
from dash import html

estilos = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
           "https://fonts.googleapis.com/icon?family=Material+Icons", dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True,
                external_stylesheets=estilos + [dbc_css])

sidebar = html.Div(
    [
        # html.H2("Sidebar", className="display-4"),
        html.Img(src=dash.get_asset_url('1.png'), style={
            'max-width': '100%', 'height': 'auto'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page['name']),
                    ],
                    href=page['path'],
                    active='exact',
                    # class_name='mb-1'
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
            # class_name='m-3'
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Informações")),
                dbc.ModalBody([
                    "Toda informação apresentada no painel será sempre referente a ",
                    html.Strong("dois dias atrás (D-2)"),
                    " para dados diários e ao ",
                    html.Strong("mês anterior (M-1)"),
                    " para dados mensais. Essas informações são obtidas diretamente do Sisbr Analítico. Para a guia de ",
                    html.Strong("Produtos"),
                    ", os dados serão atualizados conforme a CNV. Para uma análise detalhada, recomendamos utilizar a própria CNV."]),
                dbc.ModalFooter(
                    dbc.Button(
                        "Fechar", id="close", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="modal_home",
            is_open=True,

        )
    ],
    className="SIDEBAR_STYLE",

)


app.layout = html.Div([
    dbc.Row([
        dbc.Col(sidebar, width=2),  # Largura do sidebar
        # Conteúdo centralizado com padding
        dbc.Col(dash.page_container, md=9,
                className="mx-5", style={"margin-top": "10px"}),
    ])
])


@app.callback(
    Output("modal_home", "is_open"),
    Input("close", "n_clicks"),
    [State("modal_home", "is_open")],
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open


# Rodar servidor
if __name__ == '__main__':
    app.run_server(host='10.23.1.138', debug=True, port=80)
