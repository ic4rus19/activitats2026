import hmac

import streamlit as st

from src.admin.activitats import mostrar_admin_activitats
from src.admin.espais import mostrar_admin_espais


def contrasenya_correcta():
    return hmac.compare_digest(
        st.session_state.get("admin_password", ""),
        st.secrets["ADMIN_PASSWORD"],
    )


def mostrar_login_admin():
    st.info("Introdueix la contrasenya per accedir a l'administració.")

    with st.form("formulari_login_admin"):
        st.text_input(
            "Contrasenya",
            type="password",
            key="admin_password",
        )

        entrar = st.form_submit_button(
            "Entrar",
            use_container_width=True,
        )

    if entrar:
        if contrasenya_correcta():
            st.session_state["admin_autenticat"] = True
            st.session_state.pop("admin_password", None)
            st.rerun()
        else:
            st.error("Contrasenya incorrecta.")


def mostrar_administracio(df):
    if not st.session_state.get("admin_autenticat", False):
        mostrar_login_admin()
        return

    col_titol, col_sortir = st.columns([4, 1])

    with col_titol:
        st.success("Sessió d'administració iniciada.")

    with col_sortir:
        if st.button(
            "Tancar sessió",
            use_container_width=True,
        ):
            st.session_state["admin_autenticat"] = False
            st.rerun()

    pestanya_activitats, pestanya_espais = st.tabs(
    [
        "📋 Gestió d'activitats",
        "🏢 Gestió d'espais",
    ]
)

    with pestanya_activitats:
        mostrar_admin_activitats(df)

    with pestanya_espais:
        mostrar_admin_espais()