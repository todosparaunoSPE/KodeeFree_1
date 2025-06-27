# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 09:53:14 2025

@author: jahop
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# --- Imagen en sidebar ---
with st.sidebar:
    st.image("logo.png", width=150)

# --- Simulación de datos de producción ---
np.random.seed(42)
num_pozos = 6
dias = 60

pozos = [f"Pozo-{i+1}" for i in range(num_pozos)]
fechas = [datetime.today() - timedelta(days=i) for i in range(dias)]

data = []
for fecha in fechas:
    for pozo in pozos:
        produccion = np.random.randint(1000, 2000)
        data.append({"Fecha": fecha.date(), "Pozo": pozo, "Produccion_bpd": produccion})

df_simulado = pd.DataFrame(data)

# --- Título y descripción ---
st.title("📊 Dashboard Producción Petrolera - KodeFree Data Engineer Jr")
st.markdown("""
Bienvenido al dashboard interactivo de producción petrolera.  
Aquí puedes explorar datos simulados y visualizar gráficos dinámicos.
""")

# --- Barra lateral: filtros ---
st.sidebar.header("Filtros")
limite = st.sidebar.slider("Número de registros a mostrar", min_value=1, max_value=300, value=30, step=1)

# --- Cargar datos simulados ---
df = df_simulado.head(limite)

# --- Limpieza de datos ---
if 'Fecha' in df.columns:
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

# --- Mostrar tabla ---
st.subheader("Datos de producción")
st.dataframe(df)

# --- Gráfico: Producción total diaria ---
if 'Fecha' in df.columns and 'Produccion_bpd' in df.columns:
    prod_diaria = df.groupby('Fecha')['Produccion_bpd'].sum().reset_index()
    fig = px.line(prod_diaria, x='Fecha', y='Produccion_bpd',
                  title='Producción Total Diaria (barriles por día)',
                  labels={'Produccion_bpd': 'Producción (bpd)', 'Fecha': 'Fecha'})
    st.plotly_chart(fig)
else:
    st.warning("Las columnas 'Fecha' o 'Produccion_bpd' no están disponibles para graficar producción diaria.")

# --- Gráfico: Producción por pozo ---
if 'Pozo' in df.columns and 'Produccion_bpd' in df.columns:
    fig2 = px.bar(df, x='Pozo', y='Produccion_bpd', title='Producción por Pozo',
                  labels={'Produccion_bpd': 'Producción (bpd)', 'Pozo': 'Pozo'})
    st.plotly_chart(fig2)
else:
    st.warning("No se encontraron columnas 'Pozo' o 'Produccion_bpd' para graficar producción por pozo.")

# --- Sección de ayuda ---
with st.expander("❓ Acerca de los datos utilizados"):
    st.markdown(
        """
        ### Datos simulados de producción petrolera

        - Se generaron automáticamente usando Python y NumPy.
        - 6 pozos ficticios: Pozo-1 a Pozo-6.
        - Producción aleatoria entre 1000 y 2000 barriles diarios por pozo.
        - Fechas correspondientes a los últimos 60 días.

        Este dashboard simula cómo se vería el análisis si se conectara a una base real como Databricks.

        ---
        **Herramientas usadas:**  
        Streamlit, Pandas, Plotly.
        """
    )

# --- Footer ---
st.markdown("---")
st.caption("Creado por Javier Horacio Pérez Ricárdez para la posición Data Engineer Jr en KodeFree.")
