import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

data_dir = '../Dados/Brazilian E-Commerce Public Dataset by Olist/'
avaliacoes_df = pd.read_csv(os.path.join(data_dir, 'olist_order_reviews_dataset.csv'))

def analise_exploratoria():

    # 1. Análise de Performance de Vendas (Volume de Vendas por Categoria)
    pedidos_df = pd.read_csv('../Dados/Tratados/olist_orders_dataset.csv')
    order_items_df = pd.read_csv('../Dados/Tratados/olist_order_items_dataset.csv')
    products_df = pd.read_csv('../Dados/Tratados/olist_products_dataset.csv')
    product_category_translation_df = pd.read_csv('../Dados/Tratados/product_category_name_translation.csv')

    # 1.2. Traduzir os nomes das categorias
    products_df = products_df.merge(product_category_translation_df, on='product_category_name', how='left')

    # 1.3. Juntar orders e order_items
    merged_df = pedidos_df.merge(order_items_df, on='order_id', how='inner')

    # 1.4. Juntar com products
    merged_df = merged_df.merge(products_df, on='product_id', how='inner')

    # 1.5. Filtrar pedidos entregues
    merged_df_filtered = merged_df[merged_df['order_status'] == 'delivered']

    # 1.6. Agrupar e calcular volume de vendas
    volume_vendas_por_categoria = merged_df_filtered.groupby('product_category_name_english')['valor_total'].sum().reset_index().rename(columns={'valor_total': 'volume_vendas'})

    # 1.7. Ordenar por volume de vendas
    volume_vendas_por_categoria_ordenado = volume_vendas_por_categoria.sort_values(by='volume_vendas', ascending=False)

    # 1.8. Exibir resultados
    print("Volume de vendas por categoria:")
    print(volume_vendas_por_categoria_ordenado.head(10).to_markdown(index=False, numalign="left", stralign="left"))

    # 1.9. Visualização: Gráfico de barras do volume de vendas por categoria (Top 10)
    plt.figure(figsize=(12, 6))
    sns.barplot(data=volume_vendas_por_categoria_ordenado.head(10), x='product_category_name_english', y='volume_vendas')
    plt.xticks(rotation=45, ha='right')
    plt.title('Volume de Vendas por Categoria (Top 10)')
    plt.xlabel('Categoria do Produto')
    plt.ylabel('Volume de Vendas')
    plt.savefig('../Figuras/volume_vendas_por_categoria.png')
    plt.show()

    # 2. Análise de Logística (Prazos de Entrega)
    # 2.2. Calcular estatísticas de tempo de entrega e atraso
    print("\nEstatísticas de tempo de entrega:")
    print(f"- Média: {pedidos_df['tempo_entrega'].mean():.2f} dias")
    print(f"- Mediana: {pedidos_df['tempo_entrega'].median():.2f} dias")

    print("\nEstatísticas de atraso na entrega:")
    print(f"- Média: {pedidos_df['atraso_entrega'].mean():.2f} dias")
    print(f"- Mediana: {pedidos_df['atraso_entrega'].median():.2f} dias")

    # 2.3. Visualização: Histograma do tempo de entrega
    plt.figure(figsize=(10, 5))
    sns.histplot(pedidos_df['tempo_entrega'], bins=30, kde=True)
    plt.title('Distribuição do Tempo de Entrega')
    plt.xlabel('Tempo de Entrega (dias)')
    plt.ylabel('Frequência')
    plt.savefig('../Figuras/distribuicao_tempo_entrega.png')
    plt.show()

    # 3. Análise de Satisfação do Cliente (Avaliações de Produtos)
    # 3.2. Juntar os DataFrames
    merged_reviews_df = order_items_df.merge(avaliacoes_df, on='order_id', how='inner')

    # 3.3. Calcular média de avaliação por produto
    media_avaliacao_por_produto = merged_reviews_df.groupby('product_id')['review_score'].mean().reset_index().rename(columns={'review_score': 'media_avaliacao'})

    # 3.4. Ordenar por média de avaliação
    media_avaliacao_por_produto_ordenado = media_avaliacao_por_produto.sort_values(by='media_avaliacao', ascending=False)

    # 3.5. Exibir 10 melhores e 10 piores produtos
    print("\n10 melhores produtos:")
    print(media_avaliacao_por_produto_ordenado.head(10).to_markdown(index=False, numalign="left", stralign="left"))

    print("\n10 piores produtos:")
    print(media_avaliacao_por_produto_ordenado.tail(10).to_markdown(index=False, numalign="left", stralign="left"))

    # 3.6. Visualização: Histograma da distribuição das avaliações
    plt.figure(figsize=(10, 5))
    sns.histplot(avaliacoes_df['review_score'], bins=5, discrete=True)
    plt.title('Distribuição das Avaliações dos Produtos')
    plt.xlabel('Avaliação')
    plt.ylabel('Frequência')
    plt.savefig('../Figuras/distribuicao_avaliacoes.png')
    plt.show()

    # 4. Análise Financeira (Lucratividade Estimada por Categoria)
    # 4.1. Agrupar e calcular receita total por categoria
    lucro_estimado_por_categoria = merged_df_filtered.groupby('product_category_name_english')['valor_total'].sum().reset_index().rename(columns={'valor_total': 'lucro_estimado'})

    # 4.2. Ordenar por lucro estimado
    lucro_estimado_por_categoria_ordenado = lucro_estimado_por_categoria.sort_values(by='lucro_estimado', ascending=False)

    # 4.3. Exibir resultados
    print("\nLucratividade Estimada por categoria:")
    print(lucro_estimado_por_categoria_ordenado.head(10).to_markdown(index=False, numalign="left", stralign="left"))

    # 4.4. Visualização: Gráfico de barras do lucro estimado por categoria (Top 10)
    plt.figure(figsize=(12, 6))
    sns.barplot(data=lucro_estimado_por_categoria_ordenado.head(10), x='product_category_name_english', y='lucro_estimado')
    plt.xticks(rotation=45, ha='right')
    plt.title('Lucratividade Estimada por Categoria (Top 10)')
    plt.xlabel('Categoria do Produto')
    plt.ylabel('Lucratividade Estimada')
    plt.savefig('../Figuras/lucro_estimado_por_categoria.png')
    plt.show()

    # Salvando os dados para o relatório
    volume_vendas_por_categoria_ordenado.to_csv('../Dados/Tratados/volume_vendas_por_categoria_ordenado.csv', index=False)
    media_avaliacao_por_produto_ordenado.to_csv('../Dados/Tratados/media_avaliacao_por_produto_ordenado.csv', index=False)
    lucro_estimado_por_categoria_ordenado.to_csv('../Dados/Tratados/lucro_estimado_por_categoria_ordenado.csv', index=False)

    # Calcular e salvar métricas de entrega
    metricas_entrega = pd.DataFrame({
        'tempo_entrega': [pedidos_df['tempo_entrega'].mean(), pedidos_df['tempo_entrega'].median()],
        'atraso_entrega': [pedidos_df['atraso_entrega'].mean(), pedidos_df['atraso_entrega'].median()]
    }, index=['Média', 'Mediana'])
    metricas_entrega.to_csv('../Dados/Tratados/orders_df_metrics.csv', index=True)
