import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text


def get_engine():
    cfg = st.secrets["postgres"]

    url = (
        f"postgresql+psycopg2://{cfg['user']}:{cfg['password']}"
        f"@{cfg['host']}:{cfg['port']}/{cfg['database']}"
    )

    return create_engine(url)


def llegir_activitats_postgresql():
    engine = get_engine()

    consulta = "SELECT * FROM activitats ORDER BY data_inici, hora_inici"

    df = pd.read_sql(consulta, engine)

    return df

def llegir_activitats_app():
    df = llegir_activitats_postgresql()

    df = df.rename(columns={
        "activitat": "Activitat",
        "tipus": "Tipus",
        "espai": "Espai",
        "data_inici": "Data inici",
        "data_fi": "Data fi",
        "dies_setmana": "Dies setmana",
        "hora_inici": "Hora inici",
        "hora_fi": "Hora fi",
        "organitza": "Organitza",
        "coordinacio": "Coordinació",
        "material": "Material",
        "tasques": "Tasques",
        "publicada": "Publicada",
        "categoria": "Origen",
    })

    df["Publicada"] = df["Publicada"].apply(lambda x: "Sí" if x else "No")

    return df

def importar_dataframe_a_postgresql(df):
    engine = get_engine()

    df.to_sql(
        "activitats",
        engine,
        if_exists="append",
        index=False
    )
    
from sqlalchemy import text

# *************************************************Ingresamos actividad
def inserir_activitat(activitat):
    engine = get_engine()

    consulta = text("""
        INSERT INTO activitats (
            activitat,
            tipus,
            espai,
            data_inici,
            data_fi,
            dies_setmana,
            hora_inici,
            hora_fi,
            organitza,
            coordinacio,
            material,
            tasques,
            publicada,
            categoria
        )
        VALUES (
            :activitat,
            :tipus,
            :espai,
            :data_inici,
            :data_fi,
            :dies_setmana,
            :hora_inici,
            :hora_fi,
            :organitza,
            :coordinacio,
            :material,
            :tasques,
            :publicada,
            :categoria
        )
    """)

    with engine.begin() as conn:
        conn.execute(consulta, activitat)
        
        
def activitat_te_lloc_el_dia_db(data_inici, data_fi, dies_setmana, dia):
    dies_setmana = str(dies_setmana).strip().lower()

    if data_inici > dia.date() or data_fi < dia.date():
        return False

    if dies_setmana in ["", "nan", "none"]:
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


def hi_ha_solapament(espai, data_inici, data_fi, dies_setmana, hora_inici, hora_fi):
    engine = get_engine()

    consulta = text("""
        SELECT *
        FROM activitats
        WHERE espai = :espai
          AND data_inici <= :data_fi
          AND data_fi >= :data_inici
          AND hora_inici < :hora_fi
          AND hora_fi > :hora_inici
    """)

    params = {
        "espai": espai,
        "data_inici": data_inici,
        "data_fi": data_fi,
        "hora_inici": hora_inici,
        "hora_fi": hora_fi,
    }

    df = pd.read_sql(consulta, engine, params=params)

    if df.empty:
        return df

    conflictes = []

    inici_comprovacio = pd.Timestamp(data_inici)
    fi_comprovacio = pd.Timestamp(data_fi)

    for _, fila in df.iterrows():
        inici_solapament = max(inici_comprovacio, pd.Timestamp(fila["data_inici"]))
        fi_solapament = min(fi_comprovacio, pd.Timestamp(fila["data_fi"]))

        dies = pd.date_range(inici_solapament, fi_solapament)

        for dia in dies:
            nova_te_lloc = activitat_te_lloc_el_dia_db(
                data_inici,
                data_fi,
                dies_setmana,
                dia
            )

            existent_te_lloc = activitat_te_lloc_el_dia_db(
                fila["data_inici"],
                fila["data_fi"],
                fila["dies_setmana"],
                dia
            )

            if nova_te_lloc and existent_te_lloc:
                conflictes.append(fila)
                break

    if conflictes:
        return pd.DataFrame(conflictes)

    return pd.DataFrame()


# ******************************************     LECTURA DE ACTIVIDADES
def llegir_activitats_admin():
    engine = get_engine()

    consulta = """
        SELECT
            id,
            activitat,
            espai,
            data_inici
        FROM activitats
        ORDER BY data_inici, activitat
    """

    return pd.read_sql(consulta, engine)

# ******************************************      ELIMINAR
def eliminar_activitat(id_activitat):
    engine = get_engine()

    consulta = text("""
        DELETE FROM activitats
        WHERE id = :id
    """)

    with engine.begin() as conn:
        conn.execute(
            consulta,
            {"id": id_activitat}
        )

def obtenir_activitat_per_id(id_activitat):
    engine = get_engine()

    consulta = text("""
        SELECT *
        FROM activitats
        WHERE id = :id
    """)

    df = pd.read_sql(consulta, engine, params={"id": id_activitat})

    if df.empty:
        return None

    return df.iloc[0]


def actualitzar_activitat(id_activitat, activitat):
    engine = get_engine()

    consulta = text("""
        UPDATE activitats
        SET
            activitat = :activitat,
            tipus = :tipus,
            espai = :espai,
            data_inici = :data_inici,
            data_fi = :data_fi,
            dies_setmana = :dies_setmana,
            hora_inici = :hora_inici,
            hora_fi = :hora_fi,
            organitza = :organitza,
            coordinacio = :coordinacio,
            material = :material,
            tasques = :tasques,
            publicada = :publicada,
            categoria = :categoria
        WHERE id = :id
    """)

    activitat["id"] = id_activitat

    with engine.begin() as conn:
        conn.execute(consulta, activitat)

def hi_ha_solapament_editant(id_activitat, espai, data_inici, data_fi, dies_setmana, hora_inici, hora_fi):
    engine = get_engine()

    consulta = text("""
        SELECT *
        FROM activitats
        WHERE id <> :id
          AND espai = :espai
          AND data_inici <= :data_fi
          AND data_fi >= :data_inici
          AND hora_inici < :hora_fi
          AND hora_fi > :hora_inici
    """)

    params = {
        "id": id_activitat,
        "espai": espai,
        "data_inici": data_inici,
        "data_fi": data_fi,
        "hora_inici": hora_inici,
        "hora_fi": hora_fi,
    }

    df = pd.read_sql(consulta, engine, params=params)

    if df.empty:
        return df

    conflictes = []

    inici_comprovacio = pd.Timestamp(data_inici)
    fi_comprovacio = pd.Timestamp(data_fi)

    for _, fila in df.iterrows():
        inici_solapament = max(inici_comprovacio, pd.Timestamp(fila["data_inici"]))
        fi_solapament = min(fi_comprovacio, pd.Timestamp(fila["data_fi"]))

        dies = pd.date_range(inici_solapament, fi_solapament)

        for dia in dies:
            nova_te_lloc = activitat_te_lloc_el_dia_db(
                data_inici,
                data_fi,
                dies_setmana,
                dia
            )

            existent_te_lloc = activitat_te_lloc_el_dia_db(
                fila["data_inici"],
                fila["data_fi"],
                fila["dies_setmana"],
                dia
            )

            if nova_te_lloc and existent_te_lloc:
                conflictes.append(fila)
                break

    if conflictes:
        return pd.DataFrame(conflictes)

    return pd.DataFrame()

# *************************************** Tabla espais
def llegir_espais():
    engine = get_engine()

    consulta = """
        SELECT nom
        FROM espais
        WHERE actiu = true
        ORDER BY nom
    """

    df = pd.read_sql(consulta, engine)

    return df["nom"].tolist()