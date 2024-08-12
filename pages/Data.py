import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from datetime import datetime
from babel.dates import format_date
import pandas as pd
import numpy as np


def read_excel_data(filepath):
    return pd.read_excel(filepath)


def get_total_on_latest_date(df, value_column, date_column, date_format='%d/%m/%Y'):
    latest_date = pd.to_datetime(df[date_column].max())
    if pd.isna(latest_date):
        return 0, 'Data não disponível'
    latest_data_df = df[df[date_column] == latest_date]
    total_value_latest_date = latest_data_df[value_column].sum()
    formatted_latest_date = latest_date.strftime(date_format)
    return total_value_latest_date, formatted_latest_date


def get_monthly_totals_and_dates(df, value_column, date_column, date_format='%Y-%m'):
    df[date_column] = pd.to_datetime(df[date_column])
    monthly_data = df.groupby(df[date_column].dt.to_period('M'))[
        value_column].sum().reset_index()
    monthly_data[date_column] = monthly_data[date_column].dt.start_time
    monthly_totals = monthly_data[value_column].tolist()
    datesm = monthly_data[date_column].tolist()
    return monthly_totals, datesm


def process_cooperados_total():
    df = read_excel_data(
        r"C:\Users\osmar.rinco\OneDrive - Sicoob\Metas Diárias\Cooperados\Cooperados Total - Diário.xlsx")
    if df.empty:
        return 0, None, [], []
    total_value, latest_date = get_total_on_latest_date(
        df, 'Quantidade de Associados', 'Data Movimento', date_format='%m/%Y')
    monthly_totals, datescoop = get_monthly_totals_and_dates(
        df, 'Quantidade de Associados', 'Ano-Mês Movimento', date_format='%Y-%m')
    return total_value, latest_date, monthly_totals, datescoop

# Função para formatar a data para o formato pt-BR


def format_date_pt_br(date):
    return format_date(date, format='MMMM yyyy', locale='pt_BR').capitalize()


# Chama a função para processar os dados
total_value, latest_date, monthly_totals, datescoop = process_cooperados_total()

# Converte as datas de string para objetos datetime
dates = [datetime.strptime(date.strftime('%Y-%m'), '%Y-%m')
         for date in datescoop]

# Formata as datas
formatted_dates = [format_date_pt_br(date) for date in dates]

# Inicializa o app do Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                go.Scatter(
                    x=dates,
                    y=monthly_totals,
                    mode='lines+markers'
                )
            ],
            'layout': go.Layout(
                title='Cooperados por mês e ano',
                xaxis={
                    'title': 'Data',
                    'tickmode': 'array',
                    'tickvals': dates,
                    'ticktext': formatted_dates
                },
                yaxis={'title': 'Valores'}
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
