import pandas as pd
import streamlit as st

from src.utils import nom_categoria, text_buit


def mostrar_vista_interna(df_filtrat):
    st.subheader("Vista interna")
    text_cerca = st.text_input(
    "Cercar activitat",
    placeholder="Escriu el nom de l'activitat..."
)

    if text_cerca:
        df_filtrat = df_filtrat[
        df_filtrat["Activitat"].str.contains(text_cerca, case=False, na=False)
    ]

    st.write(f"S'han trobat {len(df_filtrat)} activitats.")

    cols = st.columns(3)

    for i, (_, fila) in enumerate(df_filtrat.sort_values("Data inici").iterrows()):
        data_inici = fila["Data inici"].strftime("%d/%m/%Y")

        material = text_buit(fila["Material"])
        tasques = text_buit(fila["Tasques"])

        contingut = f"""
📅 {data_inici}

**{fila['Activitat']}**

📍 {fila['Espai']}

🕒 {str(fila['Hora inici'])[:5]} - {str(fila['Hora fi'])[:5]}

🏷️ {nom_categoria(fila['Origen'])}

🌐 Publicada: {fila['Publicada']}
"""

        if material:
            contingut += f"\n🧰 Material: {material}"

        if tasques:
            contingut += f"\n📝 Tasques: {tasques}"

        with cols[i % 3]:
            st.info(contingut)

    st.subheader("Taula de dades")
    st.dataframe(df_filtrat, use_container_width=True)