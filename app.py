import pandas as pd
import streamlit as st

from src.vista_publica import mostrar_vista_publica
from src.vista_interna import mostrar_vista_interna
from src.vista_calendari import mostrar_calendari
from src.vista_setmanal import mostrar_agenda_setmanal
from src.vista_espais import mostrar_ocupacio_espais
from src.vista_admin import mostrar_administracio
from src.vista_estadistiques import mostrar_estadistiques

from src.db import (
    llegir_activitats_app,
    llegir_espais,
)

st.set_page_config(
    page_title="Gestió d'Activitats Municipals",
    layout="wide"
)

st.title("Gestió d'Activitats Municipals")
st.caption("Ajuntament de Vallgorguina")

df = llegir_activitats_app()

df["Data inici"] = pd.to_datetime(df["Data inici"], errors="coerce")
df["Data fi"] = pd.to_datetime(df["Data fi"], errors="coerce")

categories = {
    "Totes": "Totes",
    "PUNTUAL": "Puntual",
    "FIXA": "Fixa",
    "ESTIU": "Estiu",
}

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

espais = llegir_espais()

with st.sidebar:
    st.title("Menú")

    opcio_menu = st.radio(
        "Selecciona una vista",
        [
            "🏠 Vista pública",
            "📋 Vista interna",
            "📅 Calendari mensual",
            "🗓️ Agenda setmanal",
            "🏢 Ocupació d'espais",
            "🛠️ Administració",
            "📊 Estadístiques",
        ]
    )

    if opcio_menu != "🛠️ Administració":
        st.divider()

        st.subheader("Filtres")

        origen_mostrar = st.selectbox(
            "Categoria",
            list(categories.values())
        )

        espai = st.selectbox(
            "Espai",
            ["Tots"] + espais
        )

        publicada = st.selectbox(
            "Publicada",
            ["Totes"] + sorted(df["Publicada"].dropna().unique().tolist())
        )

        mes = st.selectbox(
            "Mes",
            list(mesos.keys())
        )

    else:
        origen_mostrar = "Totes"
        espai = "Tots"
        publicada = "Totes"
        mes = "Tots"

origen = None

for clau, valor in categories.items():
    if valor == origen_mostrar:
        origen = clau
        break

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

titols = {
    "🏠 Vista pública": "Vista pública",
    "📋 Vista interna": "Vista interna",
    "📅 Calendari mensual": "Calendari mensual",
    "🗓️ Agenda setmanal": "Agenda setmanal",
    "🏢 Ocupació d'espais": "Ocupació d'espais",
    "🛠️ Administració": "Administració",
    "📊 Estadístiques": "Estadístiques",
}

st.header(titols[opcio_menu])
st.divider()

if opcio_menu == "🏠 Vista pública":
    mostrar_vista_publica(df_filtrat)

elif opcio_menu == "📋 Vista interna":
    mostrar_vista_interna(df_filtrat)

elif opcio_menu == "📅 Calendari mensual":
    mostrar_calendari(df_filtrat, mes, mesos)

elif opcio_menu == "🗓️ Agenda setmanal":
    mostrar_agenda_setmanal(df_filtrat, mes, mesos)

elif opcio_menu == "🏢 Ocupació d'espais":
    mostrar_ocupacio_espais(df_filtrat, mes, mesos)

elif opcio_menu == "🛠️ Administració":
    mostrar_administracio(df)

elif opcio_menu == "📊 Estadístiques":
    mostrar_estadistiques(df_filtrat)