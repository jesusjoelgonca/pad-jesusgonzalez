# Proyecto de Web Scraping: Análisis de Mercado Libre  

## Descripción General  
Proyecto académico para extraer y analizar datos del **Samsung Galaxy S24 Ultra** en Mercado Libre Colombia usando tres técnicas de web scraping:  
1. **BeautifulSoup** (análisis de HTML estático)  
2. **Scrapy** (framework de crawling escalable)  
3. **Selenium** (automatización de navegadores para contenido dinámico)  

Datos extraídos:  
- ID del producto  
- Título del producto  
- Precio  
- Enlaces e imágenes  
- Capacidad (256GB/512GB/1TB)  
- RAM (12GB/16GB)  
- Color (Black, Gray, Violet, Yellow)  

---

## Técnicas de Web Scraping Implementadas  

### BeautifulSoup  
- **Enfoque**: Análisis de HTML estático con `requests` + `BeautifulSoup4`  
- **Ventajas**:  
  - Fácil implementación  
  - Ideal para páginas sin JavaScript  
- **Desventajas**:  
  - Limitado para contenido dinámico  
  - Requiere ajustes manuales para enlaces  
- **Resultados**:  
  - ✅ Extracción exitosa de títulos y precios  
  - ❌ Dificultades iniciales para obtener URLs completas  

### Scrapy  
- **Enfoque**: Framework especializado con selectores CSS múltiples  
- **Ventajas**:  
  - Escalabilidad para proyectos grandes  
  - Integración nativa de pipelines  
- **Desventajas**:  
  - Curva de aprendizaje más pronunciada  
- **Resultados**:  
  - ✅ Extracción robusta tras optimizar selectores  
  - 📈 Obtuvo **100 productos** vs. 50 de otros métodos  

### Selenium  
- **Enfoque**: Automatización completa del navegador con ChromeDriver  
- **Ventajas**:  
  - Manejo de contenido dinámico  
  - Simulación de navegación real  
- **Desventajas**:  
  - Mayor consumo de recursos  
  - Requiere configuración adicional  
- **Resultados**:  
  - ✅ Extracción completa de todos los campos  
  - 🏆 Mejor precisión en captura de imágenes y enlaces  

---

## Producto Analizado: Samsung Galaxy S24 Ultra  

**Plataforma**: [Mercado Libre Colombia](https://listado.mercadolibre.com.co/samsung-s24-ultra)  
**Características clave**:  
- **Rango de precios**: COP $3,299,000 - $7,699,900  
- **Precio promedio**: ~COP $5,000,000  
- **Capacidades más comunes**:  
  - 256GB: 120 productos (65%)  
  - 512GB: 45 productos (25%)  
  - 1TB: 5 productos (3%)  
- **Colores populares**:  
  - Negro: 38 productos  
  - Violeta: 28 productos  
  - Gris: 24 productos  

![Distribución de Precios](distribucion_precios.png)  
*Distribución de precios del Samsung Galaxy S24 Ultra*

![Productos por Capacidad](productos_por_capacidad.png)  
*Comparativa de capacidades disponibles*

![Productos por Color](productos_por_color.png)  
*Preferencias de color en el mercado colombiano*

---

## Comparativa de Métodos  

![Comparación de Métodos](comparacion_metodos.png)  
*Rendimiento de las tres técnicas de scraping*

| Métrica                | BeautifulSoup | Scrapy | Selenium |
|-----------------------|---------------|--------|----------|
| Productos extraídos   | 50            | **100**| 50       |
| Velocidad             | Alta          | Muy alta| Baja     |
| Complejidad           | Baja          | Alta   | Muy alta |
| Manejo de JavaScript  | ❌            | ❌     | ✅       |
| Recursos necesarios   | Bajos         | Medios | Altos    |

---

## Objetivos Alcanzados  

### Objetivo Principal  
✅ Analizar la oferta del Samsung Galaxy S24 Ultra en Mercado Libre Colombia mediante técnicas de web scraping  

### Objetivos Específicos  
1. ✅ Implementar y comparar tres metodologías de web scraping (BeautifulSoup, Selenium y Scrapy)  
2. ✅ Recopilar datos estructurados sobre precios, títulos y enlaces  
3. ✅ Analizar variabilidad de precios (rango de COP $3.3M - $7.7M)  
4. ✅ Identificar patrones de comercialización (preferencia por 256GB y color negro)  

---

## Conclusiones  

1. **Scrapy** demostró ser la herramienta más eficiente para extracciones escalables, obteniendo **100 productos** vs. 50 de otras técnicas.  
2. **Selenium** fue crucial para capturar contenido dinámico como imágenes y enlaces, aunque su rendimiento fue más lento.  
3. **Mercado Colombiano**:  
   - El rango de precios más común es **COP $3.5M - $4M**  
   - La capacidad de **256GB** domina el mercado (65% de ofertas)  
   - El color **negro** es el más demandado (38 productos)  
4. Las diferencias en cantidad de datos extraídos sugieren posibles limitaciones anti-scraping en Mercado Libre que requieren estrategias de mitigación en futuras implementaciones.  