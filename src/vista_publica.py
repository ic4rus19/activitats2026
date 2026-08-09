import pandas as pd
import streamlit as st

from src.utils import activitat_te_lloc_el_dia


def mostrar_vista_publica(df_filtrat):

    avui = pd.Timestamp.today().normalize()

    inici_setmana = avui - pd.Timedelta(days=avui.weekday())
    fi_setmana = inici_setmana + pd.Timedelta(days=6)

    st.caption(
        f"Setmana del {inici_setmana.strftime('%d/%m/%Y')} "
        f"al {fi_setmana.strftime('%d/%m/%Y')}"
    )

    df_public = df_filtrat[
        df_filtrat["Publicada"].astype(str).str.lower().isin(["si", "sí"])
    ]

    df_public = df_public[
        (df_public["Data inici"] <= fi_setmana) &
        (df_public["Data fi"] >= inici_setmana)
    ]

    noms_dies = {
        0: "Dilluns",
        1: "Dimarts",
        2: "Dimecres",
        3: "Dijous",
        4: "Divendres",
        5: "Dissabte",
        6: "Diumenge",
    }

    dies_setmana = list(pd.date_range(inici_setmana, fi_setmana))

    for dia in dies_setmana:
        activitats_dia = df_public[
            df_public.apply(
                lambda fila: activitat_te_lloc_el_dia(fila, dia),
                axis=1
            )
        ].sort_values("Hora inici")

        if activitats_dia.empty:
            continue

        with st.container(border=True):
            st.markdown(
            f"<div style='font-size:20px; font-weight:bold; color:#c62828;'>• {noms_dies[dia.weekday()]} •</div>"
            f"<div style='font-size:24px; font-weight:bold; color:#333;'>{dia.strftime('%d/%m/%Y')}</div>",
            unsafe_allow_html=True
                        )
            for _, fila in activitats_dia.iterrows():
                hora_inici = str(fila["Hora inici"])[:5]
                hora_fi = str(fila["Hora fi"])[:5]

                estat = str(fila.get("Estat", "ACTIVA")).strip().upper()

                st.markdown(f"🕒 **{hora_inici} - {hora_fi}**")
                st.markdown(f"**{fila['Activitat']}**")

                if estat == "PENDENT D'APROVACIÓ":
                    st.warning("⏳ Pendent d'aprovació")

                st.markdown(f"📍 {fila['Espai']}")
                st.markdown(f"👥 {fila['Organitza']}")
                st.divider()