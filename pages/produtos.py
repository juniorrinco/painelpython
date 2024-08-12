import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, dcc, html, MATCH
import plotly.express as px
import pandas as pd
import numpy as np
from pages import excel

# Registra a página no app Dash
dash.register_page(__name__, path='/produtos', name='Produtos+')

produtos, data_produtos = excel.process_produtos_cnv()


# Formatação de valores com a função numero_formato do excel.py
formatadoConsginado = excel.numero_formato(produtos['Consignado'])
formatadoCreditoDigital = excel.numero_formato(
    produtos['Crédito Digital'], is_integer=True)
formatadoConsorcios = excel.numero_formato(produtos['Consórcios'])
formatadoCambio = excel.numero_formato(produtos['Câmbio'])
formatadoPoupanca = excel.numero_formato(produtos['Poupança'])
formatadoPrevi = excel.numero_formato(produtos['Previdência'], is_integer=True)
formatadoRendaFixa = excel.numero_formato(produtos['Renda Fixa'])
formatadoCapital = excel.numero_formato(produtos['Capital'])
formatadoSicoobcard = excel.numero_formato(produtos['SicoobCard'])
formatadoCoopcerto = excel.numero_formato(produtos['Coopcerto'])
formatadoCobrana = excel.numero_formato(produtos['Cobrança Bancária'])
formatadoSipag = excel.numero_formato(produtos['Sipag'])
formatadosSegurosG = excel.numero_formato(produtos['Seguros Gerais'])
formatadosSegurosVA = excel.numero_formato(produtos['Seguro Vida Arrecadação'])
formatadosCreditoRural = excel.numero_formato(produtos['Crédito Rural'])
formatadosSeguroR = excel.numero_formato(produtos['Seguro Rural'])


# Dados para os títulos e valores dos cartões
card_credito = [
    ("Consignado", f'R$ {formatadoConsginado}'),
    ("Crédito Digital", formatadoCreditoDigital),
    ("Consórcio", f'R$ {formatadoConsorcios}'),
    ("Câmbio", f'$ {formatadoCambio}'),
]
card_investimentos = [
    ("Poupança", f'R$ {formatadoPoupanca}'),
    ("Previdência",  formatadoPrevi),
    ("Renda Fixa", f'R$ {formatadoRendaFixa}'),
    ("Capital", f'R$ {formatadoCapital}'),
]
card_recebimento = [
    ("SicoobCard", f'R$ {formatadoSicoobcard}'),
    ("Coopcerto", f'R$ {formatadoCoopcerto}'),
    ("Cobrança Bancária", f'R$ {formatadoCobrana}'),
    ("Sipag", f'R$ {formatadoSipag}'),
]
card_protecao = [
    ("Seguros Gerais", f'R$ {formatadosSegurosG}'),
    ("Seguro Vida Ar.", f'R$ {formatadosSegurosVA}'),
]
card_rural = [
    ("Crédito Rural", f'R$ {formatadosCreditoRural}'),
    ("Seguro Rural", f'R$ {formatadosSeguroR}'),

]

datas_atualizacao = {
    "Consignado": f'Última atualização: {data_produtos}',
    "Crédito Digital": f'Última atualização: {data_produtos}',
    "Consórcio": f'Última atualização: {data_produtos}',
    "Câmbio": f'Última atualização: {data_produtos}',
    "Poupança": f'Última atualização: {data_produtos}',
    "Previdência": f'Última atualização: {data_produtos}',
    "Renda Fixa": f'Última atualização: {data_produtos}',
    "Capital": f'Última atualização: {data_produtos}',
    "SicoobCard": f'Última atualização: {data_produtos}',
    "Coopcerto": f'Última atualização: {data_produtos}',
    "Cobrança Bancária": f'Última atualização: {data_produtos}',
    "Sipag": f'Última atualização: {data_produtos}',
    "Seguros Gerais": f'Última atualização: {data_produtos}',
    "Seguro Vida Arrecadação": f'Última atualização: {data_produtos}',
    "Crédito Rural": f'Última atualização: {data_produtos}',
    "Seguro Rural": f'Última atualização: {data_produtos}',
}


# Função para criar um cartão e título
def create_card(title, value, update_dates_dict):
    # Cria um ID único baseado no título
    card_id = f"card_{title.replace(' ', '_').lower()}"
    card_body = dbc.CardBody([
        html.H5(title, className="card-title"),
        html.P(value, className="card-text")
    ])
    card = dbc.Card(card_body, className="mb-4", id=card_id)

    # Cria um tooltip com a data de atualização se disponível
    tooltip = dbc.Tooltip(update_dates_dict.get(
        title, ""), target=card_id) if title in update_dates_dict else None

    return card, tooltip


# Função para criar linhas de cartões para cada conjunto de dados
def create_rows_for_cards(card_data, update_dates_dict, max_cols=4):
    row_content = []
    for title, value in card_data:
        card, tooltip = create_card(title, value, update_dates_dict)
        col = dbc.Col([card], width=12, sm=6, md=4, lg=3)
        row_content.append(col)
        if tooltip:
            # Adiciona o tooltip separadamente se existir
            row_content.append(tooltip)

    return dbc.Row(row_content, justify="around")


# Criando linhas de cartões para cada conjunto de dados
rows_credito = create_rows_for_cards(card_credito, datas_atualizacao)
rows_investimentos = create_rows_for_cards(
    card_investimentos, datas_atualizacao)
rows_recebimento = create_rows_for_cards(
    card_recebimento, datas_atualizacao)
rows_protecao = create_rows_for_cards(card_protecao, datas_atualizacao)
rows_rural = create_rows_for_cards(card_rural, datas_atualizacao)


# Função para criar um cartão completo com cabeçalho e corpo
def create_card_with_header(button_label, card_body_rows, button_class):
    return dbc.Card(
        [

            html.Button(button_label, className=button_class, disabled=True),
            # className="meu-botao-link",  # Removido para evitar conflito de estilos
            dbc.CardBody(card_body_rows),
        ],
        className="color_fundo_card_produtos mb-3",
        style={"width": "100%"}
    )


credito = create_card_with_header(
    "COMBO CRÉDITO", rows_credito, "combocredito")
investimentos = create_card_with_header(
    "COMBO INVESTIMENTO",  rows_investimentos, "comboinvestimento")
recebimento = create_card_with_header(
    "COMBO RECEBIMENTO E PAGAMENTO", rows_recebimento, "comborecebimento")
protecao = create_card_with_header(
    "COMBO PROTEÇÃO",  rows_protecao, "comboprotecao")
rural = create_card_with_header(
    "RURAL",  rows_rural, "comborural")

layout = dbc.Container(
    [credito, investimentos, recebimento, protecao, rural],
    fluid=True,
    className="py-1"  # py-3 para adicionar padding vertical
)
