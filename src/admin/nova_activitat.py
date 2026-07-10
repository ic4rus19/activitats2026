from datetime import time

import streamlit as st

from src.db import (
    hi_ha_solapament,
    inserir_activitat,
    llegir_espais,
)


ESTATS_ACTIVITAT = [
    "ACTIVA",
    "PENDENT D'APROVACIÓ",
    "FINALITZADA",
]


def mostrar_nova_activitat():
    st.subheader("➕ Nova activitat")

    if "formulari_nova_key" not in st.session_state:
        st.session_state["formulari_nova_key"] = 0

    clau_formulari = (
        "formulari_nova_activitat_"
        f"{st.session_state['formulari_nova_key']}"
    )

    with st.form(clau_formulari):
        activitat = st.text_input("Activitat")
        tipus = st.text_input("Tipus")

        espais = llegir_espais()

        espai = st.selectbox(
            "Espai",
            ["Selecciona un espai"] + espais,
        )

        col1, col2 = st.columns(2)

        data_inici = col1.date_input(
            "Data inici",
            format="DD/MM/YYYY",
        )

        data_fi = col2.date_input(
            "Data fi",
            format="DD/MM/YYYY",
        )

        dies_seleccionats = st.multiselect(
            "Dies setmana",
            [
                "Dilluns",
                "Dimarts",
                "Dimecres",
                "Dijous",
                "Divendres",
                "Dissabte",
                "Diumenge",
            ],
        )

        dies_setmana = ", ".join(dies_seleccionats)

        col3, col4 = st.columns(2)

        hora_inici = col3.time_input(
            "Hora inici",
            value=time(9, 0),
        )

        hora_fi = col4.time_input(
            "Hora fi",
            value=time(10, 0),
        )

        organitza = st.text_input("Organitza")
        coordinacio = st.text_input("Coordinació")

        material = st.text_area("Material")
        tasques = st.text_area("Tasques")

        publicada = st.checkbox("Publicada")

        categoria = st.selectbox(
            "Categoria",
            [
                "PUNTUAL",
                "FIXA",
                "ESTIU",
            ],
        )

        estat = st.selectbox(
            "Estat",
            ESTATS_ACTIVITAT,
            index=0,
        )

        guardar = st.form_submit_button(
            "Guardar activitat"
        )

        if guardar:
            if not activitat.strip():
                st.error(
                    "Cal informar el nom de l'activitat."
                )

            elif not tipus.strip():
                st.error(
                    "Cal informar el tipus d'activitat."
                )

            elif espai == "Selecciona un espai":
                st.error(
                    "Cal seleccionar un espai."
                )

            elif data_fi < data_inici:
                st.error(
                    "La data fi no pot ser anterior "
                    "a la data inici."
                )

            elif hora_fi <= hora_inici:
                st.error(
                    "L'hora fi ha de ser posterior "
                    "a l'hora inici."
                )

            else:
                solapaments = hi_ha_solapament(
                    espai,
                    data_inici,
                    data_fi,
                    dies_setmana,
                    hora_inici,
                    hora_fi,
                )

                if not solapaments.empty:
                    st.error(
                        "Aquest espai ja està ocupat "
                        "en aquest horari."
                    )

                    st.dataframe(
                        solapaments,
                        use_container_width=True,
                    )

                else:
                    nova_activitat = {
                        "activitat": activitat,
                        "tipus": tipus,
                        "espai": espai,
                        "data_inici": data_inici,
                        "data_fi": data_fi,
                        "dies_setmana": dies_setmana,
                        "hora_inici": hora_inici,
                        "hora_fi": hora_fi,
                        "organitza": organitza,
                        "coordinacio": coordinacio,
                        "material": material,
                        "tasques": tasques,
                        "publicada": publicada,
                        "categoria": categoria,
                        "estat": estat,
                    }

                    inserir_activitat(nova_activitat)

                    st.session_state["missatge_admin"] = (
                        f"✅ Activitat '{activitat}' "
                        "guardada correctament."
                    )

                    st.session_state["formulari_nova_key"] += 1

                    st.rerun()