import streamlit as st

from src.db import (
    actualitzar_espai,
    actualitzar_estat_espai,
    inserir_espai,
    llegir_espais_admin,
)


def mostrar_admin_espais():
    st.write("Gestió del catàleg d'espais disponibles.")

    st.subheader("➕ Nou espai")

    with st.form("formulari_nou_espai"):
        nom = st.text_input(
            "Nom de l'espai",
            placeholder="Exemple: Sala Nova"
        )

        guardar = st.form_submit_button("Guardar espai")

        if guardar:
            if not nom.strip():
                st.error("Cal informar el nom de l'espai.")
            else:
                inserir_espai(nom.strip())
                st.success("Espai afegit correctament.")
                st.rerun()

    st.divider()

    st.subheader("✏️ Editar espai")

    df_espais = llegir_espais_admin()

    if df_espais.empty:
        st.info("No hi ha espais registrats.")
        return

    df_espais["text_opcio"] = (
        df_espais["id"].astype(str)
        + " - "
        + df_espais["nom"]
    )

    opcio = st.selectbox(
        "Busca i selecciona un espai",
        df_espais["text_opcio"].tolist()
    )

    id_espai = int(opcio.split(" - ")[0])

    espai_actual = df_espais[
        df_espais["id"] == id_espai
    ].iloc[0]

    with st.form("formulari_editar_espai"):
        nou_nom = st.text_input(
            "Nom de l'espai",
            value=espai_actual["nom"]
        )

        actiu = st.checkbox(
            "Espai actiu",
            value=bool(espai_actual["actiu"])
        )

        guardar_canvis = st.form_submit_button("Guardar canvis")

        if guardar_canvis:
            if not nou_nom.strip():
                st.error("Cal informar el nom de l'espai.")
            else:
                actualitzar_espai(
                    id_espai,
                    nou_nom.strip()
                )

                actualitzar_estat_espai(
                    id_espai,
                    actiu
                )

                st.success("Espai actualitzat correctament.")
                st.rerun()

    st.divider()

    st.subheader("Llistat d'espais")

    df_espais = llegir_espais_admin()

    st.write(f"Hi ha {len(df_espais)} espais registrats.")

    st.dataframe(
        df_espais,
        use_container_width=True
    )