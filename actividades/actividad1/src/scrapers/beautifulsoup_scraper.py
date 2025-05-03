from datetime import datetime
import requests
from bs4 import BeautifulSoup

from actividades.actividad1.src.scrapers.base_scraper import BaseScraper
from actividades.actividad1.src.models.producto import Producto


class BeautifulSoupScraper(BaseScraper):
    """Implementación de scraper usando BeautifulSoup."""

    def __init__(self, url):
        """
        Inicializa el scraper de Beautifulsoup.

        Args:
            url (str): URL a analizar
        """
        super().__init__(url)

    def extraer_datos(self):
        """
        Extrae datos de productos de Mercado Libre usando BeautifulSoup.
        """
        try:
            # Realizar la petición HTTP
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            respuesta = requests.get(self.url, headers=headers)
            respuesta.raise_for_status()  # Verificar si la petición fue exitosa

            # Parsear el HTML
            soup = BeautifulSoup(respuesta.text, 'html.parser')

            # Buscar el contenedor principal (la lista ordenada ol)
            contenedor_principal = soup.select_one('ol.ui-search-layout')
            if not contenedor_principal:
                print("No se pudo encontrar el contenedor principal de productos")
                return self.resultados

            # Encontrar los elementos que contienen la información de los productos (divs)
            productos = contenedor_principal.select('div.ui-search-result__wrapper')
            print(f"Se encontraron {len(productos)} productos en el contenedor")

            for producto in productos:
                try:
                    # Extraer título
                    titulo_elem = producto.select_one('.poly-component__title')
                    titulo = titulo_elem.text.strip() if titulo_elem else "No disponible"

                    # Extraer precio (buscar en la estructura anidada)
                    precio_elem = producto.select_one('.andes-money-amount__fraction')
                    precio = f"${precio_elem.text.strip()}" if precio_elem else "No disponible"

                    # Extraer link - Intentar múltiples selectores
                    link = "No disponible"
                    # Opción 1: Buscar en la envoltura del título
                    link_elem = producto.select_one('.poly-component__title-wrapper a')
                    if link_elem and link_elem.has_attr('href'):
                        link = link_elem['href']
                    # Opción 2: Buscar cualquier enlace
                    if link == "No disponible":
                        link_elem = producto.select_one('a')
                        if link_elem and link_elem.has_attr('href'):
                            link = link_elem['href']

                    # Extraer imagen
                    imagen = "No disponible"
                    img_elem = producto.select_one('.poly-component__picture')
                    if img_elem and img_elem.has_attr('src'):
                        imagen = img_elem['src']
                    # Si la imagen es base64, buscar otra
                    if imagen.startswith('data:image'):
                        img_elem = producto.select_one('img')
                        if img_elem:
                            imagen = img_elem.get('data-src') or img_elem.get('src') or "No disponible"

                    # Crear objeto Producto
                    producto_obj = Producto(
                        titulo=titulo,
                        precio=precio,
                        link=link,
                        imagen=imagen,
                        metodo='BeautifulSoup'
                    )

                    # Guardar los datos extraídos como diccionario
                    self.resultados.append(producto_obj.to_dict())

                except Exception as e:
                    print(f"Error al procesar un producto: {e}")

            print(f"BeautifulSoup: Se han extraído datos de {len(self.resultados)} productos")
        except Exception as e:
            print(f"Error durante la extracción con BeautifulSoup: {e}")

        return self.resultados