import streamlit as st
import pandas as pd
import os
import json
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# Detectar entorno automáticamente
if os.path.exists("/workspaces"):
    # Estamos en GitHub Codespaces
    BASE_PATH = "/workspaces/pad-jesusgonzalez"
elif os.path.exists("/app"):
    # Estamos en Docker
    BASE_PATH = "/app"
else:
    # Desarrollo local
    BASE_PATH = os.getcwd()

csv_path = f"{BASE_PATH}/actividades/actividad1/static/csv/data_extractor.csv"
data_dir = f"{BASE_PATH}/actividades/actividad1/data"
db_dir = f"{BASE_PATH}/actividades/actividad1/static/db"

st.set_page_config(
    page_title="📊 MercadoLibre Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header principal
st.title("🛒 Análisis MercadoLibre - Samsung S24 Ultra")
st.markdown("### Dashboard de datos extraídos automáticamente")

# Sidebar con información
with st.sidebar:
    st.markdown("## 📋 Información del Sistema")
    st.info(f"**Entorno:** {'Docker' if os.path.exists('/app') else 'Codespaces' if os.path.exists('/workspaces') else 'Local'}")
    
    # Botón de actualización manual
    if st.button("🔄 Verificar Nuevos Datos"):
        st.rerun()
    
    # Estado de archivos
    st.markdown("## 📁 Estado de Archivos")
    archivos_estado = {
        "CSV Principal": os.path.exists(csv_path),
        "Directorio Data": os.path.exists(data_dir),
        "Directorio DB": os.path.exists(db_dir)
    }
    
    for archivo, existe in archivos_estado.items():
        if existe:
            st.success(f"✅ {archivo}")
        else:
            st.error(f"❌ {archivo}")

# Función para cargar datos
@st.cache_data
def cargar_datos():
    """Carga y procesa los datos del CSV principal"""
    try:
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            # Limpiar y procesar datos
            if 'precio_numerico' in df.columns:
                df['precio_numerico'] = pd.to_numeric(df['precio_numerico'], errors='coerce')
            return df
        else:
            return None
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return None

# Función para cargar resultados JSON
@st.cache_data
def cargar_resultados_json():
    """Carga los resultados de cada método de scraping"""
    resultados = {}
    json_files = {
        "BeautifulSoup": "resultados_beautifulsoup.json",
        "Selenium": "resultados_selenium.json",
        "Scrapy": "resultados_scrapy.json"
    }
    
    for method, filename in json_files.items():
        file_path = os.path.join(data_dir, filename)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    resultados[method] = data if isinstance(data, list) else []
            except Exception as e:
                st.warning(f"Error cargando {method}: {e}")
                resultados[method] = []
        else:
            resultados[method] = []
    
    return resultados

# Cargar datos
df = cargar_datos()
resultados_json = cargar_resultados_json()

# Verificar si hay datos disponibles
if df is not None and len(df) > 0:
    # === MÉTRICAS PRINCIPALES ===
    st.markdown("## 📊 Métricas Principales")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📦 Total Productos", len(df))
    
    with col2:
        if 'precio_numerico' in df.columns:
            precio_promedio = df['precio_numerico'].mean()
            st.metric("💰 Precio Promedio", f"${precio_promedio:,.0f}")
    
    with col3:
        if 'método' in df.columns:
            metodos_usados = df['método'].nunique()
            st.metric("🔧 Métodos", metodos_usados)
    
    with col4:
        # Contar productos por método
        total_beautifulsoup = len(resultados_json.get('BeautifulSoup', []))
        total_selenium = len(resultados_json.get('Selenium', []))
        total_scrapy = len(resultados_json.get('Scrapy', []))
        metodo_mas_exitoso = max([
            ('BeautifulSoup', total_beautifulsoup),
            ('Selenium', total_selenium), 
            ('Scrapy', total_scrapy)
        ], key=lambda x: x[1])
        st.metric("🏆 Método Exitoso", f"{metodo_mas_exitoso[0]} ({metodo_mas_exitoso[1]})")
    
    with col5:
        # Última actualización
        if os.path.exists(csv_path):
            timestamp = os.path.getmtime(csv_path)
            fecha = pd.Timestamp.fromtimestamp(timestamp).strftime('%d/%m %H:%M')
            st.metric("🕐 Última Actualización", fecha)

    st.markdown("---")

    # === TABS PRINCIPALES ===
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Datos", "📊 Análisis", "🔍 Por Método", "📈 Gráficos", "💾 Descarga"
    ])

    with tab1:
        st.subheader("📋 Tabla Completa de Productos")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'método' in df.columns:
                metodos_disponibles = ['Todos'] + list(df['método'].unique())
                metodo_filtro = st.selectbox("🔧 Filtrar por método:", metodos_disponibles)
        
        with col2:
            if 'precio_numerico' in df.columns:
                precio_min = int(df['precio_numerico'].min())
                precio_max = int(df['precio_numerico'].max())
                rango_precios = st.slider(
                    "💰 Rango de precios:", 
                    precio_min, precio_max, 
                    (precio_min, precio_max)
                )
        
        with col3:
            # Búsqueda por texto
            if 'título' in df.columns:
                busqueda = st.text_input("🔍 Buscar en títulos:", "")
        
        # Aplicar filtros
        df_filtrado = df.copy()
        
        if 'metodo_filtro' in locals() and metodo_filtro != "Todos":
            df_filtrado = df_filtrado[df_filtrado['método'] == metodo_filtro]
        
        if 'rango_precios' in locals() and 'precio_numerico' in df.columns:
            df_filtrado = df_filtrado[
                (df_filtrado['precio_numerico'] >= rango_precios[0]) & 
                (df_filtrado['precio_numerico'] <= rango_precios[1])
            ]
        
        if 'busqueda' in locals() and busqueda and 'título' in df.columns:
            df_filtrado = df_filtrado[
                df_filtrado['título'].str.contains(busqueda, case=False, na=False)
            ]
        
        # Mostrar resultados filtrados
        st.write(f"**Mostrando {len(df_filtrado)} de {len(df)} productos**")
        st.dataframe(df_filtrado, use_container_width=True, height=500)

    with tab2:
        st.subheader("📊 Análisis de Datos")
        
        if 'precio_numerico' in df.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                # Distribución de precios
                fig_hist = px.histogram(
                    df, x='precio_numerico', 
                    title="Distribución de Precios",
                    labels={'precio_numerico': 'Precio (COP)', 'count': 'Cantidad'}
                )
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                # Box plot de precios por método
                if 'método' in df.columns:
                    fig_box = px.box(
                        df, x='método', y='precio_numerico',
                        title="Precios por Método de Extracción"
                    )
                    st.plotly_chart(fig_box, use_container_width=True)
        
        # Estadísticas descriptivas
        if 'precio_numerico' in df.columns:
            st.subheader("📈 Estadísticas de Precios")
            stats = df['precio_numerico'].describe()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("💸 Precio Mínimo", f"${stats['min']:,.0f}")
            with col2:
                st.metric("💰 Precio Máximo", f"${stats['max']:,.0f}")
            with col3:
                st.metric("📊 Mediana", f"${stats['50%']:,.0f}")
            with col4:
                st.metric("📏 Desv. Estándar", f"${stats['std']:,.0f}")

    with tab3:
        st.subheader("🔍 Resultados por Método de Scraping")
        
        # Métricas por método
        col1, col2, col3 = st.columns(3)
        
        metodos_info = [
            ("🍲 BeautifulSoup", resultados_json.get('BeautifulSoup', []), col1),
            ("🤖 Selenium", resultados_json.get('Selenium', []), col2),
            ("🕷️ Scrapy", resultados_json.get('Scrapy', []), col3)
        ]
        
        for nombre, datos, columna in metodos_info:
            with columna:
                st.markdown(f"### {nombre}")
                if len(datos) > 0:
                    st.success(f"✅ {len(datos)} productos")
                    
                    # Mostrar muestra
                    with st.expander("Ver muestra"):
                        muestra = datos[:2] if len(datos) > 2 else datos
                        for i, producto in enumerate(muestra, 1):
                            st.write(f"**Producto {i}:**")
                            # Mostrar solo campos principales
                            if isinstance(producto, dict):
                                campos_mostrar = ['título', 'precio', 'link']
                                for campo in campos_mostrar:
                                    if campo in producto:
                                        st.write(f"- **{campo}:** {producto[campo]}")
                            st.markdown("---")
                else:
                    st.error("❌ Sin datos")

    with tab4:
        st.subheader("📈 Gráficos Generados")
        
        # Buscar gráficos generados
        graficos_disponibles = [
            ("distribucion_precios.png", "💰 Distribución de Precios"),
            ("productos_por_capacidad.png", "💾 Productos por Capacidad"),
            ("productos_por_color.png", "🎨 Productos por Color"),
            ("comparacion_metodos.png", "⚖️ Comparación de Métodos")
        ]
        
        graficos_encontrados = 0
        for archivo, titulo in graficos_disponibles:
            img_path = os.path.join(data_dir, archivo)
            if os.path.exists(img_path):
                st.markdown(f"### {titulo}")
                st.image(img_path, use_column_width=True)
                graficos_encontrados += 1
        
        if graficos_encontrados == 0:
            st.info("📊 No se encontraron gráficos generados. Se crearán en la próxima ejecución del pipeline.")

    with tab5:
        st.subheader("💾 Descarga de Datos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Descargar CSV principal
            if df is not None:
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="📥 Descargar CSV Principal",
                    data=csv_data,
                    file_name=f"mercadolibre_productos_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            # Descargar datos JSON combinados
            datos_combinados = {
                "metadata": {
                    "total_productos": len(df) if df is not None else 0,
                    "fecha_extraccion": pd.Timestamp.now().isoformat(),
                    "metodos_usados": list(resultados_json.keys())
                },
                "resultados": resultados_json
            }
            
            json_data = json.dumps(datos_combinados, ensure_ascii=False, indent=2)
            st.download_button(
                label="📥 Descargar JSON Completo",
                data=json_data,
                file_name=f"mercadolibre_completo_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json"
            )

else:
    # === NO HAY DATOS ===
    st.warning("⚠️ No se encontraron datos extraídos")
    
    st.markdown("""
    ### 🔄 Los datos se generan automáticamente cuando:
    
    1. **Se ejecuta el GitHub Action** (push a main branch)
    2. **Se ejecuta manualmente** el workflow
    3. **Programación automática** (si está configurada)
    
    ### 📋 Para generar datos manualmente:
    
    ```bash
    # En terminal local o Codespaces
    python actividades/actividad1/src/main_extracto.py
    ```
    """)
    
    # Información de debug
    with st.expander("🔧 Información de Debug"):
        st.code(f"""
Entorno: {'Docker' if os.path.exists('/app') else 'Codespaces' if os.path.exists('/workspaces') else 'Local'}
Base Path: {BASE_PATH}
CSV Path: {csv_path}
CSV Existe: {os.path.exists(csv_path)}
Data Dir: {data_dir}
Data Dir Existe: {os.path.exists(data_dir)}

Archivos en data dir:
{os.listdir(data_dir) if os.path.exists(data_dir) else 'Directorio no existe'}
        """)

# Footer
st.markdown("---")
st.markdown("🤖 **Datos actualizados automáticamente por GitHub Actions** | 🔄 Última verificación: " + pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'))