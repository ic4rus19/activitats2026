import streamlit as st

from src.db import (
    actualitzar_activitat,
    hi_ha_solapament_editant,
    llegir_activitats_admin,
    llegir_espais,
    obtenir_activitat_per_id,
)
from src.utils import text_buit


ESTATS_ACTIVITAT = [
    "ACTIVA",
    "PENDENT D'APROVACIÓ",
    "FINALITZADA",
]


def mostrar_editar_activitat():
    st.subheader("🔍 Cercar activitat")

    text_cerca = st.text_input(
        "",
        placeholder="Escriu el nom de l'activitat...",
        key="cerca_editar_activitat",
    )

    st.subheader("✏️ Editar activitat")

    df_admin_edit = llegir_activitats_admin()

    if text_cerca:
        df_admin_edit = df_admin_edit[
            df_admin_edit["activitat"].str.contains(
                text_cerca,
                case=False,
                na=False,
            )
        ]

    if df_admin_edit.empty:
        st.info("No s'han trobat activitats per editar.")
        return

    df_admin_edit["text_opcio"] = (
        df_admin_edit["id"].astype(str)
        + " - "
        + df_admin_edit["data_inici"].astype(str)
        + " - "
        + df_admin_edit["activitat"]
        + " - "
        + df_admin_edit["espai"]
    )

    opcio_edit = st.selectbox(
        "",
        df_admin_edit["text_opcio"].tolist(),
        key="select_editar_activitat",
    )

    id_edit = int(opcio_edit.split(" - ")[0])

    activitat_actual = obtenir_activitat_per_id(id_edit)

    if activitat_actual is None:
        st.error("No s'ha pogut carregar l'activitat seleccionada.")
        return

    with st.form("formulari_editar_activitat"):
        activitat = st.text_input(
            "Activitat",
            value=activitat_actual["activitat"],
        )

        tipus = st.text_input(
            "Tipus",
            value=activitat_actual["tipus"],
        )

        espais = llegir_espais()
        espai_actual = activitat_actual["espai"]

        espai = st.selectbox(
            "Espai",
            espais,
            index=(
                espais.index(espai_actual)
                if espai_actual in espais
                else 0
            ),
        )

        col1, col2 = st.columns(2)

        data_inici = col1.date_input(
            "Data inici",
            value=activitat_actual["data_inici"],
            format="DD/MM/YYYY",
        )

        data_fi = col2.date_input(
            "Data fi",
            value=activitat_actual["data_fi"],
            format="DD/MM/YYYY",
        )

        dies_posibles = [
            "Dilluns",
            "Dimarts",
            "Dimecres",
            "Dijous",
            "Divendres",
            "Dissabte",
            "Diumenge",
        ]

        dies_actuals_text = text_buit(
            activitat_actual["dies_setmana"]
        )

        dies_actuals = [
            dia
            for dia in dies_posibles
            if dia.lower() in dies_actuals_text.lower()
        ]

        dies_seleccionats = st.multiselect(
            "Dies setmana",
            dies_posibles,
            default=dies_actuals,
        )

        dies_setmana = ", ".join(dies_seleccionats)

        col3, col4 = st.columns(2)

        hora_inici = col3.time_input(
            "Hora inici",
            value=activitat_actual["hora_inici"],
        )

        hora_fi = col4.time_input(
            "Hora fi",
            value=activitat_actual["hora_fi"],
        )

        organitza = st.text_input(
            "Organitza",
            value=text_buit(
                activitat_actual["organitza"]
            ),
        )

        coordinacio = st.text_input(
            "Coordinació",
            value=text_buit(
                activitat_actual["coordinacio"]
            ),
        )

        material = st.text_area(
            "Material",
            value=text_buit(
                activitat_actual["material"]
            ),
        )

        tasques = st.text_area(
            "Tasques",
            value=text_buit(
                activitat_actual["tasques"]
            ),
        )

        publicada = st.checkbox(
            "Publicada",
            value=bool(
                activitat_actual["publicada"]
            ),
        )

        categories = [
            "PUNTUAL",
            "FIXA",
            "ESTIU",
        ]

        categoria_actual = activitat_actual["categoria"]

        categoria = st.selectbox(
            "Categoria",
            categories,
            index=(
                categories.index(categoria_actual)
                if categoria_actual in categories
                else 0
            ),
        )

        estat_actual = activitat_actual.get(
            "estat",
            "ACTIVA",
        )

        estat = st.selectbox(
            "Estat",
            ESTATS_ACTIVITAT,
            index=(
                ESTATS_ACTIVITAT.index(estat_actual)
                if estat_actual in ESTATS_ACTIVITAT
                else 0
            ),
        )

        guardar_canvis = st.form_submit_button(
            "Guardar canvis"
        )

        if guardar_canvis:
            if not activitat.strip():
                st.error(
                    "Cal informar el nom de l'activitat."
                )

            elif not tipus.strip():
                st.error(
                    "Cal informar el tipus d'activitat."
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
                solapaments = hi_ha_solapament_editant(
                    id_edit,
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
                    activitat_modificada = {
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

                    actualitzar_activitat(
                        id_edit,
                        activitat_modificada,
                    )

                    st.session_state["missatge_admin"] = (
                        "Activitat actualitzada correctament."
                    )

                    st.rerun()