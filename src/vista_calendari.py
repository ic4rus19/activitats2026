import calendar

import pandas as pd
import streamlit as st

from src.utils import activitat_te_lloc_el_dia, icona_categoria


def mostrar_calendari(df_filtrat, mes, mesos):
    st.subheader("Calendari mensual")

    if mes == "Tots":
        st.info("Selecciona un mes als filtres per veure el calendari mensual.")
        return

    mes_num = mesos[mes]
    any_actual = 2026

    st.write(f"Calendari de {mes} {any_actual}")

    st.markdown(
        """
**Llegenda:**  
🟠 Activitat puntual · 🔵 Activitat fixa · 🟢 Activitat d'estiu
"""
    )

    dies_caps = ["Dl", "Dt", "Dc", "Dj", "Dv", "Ds", "Dg"]
    caps = st.columns(7)

    for col, nom_dia in zip(caps, dies_caps):
        col.markdown(f"**{nom_dia}**")

    calendari = calendar.monthcalendar(any_actual, mes_num)

    for setmana in calendari:
        cols = st.columns(7)

        for i, numero_dia in enumerate(setmana):
            with cols[i]:
                if numero_dia == 0:
                    st.write("")
                else:
                    dia = pd.Timestamp(any_actual, mes_num, numero_dia)

                    with st.container(border=True):
                        avui = pd.Timestamp.today().normalize()

                        if dia.normalize() == avui:
                            st.markdown(f"### 🔴 {numero_dia}")
                        else:
                            st.markdown(f"**{numero_dia}**")

                        activitats_dia = df_filtrat[
                            df_filtrat.apply(
                                lambda fila: activitat_te_lloc_el_dia(fila, dia),
                                axis=1
                            )
                        ].sort_values("Hora inici")

                        if activitats_dia.empty:
                            st.caption("—")
                        else:
                            for _, fila in activitats_dia.iterrows():
                                hora_inici = str(fila["Hora inici"])[:5]
                                hora_fi = str(fila["Hora fi"])[:5]

                                icona = icona_categoria(fila["Origen"])

                                st.caption(
                                    f"{icona} {hora_inici} - {hora_fi} · {fila['Activitat']}"
                                )
                                st.caption(f"📍 {fila['Espai']}")