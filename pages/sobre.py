import dash
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(__name__, path='/sobre', name='SOBRE')

layout = html.Div([
    html.H1("SOBRE O PAINEL DA DIRETORIA", className="text-header"),

    html.P("O Painel da Diretoria é uma ferramenta dinâmica e interativa projetada para fornecer uma visão geral rápida, mas abrangente, das métricas críticas e KPIs que são vitais para as operações e estratégia de nossa organização.", className="text-body"),

    html.H2("CARTEIRA", className="text-carteira"),
    html.P([
        "A seção ",
        html.Span("Carteira"),
        " oferece insights sobre os ativos sob gestão, incluindo:"
    ], style={"color": "#ffffff"}),
    html.Ul([
        html.Li(
            "Recuperação de Crédito: Acompanhamento do desempenho e eficiência nas ações de recuperação."),
        html.Li(
            "Contratos Inadimplentes: Monitoramento da inadimplência para ações de melhoria contínua.")
    ], className="text-list"),

    html.H2("CAPTAÇÃO", className="text-captacao"),
    html.P("Em Captação, enfocamos a saúde financeira, com dados sobre:",
           style={"color": "#ffffff"}),
    html.Ul([
        html.Li("Depósitos: Medidas dos depósitos totais e a liquidez da instituição.", style={
                "color": "#ffffff"}),
        html.Li(
            "Capital Social: O capital mantido pelos cooperados e o crescimento orgânico do mesmo.")
    ], className="text-list"),

    html.H2("COOPERATIVISMO", className="text-cooperativismo"),
    html.P("A seção Cooperativismo reflete o compromisso com nossos membros, evidenciando:",
           style={"color": "#ffffff"}),
    html.Ul([
        html.Li("NPS Geral: Nível de satisfação e lealdade dos cooperados."),
        html.Li("Novos Cooperados: Crescimento do nosso corpo social.")
    ], className="text-list"),

    html.H2("PRODUTOS", className="text-produtos"),
    html.P("Produtos mostra a adoção e o uso dos produtos oferecidos, como:",
           style={"color": "#ffffff"}),
    html.Ul([
        html.Li("Sipag: Volume transacionado através do nosso sistema de pagamentos."),
        html.Li(
            "Previdência e Seguros: Engajamento com nossas soluções de segurança financeira.")
    ], className="text-list"),

    html.H2("INDICADORES GERAIS", className="text-indicadores"),
    html.P("Finalmente, Indicadores Gerais apresenta indicadores chave de desempenho do mercado e regulatórios.",
           style={"color": "#ffffff"}),

    html.Hr(className="divider"),

    html.P("Este painel é atualizado regularmente para garantir que a diretoria tenha as informações mais atuais à mão para tomar decisões informadas e estratégicas.", className="text-footer")
    # html.Img(src=dash.get_asset_url('7.png'))
], className="sobre-container")
