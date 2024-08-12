import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import pandas as pd
from datetime import datetime
from pages import excel
dash.register_page(__name__, path='/', name='Início')

# Chama as funções definidas no excel.py para obter os dados
saldo_carteiraD, data_carteiraD, valores_carteira, datas_carteira = excel.process_carteira()
saldo_capitalD, data_capitalD, valores_capital, datas_capital = excel.process_capital()
saldo_depprazoD, data_depprazoD, monthly_totals_deprazo, dates_deprazo = excel.process_deposito_prazo()
saldo_depviD, data_depviD, monthly_totals_depvista, dates_depvista = excel.process_deposito_vista()
saldo_poup, data_poup, valores_poup, dates_poup = excel.process_poupanca()
saldo_cart, data_cart = excel.process_cartoes()
saldo_cobranca, data_cobranca = excel.process_liquidacao_cobranca()
qtd_cooperados, data_cooperados, cooperados_mes, datas_cooperados = excel.process_cooperados_total()
qtd_novoscoop, data_novoscoop = excel.process_novos_cooperados()
perc_inad15, perc_inad90, data_indicadores, contratos_inad, perc_ic, perc_iprov, iqc = excel.process_indicadores_qualitativos()
iep_sc, maior_dataSC_str = excel.process_iep_sicoob_centro()
valor_novasOp, data_novasOp = excel.process_novas_operacoes()
# Isso retorna um dicionário com os valores dos produtos e a última data
produtos, data_produtos = excel.process_produtos_cnv()
qtd_indeterminado, data_indeterminado = excel.process_indeterminados()

# Formatação de valores com a função numero_formato do excel.py
formatadoCarteiraD = excel.numero_formato(saldo_carteiraD)
formatadoCapitalD = excel.numero_formato(saldo_capitalD)
formatadoDeppD = excel.numero_formato(saldo_depprazoD)
formatadoDepvD = excel.numero_formato(saldo_depviD)
formatadoPoup = excel.numero_formato(saldo_poup)
formatadoCart = excel.numero_formato(saldo_cart)
formatadoCobranca = excel.numero_formato(saldo_cobranca)
formatadoNovasOp = excel.numero_formato(valor_novasOp)
formatadoContratosInad = excel.numero_formato(contratos_inad)
formatadoSipag = excel.numero_formato(produtos['Sipag'])
formatadosSegurosG = excel.numero_formato(produtos['Seguros Gerais'])
formatadoCooperados = excel.numero_formato(qtd_cooperados, is_integer=True)
formatadoPrevi = excel.numero_formato(produtos['Previdência'], is_integer=True)
formatadoConsginado = excel.numero_formato(produtos['Consignado'])
formatadoConsorcios = excel.numero_formato(produtos['Consórcios'])
formatadoIQC = f'{iqc:.2f}%'.replace('.', ',')
formatadoINAD90 = f'{perc_inad90:.2f}%'.replace('.', ',')
formatadoINAD15 = f'{perc_inad15:.2f}%'.replace('.', ',')
formatadoIPROV = f'{perc_iprov:.2f}%'.replace('.', ',')
formatadoIC = f'{perc_ic:.2f}%'.replace('.', ',')
formatadocaptacao = excel.numero_formato(saldo_depprazoD + saldo_depviD)
formatadoNovosCoop = excel.numero_formato(qtd_novoscoop, is_integer=True)
formatadoIEPSC = f'{iep_sc:.2f}'.replace('.', ',')
formatadoIndeterminado = excel.numero_formato(
    qtd_indeterminado, is_integer=True)


# Dados para os títulos e valores dos cartões
card_carteira = [
    ("Carteira Geral", f'R$ {formatadoCarteiraD}'),
    ("Rec. De Crédito", "R$ 810,30K"),
    ("Contratos Inad", f'R$ {formatadoContratosInad}'),
    ("Novas Operações", f'R$ {formatadoNovasOp}'),
]
card_captacao = [
    ("Depósito Atual", f'R$ {formatadocaptacao}'),
    ("Capital Social", f'R$ {formatadoCapitalD}'),
    ("Indeterminado", formatadoIndeterminado),
    ("Poupança", f'R$ {formatadoPoup}'),
]
card_cooperativismo = [
    ("NPS Geral", "87"),
    ("Cooperados", formatadoCooperados),
    ("Novos Cooperados", formatadoNovosCoop),
    ("Funcionários", "454"),
    ("Ações Passivas", "23"),
    ("Ações Ativas", "1821"),
]
card_produtos = [
    ("Sipag", f'R$ {formatadoSipag}'),
    ("Previdência", formatadoPrevi),
    ("Seguros Gerais", f'R$ {formatadosSegurosG}'),
    ("Consórcios", f'R$ {formatadoConsorcios}'),
    ("Faturamento Cartão", f'R$ {formatadoCart}'),
    ("Consignado", f'R$ {formatadoConsginado}'),
]
card_indicadores = [
    ("IQC", formatadoIQC),
    ("INAD 90", formatadoINAD90),
    ("INAD 15", formatadoINAD15),
    ("IPROV", formatadoIPROV),
    ("IC", formatadoIC),
    ("IEP", formatadoIEPSC),
]

datas_atualizacao = {
    "Carteira Geral": f'Última atualização: {data_carteiraD}',
    "Rec. De Crédito": "Última atualização: 02/04/2024",
    "Depósito Atual": f'Última atualização: {data_depprazoD}',
    "Capital Social": f'Última atualização: {data_capitalD}',
    "Poupança": f'Última atualização: {data_poup}',
    "Indeterminado": f'Última atualização: {data_indeterminado}',
    "Contratos Inad": f'Última atualização: {data_indicadores}',
    "Novas Operações": f'Última atualização: {data_novasOp}',
    "Cooperados": f'Última atualização: {data_cooperados}',
    "Novos Cooperados": f'Última atualização: {data_novoscoop}',
    "Faturamento Cartão": f'Última atualização: {data_cart}',
    "IQC": f'Última atualização: {data_indicadores}',
    "INAD 90": f'Última atualização: {data_indicadores}',
    "INAD 15": f'Última atualização: {data_indicadores}',
    "IPROV": f'Última atualização: {data_indicadores}',
    "IC": f'Última atualização: {data_indicadores}',
    "IEP": f'Última atualização: {maior_dataSC_str}',
    "Sipag": f'Última atualização: {data_produtos}',
    "Seguros Gerais": f'Última atualização: {data_produtos}',
    "Consignado": f'Última atualização: {data_produtos}',
    "Previdência": f'Última atualização: {data_produtos}',
    "Consórcios": f'Última atualização: {data_produtos}',
    "NPS Geral": 'Última atualização: 2024-03',
    "Ações Passivas": 'Última atualização: 2024-03',
    "Ações Ativas": 'Última atualização: 2024-03',
    # Continue para os outros cartões conforme necessário
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
rows_carteira = create_rows_for_cards(card_carteira, datas_atualizacao)
rows_captacao = create_rows_for_cards(card_captacao, datas_atualizacao)
rows_cooperativismo = create_rows_for_cards(
    card_cooperativismo, datas_atualizacao)
rows_produtos = create_rows_for_cards(card_produtos, datas_atualizacao)
rows_indicadores = create_rows_for_cards(card_indicadores, datas_atualizacao)


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
        style={"width": "100%"}
    )


carteira = create_card_with_header(
    "CARTEIRA+", "/carteira", rows_carteira, "carteira")
captacao = create_card_with_header(
    "CAPTAÇÃO+", "/captacao", rows_captacao, "captacao")
cooperativismo = create_card_with_header(
    "COOPERATIVISMO+", "/cooperativismo", rows_cooperativismo, "cooperativismo")
produtos = create_card_with_header(
    "PRODUTOS+", "/produtos", rows_produtos, "produtos")
indicadores = create_card_with_header(
    "INDICADORES GERAIS+", "/indicadores", rows_indicadores, "indicadores")

layout = dbc.Container(
    [carteira, captacao, cooperativismo, produtos, indicadores],
    fluid=True,
    className="py-1"  # py-3 para adicionar padding vertical
)
