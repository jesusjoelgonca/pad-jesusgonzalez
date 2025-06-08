
# 📦 Extracción Automatizada de Datos con Web Scraping y Despliegue CI/CD

Este proyecto académico tiene como objetivo diseñar, contenerizar y automatizar un sistema de extracción de datos basado en técnicas avanzadas de **web scraping**. Se implementan herramientas como **Docker** y **GitHub Actions** para garantizar entornos de ejecución reproducibles y flujos de trabajo automatizados, optimizando así los procesos de ingesta y almacenamiento de datos para análisis posteriores.

---

## 📚 Descripción General

La iniciativa aborda el reto de recolectar datos estructurados desde plataformas de comercio electrónico, específicamente **MercadoLibre**, utilizando un enfoque combinado de librerías y frameworks de scraping:

- **BeautifulSoup**: Parsing HTML simple y efectivo.
- **Selenium**: Interacción con contenido dinámico basado en JavaScript.
- **Scrapy**: Crawling a gran escala y extracción eficiente.

Estos scrapers han sido **dockerizados** y se ejecutan automáticamente a través de un pipeline de **CI/CD** implementado en **GitHub Actions**. El flujo garantiza que cada actualización de código origine una nueva ejecución de scraping, manteniendo actualizados los conjuntos de datos obtenidos.

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.9+**
- **BeautifulSoup**, **Selenium**, **Scrapy**
- **Docker** y **Docker Compose**
- **GitHub Actions** (CI/CD)
- **SQLite3** (persistencia de datos)
- **CSV** (formato de exportación de datos)

---

## 🔧 Estructura del Proyecto

```
├── actividades/
│   ├── actividad1/            # Análisis comparativo de herramientas de scraping
│   │   ├── informes/           # Documentación y reportes técnicos
│   │   ├── static/
│   │   │   ├── csv/            # Almacenamiento de datos en CSV
│   │   │   └── db/             # Almacenamiento de base de datos SQLite
│   │   └── scripts/            # Scrapers individuales
│   ├── actividad3/             # Implementación de CI/CD con GitHub Actions
│   │   ├── workflows/          # Configuración de GitHub Actions
│   │   └── docker/             # Dockerfile y configuraciones de contenerización
├── docker-compose.yml          # Orquestación de servicios en desarrollo
├── README.md                    # Documentación principal
```

---

## 🚀 Pipeline de CI/CD

El proceso de automatización está diseñado para ejecutarse completamente en la nube, asegurando integraciones rápidas y despliegues consistentes:

### Flujo de Trabajo

1. **Detonador (Trigger)**: Cada `push` a la rama principal (`main`) inicia el pipeline.
2. **Checkout**: Obtención del código fuente actualizado.
3. **Docker Login**: Autenticación segura en Docker Hub usando secretos gestionados en GitHub.
4. **Build**: Construcción de imágenes Docker que contienen los scrapers.
5. **Run**: Ejecución automática de los scrapers dentro de contenedores.
6. **Persistencia**:
   - Datos extraídos guardados en **archivos CSV**.
   - Información almacenada en **bases de datos SQLite**.

### Configuración de GitHub Actions

Archivo principal del workflow:
```yaml
.github/workflows/scraper.yml
```

---

## 💾 Persistencia de Datos

Los datos extraídos son almacenados utilizando volúmenes de Docker para asegurar su persistencia entre ejecuciones:

- **CSV**: `actividades/actividad1/static/csv/`
- **SQLite3**: `actividades/actividad1/static/db/`

Estos formatos facilitan su posterior análisis y visualización en herramientas de procesamiento de datos.

---

## ⚙️ Requisitos de Instalación Local

- Docker
- Docker Compose
- Git

### Pasos de Instalación

1. Clonar el repositorio:
   ```bash
   git clone <URL-del-repositorio>
   cd <nombre-del-repositorio>
   ```

2. Construir y ejecutar los servicios:
   ```bash
   docker-compose up --build
   ```

3. Los resultados estarán disponibles en las carpetas configuradas para datos.

---

## 📊 Principales Características

- **Scraping Multi-técnica**: Integración de BeautifulSoup, Selenium y Scrapy para cubrir distintos tipos de páginas web.
- **Contenerización Completa**: Ejecución aislada y replicable de scrapers mediante Docker.
- **Automatización Continua**: Integración y despliegue automáticos con GitHub Actions.
- **Persistencia de Alta Fiabilidad**: Almacenamiento estructurado de resultados en CSV y bases de datos relacionales.
- **Monitorización de Calidad**: Validaciones automáticas de integridad de datos.

---

## 📖 Documentación Relacionada

- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Scrapy Documentation](https://docs.scrapy.org/en/latest/)
