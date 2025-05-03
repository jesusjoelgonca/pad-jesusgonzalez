import json
import os
from pathlib import Path

import pandas as pd

# Obtener la ruta del proyecto actual (directorio donde se ejecuta el script)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = os.path.join(BASE_DIR, "data")
INFORMES_DIR = os.path.join(BASE_DIR, "informes")

# Crear directorios si no existen
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(INFORMES_DIR, exist_ok=True)

# Constantes del proyecto
URL_MERCADOLIBRE = "https://listado.mercadolibre.com.co/samsung-s24-ultra#D[A:samsung%20s24%20ultra]"
PRODUCTO = "Samsung S24 Ultra"
TIEMPO_ESPERA = 5  # Tiempo de espera en segundos para páginas dinámicas


class BaseScraper:
    """Clase base que define la interfaz común para todos los scrapers."""

    def __init__(self, url):
        """
        Inicializa el scraper con la URL a analizar.

        Args:
            url (str): URL del sitio a escrapear
        """
        self.url = url
        self.resultados = []

    def extraer_datos(self):
        """
        Método que debe ser implementado por las clases hijas.
        Extrae los datos de la página web.
        """
        raise NotImplementedError("Subclase debe implementar este método abstracto")

    def guardar_datos(self, nombre_archivo):
        """
        Guarda los datos extraídos en formato JSON.

        Args:
            nombre_archivo (str): Nombre del archivo donde se guardarán los datos
        """
        ruta_completa = os.path.join(DATA_DIR, f"{nombre_archivo}.json")
        with open(ruta_completa, 'w', encoding='utf-8') as f:
            json.dump(self.resultados, f, ensure_ascii=False, indent=4)

        print(f"Datos guardados en {ruta_completa}")

    def convertir_a_dataframe(self):
        """
        Convierte los resultados a un DataFrame de pandas.

        Returns:
            pandas.DataFrame: DataFrame con los resultados
        """
        return pd.DataFrame(self.resultados)
