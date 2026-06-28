import streamlit as st

from src.admin.activitats import mostrar_admin_activitats
from src.admin.espais import mostrar_admin_espais


def mostrar_administracio(df):
    pestanya_activitats, pestanya_espais = st.tabs(
        ["📋 Activitats", "🏢 Espais"]
    )

    with pestanya_activitats:
        mostrar_admin_activitats(df)

    with pestanya_espais:
        mostrar_admin_espais()