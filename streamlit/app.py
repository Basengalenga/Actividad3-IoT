import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import OperationalError
import time

# Configuración de la página
st.set_page_config(page_title="IoT EpicMomo Dashboard", layout="wide")

# 1. Configuración de conexión (Igual que tu capturador)
DB_PARAMS = {
    "host": "db",
    "database": "epicmomo",
    "user": "admin",
    "password": "admin"
}

# Función para consultar datos con manejo de errores creativos
def get_data(table_name):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        query = f"SELECT value, ts FROM {table_name} ORDER BY ts DESC LIMIT 50"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df, None
    except OperationalError:
        return None, "🔌 Error de Conexión: ¿Está prendido el Docker de Postgres?"
    except Exception as e:
        if "does not exist" in str(e):
            return None, f"❌ Tabla '{table_name}' no encontrada. ¿Corriste el script de creación?"
        return None, f"🤯 Error inesperado: {e}"

# --- INTERFAZ DE STREAMLIT ---
st.title("🚀 IoT Data Ingestion & Visualization")
st.markdown(f"**Proyecto:** {DB_PARAMS['database']} | **Status:** Real-time")

# Sidebar para control
with st.sidebar:
    st.header("Configuración")
    refresh_rate = st.slider("Refresco (segundos)", 1, 10, 2)
    st.info("Este dashboard lee las tablas lake_raw_data_int y float.")

# Layout de dos columnas
col1, col2 = st.columns(2)

# Función para renderizar cada métrica
def render_metric(column, title, table_name, color):
    df, error = get_data(table_name)
    
    with column:
        st.subheader(title)
        
        if error:
            st.error(error)
            st.warning("⚠️ El sistema está en espera de una señal válida.")
        elif df is None or df.empty:
            st.info("🏜️ Tabla vacía: La base de datos existe, pero el Generador no ha enviado nada aún.")
            st.image("https://media.giphy.com/media/uVOTxMagGsgXS/giphy.gif", width=200) # Un gif de desierto/espera
        else:
            # Mostrar métrica actual
            latest_val = df['value'].iloc[0]
            st.metric(label="Último valor capturado", value=f"{latest_val}", delta_color="normal")
            
            # Gráfico de serie de tiempo (Requisito UPY) [cite: 39]
            st.area_chart(df.set_index('ts')['value'], color=color)
            
            # Tabla de datos crudos (Para tu captura de pantalla del reporte) 
            with st.expander("Ver datos crudos (Raw)"):
                st.dataframe(df, use_container_width=True)

# Ejecutar renderizado
render_metric(col1, "🔢 Flujo de Enteros", "lake_raw_data_int", "#FF4B4B")
render_metric(col2, "🌊 Flujo de Flotantes", "lake_raw_data_float", "#1C83E1")

# Auto-refresco
time.sleep(refresh_rate)
st.rerun()