import streamlit as st

from src.admin.editar_activitat import mostrar_editar_activitat
from src.admin.eliminar_activitat import mostrar_eliminar_activitat
from src.admin.exportar_activitats import mostrar_exportar_activitats
from src.admin.nova_activitat import mostrar_nova_activitat
from src.utils import mostrar_titol_modul


def mostrar_admin_activitats(df):
    if "missatge_admin" in st.session_state:
        st.success(st.session_state["missatge_admin"])
        del st.session_state["missatge_admin"]

    mostrar_titol_modul(
        "📋 Gestió d'activitats",
        "blue",
    )

    pestanya_editar, pestanya_nova, pestanya_eliminar, pestanya_exportar = st.tabs(
        [
            "✏️ Editar",
            "➕ Nova activitat",
            "🗑️ Eliminar",
            "📥 Exportar",
        ]
    )

    with pestanya_editar:
        mostrar_editar_activitat()

    with pestanya_nova:
        mostrar_nova_activitat()

    with pestanya_eliminar:
        mostrar_eliminar_activitat()

    with pestanya_exportar:
        mostrar_exportar_activitats()