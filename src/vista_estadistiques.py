import streamlit as st


def mostrar_estadistiques(df):

    st.subheader("Estadístiques")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total activitats",
        len(df)
    )

    col2.metric(
        "Publicades",
        len(df[df["Publicada"] == "Sí"])
    )

    col3.metric(
        "No publicades",
        len(df[df["Publicada"] == "No"])
    )

    st.divider()

    st.subheader("Activitats per categoria")

    st.bar_chart(
        df["Origen"].value_counts()
    )

    st.subheader("Activitats per espai")

    st.bar_chart(
        df["Espai"].value_counts()
    )