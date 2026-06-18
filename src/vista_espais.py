import pandas as pd
import streamlit as st

from src.utils import activitat_te_lloc_el_dia
from src.db import llegir_espais


def mostrar_ocupacio_espais(df_filtrat, mes, mesos):

    if mes == "Tots":
        st.info("Selecciona un mes per veure l'ocupació d'espais.")
        return

    mes_num = mesos[mes]
    any_actual = 2026

    espais_disponibles = llegir_espais()

    espai_seleccionat = st.selectbox(
        "Selecciona un espai",
        espais_disponibles
    )

    df_espai = df_filtrat[
        df_filtrat["Espai"] == espai_seleccionat
    ]

    if df_espai.empty:
        st.info("Aquest espai no té activitats en el període seleccionat.")
        return

    st.write(f"Ocupació de l'espai: **{espai_seleccionat}**")

    inici_mes = pd.Timestamp(any_actual, mes_num, 1)
    fi_mes = inici_mes + pd.offsets.MonthEnd(1)

    dies_mes = pd.date_range(inici_mes, fi_mes)

    noms_dies = {
        0: "Dilluns",
        1: "Dimarts",
        2: "Dimecres",
        3: "Dijous",
        4: "Divendres",
        5: "Dissabte",
        6: "Diumenge",
    }

    for dia in dies_mes:
        activitats_dia = df_espai[
            df_espai.apply(
                lambda fila: activitat_te_lloc_el_dia(fila, dia),
                axis=1
            )
        ].sort_values("Hora inici")

        if not activitats_dia.empty:
            st.markdown(
                f"### 📅 {noms_dies[dia.weekday()]} "
                f"{dia.strftime('%d/%m/%Y')}"
            )

            for _, fila in activitats_dia.iterrows():
                hora_inici = str(fila["Hora inici"])[:5]
                hora_fi = str(fila["Hora fi"])[:5]

                with st.container(border=True):
                    st.markdown(
                        f"""
**{hora_inici} - {hora_fi}**  
{fila['Activitat']}
"""
                    )