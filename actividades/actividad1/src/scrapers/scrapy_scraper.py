import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import Response

from models.producto import Producto
from .base_scraper import BaseScraper


class MercadoLibreSpider(scrapy.Spider):
    """Spider de Scrapy para extraer datos de Mercado Libre."""

    name = 'mercadolibre_spider'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    resultados = []  # Hacerlo variable de clase para compartir entre instancias

    def __init__(self, url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [url] if url else []
        # Limpiar resultados previos
        MercadoLibreSpider.resultados = []

    def parse(self, response: Response, **kwargs):
        """Método que parsea la respuesta y extrae los datos."""
        # Buscar contenedor principal
        contenedor = response.css('ol.ui-search-layout')
        if not contenedor:
            print("Scrapy: No se encontró el contenedor principal")
            return

        # Encontrar productos - prueba con varios selectores
        productos = contenedor.css('div.ui-search-result__wrapper, li.ui-search-layout__item')
        print(f"Scrapy: Se encontraron {len(productos)} productos en el contenedor")

        for producto in productos:
            try:
                # Extraer título - probar múltiples selectores
                titulo = (producto.css('.ui-search-item__title::text, .poly-component__title::text').get() or
                          producto.css('h2::text').get())

                # Extraer precio - probar múltiples selectores
                precio = (producto.css('.price-tag-fraction::text, .andes-money-amount__fraction::text').get() or
                          producto.css('.price::text').get())

                # Extraer link - probar múltiples selectores
                link = (producto.css(
                    '.ui-search-link::attr(href), .poly-component__title-wrapper a::attr(href)').get() or
                        producto.css('a::attr(href)').get())

                # Extraer imagen - probar múltiples selectores
                imagen = (producto.css(
                    '.slick-slide.slick-active img::attr(src), .poly-component__picture::attr(src)').get() or
                          producto.css('img::attr(src)').get())

                # Crear objeto Producto
                producto_obj = Producto(
                    titulo=titulo.strip() if titulo else "No disponible",
                    precio=f"${precio.strip()}" if precio else "No disponible",
                    link=link if link else "No disponible",
                    imagen=imagen if imagen else "No disponible",
                    metodo='Scrapy'
                )

                # Guardar los datos extraídos como diccionario
                MercadoLibreSpider.resultados.append(producto_obj.to_dict())
                yield producto_obj.to_dict()

            except Exception as e:
                print(f"Scrapy: Error al procesar un producto - {e}")


class ScrapyScraper(BaseScraper):
    """Implementación de scraper usando Scrapy."""

    def __init__(self, url):
        """
        Inicializa el scraper de Scrapy.

        Args:
            url (str): URL a analizar
        """
        super().__init__(url)

    def extraer_datos(self):
        """
        Extrae datos de productos de Mercado Libre usando Scrapy.
        """
        try:
            # Configurar proceso de Scrapy
            process = CrawlerProcess(settings={
                'LOG_ENABLED': False,
                'DOWNLOAD_DELAY': 1,
                'CONCURRENT_REQUESTS': 1,
                'COOKIES_ENABLED': True,
            })

            # Ejecutar el spider
            process.crawl(MercadoLibreSpider, url=self.url)
            process.start()

            # Recuperar resultados de la variable de clase
            self.resultados = MercadoLibreSpider.resultados

            print(f"Scrapy: Se han extraído datos de {len(self.resultados)} productos")

        except Exception as e:
            print(f"Error durante la extracción con Scrapy: {e}")

        return self.resultados