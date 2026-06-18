import calendar

import pandas as pd
import streamlit as st

from src.utils import activitat_te_lloc_el_dia, icona_categoria


def mostrar_agenda_setmanal(df_filtrat, mes, mesos):

    if mes == "Tots":
        st.info("Selecciona un mes per veure l'agenda setmanal.")
        return

    mes_num = mesos[mes]
    any_actual = 2026

    setmanes = calendar.monthcalendar(any_actual, mes_num)

    opcions_setmanes = []

    for idx, setmana in enumerate(setmanes, start=1):
        dies_valids = [dia for dia in setmana if dia != 0]

        primer_dia = dies_valids[0]
        ultim_dia = dies_valids[-1]

        opcions_setmanes.append(
            f"Setmana {idx}: {primer_dia:02d}/{mes_num:02d} - {ultim_dia:02d}/{mes_num:02d}"
        )

    setmana_text = st.selectbox("Setmana", opcions_setmanes)

    index_setmana = opcions_setmanes.index(setmana_text)

    setmana = setmanes[index_setmana]

    noms_dies = {
        0: "Dilluns",
        1: "Dimarts",
        2: "Dimecres",
        3: "Dijous",
        4: "Divendres",
        5: "Dissabte",
        6: "Diumenge",
    }

    for posicio, numero_dia in enumerate(setmana):

        if numero_dia == 0:
            continue

        dia = pd.Timestamp(any_actual, mes_num, numero_dia)

        activitats_dia = df_filtrat[
            df_filtrat.apply(
                lambda fila: activitat_te_lloc_el_dia(fila, dia),
                axis=1
            )
        ].sort_values("Hora inici")

        st.markdown(
            f"### {noms_dies[posicio]} {dia.strftime('%d/%m/%Y')}"
        )

        if activitats_dia.empty:
            st.caption("Sense activitats")

        else:
            for _, fila in activitats_dia.iterrows():

                hora_inici = str(fila["Hora inici"])[:5]
                hora_fi = str(fila["Hora fi"])[:5]

                icona = icona_categoria(fila["Origen"])

                with st.container(border=True):
                    st.markdown(
                        f"{icona} **{hora_inici} - {hora_fi}** · "
                        f"{fila['Activitat']} · 📍 {fila['Espai']}"
                )