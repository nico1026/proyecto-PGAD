import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


st.set_page_config(
    page_title="Proyecto PGAD",
    page_icon="📊",
    layout="wide"
)

st.title("🚀 Juan Felipe Sanchez || David Nicolas Sotelo")
st.markdown("Análisis de transacciones y clientes.")

@st.cache_data
def load_data():
    df = pd.read_csv('DATASET_FINAL_R1.csv')# carga de datos
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    return df
df = load_data()
if st.checkbox('Mostrar vista previa de los datos'):
    st.subheader('Muestra del Dataset')
    st.write(df.head(10))

st.sidebar.header("🔍 Filtros de Usuario")

# Filtro de Ciudad
ciudades = sorted(df['city'].dropna().unique().tolist())
ciudad_seleccionada = st.sidebar.multiselect(
    "Selecciona la Ciudad:",
    options=ciudades,
    default=ciudades
)
# Filtro de Categoría
categorias = sorted(df['category'].dropna().unique().tolist())
categoria_seleccionada = st.sidebar.multiselect(
    "Selecciona Categoría:",
    options=categorias,
    default=categorias
)

# --- APLICACIÓN DE FILTROS ---
df_filtrado = df[
    (df['city'].isin(ciudad_seleccionada)) & 
    (df['category'].isin(categoria_seleccionada))
]

st.subheader("📌 Resumen con Filtros Aplicados")
col1, col2, col3, col4 = st.columns(4)

with col1:    
    total_ventas = df_filtrado['total_amount'].sum()
    st.metric("Ventas Totales", f"${total_ventas:,.2f}")

with col2:
    cantidad = len(df_filtrado)
    st.metric("Transacciones", f"{cantidad:,}")

with col3:
    promedio = df_filtrado['total_amount'].mean() if not df_filtrado.empty else 0
    st.metric("Ticket Promedio", f"${promedio:,.2f}")

with col4:
    # Cantidad de productos distintos en la selección
    productos_distintos = df_filtrado['category'].nunique()
    st.metric("Categorías Vistas", productos_distintos)

st.divider()

st.subheader("📈 Ventas por Categoría")
if not df_filtrado.empty:
    ventas_cat = df_filtrado.groupby('category')['total_amount'].sum().reset_index()
    st.bar_chart(data=ventas_cat, x='category', y='total_amount', color="#29b5e8")
else:
    st.warning("No hay datos para mostrar con los filtros seleccionados.")

