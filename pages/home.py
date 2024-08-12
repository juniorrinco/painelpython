import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import pandas as pd
from datetime import datetime
from pages import excel

dash.register_page(__name__, path="/", name="Início")

# Chama as funções definidas no excel.py para obter os dados
saldo_carteiraD, data_carteiraD, valores_carteira, datas_carteira = (
    excel.process_faturamento()
)
saldo_capitalD, data_capitalD, valores_capital, datas_capital = excel.process_capital()
saldo_depprazoD, data_depprazoD, monthly_totals_deprazo, dates_deprazo = (
    excel.process_deposito_prazo()
)
saldo_depviD, data_depviD, monthly_totals_depvista, dates_depvista = (
    excel.process_deposito_vista()
)
saldo_poup, data_poup, valores_poup, dates_poup = excel.process_receita()
qtd_cooperados, data_cooperados, cooperados_mes, datas_cooperados = (
    excel.process_cooperados_total()
)
qtd_novoscoop, data_novoscoop = excel.process_novos_cooperados()


# Formatação de valores com a função numero_formato do excel.py
formatadoCarteiraD = excel.numero_formato(saldo_carteiraD)
formatadoCapitalD = excel.numero_formato(saldo_capitalD)
formatadoDeppD = excel.numero_formato(saldo_depprazoD)
formatadoDepvD = excel.numero_formato(saldo_depviD)
formatadoPoup = excel.numero_formato(saldo_poup)
formatadoCooperados = excel.numero_formato(qtd_cooperados, is_integer=True)
formatadocaptacao = excel.numero_formato(saldo_depprazoD + saldo_depviD)
formatadoNovosCoop = excel.numero_formato(qtd_novoscoop, is_integer=True)


# Dados para os títulos e valores dos cartões
card_carteira = [
    ("Faturamento", f"R$ {formatadoCarteiraD}"),
    ("Rec. De Crédito", "R$ 810,30K"),
]
card_captacao = [
    ("Depósito Atual", f"R$ {formatadocaptacao}"),
    ("Capital Social", f"R$ {formatadoCapitalD}"),
    ("Receita", f"R$ {formatadoPoup}"),
]
card_clientes = [
    ("NPS Geral", "87"),
    ("Clientes", formatadoCooperados),
    ("Novos Clientes", formatadoNovosCoop),
]


datas_atualizacao = {
    "Faturamento": f"Última atualização: {data_carteiraD}",
    "Rec. De Crédito": "Última atualização: 02/04/2024",
    "Depósito Atual": f"Última atualização: {data_depprazoD}",
    "Capital Social": f"Última atualização: {data_capitalD}",
    "Receita": f"Última atualização: {data_poup}",
    "Clientes": f"Última atualização: {data_cooperados}",
    "Novos Clientes": f"Última atualização: {data_novoscoop}",
    "NPS Geral": "Última atualização: 2024-03",
    # Continue para os outros cartões conforme necessário
}


# Função para criar um cartão e título
def create_card(title, value, update_dates_dict):
    # Cria um ID único baseado no título
    card_id = f"card_{title.replace(' ', '_').lower()}"
    card_body = dbc.CardBody(
        [html.H5(title, className="card-title"), html.P(value, className="card-text")]
    )
    card = dbc.Card(card_body, className="mb-4", id=card_id)

    # Cria um tooltip com a data de atualização se disponível
    tooltip = (
        dbc.Tooltip(update_dates_dict.get(title, ""), target=card_id)
        if title in update_dates_dict
        else None
    )

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
rows_carteira = create_rows_for_cards(card_carteira, datas_atualizacao)
rows_captacao = create_rows_for_cards(card_captacao, datas_atualizacao)
rows_clientes = create_rows_for_cards(card_clientes, datas_atualizacao)


# Função para criar um cartão completo com cabeçalho e corpo
def create_card_with_header(button_label, link_href, card_body_rows, button_class):
    return dbc.Card(
        [
            dcc.Link(
                dbc.Button(button_label, className=button_class),
                href=link_href,
                # className="meu-botao-link",  # Removido para evitar conflito de estilos
            ),
            dbc.CardBody(card_body_rows),
        ],
        className="color_fundo_card mb-3",
        style={"width": "100%"},
    )


carteira = create_card_with_header("CARTEIRA+", "/carteira", rows_carteira, "carteira")
captacao = create_card_with_header("CAPTAÇÃO+", "/captacao", rows_captacao, "captacao")
clientes = create_card_with_header("CLIENTES+", "/clientes", rows_clientes, "clientes")

layout = dbc.Container(
    [carteira, captacao, clientes],
    fluid=True,
    className="py-1",  # py-3 para adicionar padding vertical
)
