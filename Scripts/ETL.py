import pandas as pd
import os

diretorio_saida = "../Dados/Tratados/"

def tratar_dados():
    # 1. Extração da informação
    arquivos_df = {
        'olist_customers_dataset.csv': ['customer_id', 'customer_unique_id', 'customer_zip_code_prefix', 'customer_city', 'customer_state'],
        'olist_geolocation_dataset.csv': ['geolocation_zip_code_prefix', 'geolocation_lat', 'geolocation_lng', 'geolocation_city', 'geolocation_state'],
        'olist_order_items_dataset.csv': ['order_id', 'order_item_id', 'product_id', 'seller_id', 'shipping_limit_date', 'price', 'freight_value'],
        'olist_order_payments_dataset.csv': ['order_id', 'payment_sequential', 'payment_type', 'payment_installments', 'payment_value'],
        'olist_order_reviews_dataset.csv': ['review_id', 'order_id', 'review_score', 'review_comment_title', 'review_comment_message', 'review_creation_date', 'review_answer_timestamp'],
        'olist_orders_dataset.csv': ['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date'],
        'olist_products_dataset.csv': ['product_id', 'product_category_name', 'product_name_lenght', 'product_description_lenght', 'product_photos_qty', 'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm'],
        'olist_sellers_dataset.csv': ['seller_id', 'seller_zip_code_prefix', 'seller_city', 'seller_state'],
        'product_category_name_translation.csv': ['product_category_name', 'product_category_name_english']
    }

    diretorio_bruto = "../Dados/Brazilian E-Commerce Public Dataset by Olist/"

    os.makedirs(diretorio_saida, exist_ok=True)

    for arquivo, colunas in arquivos_df.items():
        # 1. Extração da informação
        print("Extraindo informaçoes de " + arquivo)
        dados = pd.read_csv(os.path.join(diretorio_bruto, arquivo), usecols=colunas)

        # 2. Transformação dos dados
        print(f"Tratando o arquivo {arquivo}")
        dados.dropna(subset=colunas, inplace=True)

      
        for col in dados.columns:
            if dados[col].dtype == 'object':
                dados[col] = dados[col].fillna('Outros') 
            elif dados[col].dtype in ['int64', 'float64']:
                dados[col] = dados[col].fillna(dados[col].median())

       
        colunas_datetime = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date', 'shipping_limit_date', 'review_creation_date', 'review_answer_timestamp']
        for col in colunas_datetime:
            if col in dados.columns:
                dados[col] = pd.to_datetime(dados[col], format='%Y-%m-%d %H:%M:%S', errors='coerce')

      
        colunas_categoricas = ['order_status', 'payment_type', 'product_category_name', 'customer_state', 'seller_state', 'review_id']
        for col in colunas_categoricas:
            if col in dados.columns:
                dados[col] = dados[col].astype('category')

     
        if arquivo == 'olist_orders_dataset.csv':
        
            dados['tempo_entrega'] = (dados['order_delivered_customer_date'] - dados['order_purchase_timestamp']).dt.days

       
            dados['atraso_entrega'] = (dados['order_delivered_customer_date'] - dados['order_estimated_delivery_date']).dt.days

        if arquivo == 'olist_order_items_dataset.csv':
           
            dados['valor_total'] = dados['price'] + dados['freight_value']

        # 3. Carregamento dos resultados
        caminho_arquivo_tratado = os.path.join(diretorio_saida, arquivo)
        dados.to_csv(caminho_arquivo_tratado, index=False)

    print("Dados tratados com sucesso!")
