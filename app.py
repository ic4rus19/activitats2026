import pandas as pd
import streamlit as st
import base64

from src.vista_publica import mostrar_vista_publica
from src.vista_interna import mostrar_vista_interna
from src.vista_calendari import mostrar_calendari
from src.vista_setmanal import mostrar_agenda_setmanal
from src.vista_espais import mostrar_ocupacio_espais
from src.vista_admin import mostrar_administracio

from src.db import llegir_activitats_app


def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


st.set_page_config(
    page_title="Gestió d'Activitats Municipals",
    page_icon="img/favicon-32x32.png",
    layout="wide"
)

logo = get_base64_image("img/favicon-32x32.png")

st.html(f"""
<div class="header-app">

    <img src="data:image/png;base64,{logo}" class="logo-app">

    <div class="title-app">
        Ajuntament de Vallgorguina
    </div>

    <img src="data:image/png;base64,{logo}" class="logo-app">

</div>

<style>
.header-app {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    margin-bottom: 10px;
}}

.logo-app {{
    width: 45px;
    height: auto;
}}

.title-app {{
    font-size: 34px;
    font-weight: 700;
    text-align: center;
}}

@media (max-width: 768px) {{

    .logo-app {{
        width: 28px;
    }}

    .title-app {{
        font-size: 20px;
    }}
}}
</style>
""")

df = llegir_activitats_app()

df["Data inici"] = pd.to_datetime(df["Data inici"], errors="coerce")
df["Data fi"] = pd.to_datetime(df["Data fi"], errors="coerce")

mesos = {
    "Tots": 0,
    "Gener": 1,
    "Febrer": 2,
    "Març": 3,
    "Abril": 4,
    "Maig": 5,
    "Juny": 6,
    "Juliol": 7,
    "Agost": 8,
    "Setembre": 9,
    "Octubre": 10,
    "Novembre": 11,
    "Desembre": 12,
}

with st.sidebar:
    st.title("Menú")

    st.link_button(
        "🌐 Espais Vallgorguina",
        "https://www.espaisvallgorguina.cat",
        use_container_width=True
    )

    st.divider()

    opcio_menu = st.radio(
        "Selecciona una vista",
        [
            "🏠 Agenda pública setmanal",
            "📋 Gestió interna",
            "📅 Calendari mensual",
            "🗓️ Agenda setmanal",
            "🏢 Gestió d'espais",
            "🛠️ Administració",
        ]
    )

    if opcio_menu != "🛠️ Administració":
        st.divider()

        st.subheader("Filtres")

        mes = st.selectbox(
            "Mes",
            list(mesos.keys())
        )

    else:
        mes = "Tots"


df_filtrat = df.copy()

if mes != "Tots":
    mes_num = mesos[mes]
    any_actual = pd.Timestamp.today().year

    inici_mes = pd.Timestamp(any_actual, mes_num, 1)
    fi_mes = inici_mes + pd.offsets.MonthEnd(1)

    df_filtrat = df_filtrat[
        (df_filtrat["Data inici"] <= fi_mes) &
        (df_filtrat["Data fi"] >= inici_mes)
    ]


titol_vista = {
    "🏠 Agenda pública setmanal": "Agenda pública setmanal",
    "📋 Gestió interna": "Gestió interna",
    "📅 Calendari mensual": "Calendari mensual",
    "🗓️ Agenda setmanal": "Agenda setmanal",
    "🏢 Gestió d'espais": "Gestió d'espais",
    "🛠️ Administració": "Administració",
}

st.subheader(titol_vista[opcio_menu])

if opcio_menu == "🏠 Agenda pública setmanal":
    mostrar_vista_publica(df)

elif opcio_menu == "📋 Gestió interna":
    mostrar_vista_interna(df_filtrat)

elif opcio_menu == "📅 Calendari mensual":
    mostrar_calendari(df_filtrat, mes, mesos)

elif opcio_menu == "🗓️ Agenda setmanal":
    mostrar_agenda_setmanal(df_filtrat, mes, mesos)

elif opcio_menu == "🏢 Gestió d'espais":
    mostrar_ocupacio_espais(df_filtrat, mes, mesos)

elif opcio_menu == "🛠️ Administració":
    mostrar_administracio(df)