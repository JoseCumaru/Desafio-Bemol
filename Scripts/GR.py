import pandas as pd
import os
import webbrowser
import matplotlib.pyplot as plt

dir_relatorio = "../Relatorio/"

def ler_volume_vendas():
    return pd.read_csv('../Dados/Tratados/volume_vendas_por_categoria_ordenado.csv')

def ler_media_avaliacao():
    return pd.read_csv('../Dados/Tratados/media_avaliacao_por_produto_ordenado.csv')


def ler_lucro_por_categoria():
    return pd.read_csv('../Dados/Tratados/lucro_estimado_por_categoria_ordenado.csv')  # Correção: 'lucro_estimado' em vez de 'lucro_total'


def ler_metricas_entrega():
    return pd.read_csv('../Dados/Tratados/orders_df_metrics.csv')


def gerar_relatorio():
    volume_vendas = ler_volume_vendas()
    media_avaliacao = ler_media_avaliacao()
    lucro_por_categoria = ler_lucro_por_categoria()
    metricas_entrega = ler_metricas_entrega()

    html_report = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Report</title>
    <style>
        /* Estilos CSS */
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 10px;
        }}
        h2 {{
            color: #333;
        }}
        h1, h3{{
            color: white;
            background-color: #333;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        .imagem {{
            margin-bottom: 20px;
        }}
        .imagem-grande{{
            height: 650px;
        }}
        img {{
            height:100%;
            max-width: 100%;
        }}

    </style>
</head>
<body>
"""

    html_report += "<div class='container'>\n"
    html_report += "<h1>Exploratory Data Analysis Report</h1>\n"
    html_report += "<p>This report presents the results of the exploratory data analysis conducted on the dataset of the Brazilian e-commerce.</p>\n"

    html_report += "<h2>Context</h2>"
    html_report += "<p>The Brazilian e-commerce dataset contains information about orders, products, reviews, and other data. The aim of exploratory analysis is to better understand sales patterns, customer satisfaction, and profitability by product category.</p>"

    html_report += f"""
            <h2>Logistics Analysis</h2>
            <h3>Delivery Time Statistics</h3>
            <p>Mean: {metricas_entrega['tempo_entrega'].iloc[0]:.2f} days</p>
            <p>Median: {metricas_entrega['tempo_entrega'].iloc[1]:.2f} days</p>
            <h3>Delivery Delay Statistics</h3>
            <p>Mean: {metricas_entrega['atraso_entrega'].iloc[0]:.2f} days</p>
            <p>Median: {metricas_entrega['atraso_entrega'].iloc[1]:.2f} days</p>
    """
    html_report += f'<img src="../Figuras/distribuicao_tempo_entrega.png" alt="Volume de Vendas por Categoria">\n'

    html_report += "<h2>Visualizations</h2>\n"

    html_report += "<div class='imagem'>\n"
    html_report += "<h3>Sales Performance Analysis (Sales Volume by Category)</h3>\n"
    html_report += "<p>This graph shows the total sales volume by product category. The categories with the highest sales volume are Health & Beauty and Gifts & Watches.</p>"
    html_report += f'<img src="../Figuras/volume_vendas_por_categoria.png" alt="Volume de Vendas por Categoria">\n'
    html_report += "</div>\n"

    html_report += "<div class='imagem'>\n"
    html_report += "<h3>Customer Satisfaction Analysis (Product Reviews)</h3>\n"
    html_report += "<p>This graph displays the distribution of product reviews. Most reviews are in the 5 range with a small percentage of negative reviews.</p>"
    html_report += f'<img src="../Figuras/distribuicao_avaliacoes.png" alt="Distribuição das Avaliações">\n'
    html_report += "</div>\n"

    html_report += "<div class='imagem-grande'>\n"
    html_report += "<h3>Financial Analysis (Estimated Profitability by Category)</h3>\n"
    html_report += f"<pThis graph shows profitability by product category, considering both product price and shipping value. The most profitable categories are {lucro_por_categoria['product_category_name_english'].iloc[0]} and {lucro_por_categoria['product_category_name_english'].iloc[1]}.</p>\n"
    html_report += f'<img src="../Figuras/lucro_estimado_por_categoria.png" alt="Lucratividade por Categoria">\n'
    html_report += "<h2>Conclusions</h2>"
    html_report += f"<p>Based on the analysis conducted, we can conclude that products in {volume_vendas['product_category_name_english'].iloc[0]} and {volume_vendas['product_category_name_english'].iloc[1]} categories demonstrate a high volume of sales, indicating significant demand for these items. Additionally, most product reviews fall within the 5 range, suggesting a high level of customer satisfaction. Regarding profitability, the {lucro_por_categoria['product_category_name_english'].iloc[0]} and {lucro_por_categoria['product_category_name_english'].iloc[1]} categories appear to be the most profitable, indicating priority areas for focus and investment.</p>\n\n"
    html_report += "</div>\n"


    html_report += "</div>\n</body>\n\n</html>"

    os.makedirs(dir_relatorio, exist_ok=True)
    with open(dir_relatorio + 'relatorio.html', 'w') as f:
        f.write(html_report)

    
    webbrowser.open(os.path.abspath('../Relatorio/relatorio.html'))
