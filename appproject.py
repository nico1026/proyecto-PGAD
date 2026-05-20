import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image


st.set_page_config(
    page_title="Proyecto PGAD",
    page_icon="📊",
    layout="wide"
)

st.title("🚀 Juan Felipe Sanchez || David Nicolas Sotelo")
st.markdown("Análisis de transacciones y clientes.")

@st.cache_data
def load_data():
    df = pd.read_csv('DATASET_FINAL_R1.csv') # carga de datos
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
    
    productos_distintos = df_filtrado['category'].nunique()
    st.metric("Categorías Vistas", productos_distintos)

st.divider()

st.subheader("📈 Ventas por Categoría")
if not df_filtrado.empty:
    ventas_cat = df_filtrado.groupby('category')['total_amount'].sum().reset_index()
    st.bar_chart(data=ventas_cat, x='category', y='total_amount', color="#29b5e8")
else:
    st.warning("No hay datos para mostrar con los filtros seleccionados.")

# SECCIÓN: PREDICCIÓN DE COMPRA (MODELO DE REGRESIÓN LOGÍSTICA)
st.divider()
st.subheader("🔮 Predicción de Recompra para el Próximo Mes")
st.markdown(
    "Nuestro modelo de regresión logística "
    "para evaluar si un cliente volverá a comprar el próximo mes según sus hábitos."
)

col_input1, col_input2 = st.columns(2)

with col_input1:  
    input_loyalty = st.slider(
        "Puntaje de Lealtad del Cliente (Loyalty Score):",
        min_value=0.0,
        max_value=100.0,
        value=50.0,
        step=0.5
    )

with col_input2:
    input_amount = st.number_input(
        "Monto de la Compra Actual (Total Amount en $):",
        min_value=0.0,
        value=100.0,
        step=5.0
    )


if st.button("🔮 Evaluar Cliente"):
    # Coeficientes extraídos del ANALISSS del modelo en R
    B0 = -14.7088730  # Intercept
    B1 = 0.2312211   # Coeficiente de loyalty_score
    B2 = 0.0028711   # Coeficiente de total_amount
    
    #ECUACCNN 
    z = B0 + (B1 * input_loyalty) + (B2 * input_amount)
    
    # Obtener probabilidad
    probabilidad = 1 / (1 + np.exp(-z))
    
    st.markdown("---")
    st.markdown(f"### **Probabilidad estimada de recompra:** `{probabilidad * 100:.2f}%`")
    
    # Clasificación según el umbral 
    if probabilidad >= 0.5:
        st.success(
            "✅ **Predicción:** El modelo indica que el cliente **SÍ** realizará una compra el próximo mes."
        )
    else:
        st.error(
            "❌ **Predicción:** El modelo indica que el cliente **NO** realizará una compra el próximo mes."
        )

#  EQUIPO DE TRABAJO
st.divider()
st.subheader("👥 Equipo de Proyecto")


col_team1, col_team2 = st.columns(2)

with col_team1:
    
    st.image("imagenes/nico2.jpeg", width=250)
    st.markdown(
        "<div style='text-align: center; font-weight: bold; margin-top: 5px;'>"
        "Juan Felipe Sánchez Pérez<br>"
        "<span style='font-weight: normal; color: gray;'>Científico de Datos</span>"
        "</div>", 
        unsafe_allow_html=True  # <--- Corregido aquí
    )

with col_team2:   
    st.image("imagenes/nico.jpeg", width=250)
    st.markdown(
        "<div style='text-align: center; font-weight: bold; margin-top: 5px;'>"
        "David Nicolas Sotelo Merchán<br>"
        "<span style='font-weight: normal; color: gray;'>Científico de Datos</span>"
        "</div>", 
        unsafe_allow_html=True  # <--- Corregido aquí
    )
