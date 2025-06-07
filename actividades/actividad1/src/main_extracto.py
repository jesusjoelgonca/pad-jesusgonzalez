from scrapers.base_scraper import URL_MERCADOLIBRE
from utils.helpers import AnalizadorMercadoLibre
import os
import pandas as pd

def main():
    csv_dir = "/app/actividades/actividad1/static/csv"
    csv_file = os.path.join(csv_dir, "data_extractor.csv")
    
    os.makedirs(csv_dir, exist_ok=True)
    print(f"Directorio para CSV creado/verificado: {csv_dir}")
    
    # Obtener datos
    analizador = AnalizadorMercadoLibre(URL_MERCADOLIBRE)
    analizador.ejecutar_analisis_completo()
    df = analizador.obtener_dataframe()
    
    # Guardar CSV
    df.to_csv(csv_file, index=False)
    
    # Verificar que se guardó
    if os.path.exists(csv_file):
        print(f"✅ CSV guardado exitosamente en: {csv_file}")
        print(f"Tamaño del archivo: {os.path.getsize(csv_file)} bytes")
        print(f"Contenido del directorio: {os.listdir(csv_dir)}")
    else:
        print(f"❌ Error: No se pudo crear el CSV en {csv_file}")
    
if __name__ == "__main__":
    main()