from actividades.actividad1.src.scrapers.base_scraper import URL_MERCADOLIBRE
from actividades.actividad1.src.utils.helpers import AnalizadorMercadoLibre

if __name__ == "__main__":
    # Crear instancia del analizador
    analizador = AnalizadorMercadoLibre(URL_MERCADOLIBRE)

    # Ejecutar análisis completo
    analizador.ejecutar_analisis_completo()

    # Generar estadísticas
    analizador.generar_estadisticas()
