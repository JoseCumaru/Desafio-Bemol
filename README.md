# Projeto de Análise de E-commerce Brasileiro

Este projeto realiza uma análise exploratória de dados em um conjunto de dados de e-commerce brasileiro. O objetivo é extrair insights úteis dos dados que possam ajudar a melhorar as vendas, a logística, a satisfação do cliente, a lucratividade e a eficácia do marketing.

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

- `Dados/Brazilian E-Commerce Public Dataset by Olist`: Esta pasta contém os dados brutos usados para a análise. Os dados estão divididos em vários arquivos CSV.
- `Dados/Tratados/`: Esta pasta contém os dados após a etapa de ETL (Extração, Transformação e Carregamento).
- `Scripts/`: Esta pasta contém scripts Python para a etapa de ETL, para a análise exploratória de dados e geração de ralátorio.
- `Figuras/`: Esta pasta contém figuras geradas durante a análise.
- `Relatorio/`: Esta pasta contém o relátorio que será gerado a partir dos dados tratados.
- `README.md`: Este arquivo, que contem todas as informações úteis.

## Sobre cada script

1. O script `ETL.py` serve para realizar a etapa de ETL nos dados brutos. Isso irá gerar os dados tratados na pasta `Dados/Tratados/`.
2. O script `AED.py` serve para realizar a análise exploratória de dados nos dados tratados. Isso irá gerar figuras e gráficos na pasta `Figuras/`.
3. O script `GR.py` serve para gerar o relátorio com todos os insights dos dados tratados.

## Como executar

1. Clone o repositório: `
git clone https://github.com/JoseCumaru/AED_e-commerce.git

2. Execute o script `main.py`.

## Dependências

Este projeto requer Python 3 e as seguintes bibliotecas Python instaladas:

- Pandas:  `pip install pandas`
- Matplotlib:  `pip install matplotlib`
- Seaborn:  `pip install seaborn`

## Sobre os Dados

Os dados usados neste projeto são dados públicos relacionados ao e-commerce brasileiro. Eles incluem informações sobre vendas, logística, avaliações de clientes e muito mais.
