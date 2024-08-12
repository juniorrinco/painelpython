import pandas as pd
import numpy as np
from .excel import numero_formato, process_produtos_cnv


def read_excel_data(filepath):
    return pd.read_excel(filepath)


def process_indicadores_qualitativos_teste(selected_pa=None):
    df = read_excel_data(
        r"C:\Users\osmar.rinco\OneDrive - Sicoob\Metas Diárias\Indicadores Qualitativos\IQC INAD IPROV - Diario.xlsx")
    df['Número PA'] = df['Número PA'].astype(str)
    df['Data Movimento'] = pd.to_datetime(df['Data Movimento'])

    if selected_pa:
        selected_pa = [str(pa) for pa in selected_pa]
        df = df[df['Número PA'].isin(selected_pa)]

    if df.empty:
        return {
            'perc_inad_15': [],
            'perc_inad_90': [],
            'iqc': [],
            'ic': [],
            'perc_iprov': [],
            'dates': []
        }

    df_grouped = df.groupby(df['Data Movimento'].dt.to_period('M')).agg({
        'Valor Saldo Devedor Diário INAD 15': 'sum',
        'Valor Saldo Devedor Diário INAD 90': 'sum',
        'Valor Saldo Devedor Diário': 'sum',
        '% Provisão Atual1': 'sum',
        'Nivel Risco Atual': lambda x: (x.isin(['D', 'E', 'F', 'G', 'H'])).sum()
    }).reset_index()

    df_grouped['perc_inad_15'] = df_grouped['Valor Saldo Devedor Diário INAD 15'] / \
        df_grouped['Valor Saldo Devedor Diário'] * 100
    df_grouped['perc_inad_90'] = df_grouped['Valor Saldo Devedor Diário INAD 90'] / \
        df_grouped['Valor Saldo Devedor Diário'] * 100
    df_grouped['perc_iprov'] = df_grouped['% Provisão Atual1'] / \
        df_grouped['Valor Saldo Devedor Diário'] * 100
    df_grouped['ic'] = df_grouped['% Provisão Atual1'] / \
        df_grouped['Valor Saldo Devedor Diário INAD 90'] * 100
    df_grouped['iqc'] = df_grouped['Nivel Risco Atual'] / \
        df_grouped['Valor Saldo Devedor Diário'] * 100

    df_grouped['Data Movimento'] = df_grouped['Data Movimento'].dt.strftime(
        '%Y-%m')

    return {
        'perc_inad_15': df_grouped['perc_inad_15'].tolist(),
        'perc_inad_90': df_grouped['perc_inad_90'].tolist(),
        'iqc': df_grouped['iqc'].tolist(),
        'ic': df_grouped['ic'].tolist(),
        'perc_iprov': df_grouped['perc_iprov'].tolist(),
        'dates': df_grouped['Data Movimento'].tolist()
    }


# Processamento da tabela de indicadores qualitativos
def process_indicadores_qualitativos_apo(selected_pa=None):
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
    latest_data_df = df[df['Data Movimento'] == latest_date]
    # Agrupar os dados por mês e somar os valores
    inad15_data = df.groupby(df['Data Movimento'].dt.to_period('M'))[
        'Valor Saldo Devedor Diário INAD 15'].sum().reset_index()
    inad15_totais = np.array(inad15_data['Valor Saldo Devedor Diário INAD 15'].tolist(
    ))
    saldo_data = df.groupby(df['Data Movimento'].dt.to_period('M'))[
        'Valor Saldo Devedor Diário'].sum().reset_index()
    saldo_totais = np.array(saldo_data['Valor Saldo Devedor Diário'].tolist())

    inad90_data = df.groupby(df['Data Movimento'].dt.to_period('M'))[
        'Valor Saldo Devedor Diário INAD 90'].sum().reset_index()
    inad90_totais = np.array(inad90_data['Valor Saldo Devedor Diário INAD 90'].tolist(
    ))
    niveis_risco_alto = ['D', 'E', 'F', 'G', 'H']
    df_risco_alto = df[df['Nivel Risco Atual'].isin(niveis_risco_alto)]
    iqc_data = df_risco_alto.groupby(df['Data Movimento'].dt.to_period('M'))[
        'Valor Saldo Devedor Diário'].sum().reset_index()
    iqc_totais = np.array(iqc_data['Valor Saldo Devedor Diário'].tolist(
    ))
    iprov_data = df.groupby(df['Data Movimento'].dt.to_period('M'))[
        '% Provisão Atual1'].sum().reset_index()
    iprov_totais = np.array(iprov_data['% Provisão Atual1'].tolist(
    ))
    # Converter os períodos em datas no formato desejado
    saldo_data['Data Movimento'] = saldo_data['Data Movimento'].dt.start_time
    dates = saldo_data['Data Movimento'].dt.strftime(
        date_format='%Y-%m').tolist()

    percentual_iand_15 = np.where(
        saldo_totais != 0, (inad15_totais / saldo_totais) * 100, 0)

    percentual_iand_90 = np.where(
        saldo_totais != 0, (inad90_totais / saldo_totais) * 100, 0)

    percentual_iqc = np.where(
        saldo_totais != 0, (iqc_totais / saldo_totais) * 100, 0)

    percentual_iprov = np.where(
        saldo_totais != 0, (iprov_totais / saldo_totais) * 100, 0)

    percentual_ic = np.where(
        saldo_totais != 0, (iprov_totais / inad90_totais), 0)

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

    return perc_inad_15, perc_inad_90, latest_date, contratos_inad, perc_ic, perc_iprov, perc_iqc, percentual_ic, percentual_iprov, percentual_iqc, percentual_iand_15, percentual_iand_90, dates


perc_inad_15, perc_inad_90, latest_date, contratos_inad, perc_ic, perc_iprov, perc_iqc, percentual_ic, percentual_iprov, percentual_iqc, percentual_iand_15, percentual_iand_90, dates = process_indicadores_qualitativos_apo()


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


