from scrapers.base_scraper import URL_MERCADOLIBRE
from utils.helpers import AnalizadorMercadoLibre
import os

def main():
    analizador = AnalizadorMercadoLibre(URL_MERCADOLIBRE)
    analizador.ejecutar_analisis_completo()  # Ejecuta el scraping y combina resultados
    df = analizador.obtener_dataframe()      # Obtiene el DataFrame con los datos
    os.makedirs("static/csv", exist_ok=True)
    df.to_csv("static/csv/data_extractor.csv", index=False)  # Guarda el CSV

if __name__ == "__main__":
    main()