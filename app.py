import pandas as pd
import streamlit as st
from src.vista_publica import mostrar_vista_publica
from src.vista_interna import mostrar_vista_interna
from src.vista_calendari import mostrar_calendari
from src.vista_setmanal import mostrar_agenda_setmanal
from src.vista_espais import mostrar_ocupacio_espais
from src.vista_admin import mostrar_administracio
from src.vista_estadistiques import mostrar_estadistiques

# from src.importar_excel import llegir_excel

from src.db import (
    llegir_activitats_app,
    llegir_espais,
)

st.set_page_config(
    page_title="Gestió d'Activitats Municipals",
    layout="wide"
)

st.title("Aplicació de Gestió d'Activitats Municipals")
st.caption("Ajuntament de Vallgorguina")

#df = llegir_excel("data/actv26.xlsx")
# Font principal de dades: PostgreSQL
df = llegir_activitats_app()

df["Data inici"] = pd.to_datetime(df["Data inici"], errors="coerce")
df["Data fi"] = pd.to_datetime(df["Data fi"], errors="coerce")

st.subheader("Resum general")

col1, col2, col3 = st.columns(3)

col1.metric("Activitats puntuals", len(df[df["Origen"] == "PUNTUAL"]))
col2.metric("Activitats fixes", len(df[df["Origen"] == "FIXA"]))
col3.metric("Activitats d'estiu", len(df[df["Origen"] == "ESTIU"]))

st.subheader("Filtres")

col_f1, col_f2, col_f3, col_f4 = st.columns(4)

categories = {
    "Totes": "Totes",
    "PUNTUAL": "Puntual",
    "FIXA": "Fixa",
    "ESTIU": "Estiu",
}

origen_mostrar = col_f1.selectbox(
    "Categoria",
    list(categories.values())
)

origen = None

for clau, valor in categories.items():
    if valor == origen_mostrar:
        origen = clau
        break

espais = llegir_espais()

espai = col_f2.selectbox(
    "Espai",
    ["Tots"] + espais
)

publicada = col_f3.selectbox(
    "Publicada",
    ["Totes"] + sorted(df["Publicada"].dropna().unique().tolist())
)

mesos = {
    "Tots": 0,
    "Gener": 1,
    "Febrer": 2,
    "Març": 3,
    "Abril": 4,
    "Maig": 5,
    "Juny": 6,
    "Juliol": 7,
    "Agost": 8,
    "Setembre": 9,
    "Octubre": 10,
    "Novembre": 11,
    "Desembre": 12,
}

mes = col_f4.selectbox("Mes", list(mesos.keys()))

df_filtrat = df.copy()

if origen != "Totes":
    df_filtrat = df_filtrat[df_filtrat["Origen"] == origen]

if espai != "Tots":
    df_filtrat = df_filtrat[df_filtrat["Espai"] == espai]

if publicada != "Totes":
    df_filtrat = df_filtrat[df_filtrat["Publicada"] == publicada]

if mes != "Tots":
    mes_num = mesos[mes]
    any_actual = 2026

    inici_mes = pd.Timestamp(any_actual, mes_num, 1)
    fi_mes = inici_mes + pd.offsets.MonthEnd(1)

    df_filtrat = df_filtrat[
        (df_filtrat["Data inici"] <= fi_mes) &
        (df_filtrat["Data fi"] >= inici_mes)
    ]

tab_publica, tab_interna, tab_calendari, tab_setmanal, tab_espais, tab_admin, tab_stats = st.tabs(
    [
        "Vista pública",
        "Vista interna",
        "Calendari mensual",
        "Agenda setmanal",
        "Ocupació d'espais",
        "Administració",
        "Estadístiques"
    ]
)

# **************************  Vista publica
with tab_publica:
    mostrar_vista_publica(df_filtrat)

# **************************  Vista interna
with tab_interna:
    mostrar_vista_interna(df_filtrat)
    
    
# *************************   Vista Calendari    
with tab_calendari:
    mostrar_calendari(df_filtrat, mes, mesos)
    
# *************************   Vista Semanal
with tab_setmanal:
    mostrar_agenda_setmanal(df_filtrat, mes, mesos)
    
# ************************   Vista Espais
with tab_espais:
    mostrar_ocupacio_espais(df_filtrat, mes, mesos)
    
# ************************   Vista Administrador
# **********************************************
with tab_admin:
    mostrar_administracio(df)
    
with tab_stats:
    mostrar_estadistiques(df_filtrat)