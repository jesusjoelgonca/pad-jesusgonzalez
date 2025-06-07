from scrapers.base_scraper import URL_MERCADOLIBRE
from utils.helpers import AnalizadorMercadoLibre
import os

def main():
    # Crear directorio para CSV con ruta absoluta
    csv_dir = "/app/actividades/actividad1/static/csv"
    csv_file = os.path.join(csv_dir, "data_extractor.csv")
    
    os.makedirs(csv_dir, exist_ok=True)
    
    # Obtener y analizar datos
    analizador = AnalizadorMercadoLibre(URL_MERCADOLIBRE)
    analizador.ejecutar_analisis_completo()
    
    # Mostrar preview de datos
    df = analizador.mostrar_preview_datos(10)
    df = analizador.obtener_dataframe()
    # Guardar CSV
    df.to_csv(csv_file, index=False)
    
    # Verificar que se guardó
    if os.path.exists(csv_file):
        print(f"✅ CSV guardado exitosamente en: {csv_file}")
        print(f"Tamaño del archivo: {os.path.getsize(csv_file)} bytes")
    
if __name__ == "__main__":
    main()