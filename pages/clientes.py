import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, dcc, html, MATCH
import plotly.express as px
import pandas as pd
import numpy as np
from pages import excel
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate


qtd_cooperados, data_cooperados, cooperados_mes, datas_mes = (
    excel.process_cooperados_total()
)
qtd_novoscoop, data_novoscoop = excel.process_novos_cooperados()
dash.register_page(__name__, path="/clientes", name="Clientes+")
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


def read_excel_data(filepath):
    df = pd.read_excel(filepath)
    df["Ano-Mês Movimento"] = pd.to_datetime(df["Ano-Mês Movimento"]).dt.to_period("M")
    return df


# Cria o gráfico de linha com Plotly Express
fig = px.area(
    x=datas_mes,
    y=cooperados_mes,
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
            "text": "Cooperados totais por mês e ano",
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


layout = dbc.Container(
    [
        dbc.Button(
            "Selecionar Filtros",
            id="open_cooperativismo",
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
                                id="dropdown-regional-cooperativismo",
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
                            id="dropdown-pa-cooperativismo",
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
                        id="close_cooperativismo",
                        className="botão_modal ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id="modal_cooperativismo",
            is_open=False,
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            html.Legend(
                                "Clientes Totais", style={"text-align": "center"}
                            ),
                            html.H5(
                                qtd_cooperados,
                                id="p-cooperadost-dashboards",
                                style={"text-align": "center"},
                            ),
                        ]
                    ),
                    width=2,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            html.Legend(
                                "Novos Clientes", style={"text-align": "center"}
                            ),
                            html.H5(
                                qtd_novoscoop,
                                id="p-novoscoop-dashboards",
                                style={"text-align": "center"},
                            ),
                        ]
                    ),
                    width=2,
                ),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dcc.Graph(
                                id="cooperados-graph",
                                figure=fig,
                                className="grafico-arredondado",
                            )
                        ]
                    ),
                    width=12,
                ),
            ]
        ),
    ],
    fluid=True,
)


# função e callback para ativar e desativar o modal para aparecer os filtros também
@callback(
    Output("modal_cooperativismo", "is_open"),
    [
        Input("open_cooperativismo", "n_clicks"),
        Input("close_cooperativismo", "n_clicks"),
    ],
    [State("modal_cooperativismo", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Callback para atualizar as opções do dropdown de PA baseado na seleção de Regional
@callback(
    Output("dropdown-pa-cooperativismo", "options"),
    [Input("dropdown-regional-cooperativismo", "value")],
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
    Output("dropdown-regional-cooperativismo", "value"),
    Input("dropdown-pa-cooperativismo", "value"),
    State("dropdown-regional-cooperativismo", "value"),
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
    [
        Output("p-cooperadost-dashboards", "children"),
        Output("p-novoscoop-dashboards", "children"),
    ],
    [Input("dropdown-pa-cooperativismo", "value")],
)
def update_cards_cap(selected_pa):
    # Se selected_pa é None ou vazio, passa None para as funções de processamento
    selected_pa = selected_pa if selected_pa else None

    # Processa os dados para cada categoria
    qtd_cooperados, data_cooperados, cooperados_mes, datas_mes = (
        excel.process_cooperados_total(selected_pa)
    )
    qtd_novoscoop, data_novoscoop = excel.process_novos_cooperados(selected_pa)

    # Retorna os valores formatados
    return (f"{qtd_cooperados}", f"{qtd_novoscoop}")


@callback(
    Output("cooperados-graph", "figure"),
    [Input("dropdown-pa-cooperativismo", "value")],
    prevent_initial_call=True,  # Adiciona isto para evitar a chamada inicial
)
def update_graph(selected_pa):
    if not selected_pa:  # Se nada for selecionado, retorna o estado inicial do gráfico
        selected_pa = None  # Isso fará com que process_carteira retorne todos os dados

    try:
        qtd_cooperados, data_cooperados, cooperados_mes, datas_mes = (
            excel.process_cooperados_total(selected_pa)
        )
        if not datas_mes or not cooperados_mes:
            return go.Figure()  # Se não houver dados, retorna gráfico vazio
    except PreventUpdate:
        return go.Figure()  # Evita atualizar se não há dados

    # Criando o gráfico
    fig = px.area(
        # Certifique-se de que isso é uma lista de datas ou uma série pandas de datas
        x=datas_mes,
        # Certifique-se de que isso é uma lista de valores ou uma série pandas de valores
        y=cooperados_mes,
        title="Cooperados totais por mês e ano",
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
                "text": "Cooperados totais por mês e ano",
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
