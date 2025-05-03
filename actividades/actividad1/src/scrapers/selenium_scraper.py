import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from actividades.actividad1.src.models.producto import Producto
from actividades.actividad1.src.scrapers.base_scraper import BaseScraper, TIEMPO_ESPERA


class SeleniumScraper(BaseScraper):
    """Implementación de scraper usando Selenium."""

    def __init__(self, url):
        """
        Inicializa el scraper de Selenium.

        Args:
            url (str): URL a analizar
        """
        super().__init__(url)

    def extraer_datos(self):
        """
        Extrae datos de productos de Mercado Libre usando Selenium.
        """
        driver = None
        try:
            # Configurar opciones de Edge
            edge_options = EdgeOptions()
            edge_options.add_argument("--headless")  # Ejecutar en modo sin interfaz gráfica
            edge_options.add_argument("--disable-gpu")
            edge_options.add_argument("--window-size=1920,1080")
            edge_options.add_argument("--no-sandbox")
            edge_options.add_argument("--disable-dev-shm-usage")

            try:
                # Inicializar el driver de Edge
                service = EdgeService(EdgeChromiumDriverManager().install())
                driver = webdriver.Edge(service=service, options=edge_options)

                # Navegar a la URL
                driver.get(self.url)

                # Esperar a que la página cargue completamente
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ol.ui-search-layout"))
                )

                # Dar tiempo adicional para cargar elementos dinámicos
                time.sleep(TIEMPO_ESPERA)

                # Encontrar contenedor principal
                contenedor = driver.find_element(By.CSS_SELECTOR, 'ol.ui-search-layout')

                # Encontrar los elementos que contienen la información de los productos
                productos = contenedor.find_elements(By.CSS_SELECTOR, 'div.ui-search-result__wrapper')
                print(f"Selenium: Se encontraron {len(productos)} productos en el contenedor")

                for producto in productos:
                    try:
                        # Extraer título
                        titulo_elem = producto.find_element(By.CSS_SELECTOR, '.poly-component__title')
                        titulo = titulo_elem.text.strip() if titulo_elem else "No disponible"

                        # Extraer precio
                        precio_elem = producto.find_element(By.CSS_SELECTOR, '.andes-money-amount__fraction')
                        precio = f"${precio_elem.text.strip()}" if precio_elem else "No disponible"

                        # Extraer link
                        link_elem = producto.find_element(By.CSS_SELECTOR, '.poly-component__title-wrapper a')
                        link = link_elem.get_attribute('href') if link_elem else "No disponible"

                        # Extraer imagen
                        img_elem = producto.find_element(By.CSS_SELECTOR, '.poly-component__picture')
                        imagen = img_elem.get_attribute('src') if img_elem else "No disponible"

                        # Crear objeto Producto
                        producto_obj = Producto(
                            titulo=titulo,
                            precio=precio,
                            link=link,
                            imagen=imagen,
                            metodo='Selenium'
                        )

                        # Guardar los datos extraídos como diccionario
                        self.resultados.append(producto_obj.to_dict())

                    except Exception as e:
                        print(f"Error al procesar un producto: {e}")

                print(f"Selenium: Se han extraído datos de {len(self.resultados)} productos")

            except Exception as driver_error:
                print(f"Error al inicializar o usar el driver de Edge: {driver_error}")
                print("Creando un array de resultados vacío...")

        except Exception as e:
            print(f"Error general durante la extracción con Selenium: {e}")
        finally:
            if driver:
                driver.quit()

        return self.resultados