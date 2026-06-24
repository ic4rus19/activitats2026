import pandas as pd
import streamlit as st

from src.utils import nom_categoria, text_buit


def mostrar_vista_interna(df_filtrat):

    st.markdown("### 🔍 Cercar activitat o espai")

    text_cerca = st.text_input(
    "",
    placeholder="Escriu una activitat o un espai..."
    )

    if text_cerca:
        df_filtrat = df_filtrat[
            (
                df_filtrat["Activitat"].str.contains(
                    text_cerca,
                    case=False,
                    na=False
                )
            )
            |
            (
                df_filtrat["Espai"].str.contains(
                    text_cerca,
                    case=False,
                    na=False
                )
            )
        ]

        st.write(f"S'han trobat {len(df_filtrat)} activitats.")

        cols = st.columns(3)

        for i, (_, fila) in enumerate(
            df_filtrat.sort_values("Data inici").iterrows()
        ):

            data_inici = fila["Data inici"].strftime("%d/%m/%Y")
            data_fi = fila["Data fi"].strftime("%d/%m/%Y")

            material = text_buit(fila["Material"])
            tasques = text_buit(fila["Tasques"])

            estat = str(
                fila.get("Estat", "ACTIVA")
            ).strip()

            contingut = f"""
📅 {data_inici} ➜ {data_fi}

**{fila['Activitat']}**

📍 {fila['Espai']}

🕒 {str(fila['Hora inici'])[:5]} - {str(fila['Hora fi'])[:5]}

🏷️ {nom_categoria(fila['Origen'])} | 📌 {estat}
"""

            if material:
                contingut += f"\n🧰 Material: {material}"

            if tasques:
                contingut += f"\n📝 Tasques: {tasques}"

            with cols[i % 3]:
                st.info(contingut)

    st.subheader("Taula de dades")

    columnes_ocultes = [
        "Publicada",
        "Origen",
        "Estat",
    ]

    columnes_visibles = [
        c for c in df_filtrat.columns
        if c not in columnes_ocultes
    ]

    df_mostrar = df_filtrat[columnes_visibles]

    st.dataframe(
        df_mostrar,
        use_container_width=True
    )