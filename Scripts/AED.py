import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

diretorio_dados = '../Dados/Brazilian E-Commerce Public Dataset by Olist/'
avaliacoes_df = pd.read_csv(os.path.join(diretorio_dados, 'olist_order_reviews_dataset.csv'))
diretorio_figuras = "../Figuras/"

def analise_exploratoria():

    # 1. Análise de Performance de Vendas (Volume de Vendas por Categoria)
    pedidos_df = pd.read_csv('../Dados/Tratados/olist_orders_dataset.csv')
    order_items_df = pd.read_csv('../Dados/Tratados/olist_order_items_dataset.csv')
    produtos_df = pd.read_csv('../Dados/Tratados/olist_products_dataset.csv')
    traducao_categoria_produto_df = pd.read_csv('../Dados/Tratados/product_category_name_translation.csv')

  
    produtos_df = produtos_df.merge(traducao_categoria_produto_df, on='product_category_name', how='left')

   
    merged_df = pedidos_df.merge(order_items_df, on='order_id', how='inner')


    merged_df = merged_df.merge(produtos_df, on='product_id', how='inner')


    merged_df_filtrado = merged_df[merged_df['order_status'] == 'delivered']

  
    volume_vendas_por_categoria = merged_df_filtrado.groupby('product_category_name_english')['valor_total'].sum().reset_index().rename(columns={'valor_total': 'volume_vendas'})

  
    volume_vendas_por_categoria_ordenado = volume_vendas_por_categoria.sort_values(by='volume_vendas', ascending=False)

    print("Volume de vendas por categoria:")
    print(volume_vendas_por_categoria_ordenado.head(10).to_markdown(index=False, numalign="left", stralign="left"))

    os.makedirs(diretorio_figuras, exist_ok=True)
    
    plt.figure(figsize=(12, 6))
    sns.barplot(data=volume_vendas_por_categoria_ordenado.head(10), x='product_category_name_english', y='volume_vendas')
    plt.xticks(rotation=45, ha='right')
    plt.title('Volume de Vendas por Categoria (Top 10)')
    plt.xlabel('Categoria do Produto')
    plt.ylabel('Volume de Vendas')
    plt.savefig('../Figuras/volume_vendas_por_categoria.png')
    plt.show()

    # 2. Análise de Logística (Prazos de Entrega)
    print("\nEstatísticas de tempo de entrega:")
    print(f"- Média: {pedidos_df['tempo_entrega'].mean():.2f} dias")
    print(f"- Mediana: {pedidos_df['tempo_entrega'].median():.2f} dias")

    print("\nEstatísticas de atraso na entrega:")
    print(f"- Média: {pedidos_df['atraso_entrega'].mean():.2f} dias")
    print(f"- Mediana: {pedidos_df['atraso_entrega'].median():.2f} dias")

    plt.figure(figsize=(10, 5))
    sns.histplot(pedidos_df['tempo_entrega'], bins=30, kde=True)
    plt.title('Distribuição do Tempo de Entrega')
    plt.xlabel('Tempo de Entrega (dias)')
    plt.ylabel('Frequência')
    plt.savefig('../Figuras/distribuicao_tempo_entrega.png')
    plt.show()

    # 3. Análise de Satisfação do Cliente (Avaliações de Produtos)
    merged_reviews_df = order_items_df.merge(avaliacoes_df, on='order_id', how='inner')

 
    media_avaliacao_por_produto = merged_reviews_df.groupby('product_id')['review_score'].mean().reset_index().rename(columns={'review_score': 'media_avaliacao'})


    media_avaliacao_por_produto_ordenado = media_avaliacao_por_produto.sort_values(by='media_avaliacao', ascending=False)

    
    print("\n10 melhores produtos:")
    print(media_avaliacao_por_produto_ordenado.head(10).to_markdown(index=False, numalign="left", stralign="left"))

    print("\n10 piores produtos:")
    print(media_avaliacao_por_produto_ordenado.tail(10).to_markdown(index=False, numalign="left", stralign="left"))

    plt.figure(figsize=(10, 5))
    sns.histplot(avaliacoes_df['review_score'], bins=5, discrete=True)
    plt.title('Distribuição das Avaliações dos Produtos')
    plt.xlabel('Avaliação')
    plt.ylabel('Frequência')
    plt.savefig('../Figuras/distribuicao_avaliacoes.png')
    plt.show()

    # 4. Análise Financeira (Lucratividade Estimada por Categoria)
    lucro_estimado_por_categoria = merged_df_filtrado.groupby('product_category_name_english')['valor_total'].sum().reset_index().rename(columns={'valor_total': 'lucro_estimado'})

    lucro_estimado_por_categoria_ordenado = lucro_estimado_por_categoria.sort_values(by='lucro_estimado', ascending=False)

    print("\nLucratividade Estimada por categoria:")
    print(lucro_estimado_por_categoria_ordenado.head(10).to_markdown(index=False, numalign="left", stralign="left"))


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


    metricas_entrega = pd.DataFrame({
        'tempo_entrega': [pedidos_df['tempo_entrega'].mean(), pedidos_df['tempo_entrega'].median()],
        'atraso_entrega': [pedidos_df['atraso_entrega'].mean(), pedidos_df['atraso_entrega'].median()]
    }, index=['Média', 'Mediana'])
    metricas_entrega.to_csv('../Dados/Tratados/orders_df_metrics.csv', index=True)
