import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, dcc, html, MATCH
import plotly.express as px
from .teste import process_indicadores_qualitativos_apo
from .excel import process_indicadores_qualitativos, process_iep


# Obtém os dados dos indicadores
perc_inad_15, perc_inad_90, latest_date, contratos_inad, perc_ic, perc_iprov, perc_iqc = process_indicadores_qualitativos()
perc_inad_15, perc_inad_90, latest_date, contratos_inad, perc_ic, perc_iprov, perc_iqc, percentual_ic, percentual_iprov, percentual_iqc, percentual_iand_15, percentual_iand_90, dates = process_indicadores_qualitativos_apo()
iep_real, latest_date, iep_pa, dates_iep = process_iep()

cat_regional = {'Regional1': ["Thainã"],
                'Regional2': ["Ilson"],
                'Regional3': ["Wesley"],
                'S/R': ["97"]}
cat_pa = {"Regional1": ["1", "2", "9", "10", "12", "16"],
          "Regional2": ["3", "4", "5", "7", "15", "17"],
          "Regional3": ["6", "8", "11", "13", "14", "18", "19"],
          "S/R": ["97"]}

# Registra a página no app Dash
dash.register_page(__name__, path='/indicadores', name='Indicadores Gerais+')


formatadoIQC = f'{perc_iqc:.2f}%'.replace('.', ',')
formatadoINAD90 = f'{perc_inad_90:.2f}%'.replace('.', ',')
formatadoINAD15 = f'{perc_inad_15:.2f}%'.replace('.', ',')
formatadoIPROV = f'{perc_iprov:.2f}%'.replace('.', ',')
formatadoIC = f'{perc_ic:.2f}%'.replace('.', ',')
formatadoIEP = f'{iep_real:.2f}'.replace('.', ',')

# Cria o gráfico de linha com Plotly Express
fig = px.area(

    x=dates,
    y=percentual_iand_15,
    # title='Carteira Total por mês e ano',
    labels={'x': 'Data', 'y': 'Valor (%)'},
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
        'text': 'Inad15 por mês e ano',
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

fig.update_yaxes(tickformat=".2%")

# Adiciona um Dropdown para os filtros de dados acima do gráfico
tipo_indicadores_dropdown = dcc.Dropdown(
    id='tipo_indicador_dropdown',
    options=[
        {'label': 'INAD 15', 'value': 'inad15'},
        {'label': 'INAD 90', 'value': 'inad90'},
        {'label': 'IPROV', 'value': 'iprov'},
        {'label': 'IQC', 'value': 'iqc'},
        {'label': 'IC', 'value': 'ic'},
        {'label': 'IEP', 'value': 'iep'}],
    value='inad15',  # Valor default
    clearable=False,
    style={"width": "100%"},
)

layout = dbc.Container([
    dbc.Button("Selecionar Filtros", id="open_indicadores", n_clicks=0,
               className="botão_modal mb-4"),
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Filtros")),
            dbc.ModalBody([html.Label("Regionais"),
                          html.Div(
                dcc.Dropdown(cat_regional,
                             id="dropdown-regional-indicadores",
                             clearable=False,
                             style={"width": "100%"},
                             persistence=True,
                             persistence_type="session",
                             multi=True)
            ), html.Label("PA",
                          style={"margin-top": "10px"}),
                dcc.Dropdown(cat_pa,
                             id="dropdown-pa-indicadores",
                             clearable=False,
                             style={"width": "100%"},
                             persistence=True,
                             persistence_type="session",
                             multi=True
                             ),
                html.Label("Opções Gráfico",
                           style={"margin-top": "10px"}),
                dbc.Col(tipo_indicadores_dropdown),
            ]),
            dbc.ModalFooter(
                dbc.Button(
                    "Fechar", id="close_indicadores", className="botão_modal ms-auto", n_clicks=0
                )
            ),
        ],
        id="modal_indicadores",
        is_open=False,

    ),
    dbc.Row([
        dbc.Col(dbc.Card([html.Legend("IPROV", style={'text-align': 'center'}), html.H5(
            formatadoIPROV, id="p-iprovi-dashboards", style={'text-align': 'center'})]), width=2),
        dbc.Col(dbc.Card([html.Legend("INAD 90", style={'text-align': 'center'}), html.H5(
            formatadoINAD90, id="p-inad90i-dashboards", style={'text-align': 'center'})]), width=2),
        dbc.Col(dbc.Card([html.Legend("INAD 15", style={'text-align': 'center'}), html.H5(
            formatadoINAD15, id="p-inad15i-dashboards", style={'text-align': 'center'})]), width=2),
        dbc.Col(dbc.Card([html.Legend("IC", style={'text-align': 'center'}), html.H5(
            formatadoIC, id="p-ici-dashboards", style={'text-align': 'center'})]), width=2),
        dbc.Col(dbc.Card([html.Legend("IQC", style={'text-align': 'center'}), html.H5(
            formatadoIQC, id="p-iqci-dashboards", style={'text-align': 'center'})]), width=2),
        dbc.Col(dbc.Card([html.Legend("IEP", style={'text-align': 'center'}), html.H5(
            formatadoIEP, id="p-iep-dashboards", style={'text-align': 'center'})]), width=2),
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dbc.Card([dcc.Graph(id="indicadores-graph", figure=fig,
                className="grafico-arredondado")]), width=12)
    ])
], fluid=True)


# função e callback para ativar e desativar o modal para aparecer os filtros também
@ callback(
    Output("modal_indicadores", "is_open"),
    [Input("open_indicadores", "n_clicks"),
     Input("close_indicadores", "n_clicks")],
    [State("modal_indicadores", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Callback para atualizar as opções do dropdown de PA baseado na seleção de Regional
@ callback(
    Output("dropdown-pa-indicadores", "options"),
    [Input("dropdown-regional-indicadores", "value")]
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
    Output("dropdown-regional-indicadores", "value"),
    Input("dropdown-pa-indicadores", "value"),
    State("dropdown-regional-indicadores", "value")
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
    Output('indicadores-graph', 'figure'),
    [Input('tipo_indicador_dropdown', 'value'),
     Input('dropdown-pa-indicadores', 'value')],
    prevent_initial_call=True
)
def update_graph(tipo_indicador, selected_pa):
    # perc_inad_15, perc_inad_90, latest_date, contratos_inad, perc_ic, perc_iprov, perc_iqc, percentual_ic, percentual_iprov, percentual_iqc, percentual_iand_15, percentual_iand_90, dates = process_indicadores_qualitativos_apo()
    data_y = []
    data_x = []
    if tipo_indicador == 'inad15':
        _, _, _, _, _, _, _, _, _, _, data_y, _, data_x = process_indicadores_qualitativos_apo(
            selected_pa)
    elif tipo_indicador == 'inad90':
        _, _, _, _, _, _, _, _, _, _, _, data_y, data_x = process_indicadores_qualitativos_apo(
            selected_pa)
    elif tipo_indicador == 'iqc':
        _, _, _, _, _, _, _, _, _, data_y, _, _, data_x = process_indicadores_qualitativos_apo(
            selected_pa)
    elif tipo_indicador == 'iprov':
        _, _, _, _, _, _, _, _, data_y, _, _, _, data_x = process_indicadores_qualitativos_apo(
            selected_pa)
    elif tipo_indicador == 'ic':
        _, _, _, _, _, _, _, data_y, _, _, _, _, data_x = process_indicadores_qualitativos_apo(
            selected_pa)
    elif tipo_indicador == 'iep':
        _, _, data_y, data_x = process_iep(selected_pa)

  # Cria o gráfico com os dados atualizados
    fig = px.area(
        x=data_x,
        y=data_y,
        labels={'x': 'Data', 'y': 'Valor (%)'},
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
            'text': tipo_indicador.replace('_', ' ').title() + ' por mês e ano',
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
        Output('p-iprovi-dashboards', 'children'),
        Output('p-inad90i-dashboards', 'children'),
        Output('p-inad15i-dashboards', 'children'),
        Output('p-ici-dashboards', 'children'),
        Output('p-iqci-dashboards', 'children'),
        Output('p-iep-dashboards', 'children')
    ],
    [Input('dropdown-pa-indicadores', 'value')]
)
def update_cards(selected_pa):
    if not selected_pa:
        selected_pa = None

    perc_inad15, perc_inad90, _, _, perc_ic, perc_iprov, iqc, = process_indicadores_qualitativos(
        selected_pa)
    iep_real, _, _, _ = process_iep(selected_pa)

    # Formata os valores para serem mostrados nos cards
    formatted_iprov = f'{perc_iprov:.2f}%'.replace('.', ',')
    formatted_inad90 = f'{perc_inad90:.2f}%'.replace('.', ',')
    formatted_inad15 = f'{perc_inad15:.2f}%'.replace('.', ',')
    formatted_ic = f'{perc_ic:.2f}%'.replace('.', ',')
    formatted_iqc = f'{iqc:.2f}%'.replace('.', ',')
    formatted_iep = f'{iep_real:.2f}'.replace('.', ',')

    # Retorna os valores formatados para serem mostrados nos respectivos cards
    return formatted_iprov, formatted_inad90, formatted_inad15, formatted_ic, formatted_iqc, formatted_iep
