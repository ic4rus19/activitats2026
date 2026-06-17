import pandas as pd


def llegir_excel(ruta_excel: str) -> pd.DataFrame:
    fulls = [
        "ACTIVITATS_PUNTUALS",
        "ACTIVITATS_FIXES",
        "ACTIVITATS_ESTIU",
    ]

    dades = []

    for full in fulls:
        df = pd.read_excel(ruta_excel, sheet_name=full)
        df["Origen"] = full
        dades.append(df)

    resultat = pd.concat(dades, ignore_index=True)
    return resultat