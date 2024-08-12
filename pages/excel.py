import pandas as pd
import numpy as np

# Função para ler dados do Excel


def read_excel_data(filepath):
    return pd.read_excel(filepath)


def get_total_on_latest_date(df, value_column, date_column, date_format='%d/%m/%Y'):
    # Identifica a última data disponível no DataFrame
    latest_date = pd.to_datetime(df[date_column].max())

    # Verifica se latest_date é NaT
    if pd.isna(latest_date):
        # Retorna zero ou outro valor adequado e uma mensagem
        return 0, 'Data não disponível'

    # Filtra o DataFrame para obter apenas as linhas com a última data
    latest_data_df = df[df[date_column] == latest_date]

    # Calcula a soma dos valores na última data
    total_value_latest_date = latest_data_df[value_column].sum()

    # Formata a última data para o formato desejado
    formatted_latest_date = latest_date.strftime(date_format)

    return total_value_latest_date, formatted_latest_date


def get_monthly_totals_and_dates(df, value_column, date_column, date_format='%Y-%m'):
    # Garantir que a coluna de data está no formato datetime
    df[date_column] = pd.to_datetime(df[date_column])

    # Agrupar os dados por mês e somar os valores
    monthly_data = df.groupby(df[date_column].dt.to_period('M'))[
        value_column].sum().reset_index()

    # Converter os períodos em datas no formato desejado
    monthly_data[date_column] = monthly_data[date_column].dt.start_time

    monthly_totals = monthly_data[value_column].tolist()
    dates = monthly_data[date_column].dt.strftime(date_format).tolist()

    return monthly_totals, dates


# Função para obter a última data com formatação específica
def get_latest_date(df, date_column, date_format='%d/%m/%Y'):
    return pd.to_datetime(df[date_column].max()).strftime(date_format)


# Processamento dos dados da tabela da carteira
def process_carteira(selected_pa=None):
    df = read_excel_data(
        r"C:\Users\osmar.rinco\OneDrive - Sicoob\Metas Diárias\Crédito\Posição Das Carteiras - Diario.xlsx")

    # Convertendo 'Número PA' para string para garantir a comparação correta
    df['Número PA'] = df['Número PA'].astype(str)

    if selected_pa:
        # Verificação para garantir que selected_pa é uma lista de strings
        selected_pa = [str(pa) for pa in selected_pa]
        # Filtrando o DataFrame
        df = df[df['Número PA'].isin(selected_pa)]

    if df.empty:
        return 0, None, [], []  # Retorna valores padrão

    total_value, latest_date = get_total_on_latest_date(
        df, 'Valor Saldo Devedor', 'Data Movimento')
    monthly_totals, dates = get_monthly_totals_and_dates(
        df, 'Valor Saldo Devedor', 'Data Movimento')

    return total_value, latest_date, monthly_totals, dates


# Processamento dos dados da tabela da carteira
def process_poupanca(selected_pa=None):
    df = read_excel_data(
        r"C:\Users\osmar.rinco\OneDrive - Sicoob\Metas Diárias\Poupança\Poupança - Diario.xlsx")

    # Convertendo 'Número PA' para string para garantir a comparação correta
    df['Número PA'] = df['Número PA'].astype(str)

    if selected_pa:
        # Verificação para garantir que selected_pa é uma lista de strings
        selected_pa = [str(pa) for pa in selected_pa]
        # Filtrando o DataFrame
        df = df[df['Número PA'].isin(selected_pa)]

    if df.empty:
        return 0, None, [], []  # Retorna valores padrão

    total_value, latest_date = get_total_on_latest_date(
        df, 'Valor Saldo Último dia Mês', 'Data Movimento')
    monthly_totals, dates = get_monthly_totals_and_dates(
        df, 'Valor Saldo Último dia Mês', 'Data Movimento')

    return total_value, latest_date, monthly_totals, dates


# Processamento dos dados da tabela do capital
def process_capital(selected_pa=None):
    df = read_excel_data(
        r"C:\Users\osmar.rinco\OneDrive - Sicoob\Metas Diárias\Capital\Capital Social - Diario.xlsx")
    # Convertendo 'Número PA' para string para garantir a comparação correta
    df['Número PA'] = df['Número PA'].astype(str)

    if selected_pa:
        # Verificação para garantir que selected_pa é uma lista de strings
        selected_pa = [str(pa) for pa in selected_pa]
        # Filtrando o DataFrame
        df = df[df['Número PA'].isin(selected_pa)]

    if df.empty:
        return 0, None, [], []  # Retorna valores padrão
    total_value, latest_date = get_total_on_latest_date(
        df, 'Valor Saldo Final Integralizado', 'Data Movimento')
    monthly_totals, dates = get_monthly_totals_and_dates(
        df, 'Valor Saldo Final Integralizado', 'Data Movimento')

    return total_value, latest_date, monthly_totals, dates


# Processamento da tabela de depósito a prazo
def process_deposito_prazo(selected_pa=None):
    df = read_excel_data(
        r"C:\Users\osmar.rinco\OneDrive - Sicoob\Metas Diárias\Captação\Deposito a Prazo - Diario.xlsx")
    # Convertendo 'Número PA' para string para garantir a comparação correta
    df['Número PA'] = df['Número PA'].astype(str)

    if selected_pa:
        # Verificação para garantir que selected_pa é uma lista de strings
        selected_pa = [str(pa) for pa in selected_pa]
        # Filtrando o DataFrame
        df = df[df['Número PA'].isin(selected_pa)]

    if df.empty:
        return 0, None, [], []  # Retorna valores padrão
    total_value, latest_date = get_total_on_latest_date(
        df, 'Valor Saldo Diário', 'Data Movimento')
    monthly_totals, dates = get_monthly_totals_and_dates(
        df, 'Valor Saldo Diário', 'Data Movimento')

    return total_value, latest_date, monthly_totals, dates


# Processamento da tabela de depósito a prazo LCI
def process_deposito_prazo_lci(selected_pa=None):
    df = read_excel_data(
        r"C:\Users\osmar.rinco\OneDrive - Sicoob\Metas Diárias\Captação\Deposito a Prazo - Diario.xlsx")
    df['Número PA'] = df['Número PA'].astype(str)

    if selected_pa:
        # Verificação para garantir que selected_pa é uma lista de strings
        selected_pa = [str(pa) for pa in selected_pa]
        # Filtrando o DataFrame
        df = df[df['Número PA'].isin(selected_pa)]

    lci_df = df[df['Tipo Modalidade Captação'] == 'LCI']

    if lci_df.empty:
        return (0, 'Data não disponível', [], [])
    total_value, latest_date = get_total_on_latest_date(
        lci_df, 'Valor Saldo Diário', 'Data Movimento')
    monthly_totals, dates = get_monthly_totals_and_dates(
        lci_df, 'Valor Saldo Diário', 'Data Movimento')

    return total_value, latest_date, monthly_totals, dates


# Processamento da tabela de depósito a prazo RDC
def process_deposito_prazo_rdc(selected_pa=None):
    df = read_excel_data(
        r"C:\Users\osmar.rinco\OneDrive - Sicoob\Metas Diárias\Captação\Deposito a Prazo - Diario.xlsx")
    df['Número PA'] = df['Número PA'].astype(str)

    if selected_pa:
        # Verificação para garantir que selected_pa é uma lista de strings
        selected_pa = [str(pa) for pa in selected_pa]
        # Filtrando o DataFrame
        df = df[df['Número PA'].isin(selected_pa)]

    rdc_df = df[df['Tipo Modalidade Captação'] == 'RDC']

    if rdc_df.empty:
        return (0, 'Data não disponível', [], [])
    total_value, latest_date = get_total_on_latest_date(
        rdc_df, 'Valor Saldo Diário', 'Data Movimento')
    monthly_totals, dates = get_monthly_totals_and_dates(
        rdc_df, 'Valor Saldo Diário', 'Data Movimento')

    return total_value, latest_date, monthly_totals, dates


# Processamento da tabela de depósito a prazo LCA
def process_deposito_prazo_lca(selected_pa=None):
    df = read_excel_data(
        r"C:\Users\osmar.rinco\OneDrive - Sicoob\Metas Diárias\Captação\Deposito a Prazo - Diario.xlsx")
    df['Número PA'] = df['Número PA'].astype(str)

    if selected_pa:
        df = df[df['Número PA'].isin([str(pa) for pa in selected_pa])]

    lca_df = df[df['Tipo Modalidade Captação'] == 'LCA']

    if lca_df.empty:
        return (0, 'Data não disponível', [], [])

    total_value, latest_date = get_total_on_latest_date(
        lca_df, 'Valor Saldo Diário', 'Data Movimento')
    monthly_totals, dates = get_monthly_totals_and_dates(
        lca_df, 'Valor Saldo Diário', 'Data Movimento')

    return total_value, latest_date, monthly_totals, dates


# Processamento da tabela de depósito à vista
def process_deposito_vista(selected_pa=None):
    df = read_excel_data(
        r"C:\Users\osmar.rinco\OneDrive - Sicoob\Metas Diárias\Captação\Deposito a Vista - Diario.xlsx")
    # Convertendo 'Número PA' para string para garantir a comparação correta
    df['Número PA'] = df['Número PA'].astype(str)

    if selected_pa:
        # Verificação para garantir que selected_pa é uma lista de strings
        selected_pa = [str(pa) for pa in selected_pa]
        # Filtrando o DataFrame
        df = df[df['Número PA'].isin(selected_pa)]

    if df.empty:
        return 0, None, [], []  # Retorna valores padrão
    total_value, latest_date = get_total_on_latest_date(
        df, 'Valor Saldo Final Depósito Conta Corrente', 'Data Movimento')
    monthly_totals, dates = get_monthly_totals_and_dates(
        df, 'Valor Saldo Final Depósito Conta Corrente', 'Data Movimento')
    return total_value, latest_date, monthly_totals, dates


# Processamento da tabela de cartões
def process_cartoes():
    df = read_excel_data(
        r"C:\Users\osmar.rinco\OneDrive - Sicoob\Metas Diárias\Cartões\Cartão Faturamento - Diario.xlsx")
    return get_total_on_latest_date(df, 'Valor Transação', 'Data')


# Processamento da tabela de liquidação cobrança
def process_liquidacao_cobranca():
    df = read_excel_data(
        r"C:\Users\osmar.rinco\OneDrive - Sicoob\Metas Diárias\Cobrança Bancária\Liquidação Cobrança - Diario.xlsx")
    return get_total_on_latest_date(df, 'Valor Liquidado', 'Data Movimento')


# Processamento da tabela de cooperados total
def process_cooperados_total(selected_pa=None):
    df = read_excel_data(
        r"C:\Users\osmar.rinco\OneDrive - Sicoob\Metas Diárias\Cooperados\Cooperados Total - Diário.xlsx")
    # Convertendo 'Número PA' para string para garantir a comparação correta
    df['Número PA'] = df['Número PA'].astype(str)

    if selected_pa:
        # Verificação para garantir que selected_pa é uma lista de strings
        selected_pa = [str(pa) for pa in selected_pa]
        # Filtrando o DataFrame
        df = df[df['Número PA'].isin(selected_pa)]

    if df.empty:
        return 0, None, [], []  # Retorna valores padrão
    total_value, latest_date = get_total_on_latest_date(
        df, 'Quantidade de Associados', 'Data Movimento', date_format='%m/%Y')
    monthly_totals, dates = get_monthly_totals_and_dates(
        df, 'Quantidade de Associados', 'Ano-Mês Movimento', date_format='%Y-%m')
    return total_value, latest_date, monthly_totals, dates


# Processamento da tabela de novos cooperados
def process_novos_cooperados(selected_pa=None):
    df = read_excel_data(
        r"C:\Users\osmar.rinco\OneDrive - Sicoob\Metas Diárias\Cooperados\Novos cooperados Diário Analítico.xlsx")
    df['Data Matricula'] = pd.to_datetime(df['Data Matricula'])
    start_of_month = pd.Timestamp.now().normalize().replace(day=1)

    # Adicione uma verificação para filtrar por PAs, se uma lista de PAs for fornecida
    if selected_pa:
        df = df[df['Número PA'].astype(str).isin(selected_pa)]

    df = df[df['Data Matricula'] >= start_of_month]
    total_novos_cooperados = df['Quantidade de Associados'].sum()
    latest_date = start_of_month.strftime('%m/%Y')
    return total_novos_cooperados, latest_date

# Processar indicadores qualitativos


def process_indicadores_qualitativos(selected_pa=None):
    df = read_excel_data(
        r"C:\Users\osmar.rinco\OneDrive - Sicoob\Metas Diárias\Indicadores Qualitativos\IQC INAD IPROV - Diario.xlsx")
    # Garantir que 'Número PA' é uma string para comparação
    df['Número PA'] = df['Número PA'].astype(str)

    if selected_pa:
        # Verificação para garantir que selected_pa é uma lista de strings
        selected_pa = [str(pa) for pa in selected_pa]
        # Filtrando o DataFrame
        df = df[df['Número PA'].isin(selected_pa)]

    if df.empty:
        # Retorna valores padrão se não houver valores
        return 0, 0, None, 0, 0, 0, 0, [], []
    # Convertendo a coluna de Data para datetime
    latest_date = pd.to_datetime(df['Data Movimento'].max())
    # Formata a última data para o formato desejado
    ultima_data_convertida = pd.to_datetime(
        df['Data Movimento'].max()).strftime('%d/%m/%Y')
    latest_data_df = df[df['Data Movimento'] == latest_date]
    total_value_latest_date_saldo_inad15 = latest_data_df['Valor Saldo Devedor Diário INAD 15'].sum(
    )
    total_value_latest_date_saldo_inad90 = latest_data_df['Valor Saldo Devedor Diário INAD 90'].sum(
    )
    total_value_latest_date_saldo_provisao = latest_data_df['% Provisão Atual1'].sum(
    )
    total_value_latest_date_saldo_devedor = latest_data_df['Valor Saldo Devedor Diário'].sum(
    )
    perc_inad_15 = (total_value_latest_date_saldo_inad15 / total_value_latest_date_saldo_devedor) * \
        100 if total_value_latest_date_saldo_devedor else 0
    perc_inad_90 = (total_value_latest_date_saldo_inad90 / total_value_latest_date_saldo_devedor) * \
        100 if total_value_latest_date_saldo_devedor else 0
    perc_iprov = (total_value_latest_date_saldo_provisao / total_value_latest_date_saldo_devedor) * \
        100 if total_value_latest_date_saldo_devedor else 0
    perc_ic = (total_value_latest_date_saldo_provisao /
               total_value_latest_date_saldo_inad90)
    contratos_inad = total_value_latest_date_saldo_inad15 + \
        total_value_latest_date_saldo_inad90
    niveis_risco_alto = ['D', 'E', 'F', 'G', 'H']
    # df_risco_alto = df[df['Nivel Risco Atual'].isin(niveis_risco_alto)]
    saldo_devedor_risco_alto = df['Valor Saldo Devedor Diário'][(
        df['Nivel Risco Atual'].isin(niveis_risco_alto)) & (df['Data Movimento'] == latest_date)].sum()
    perc_iqc = (saldo_devedor_risco_alto / total_value_latest_date_saldo_devedor) * \
        100 if total_value_latest_date_saldo_devedor else 0

    return perc_inad_15, perc_inad_90, ultima_data_convertida, contratos_inad, perc_ic, perc_iprov, perc_iqc


# Processamento da tabela IEP do Sicoob Centro
def process_iep_sicoob_centro():
    df = read_excel_data(
        r"C:\Users\osmar.rinco\OneDrive - Sicoob\Metas Diárias\Indicadores Qualitativos\IEP SC.xlsx")
    df['Ano-Mês Movimento'] = pd.to_datetime(
        df['Ano-Mês Movimento'], format='%Y-%m')
    latest_data = df[df['Ano-Mês Movimento'] == df['Ano-Mês Movimento'].max()]
    iep_sc = latest_data['Valor Acumulado 12 Meses'].sum()
    latest_date = latest_data['Ano-Mês Movimento'].max().strftime('%m/%Y')
    return iep_sc, latest_date


# Processamento da tabela IEP por PA
def process_iep(selected_pa=None):
    df = read_excel_data(
        r"C:\Users\osmar.rinco\OneDrive - Sicoob\Metas Diárias\Indicadores Qualitativos\IEP PA.xlsx")
    # Garantir que 'Número PA' é uma string para comparação
    df['Número PA'] = df['Número PA'].astype(str)

    if selected_pa:
        # Verificação para garantir que selected_pa é uma lista de strings
        selected_pa = [str(pa) for pa in selected_pa]
        # Filtrando o DataFrame
        df = df[df['Número PA'].isin(selected_pa)]

    if df.empty:
        # Retorna valores padrão se não houver valores
        return 0, 0, [], []
    df['Ano-Mês Movimento'] = pd.to_datetime(
        df['Ano-Mês Movimento'], format='%Y-%m')
    # Agrupar os dados por mês e somar os valores
    divisor_data = df.groupby(df['Ano-Mês Movimento'].dt.to_period('M'))[
        'Divisor'].sum().reset_index()
    divisor_totais = np.array(divisor_data['Divisor'].tolist(
    ))
    dividendo_data = df.groupby(df['Ano-Mês Movimento'].dt.to_period('M'))[
        'Dividendo'].sum().reset_index()
    dividendo_totais = np.array(dividendo_data['Dividendo'].tolist(
    ))
    dates = divisor_data['Ano-Mês Movimento'].dt.strftime(
        date_format='%Y-%m').tolist()

    iep_pa = np.where(
        divisor_totais != 0, (dividendo_totais / divisor_totais) * 100 * -1, 0)

    latest_data = df[df['Ano-Mês Movimento'] == df['Ano-Mês Movimento'].max()]
    divisor = latest_data['Divisor'].sum()
    dividendo = latest_data['Dividendo'].sum()
    iep_real = (dividendo/divisor)*100*-1
    latest_date = latest_data['Ano-Mês Movimento'].max().strftime('%m/%Y')
    return iep_real, latest_date, iep_pa, dates


# Processamento da tabela de novas operações
def process_novas_operacoes(selected_pa=None):
    df = read_excel_data(
        r"C:\Users\osmar.rinco\OneDrive - Sicoob\Metas Diárias\Novas Operações\Novas Operações - Diário.xlsx")
    # Convertendo 'Número PA' para string para garantir a comparação correta
    df['Número PA'] = df['Número PA'].astype(str)

    if selected_pa:
        # Verificação para garantir que selected_pa é uma lista de strings
        selected_pa = [str(pa) for pa in selected_pa]
        # Filtrando o DataFrame
        df = df[df['Número PA'].isin(selected_pa)]

    if df.empty:
        return 0, None, [], []  # Retorna valores padrão
    total_novas_operacoes = df['Valor Contrato'].sum()
    latest_date = get_latest_date(df, 'Data Movimento')
    return total_novas_operacoes, latest_date


# Processamento da tabela de produtos CNV (Sipag, Previdência, Seguros Gerais, Consórcios, Faturamento Cartão, Consignado)
def process_produtos_cnv(selected_pa=None):
    df = read_excel_data(
        r"C:\Users\osmar.rinco\OneDrive - Sicoob\Metas Diárias\Metas CNV\produtos_cnv.xlsx")
    produtos = {
        'Sipag': df[df['PRODUTO'] == 'SIPAG']['Produção'].sum(),
        'Previdência': df[df['PRODUTO'].isin(['PREVIDENCIA_MI', 'PREVIDENCIA_VGBL'])]['Produção'].sum(),
        'Seguros Gerais': df[df['PRODUTO'] == 'SEGUROS_GERAIS']['Produção'].sum(),
        'Consórcios': df[df['PRODUTO'] == 'CONSORCIOS']['Produção'].sum(),
        'Faturamento Cartão': df[df['PRODUTO'] == 'FATURAMENTO_CARTAO']['Produção'].sum(),
        'Consignado': df[df['PRODUTO'] == 'CONSIGNADO']['Produção'].sum(),
        'Crédito Digital': df[df['PRODUTO'] == 'CREDITO_DIGITAL']['Produção'].sum(),
        'Câmbio': df[df['PRODUTO'] == 'CAMBIO']['Produção'].sum(),
        'Poupança': df[df['PRODUTO'] == 'POUPANCA']['Produção'].sum(),
        'Renda Fixa': df[df['PRODUTO'] == 'RENDA_FIXA']['Produção'].sum(),
        'Capital': df[df['PRODUTO'] == 'CAPITAL']['Produção'].sum(),
        'SicoobCard': df[df['PRODUTO'] == 'CARTOES']['Produção'].sum(),
        'Coopcerto': df[df['PRODUTO'] == 'COOPCERTO']['Produção'].sum(),
        'Cobrança Bancária': df[df['PRODUTO'] == 'COBRANCA']['Produção'].sum(),
        'Seguro Vida Arrecadação': df[df['PRODUTO'] == 'SEGURO_VIDA']['Produção'].sum(),
        'Crédito Rural': df[df['PRODUTO'] == 'CREDITO_RURAL']['Produção'].sum(),
        'Seguro Rural': df[df['PRODUTO'] == 'SEGURO_RURAL']['Produção'].sum()
    }
    latest_date = get_latest_date(df, 'Data Atualização')
    return produtos, latest_date


# Processamento da tabela de indeterminados
def process_indeterminados():
    df = read_excel_data(
        r"C:\Users\osmar.rinco\OneDrive - Sicoob\Metas Diárias\Indeterminados\Cooperados com indeterminado.xlsx")
    indeterminado_filtro = ['SIM']
    qtd_indeterminado = df[df['Indicador Associado Possui Integralização Indeterminada'].isin(
        indeterminado_filtro)]['Indicador Associado Possui Integralização Indeterminada'].count()
    data_indeterminado = pd.to_datetime(
        df['Ano-Mês Movimento'].max()).strftime('%m/%Y')
    return qtd_indeterminado, data_indeterminado


# Função de formatação de número adaptada para os diferentes tipos de valores
def numero_formato(num, precision=1, is_integer=False):
    if is_integer:
        return f"{num:,}".replace(',', '.')
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    num_formatado = f'{num:.{precision}f}'.replace('.', ',')
    return f'{num_formatado}{" KMBT"[magnitude]}'.strip()
