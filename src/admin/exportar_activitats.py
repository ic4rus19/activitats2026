from io import BytesIO

import pandas as pd
import streamlit as st

from src.db import llegir_activitats_postgresql


def mostrar_exportar_activitats():
    st.subheader("📥 Exportar activitats")

    st.write(
        "Descarrega totes les activitats "
        "en un fitxer Excel."
    )

    df_export = llegir_activitats_postgresql()

    buffer = BytesIO()

    with pd.ExcelWriter(
        buffer,
        engine="openpyxl",
    ) as writer:
        df_export.to_excel(
            writer,
            index=False,
            sheet_name="ACTIVITATS",
        )

    st.download_button(
        label="Descarregar Excel",
        data=buffer.getvalue(),
        file_name="activitats_2026.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        use_container_width=True,
    )