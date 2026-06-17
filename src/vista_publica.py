import streamlit as st


def mostrar_vista_publica(df_filtrat):
    st.subheader("Agenda pública")

    df_public = df_filtrat[
        df_filtrat["Publicada"].astype(str).str.lower().isin(["si", "sí"])
    ]

    st.write(f"S'han trobat {len(df_public)} activitats publicades.")

    cols = st.columns(3)

    for i, (_, fila) in enumerate(df_public.sort_values("Data inici").iterrows()):

        dies = {
            0: "Dilluns",
            1: "Dimarts",
            2: "Dimecres",
            3: "Dijous",
            4: "Divendres",
            5: "Dissabte",
            6: "Diumenge",
        }

        dia_setmana = dies[fila["Data inici"].weekday()]

        data_inici = (
            f"{dia_setmana} "
            f"{fila['Data inici'].strftime('%d/%m/%Y')}"
        )

        data_fi = fila["Data fi"].strftime("%d/%m/%Y")

        with cols[i % 3]:
            st.info(
                f"""
📅 {data_inici}
 **Fins: 🔴{data_fi}🔴**

**{fila['Activitat']}**

📍 {fila['Espai']}

🕒 {str(fila['Hora inici'])[:5]} - {str(fila['Hora fi'])[:5]}
""")