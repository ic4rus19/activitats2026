import pandas as pd

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
    if origen == "ACTIVITATS_PUNTUALS":
        return "Puntual"
    if origen == "ACTIVITATS_FIXES":
        return "Fixa"
    if origen == "ACTIVITATS_ESTIU":
        return "Estiu"
    return origen


def icona_categoria(origen):
    if origen == "ACTIVITATS_PUNTUALS":
        return "🟠"
    if origen == "ACTIVITATS_FIXES":
        return "🔵"
    if origen == "ACTIVITATS_ESTIU":
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

