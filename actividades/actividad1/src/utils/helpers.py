import json
import os

import matplotlib.pyplot as plt
import pandas as pd

from models.producto import Producto
from scrapers.base_scraper import DATA_DIR
from scrapers.beautifulsoup_scraper import BeautifulSoupScraper
from scrapers.scrapy_scraper import ScrapyScraper
from scrapers.selenium_scraper import SeleniumScraper


class AnalizadorMercadoLibre:
    """
    Clase que coordina el análisis de productos de Mercado Libre
    usando diferentes métodos de scraping.
    """

    def __init__(self, url):
        """
        Inicializa el analizador con la URL a analizar.

        Args:
            url (str): URL de Mercado Libre a analizar
        """
        self.url = url
        self.bs_scraper = BeautifulSoupScraper(url)
        self.selenium_scraper = SeleniumScraper(url)
        self.scrapy_scraper = ScrapyScraper(url)
        self.resultados_combinados = []
        self.productos = []  # Lista de objetos Producto

    def ejecutar_analisis_completo(self):
        """
        Ejecuta el análisis con los tres métodos de scraping y combina los resultados.
        """
        resultados_bs = []
        resultados_selenium = []
        resultados_scrapy = []

        try:
            print("Iniciando análisis con BeautifulSoup...")
            resultados_bs = self.bs_scraper.extraer_datos()
            self.bs_scraper.guardar_datos("resultados_beautifulsoup")
        except Exception as e:
            print(f"Error en BeautifulSoup: {e}")

        try:
            print("\nIniciando análisis con Selenium...")
            resultados_selenium = self.selenium_scraper.extraer_datos()
            self.selenium_scraper.guardar_datos("resultados_selenium")
        except Exception as e:
            print(f"Error en Selenium: {e}")

        try:
            print("\nIniciando análisis con Scrapy...")
            resultados_scrapy = self.scrapy_scraper.extraer_datos()
            self.scrapy_scraper.guardar_datos("resultados_scrapy")
        except Exception as e:
            print(f"Error en Scrapy: {e}")

        # Combinar todos los resultados (cualquiera de ellos podría estar vacío)
        self.resultados_combinados = resultados_bs + resultados_selenium + resultados_scrapy

        # Convertir resultados a objetos Producto
        self.productos = [Producto.from_dict(resultado) for resultado in self.resultados_combinados]

        try:
            # Guardar resultados combinados
            resultados_combinados_path = os.path.join(DATA_DIR, 'resultados_combinados.json')
            with open(resultados_combinados_path, 'w', encoding='utf-8') as f:
                json.dump(self.resultados_combinados, f, ensure_ascii=False, indent=4)

            # Crear DataFrame si hay resultados
            if self.resultados_combinados:
                df = pd.DataFrame(self.resultados_combinados)
                df.to_csv(os.path.join(DATA_DIR, 'resultados_combinados.csv'), index=False)
        except Exception as e:
            print(f"Error al guardar resultados combinados: {e}")

        print("\nAnálisis completo finalizado!")
        print(f"Total de registros extraídos: {len(self.resultados_combinados)}")

        return self.resultados_combinados

    def generar_estadisticas(self):
        """
        Genera estadísticas básicas sobre los datos extraídos, incluyendo
        información adicional extraída con la clase Producto.
        """
        if not self.resultados_combinados:
            print("No hay resultados para generar estadísticas.")
            return

        df = pd.DataFrame(self.resultados_combinados)

        # Estadísticas por método de scraping
        print("\nRegistros por método de scraping:")
        print(df['método'].value_counts())

        # Intentar extraer precios numéricos para análisis
        df['precio_numerico'] = df['precio'].str.replace('$', '').str.replace('.', '').str.replace(',', '.').astype(
            float)

        # Estadísticas de precios
        print("\nEstadísticas de precios:")
        print(f"Precio mínimo: ${df['precio_numerico'].min():,.2f}")
        print(f"Precio máximo: ${df['precio_numerico'].max():,.2f}")
        print(f"Precio promedio: ${df['precio_numerico'].mean():,.2f}")

        # Estadísticas por capacidad si está disponible
        if 'capacidad' in df.columns:
            print("\nProductos por capacidad:")
            print(df['capacidad'].value_counts())

        # Estadísticas por color si está disponible
        if 'color' in df.columns:
            print("\nProductos por color:")
            print(df['color'].value_counts())

        # Estadísticas por RAM si está disponible
        if 'ram' in df.columns:
            print("\nProductos por RAM:")
            print(df['ram'].value_counts())

        # Distribución de precios
        plt.figure(figsize=(10, 6))
        df['precio_numerico'].hist(bins=20)
        plt.title('Distribución de precios')
        plt.xlabel('Precio (COP)')
        plt.ylabel('Frecuencia')
        plt.savefig(os.path.join(DATA_DIR, 'distribucion_precios.png'))

        # Comparación de métodos
        plt.figure(figsize=(8, 5))
        df['método'].value_counts().plot(kind='bar')
        plt.title('Comparación de métodos de scraping')
        plt.xlabel('Método')
        plt.ylabel('Cantidad de productos extraídos')
        plt.tight_layout()
        plt.savefig(os.path.join(DATA_DIR, 'comparacion_metodos.png'))

        # Si hay datos de capacidad, generar gráfico
        if 'capacidad' in df.columns and not df['capacidad'].isna().all():
            plt.figure(figsize=(8, 5))
            capacidad_counts = df['capacidad'].value_counts()
            capacidad_counts[capacidad_counts > 0].plot(kind='bar')
            plt.title('Productos por capacidad')
            plt.xlabel('Capacidad')
            plt.ylabel('Cantidad')
            plt.tight_layout()
            plt.savefig(os.path.join(DATA_DIR, 'productos_por_capacidad.png'))

        # Si hay datos de color, generar gráfico
        if 'color' in df.columns and not df['color'].isna().all():
            plt.figure(figsize=(8, 5))
            color_counts = df['color'].value_counts()
            color_counts[color_counts > 0].plot(kind='bar')
            plt.title('Productos por color')
            plt.xlabel('Color')
            plt.ylabel('Cantidad')
            plt.tight_layout()
            plt.savefig(os.path.join(DATA_DIR, 'productos_por_color.png'))

        print("\nGráficos guardados en la carpeta 'data'")

    def obtener_dataframe(self):
        """
        Devuelve los datos analizados como un DataFrame de pandas.
        """
        return pd.DataFrame(self.resultados_combinados)