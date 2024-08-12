import pandas as pd
import numpy as np


# Função para ler dados do Excel
def read_excel_data(filepath):
    return pd.read_excel(filepath)


def get_total_on_latest_date(df, value_column, date_column, date_format="%d/%m/%Y"):
    # Identifica a última data disponível no DataFrame
    latest_date = pd.to_datetime(df[date_column].max())

    # Verifica se latest_date é NaT
    if pd.isna(latest_date):
        # Retorna zero ou outro valor adequado e uma mensagem
        return 0, "Data não disponível"

    # Filtra o DataFrame para obter apenas as linhas com a última data
    latest_data_df = df[df[date_column] == latest_date]

    # Calcula a soma dos valores na última data
    total_value_latest_date = latest_data_df[value_column].sum()

    # Formata a última data para o formato desejado
    formatted_latest_date = latest_date.strftime(date_format)

    return total_value_latest_date, formatted_latest_date


def get_monthly_totals_and_dates(df, value_column, date_column, date_format="%Y-%m"):
    # Garantir que a coluna de data está no formato datetime
    df[date_column] = pd.to_datetime(df[date_column])

    # Agrupar os dados por mês e somar os valores
    monthly_data = (
        df.groupby(df[date_column].dt.to_period("M"))[value_column].sum().reset_index()
    )

    # Converter os períodos em datas no formato desejado
    monthly_data[date_column] = monthly_data[date_column].dt.start_time

    monthly_totals = monthly_data[value_column].tolist()
    dates = monthly_data[date_column].dt.strftime(date_format).tolist()

    return monthly_totals, dates


# Função para obter a última data com formatação específica
def get_latest_date(df, date_column, date_format="%d/%m/%Y"):
    return pd.to_datetime(df[date_column].max()).strftime(date_format)


# Processamento dos dados da tabela da receita
def process_receita(selected_pa=None):
    df = read_excel_data(
        r"C:\Users\junio\OneDrive\Área de Trabalho\Arquivos\Receita.xlsx"
    )

    # Convertendo 'loja' para string para garantir a comparação correta
    df["Loja"] = df["Loja"].astype(str)

    if selected_pa:
        # Verificação para garantir que selected_loja é uma lista de strings
        selected_pa = [str(pa) for pa in selected_pa]
        # Filtrando o DataFrame
        df = df[df["Loja"].isin(selected_pa)]

    if df.empty:
        return 0, None, [], []  # Retorna valores padrão

    total_value, latest_date = get_total_on_latest_date(df, "Receita", "Data Movimento")
    monthly_totals, dates = get_monthly_totals_and_dates(
        df, "Receita", "Data Movimento"
    )

    return total_value, latest_date, monthly_totals, dates


# Processamento dos dados da tabela do faturamento
def process_faturamento(selected_pa=None):
    df = read_excel_data(
        r"C:\Users\junio\OneDrive\Área de Trabalho\Arquivos\Faturamento.xlsx"
    )

    # Convertendo 'Loja' para string para garantir a comparação correta
    df["Loja"] = df["Loja"].astype(str)

    if selected_pa:
        # Verificação para garantir que selected_pa é uma lista de strings
        selected_pa = [str(pa) for pa in selected_pa]
        # Filtrando o DataFrame
        df = df[df["Loja"].isin(selected_pa)]

    if df.empty:
        return 0, None, [], []  # Retorna valores padrão

    total_value, latest_date = get_total_on_latest_date(
        df, "Faturamento", "Data Movimento"
    )
    monthly_totals, dates = get_monthly_totals_and_dates(
        df, "Faturamento", "Data Movimento"
    )

    return total_value, latest_date, monthly_totals, dates


# Processamento dos dados da tabela do capital
def process_capital(selected_pa=None):
    df = read_excel_data(
        r"C:\Users\junio\OneDrive\Área de Trabalho\Arquivos\Capital.xlsx"
    )
    # Convertendo 'Loja' para string para garantir a comparação correta
    df["Loja"] = df["Loja"].astype(str)

    if selected_pa:
        # Verificação para garantir que selected_pa é uma lista de strings
        selected_pa = [str(pa) for pa in selected_pa]
        # Filtrando o DataFrame
        df = df[df["Loja"].isin(selected_pa)]

    if df.empty:
        return 0, None, [], []  # Retorna valores padrão
    total_value, latest_date = get_total_on_latest_date(df, "Capital", "Data Movimento")
    monthly_totals, dates = get_monthly_totals_and_dates(
        df, "Capital", "Data Movimento"
    )

    return total_value, latest_date, monthly_totals, dates


# Processamento da tabela de depósito a prazo
def process_deposito_prazo(selected_pa=None):
    df = read_excel_data(
        r"C:\Users\junio\OneDrive\Área de Trabalho\Arquivos\Deposito a Prazo.xlsx"
    )
    # Convertendo 'Loja' para string para garantir a comparação correta
    df["Loja"] = df["Loja"].astype(str)

    if selected_pa:
        # Verificação para garantir que selected_pa é uma lista de strings
        selected_pa = [str(pa) for pa in selected_pa]
        # Filtrando o DataFrame
        df = df[df["Loja"].isin(selected_pa)]

    if df.empty:
        return 0, None, [], []  # Retorna valores padrão
    total_value, latest_date = get_total_on_latest_date(df, "Prazo", "Data Movimento")
    monthly_totals, dates = get_monthly_totals_and_dates(df, "Prazo", "Data Movimento")

    return total_value, latest_date, monthly_totals, dates


# Processamento da tabela de depósito à vista
def process_deposito_vista(selected_pa=None):
    df = read_excel_data(
        r"C:\Users\junio\OneDrive\Área de Trabalho\Arquivos\Deposito a Vista.xlsx"
    )
    # Convertendo 'Loja' para string para garantir a comparação correta
    df["Loja"] = df["Loja"].astype(str)

    if selected_pa:
        # Verificação para garantir que selected_pa é uma lista de strings
        selected_pa = [str(pa) for pa in selected_pa]
        # Filtrando o DataFrame
        df = df[df["Loja"].isin(selected_pa)]

    if df.empty:
        return 0, None, [], []  # Retorna valores padrão
    total_value, latest_date = get_total_on_latest_date(df, "Vista", "Data Movimento")
    monthly_totals, dates = get_monthly_totals_and_dates(df, "Vista", "Data Movimento")
    return total_value, latest_date, monthly_totals, dates


# Processamento da tabela de clientes total
def process_cooperados_total(selected_pa=None):
    df = read_excel_data(
        r"C:\Users\junio\OneDrive\Área de Trabalho\Arquivos\Clientes.xlsx"
    )
    # Convertendo 'Loja' para string para garantir a comparação correta
    df["Loja"] = df["Loja"].astype(str)

    if selected_pa:
        # Verificação para garantir que selected_pa é uma lista de strings
        selected_pa = [str(pa) for pa in selected_pa]
        # Filtrando o DataFrame
        df = df[df["Loja"].isin(selected_pa)]

    if df.empty:
        return 0, None, [], []  # Retorna valores padrão
    total_value, latest_date = get_total_on_latest_date(
        df, "Clientes", "Data Movimento", date_format="%m/%Y"
    )
    monthly_totals, dates = get_monthly_totals_and_dates(
        df, "Clientes", "Data Movimento", date_format="%Y-%m"
    )
    return total_value, latest_date, monthly_totals, dates


# Processamento da tabela de novos clientes
def process_novos_cooperados(selected_pa=None):
    df = read_excel_data(
        r"C:\Users\junio\OneDrive\Área de Trabalho\Arquivos\Novos Clientes.xlsx"
    )
    df["Data Movimento"] = pd.to_datetime(df["Data Movimento"])
    start_of_month = pd.Timestamp.now().normalize().replace(day=1)

    # Adicione uma verificação para filtrar por loja, se uma lista de loja for fornecida
    if selected_pa:
        df = df[df["Loja"].astype(str).isin(selected_pa)]

    df = df[df["Data Movimento"] >= start_of_month]
    total_novos_cooperados = df["Clientes"].sum()
    latest_date = start_of_month.strftime("%m/%Y")
    return total_novos_cooperados, latest_date


# Função de formatação de número adaptada para os diferentes tipos de valores
def numero_formato(num, precision=1, is_integer=False):
    if is_integer:
        return f"{num:,}".replace(",", ".")
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    num_formatado = f"{num:.{precision}f}".replace(".", ",")
    return f'{num_formatado}{" KMBT"[magnitude]}'.strip()
