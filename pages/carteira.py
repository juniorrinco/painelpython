from dash import callback_context
from dash import dcc, html, Output, Input, State, callback
import dash_bootstrap_components as dbc
import dash
import plotly.express as px
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
from .excel import process_carteira, numero_formato, process_indicadores_qualitativos, process_novas_operacoes


cat_regional = {'Regional1': ["Thainã"],
                'Regional2': ["Ilson"],
                'Regional3': ["Wesley"],
                'S/R': ["97"]}
cat_pa = {"Regional1": ["1", "2", "9", "10", "12", "16"],
          "Regional2": ["3", "4", "5", "7", "15", "17"],
          "Regional3": ["6", "8", "11", "13", "14", "18", "19"],
          "S/R": ["97"]}


# Registra a página no app Dash
dash.register_page(__name__, path='/carteira', name='Carteira+')


def formatar_valor_monetario(valor):
    """
    Formata o valor para o formato de moeda brasileiro sem usar abreviações.
    :param valor: O valor numérico a ser formatado.
    :return: Uma string do valor formatado em reais.
    """
    return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


# Obtém os dados da carteira
total_carteira, data_carteira, valores_carteira, datas_carteira = process_carteira()
total_novas_operacoes, latest_date = process_novas_operacoes()
valores_formatados = [formatar_valor_monetario(
    valor) for valor in valores_carteira]

# Obtém os dados dos indicadores
perc_inad_15, perc_inad_90, latest_date, contratos_inad, perc_ic, perc_iprov, perc_iqc = process_indicadores_qualitativos()
total_novas_operacoes, latest_date = process_novas_operacoes()
formatadoIQC = f'{perc_iqc:.2f}%'.replace('.', ',')
formatadoINAD90 = f'{perc_inad_90:.2f}%'.replace('.', ',')
formatadoINAD15 = f'{perc_inad_15:.2f}%'.replace('.', ',')
formatadoIPROV = f'{perc_iprov:.2f}%'.replace('.', ',')
formatadoIC = f'{perc_ic:.2f}%'.replace('.', ',')
formatadoNovasOp = numero_formato(total_novas_operacoes)
# Cria o gráfico de linha com Plotly Express
fig = px.area(
    x=datas_carteira,
    y=valores_carteira,
    # title='Carteira Total por mês e ano',
    labels={'Valor': 'R$'},
    line_shape='spline'  # suaviza a linha
)
fig.update_traces(
    line=dict(color='teal'),  # Define a cor da linha
    fill='tozeroy',  # Define o preenchimento da área abaixo da linha
)
# Personaliza o gráfico para remover a grade, o fundo e os títulos dos eixos
fig.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',  # Remove o fundo do gráfico
    'paper_bgcolor': 'rgba(0,0,0,0)',  # Remove o fundo em torno do gráfico
    'xaxis': {
        'showgrid': False,  # Remove a grade do eixo x
        'zeroline': False,  # Remove a linha zero do eixo x
        'showticklabels': True,  # Esconde os labels dos ticks do eixo x
        'title_text': ''  # Remove o título do eixo x
    },
    'yaxis': {
        'showgrid': False,  # Remove a grade do eixo y
        'zeroline': False,  # Remove a linha zero do eixo y
        'showticklabels': False,  # Esconde os labels dos ticks do eixo y
        'title_text': ''  # Remove o título do eixo y
    },
    'hovermode': 'closest',  # Define o modo de hover
    'font': {
        'color': 'black'  # Define a cor da fonte para branco
    },
    'title': {
        'text': 'Carteira Total por mês e ano',
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {
            'size': 24,  # Ajuste conforme necessário
            'color': 'black',  # Ajuste conforme necessário
            'family': "Arial Black, sans-serif",
        }},
    'legend': {
        'title': {
            'text': 'Legenda',
            'font': {
                    'family': "Arial Black, sans-serif",
            }
        }},
    'font': {
        'size': 12,  # Ajuste conforme necessário
        'family': "Arial Black, sans-serif",
    },
    # Define as margens do gráfico
    'margin': {'l': 0, 'r': 25, 't': 50, 'b': 0}
})

# Atualiza os traços do gráfico para corresponder ao estilo da imagem
fig.update_traces(
    line={'color': 'teal'},  # Define a cor da linha
    hoverinfo='none'  # Remove as informações de hover
)

fig.update_yaxes({
    'tick0': 1000000
})


# Adiciona o gráfico ao layout da página Dash
layout = dbc.Container([
    dbc.Button("Selecionar Filtros", id="open_carteira", n_clicks=0,
               className="botão_modal mb-4"),
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Filtros")),
            dbc.ModalBody([html.Label("Regionais"),
                          html.Div(
                dcc.Dropdown(cat_regional,
                             id="dropdown-regional",
                             clearable=False,
                             style={"width": "100%"},
                             persistence=True,
                             persistence_type="session",
                             multi=True)
            ), html.Label("PA",
                          style={"margin-top": "10px"}),
                dcc.Dropdown(cat_pa,
                             id="dropdown-pa-carteira",
                             clearable=False,
                             style={"width": "100%"},
                             persistence=True,
                             persistence_type="session",
                             multi=True
                             )]),
            dbc.ModalFooter(
                dbc.Button(
                    "Fechar", id="close_carteira", className="botão_modal ms-auto", n_clicks=0
                )
            ),
        ],
        id="modal_carteira",
        is_open=False,

    ),
    dbc.Row([
        dbc.Col(dbc.Card([html.Legend("IPROV", style={'text-align': 'center'}), html.H5(
            formatadoIPROV, id="p-iprov-dashboards", style={'text-align': 'center'})]), width=2),
        dbc.Col(dbc.Card([html.Legend("INAD 90", style={'text-align': 'center'}), html.H5(
            formatadoINAD90, id="p-inad90-dashboards", style={'text-align': 'center'})]), width=2),
        dbc.Col(dbc.Card([html.Legend("INAD 15", style={'text-align': 'center'}), html.H5(
            formatadoINAD15, id="p-inad15-dashboards", style={'text-align': 'center'})]), width=2),
        dbc.Col(dbc.Card([html.Legend("IC", style={'text-align': 'center'}), html.H5(
            formatadoIC, id="p-ic-dashboards", style={'text-align': 'center'})]), width=2),
        dbc.Col(dbc.Card([html.Legend("IQC", style={'text-align': 'center'}), html.H5(
            formatadoIQC, id="p-iqc-dashboards", style={'text-align': 'center'})]), width=2),
        dbc.Col(dbc.Card([html.Legend("Novas Op.", style={'text-align': 'center'}), html.H5(
            f'R$ {formatadoNovasOp}', id="p-novasop-dashboards", style={'text-align': 'center'}),]), width=2),
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dbc.Card([dcc.Graph(id="ativo-graph", figure=fig,
                className="grafico-arredondado")]), width=12)
    ])
], fluid=True)


# função e callback para ativar e desativar o modal para aparecer os filtros também
@ callback(
    Output("modal_carteira", "is_open"),
    [Input("open_carteira", "n_clicks"), Input("close_carteira", "n_clicks")],
    [State("modal_carteira", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Callback para atualizar as opções do dropdown de PA baseado na seleção de Regional
@ callback(
    Output("dropdown-pa-carteira", "options"),
    [Input("dropdown-regional", "value")]
)
def set_pa_options(selected_regional):
    if not selected_regional:
        # Se nenhum regional está selecionado, mostre todos os PAs
        all_pas = [pa for regional in cat_pa.values() for pa in regional]
        return [{'label': pa, 'value': pa} for pa in all_pas]
    else:
        # Mostre apenas PAs relacionados ao regional selecionado
        related_pas = []
        for regional in selected_regional:
            related_pas.extend(cat_pa[regional])
        return [{'label': pa, 'value': pa} for pa in related_pas]


# Callback para atualizar a seleção do dropdown de Regional baseado na seleção de PA
@callback(
    Output("dropdown-regional", "value"),
    Input("dropdown-pa-carteira", "value"),
    State("dropdown-regional", "value")
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
    Output('ativo-graph', 'figure'),
    [Input('dropdown-pa-carteira', 'value')],
    prevent_initial_call=True  # Adiciona isto para evitar a chamada inicial
)
def update_graph(selected_pa):
    if not selected_pa:  # Se nada for selecionado, retorna o estado inicial do gráfico
        selected_pa = None  # Isso fará com que process_carteira retorne todos os dados

    try:
        total_carteira, data_carteira, valores_carteira, datas_carteira = process_carteira(
            selected_pa)
        if not datas_carteira or not valores_carteira:
            return go.Figure()  # Se não houver dados, retorna gráfico vazio
    except PreventUpdate:
        return go.Figure()  # Evita atualizar se não há dados

    # Criando o gráfico
    fig = px.area(
        x=datas_carteira,
        y=valores_carteira,
        title='Carteira Total por mês e ano',
        labels={'x': 'Data', 'y': 'Valor'},
        line_shape='spline'
    )
    fig.update_traces(
        line=dict(color='teal'),  # Define a cor da linha
        fill='tozeroy',  # Define o preenchimento da área abaixo da linha
    )
    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',  # Remove o fundo do gráfico
        'paper_bgcolor': 'rgba(0,0,0,0)',  # Remove o fundo em torno do gráfico
        'xaxis': {
            'showgrid': False,  # Remove a grade do eixo x
            'zeroline': False,  # Remove a linha zero do eixo x
            'showticklabels': True,  # Esconde os labels dos ticks do eixo x
            'title_text': ''  # Remove o título do eixo x
        },
        'yaxis': {
            'showgrid': False,  # Remove a grade do eixo y
            'zeroline': False,  # Remove a linha zero do eixo y
            'showticklabels': False,  # Esconde os labels dos ticks do eixo y
            'title_text': ''  # Remove o título do eixo y
        },
        'hovermode': 'closest',  # Define o modo de hover
        'font': {
            'color': 'black'  # Define a cor da fonte para branco
        },
        'title': {
            'text': 'Carteira Total por mês e ano',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'size': 24,
                'color': 'black',
                'family': "Arial Black, sans-serif",
            }},
        'legend': {
            'title': {
                'text': 'Legenda',
                'font': {
                    'family': "Arial Black, sans-serif",
                }
            }},
        'font': {
            'size': 12,  # Ajuste conforme necessário
            'family': "Arial Black, sans-serif",
        },
        # Define as margens do gráfico
        'margin': {'l': 0, 'r': 25, 't': 50, 'b': 0}
    })

    return fig


@callback(
    [
        Output('p-iprov-dashboards', 'children'),
        Output('p-inad90-dashboards', 'children'),
        Output('p-inad15-dashboards', 'children'),
        Output('p-ic-dashboards', 'children'),
        Output('p-iqc-dashboards', 'children')
    ],
    [Input('dropdown-pa-carteira', 'value')]
)
def update_cards(selected_pa):
    if not selected_pa:
        selected_pa = None

    perc_inad_15, perc_inad_90, _, _, perc_ic, perc_iprov, perc_iqc = process_indicadores_qualitativos(
        selected_pa)

    # Formata os valores para serem mostrados nos cards
    formatted_iprov = f'{perc_iprov:.2f}%'.replace('.', ',')
    formatted_inad90 = f'{perc_inad_90:.2f}%'.replace('.', ',')
    formatted_inad15 = f'{perc_inad_15:.2f}%'.replace('.', ',')
    formatted_ic = f'{perc_ic:.2f}%'.replace('.', ',')
    formatted_iqc = f'{perc_iqc:.2f}%'.replace('.', ',')

    # Retorna os valores formatados para serem mostrados nos respectivos cards
    return formatted_iprov, formatted_inad90, formatted_inad15, formatted_ic, formatted_iqc


@callback(
    Output('p-novasop-dashboards', 'children'),
    [Input('dropdown-pa-carteira', 'value')]
)
def update_card_novasop(selected_pa):
    if not selected_pa:
        # Se não houver PA selecionado, vamos buscar todos os dados
        selected_pa = None

    # Chama a função para processar os dados com o PA selecionado
    total_novas_operacoes, _ = process_novas_operacoes(selected_pa)

    # Se o total for 0 ou None, podemos querer retornar uma mensagem ou 0 formatado
    if not total_novas_operacoes:
        return "R$ 0,00"
    # Caso haja um valor válido, formate-o para a moeda brasileira
    formatted_novas_op = numero_formato(total_novas_operacoes)

    return formatted_novas_op
