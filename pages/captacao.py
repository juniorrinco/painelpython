from dash import callback_context
from dash import dcc, html, Output, Input, State, callback
import dash_bootstrap_components as dbc
import dash
import plotly.express as px
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
from .excel import numero_formato, process_deposito_prazo, process_deposito_vista, process_capital, process_poupanca, process_deposito_prazo_lca, process_deposito_prazo_lci, process_deposito_prazo_rdc

cat_regional = {'Regional1': ["Thainã"],
                'Regional2': ["Ilson"],
                'Regional3': ["Wesley"],
                'S/R': ["97"]}
cat_pa = {"Regional1": ["1", "2", "9", "10", "12", "16"],
          "Regional2": ["3", "4", "5", "7", "15", "17"],
          "Regional3": ["6", "8", "11", "13", "14", "18", "19"],
          "S/R": ["97"]}
saldo_capitalD, data_capitalD, valores_capital, datas_capital = process_capital()
saldo_depprazoD, data_depprazoD, monthly_totals_deprazo, dates_deprazo = process_deposito_prazo()
saldo_depprazordc, data_depprazordc, monthly_totals_deprazordc, dates_deprazordc = process_deposito_prazo_rdc()
saldo_depprazolci, data_depprazolci, monthly_totals_deprazolci, dates_deprazolci = process_deposito_prazo_lci()
saldo_depprazolca, data_depprazolca, monthly_totals_deprazolca, dates_deprazolca = process_deposito_prazo_lca()
saldo_depviD, data_depviD, monthly_totals_depvista, dates_depvista = process_deposito_vista()
saldo_poup, data_poup, valores_poup, dates_poup = process_poupanca()

formatadoCapitalD = numero_formato(saldo_capitalD)
formatadoDeppD = numero_formato(saldo_depprazoD)
formatadoDepvD = numero_formato(saldo_depviD)
formatadoPoup = numero_formato(saldo_poup)
formatadoDeppRDC = numero_formato(saldo_depprazordc)
formatadoDeppLCI = numero_formato(saldo_depprazolci)
formatadoDeppLCA = numero_formato(saldo_depprazolca)


dash.register_page(__name__, path='/captacao', name='Captação+')


def formatar_valor_monetario(valor):
    """
    Formata o valor para o formato de moeda brasileiro sem usar abreviações.
    :param valor: O valor numérico a ser formatado.
    :return: Uma string do valor formatado em reais.
    """
    return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


# # Processamento de depósito a prazo
# total_deposito_vista, data_carteira, valores_carteira, datas_carteira = process_capital()
# formatted_deposito_prazo = formatar_valor_monetario(total_deposito_prazo)
# # Processamento de depósito à vista
# total_deposito_vista, latest_date_deposito_vista = process_deposito_vista()
# formatted_deposito_vista = formatar_valor_monetario(total_deposito_vista)
# Processamento de capital
total_capital, data_capital, valores_capital, datas_capital = process_capital()
formatted_capital = formatar_valor_monetario(total_capital)
# Processamento de poupança
total_value, latest_date, monthly_totals, dates = process_poupanca()
formatted_poupanca = formatar_valor_monetario(total_value)

# Cria o gráfico de linha com Plotly Express
fig = px.area(
    x=datas_capital,
    y=valores_capital,
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
        'text': 'Capital Social por mês e ano',
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

# Adiciona um Dropdown para os filtros de dados acima do gráfico
tipo_deposito_dropdown = dcc.Dropdown(
    id='tipo-deposito-dropdown',
    options=[
        {'label': 'Depósito a Vista', 'value': 'vista'},
        {'label': 'Depósito a Prazo', 'value': 'prazo'},
        {'label': 'Poupança', 'value': 'poupanca'},
        {'label': 'Capital', 'value': 'capital'},
        {'label': 'RDC', 'value': 'rdc'},
        {'label': 'LCI', 'value': 'lci'},
        {'label': 'LCA', 'value': 'lca'},
    ],
    value='vista',  # Valor default
    clearable=False,
    style={"width": "100%"},
)


layout = dbc.Container([
    dbc.Button("Selecionar Filtros", id="open_captacao", n_clicks=0,
               className="botão_modal mb-4"),
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Filtros")),
            dbc.ModalBody([html.Label("Regionais"),
                          html.Div(
                dcc.Dropdown(cat_regional,
                             id="dropdown-regional-captacao",
                             clearable=False,
                             style={"width": "100%"},
                             persistence=True,
                             persistence_type="session",
                             multi=True)
            ), html.Label("PA",
                          style={"margin-top": "10px"}),
                dcc.Dropdown(cat_pa,
                             id="dropdown-pa-captacao",
                             clearable=False,
                             style={"width": "100%"},
                             persistence=True,
                             persistence_type="session",
                             multi=True
                             ),
                html.Label("Opções Gráfico",
                           style={"margin-top": "10px"}),
                dbc.Col(tipo_deposito_dropdown),
            ]),
            dbc.ModalFooter(
                dbc.Button(
                    "Fechar", id="close_captacao", className="botão_modal ms-auto", n_clicks=0
                )
            ),
        ],
        id="modal_captacao",
        is_open=False,

    ),
    dbc.Row([
        dbc.Col(dbc.Card([html.Legend("Capital Social", style={'text-align': 'center'}), html.H5(
            f'R$ {formatadoCapitalD}', id="p-capital-dashboards", style={'text-align': 'center'})]), width=2),
        dbc.Col(dbc.Card([html.Legend("Depósito RDC", style={'text-align': 'center'}), html.H5(
            f'R$ {formatadoDeppRDC}', id="p-rdc-dashboards", style={'text-align': 'center'})]), width=2),
        dbc.Col(dbc.Card([html.Legend("Depósito LCA", style={'text-align': 'center'}), html.H5(
            f'R$ {formatadoDeppLCA}', id="p-lca-dashboards", style={'text-align': 'center'})]), width=2),
        dbc.Col(dbc.Card([html.Legend("Depósito LCI", style={'text-align': 'center'}), html.H5(
            f'R$ {formatadoDeppLCI}', id="p-lci-dashboards", style={'text-align': 'center'})]), width=2),
        dbc.Col(dbc.Card([html.Legend("Dep. a Vista", style={'text-align': 'center'}), html.H5(
            f'R$ {formatadoDepvD}', id="p-avista-dashboards", style={'text-align': 'center'})]), width=2),
        dbc.Col(dbc.Card([html.Legend("Poupança", style={'text-align': 'center'}), html.H5(
            f'R$ {formatadoPoup}', id="p-poupanca-dashboards", style={'text-align': 'center'})]), width=2),
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dbc.Card([dcc.Graph(id="captacao-graph", figure=fig,
                className="grafico-arredondado")]), width=12)
    ])
], fluid=True)


# função e callback para ativar e desativar o modal para aparecer os filtros também
@ callback(
    Output("modal_captacao", "is_open"),
    [Input("open_captacao", "n_clicks"), Input("close_captacao", "n_clicks")],
    [State("modal_captacao", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Callback para atualizar as opções do dropdown de PA baseado na seleção de Regional
@ callback(
    Output("dropdown-pa-captacao", "options"),
    [Input("dropdown-regional-captacao", "value")]
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
    Output("dropdown-regional-captacao", "value"),
    Input("dropdown-pa-captacao", "value"),
    State("dropdown-regional-captacao", "value")
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
    Output('captacao-graph', 'figure'),
    [Input('tipo-deposito-dropdown', 'value'),
     Input('dropdown-pa-captacao', 'value')],
    prevent_initial_call=True
)
def update_graph(tipo_deposito, selected_pa):
    # Inicializa variáveis para armazenar os dados do gráfico
    data_x = []
    data_y = []
    # Verifica qual tipo de depósito foi selecionado e busca os dados correspondentes
    if tipo_deposito == 'vista':
        _, _, data_y, data_x = process_deposito_vista(selected_pa)
    elif tipo_deposito == 'prazo':
        _, _, data_y, data_x = process_deposito_prazo(selected_pa)
    elif tipo_deposito == 'capital':
        _, _, data_y, data_x = process_capital(selected_pa)
    elif tipo_deposito == 'poupanca':
        _, _, data_y, data_x = process_poupanca(selected_pa)
    elif tipo_deposito == 'rdc':
        _, _, data_y, data_x = process_deposito_prazo_rdc(selected_pa)
    elif tipo_deposito == 'lci':
        _, _, data_y, data_x = process_deposito_prazo_lci(selected_pa)
    elif tipo_deposito == 'lca':
        _, _, data_y, data_x = process_deposito_prazo_lca(selected_pa)

    # Formata os valores e datas para o gráfico, se necessário
    # Formate os valores monetários, se necessário, como no exemplo:
    # formatted_values = [formatar_valor_monetario(valor) para valor em data_y]

  # Cria o gráfico com os dados atualizados
    fig = px.area(
        x=data_x,
        y=data_y,
        labels={'x': 'Data', 'y': 'Valor'},
        line_shape='spline'
    )

    # Atualiza os traços do gráfico
    fig.update_traces(
        line=dict(color='teal'),
        fill='tozeroy'
    )

    # Personaliza o layout do gráfico
    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'xaxis': {
            'showgrid': False,
            'zeroline': False,
            'showticklabels': True,
            'title_text': ''
        },
        'yaxis': {
            'showgrid': False,
            'zeroline': False,
            'showticklabels': False,
            'title_text': ''
        },
        'hovermode': 'closest',
        'font': {
            'color': 'black'
        },
        'title': {
            'text': tipo_deposito.replace('_', ' ').title() + ' por mês e ano',
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
            'size': 12,
            'family': "Arial Black, sans-serif",
        },
        'margin': {'l': 0, 'r': 25, 't': 50, 'b': 0}
    })

    return fig


@callback(
    [
        Output('p-capital-dashboards', 'children'),
        Output('p-rdc-dashboards', 'children'),
        Output('p-lca-dashboards', 'children'),
        Output('p-lci-dashboards', 'children'),
        Output('p-avista-dashboards', 'children'),
        Output('p-poupanca-dashboards', 'children')
    ],
    [Input('dropdown-pa-captacao', 'value')]
)
def update_cards_cap(selected_pa):
    # Se selected_pa é None ou vazio, passa None para as funções de processamento
    selected_pa = selected_pa if selected_pa else None

    # Processa os dados para cada categoria
    saldo_capital, _, _, _ = process_capital(selected_pa)
    saldo_depprazordc, _, _, _ = process_deposito_prazo_rdc(selected_pa)
    saldo_depprazolci, _, _, _ = process_deposito_prazo_lci(selected_pa)
    saldo_depprazolca, _, _, _ = process_deposito_prazo_lca(selected_pa)
    saldo_depvi, _, _, _ = process_deposito_vista(selected_pa)
    saldo_poup, _, _, _ = process_poupanca(selected_pa)

    # Formata os valores para serem exibidos nos cards
    formatted_capital = numero_formato(saldo_capital)
    formatted_depprazordc = numero_formato(saldo_depprazordc)
    formatted_depprazolci = numero_formato(saldo_depprazolci)
    formatted_depprazolca = numero_formato(saldo_depprazolca)
    formatted_depvi = numero_formato(saldo_depvi)
    formatted_poup = numero_formato(saldo_poup)

    # Retorna os valores formatados
    return (
        f'R$ {formatted_capital}',
        f'R$ {formatted_depprazordc}',
        f'R$ {formatted_depprazolca}',
        f'R$ {formatted_depprazolci}',
        f'R$ {formatted_depvi}',
        f'R$ {formatted_poup}'
    )
