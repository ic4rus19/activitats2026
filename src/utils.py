import pandas as pd

import streamlit as st

def activitat_te_lloc_el_dia(fila, dia):
    dies_setmana = str(fila.get("Dies setmana", "")).strip().lower()

    if fila["Data inici"] > dia or fila["Data fi"] < dia:
        return False

    if dies_setmana in ["", "nan"]:
        return True

    dies_catala = {
        0: "dilluns",
        1: "dimarts",
        2: "dimecres",
        3: "dijous",
        4: "divendres",
        5: "dissabte",
        6: "diumenge",
    }

    dia_actual = dies_catala[dia.weekday()]

    if "dilluns a divendres" in dies_setmana:
        return dia.weekday() <= 4

    if "cap de setmana" in dies_setmana:
        return dia.weekday() >= 5

    return dia_actual in dies_setmana

def nom_categoria(origen):
    if origen == "PUNTUAL":
        return "Puntual"
    if origen == "FIXA":
        return "Fixa"
    if origen == "ESTIU":
        return "Estiu"
    return origen


def icona_categoria(origen):
    if origen == "PUNTUAL":
        return "🟠"
    if origen == "FIXA":
        return "🔵"
    if origen == "ESTIU":
        return "🟢"
    return "⚪"

def text_buit(valor):
    if valor is None:
        return ""

    if str(valor).lower() == "nan":
        return ""

    if str(valor).strip() == "":
        return ""

    return str(valor).strip()



def mostrar_titol_modul(titol: str, color: str = "blue"):
    colors = {
        "blue": {
            "bg": "#e0f2fe",
            "border": "#bae6fd",
            "text": "#0369a1",
        },
        "green": {
            "bg": "#ecfdf5",
            "border": "#bbf7d0",
            "text": "#166534",
        },
    }

    c = colors[color]

    st.markdown(
        f"""
        <div style="
            background:{c['bg']};
            border:1px solid {c['border']};
            color:{c['text']};
            padding:14px;
            border-radius:12px;
            font-size:22px;
            font-weight:700;
            text-align:center;
            margin-bottom:18px;
        ">
            {titol}
        </div>
        """,
        unsafe_allow_html=True,
    )