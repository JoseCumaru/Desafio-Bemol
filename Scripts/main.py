import ETL
import AED
import GR

if __name__ == "__main__":
    ETL.tratar_dados()

    AED.analise_exploratoria()

    GR.gerar_relatorio()
