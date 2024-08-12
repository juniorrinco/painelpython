from dash import callback_context
from dash import dcc, html, Output, Input, State, callback
import dash_bootstrap_components as dbc
import dash
import plotly.express as px
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
from .excel import process_faturamento, numero_formato


cat_regional = {
    "Regional1": ["Regional 1"],
    "Regional2": ["Regional 2"],
    "Regional3": ["Regional 3"],
}
cat_pa = {
    "Regional1": [
        "1",
        "4",
    ],
    "Regional2": [
        "5",
        "7",
    ],
    "Regional3": [
        "8",
        "9",
    ],
    "S/R": ["10"],
}


# Registra a página no app Dash
dash.register_page(__name__, path="/carteira", name="Carteira+")


def formatar_valor_monetario(valor):
    """
    Formata o valor para o formato de moeda brasileiro sem usar abreviações.
    :param valor: O valor numérico a ser formatado.
    :return: Uma string do valor formatado em reais.
    """
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# Obtém os dados da carteira
total_carteira, data_carteira, valores_carteira, datas_carteira = process_faturamento()
valores_formatados = [formatar_valor_monetario(valor) for valor in valores_carteira]


# Cria o gráfico de linha com Plotly Express
fig = px.area(
    x=datas_carteira,
    y=valores_carteira,
    # title='Carteira Total por mês e ano',
    labels={"Valor": "R$"},
    line_shape="spline",  # suaviza a linha
)
fig.update_traces(
    line=dict(color="teal"),  # Define a cor da linha
    fill="tozeroy",  # Define o preenchimento da área abaixo da linha
)
# Personaliza o gráfico para remover a grade, o fundo e os títulos dos eixos
fig.update_layout(
    {
        "plot_bgcolor": "rgba(0,0,0,0)",  # Remove o fundo do gráfico
        "paper_bgcolor": "rgba(0,0,0,0)",  # Remove o fundo em torno do gráfico
        "xaxis": {
            "showgrid": False,  # Remove a grade do eixo x
            "zeroline": False,  # Remove a linha zero do eixo x
            "showticklabels": True,  # Esconde os labels dos ticks do eixo x
            "title_text": "",  # Remove o título do eixo x
        },
        "yaxis": {
            "showgrid": False,  # Remove a grade do eixo y
            "zeroline": False,  # Remove a linha zero do eixo y
            "showticklabels": False,  # Esconde os labels dos ticks do eixo y
            "title_text": "",  # Remove o título do eixo y
        },
        "hovermode": "closest",  # Define o modo de hover
        "font": {"color": "black"},  # Define a cor da fonte para branco
        "title": {
            "text": "Carteira Total por mês e ano",
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {
                "size": 24,  # Ajuste conforme necessário
                "color": "black",  # Ajuste conforme necessário
                "family": "Arial Black, sans-serif",
            },
        },
        "legend": {
            "title": {
                "text": "Legenda",
                "font": {
                    "family": "Arial Black, sans-serif",
                },
            }
        },
        "font": {
            "size": 12,  # Ajuste conforme necessário
            "family": "Arial Black, sans-serif",
        },
        # Define as margens do gráfico
        "margin": {"l": 0, "r": 25, "t": 50, "b": 0},
    }
)

# Atualiza os traços do gráfico para corresponder ao estilo da imagem
fig.update_traces(
    line={"color": "teal"},  # Define a cor da linha
    hoverinfo="none",  # Remove as informações de hover
)

fig.update_yaxes({"tick0": 1000000})


# Adiciona o gráfico ao layout da página Dash
layout = dbc.Container(
    [
        dbc.Button(
            "Selecionar Filtros",
            id="open_carteira",
            n_clicks=0,
            className="botão_modal mb-4",
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Filtros")),
                dbc.ModalBody(
                    [
                        html.Label("Regionais"),
                        html.Div(
                            dcc.Dropdown(
                                cat_regional,
                                id="dropdown-regional",
                                clearable=False,
                                style={"width": "100%"},
                                persistence=True,
                                persistence_type="session",
                                multi=True,
                            )
                        ),
                        html.Label("Loja", style={"margin-top": "10px"}),
                        dcc.Dropdown(
                            cat_pa,
                            id="dropdown-pa-carteira",
                            clearable=False,
                            style={"width": "100%"},
                            persistence=True,
                            persistence_type="session",
                            multi=True,
                        ),
                    ]
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Fechar",
                        id="close_carteira",
                        className="botão_modal ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id="modal_carteira",
            is_open=False,
        ),
        dbc.Row(
            [],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dcc.Graph(
                                id="ativo-graph",
                                figure=fig,
                                className="grafico-arredondado",
                            )
                        ]
                    ),
                    width=12,
                )
            ]
        ),
    ],
    fluid=True,
)


# função e callback para ativar e desativar o modal para aparecer os filtros também
@callback(
    Output("modal_carteira", "is_open"),
    [Input("open_carteira", "n_clicks"), Input("close_carteira", "n_clicks")],
    [State("modal_carteira", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Callback para atualizar as opções do dropdown de PA baseado na seleção de Regional
@callback(
    Output("dropdown-pa-carteira", "options"), [Input("dropdown-regional", "value")]
)
def set_pa_options(selected_regional):
    if not selected_regional:
        # Se nenhum regional está selecionado, mostre todos os PAs
        all_pas = [pa for regional in cat_pa.values() for pa in regional]
        return [{"label": pa, "value": pa} for pa in all_pas]
    else:
        # Mostre apenas PAs relacionados ao regional selecionado
        related_pas = []
        for regional in selected_regional:
            related_pas.extend(cat_pa[regional])
        return [{"label": pa, "value": pa} for pa in related_pas]


# Callback para atualizar a seleção do dropdown de Regional baseado na seleção de PA
@callback(
    Output("dropdown-regional", "value"),
    Input("dropdown-pa-carteira", "value"),
    State("dropdown-regional", "value"),
)
def set_regional_selection(selected_pas, selected_regional):
    if selected_regional is None:
        selected_regional = []
    if selected_pas:
        for regional, pas in cat_pa.items():
            if any(pa in selected_pas for pa in pas):
                if regional not in selected_regional:
                    selected_regional.append(regional)
    return selected_regional


@callback(
    Output("ativo-graph", "figure"),
    [Input("dropdown-pa-carteira", "value")],
    prevent_initial_call=True,  # Adiciona isto para evitar a chamada inicial
)
def update_graph(selected_pa):
    if not selected_pa:  # Se nada for selecionado, retorna o estado inicial do gráfico
        selected_pa = None  # Isso fará com que process_carteira retorne todos os dados

    try:
        total_carteira, data_carteira, valores_carteira, datas_carteira = (
            process_faturamento(selected_pa)
        )
        if not datas_carteira or not valores_carteira:
            return go.Figure()  # Se não houver dados, retorna gráfico vazio
    except PreventUpdate:
        return go.Figure()  # Evita atualizar se não há dados

    # Criando o gráfico
    fig = px.area(
        x=datas_carteira,
        y=valores_carteira,
        title="Carteira Total por mês e ano",
        labels={"x": "Data", "y": "Valor"},
        line_shape="spline",
    )
    fig.update_traces(
        line=dict(color="teal"),  # Define a cor da linha
        fill="tozeroy",  # Define o preenchimento da área abaixo da linha
    )
    fig.update_layout(
        {
            "plot_bgcolor": "rgba(0,0,0,0)",  # Remove o fundo do gráfico
            "paper_bgcolor": "rgba(0,0,0,0)",  # Remove o fundo em torno do gráfico
            "xaxis": {
                "showgrid": False,  # Remove a grade do eixo x
                "zeroline": False,  # Remove a linha zero do eixo x
                "showticklabels": True,  # Esconde os labels dos ticks do eixo x
                "title_text": "",  # Remove o título do eixo x
            },
            "yaxis": {
                "showgrid": False,  # Remove a grade do eixo y
                "zeroline": False,  # Remove a linha zero do eixo y
                "showticklabels": False,  # Esconde os labels dos ticks do eixo y
                "title_text": "",  # Remove o título do eixo y
            },
            "hovermode": "closest",  # Define o modo de hover
            "font": {"color": "black"},  # Define a cor da fonte para branco
            "title": {
                "text": "Carteira Total por mês e ano",
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
                "font": {
                    "size": 24,
                    "color": "black",
                    "family": "Arial Black, sans-serif",
                },
            },
            "legend": {
                "title": {
                    "text": "Legenda",
                    "font": {
                        "family": "Arial Black, sans-serif",
                    },
                }
            },
            "font": {
                "size": 12,  # Ajuste conforme necessário
                "family": "Arial Black, sans-serif",
            },
            # Define as margens do gráfico
            "margin": {"l": 0, "r": 25, "t": 50, "b": 0},
        }
    )

    return fig
