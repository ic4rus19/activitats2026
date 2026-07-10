import streamlit as st

from src.db import (
    eliminar_activitat,
    llegir_activitats_admin,
)


def mostrar_eliminar_activitat():
    st.subheader("🗑️ Eliminar activitat")

    text_cerca_eliminar = st.text_input(
        "Cercar activitat",
        placeholder="Escriu el nom de l'activitat...",
        key="cerca_eliminar_activitat",
    )

    df_admin = llegir_activitats_admin()

    if text_cerca_eliminar:
        df_admin = df_admin[
            df_admin["activitat"].str.contains(
                text_cerca_eliminar,
                case=False,
                na=False,
            )
        ]

    if df_admin.empty:
        st.info("No s'han trobat activitats per eliminar.")
        return

    df_admin["text_opcio"] = (
        df_admin["id"].astype(str)
        + " - "
        + df_admin["data_inici"].astype(str)
        + " - "
        + df_admin["activitat"]
        + " - "
        + df_admin["espai"]
    )

    opcio = st.selectbox(
        "Selecciona una activitat per eliminar",
        df_admin["text_opcio"].tolist(),
        key="select_eliminar_activitat",
    )

    id_seleccionat = int(
        opcio.split(" - ")[0]
    )

    confirmar = st.checkbox(
        "Confirmo que vull eliminar aquesta activitat",
        key="confirmar_eliminar_activitat",
    )

    if st.button(
        "Eliminar activitat",
        key="btn_eliminar_activitat",
    ):
        if not confirmar:
            st.error("Cal confirmar l'eliminació.")
            return

        eliminar_activitat(id_seleccionat)

        st.session_state["missatge_admin"] = (
            "Activitat eliminada correctament."
        )

        st.rerun()