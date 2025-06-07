
# 📊 Programación para Análisis de Datos

¡Bienvenido al proyecto académico que explora cómo extraer datos de productos en línea usando técnicas de web scraping!

---

## 📚 Estructura del Repositorio

El proyecto está organizado en carpetas por actividad. Cada actividad incluye su propio informe detallado:

### Actividad 1 - Análisis y herramientas de extracción de datos
- **Enfoque:** Comparación de BeautifulSoup, Selenium y Scrapy  
- 🔗 Ver Informe Completo

### Actividad 3 - Optimización de procesos con GitHub Actions
- **Automatización de extracción e ingesta de datos**  
- **Implementación de CI/CD en entornos Docker**

---

## 🔄 Automatización con GitHub Actions

Este proyecto implementa un pipeline automatizado que ejecuta procesos de extracción e ingesta de datos de MercadoLibre utilizando GitHub Actions.

### Flujo de Trabajo Implementado

#### 🔍 Detalles del Proceso Automatizado

- **Trigger:** Se activa automáticamente con cada push a la rama `main`  
- **Entorno:** Utiliza un runner Ubuntu para la ejecución

#### Pasos del Pipeline:
1. **Checkout:** Descarga el código fuente actual  
2. **Docker Login:** Autentica con Docker Hub usando secretos seguros  
3. **Build:** Construye la imagen Docker con las dependencias  
4. **Extracción:** Ejecuta el scraper para obtener datos de MercadoLibre  
5. **Ingesta:** Procesa y guarda los datos en la base de datos

---

## 💾 Persistencia de Datos

El workflow utiliza volúmenes Docker para garantizar que los datos extraídos y procesados persistan entre ejecuciones:

- **CSV:** `actividades/actividad1/static/csv`  
- **Base de datos:** `actividades/actividad1/static/db`

---

## 🚀 Ejecución Local

### Requisitos
- Python 3.9+  
- Docker  
- Git  

### Pasos de ejecución
1. Clonar el repositorio:
   ```bash
   git clone <URL-del-repositorio>
   cd <nombre-del-repositorio>
   ```

2. Construir y ejecutar con Docker:
   ```bash
   docker-compose up --build
   ```

---

## 📊 Resultados y Características

- **Multi-técnica:** Combina BeautifulSoup, Selenium y Scrapy  
- **Integración Continua:** Pipeline totalmente automatizado  
- **Análisis de Productos:** Extracción y visualización de características  
- **Monitoreo de Calidad:** Detección de datos nulos e inconsistencias