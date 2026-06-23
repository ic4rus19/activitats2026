import calendar
from io import BytesIO

import pandas as pd
import streamlit as st

from src.utils import activitat_te_lloc_el_dia, icona_categoria


def mostrar_agenda_setmanal(df_filtrat, mes, mesos):

    mode_setmana = st.radio(
        "Període",
        ["Setmana del mes", "Aquesta setmana", "Setmana vinent"],
        horizontal=True
    )

    noms_dies = {
        0: "Dilluns",
        1: "Dimarts",
        2: "Dimecres",
        3: "Dijous",
        4: "Divendres",
        5: "Dissabte",
        6: "Diumenge",
    }

    if mode_setmana == "Setmana del mes":
        if mes == "Tots":
            st.info("Selecciona un mes per veure l'agenda setmanal.")
            return

        mes_num = mesos[mes]
        any_actual = pd.Timestamp.today().year

        setmanes = calendar.monthcalendar(any_actual, mes_num)

        opcions_setmanes = []

        for idx, setmana in enumerate(setmanes, start=1):
            dies_valids = [dia for dia in setmana if dia != 0]

            primer_dia = dies_valids[0]
            ultim_dia = dies_valids[-1]

            opcions_setmanes.append(
                f"Setmana {idx}: "
                f"{primer_dia:02d}/{mes_num:02d} - "
                f"{ultim_dia:02d}/{mes_num:02d}"
            )

        setmana_text = st.selectbox("Setmana", opcions_setmanes)
        index_setmana = opcions_setmanes.index(setmana_text)
        setmana = setmanes[index_setmana]

        dies_a_mostrar = []

        for numero_dia in setmana:
            if numero_dia == 0:
                continue

            dia = pd.Timestamp(any_actual, mes_num, numero_dia)
            dies_a_mostrar.append(dia)

        nom_fitxer = "informe_setmanal_activitats.xlsx"

    else:
        avui = pd.Timestamp.today().normalize()

        if mode_setmana == "Setmana vinent":
            avui = avui + pd.Timedelta(days=7)

        inici_setmana = avui - pd.Timedelta(days=avui.weekday())
        fi_setmana = inici_setmana + pd.Timedelta(days=6)

        st.caption(
            f"Setmana del {inici_setmana.strftime('%d/%m/%Y')} "
            f"al {fi_setmana.strftime('%d/%m/%Y')}"
        )

        dies_a_mostrar = list(pd.date_range(inici_setmana, fi_setmana))

        nom_fitxer = (
            f"informe_setmanal_"
            f"{inici_setmana.strftime('%Y%m%d')}_"
            f"{fi_setmana.strftime('%Y%m%d')}.xlsx"
        )

    files_informe = []

    for dia in dies_a_mostrar:

        activitats_dia = df_filtrat[
            df_filtrat.apply(
                lambda fila: activitat_te_lloc_el_dia(fila, dia),
                axis=1
            )
        ].sort_values("Hora inici")

        st.markdown(
            f"### {noms_dies[dia.weekday()]} {dia.strftime('%d/%m/%Y')}"
        )

        if activitats_dia.empty:
            st.caption("Sense activitats")

        else:
            for _, fila in activitats_dia.iterrows():

                hora_inici = str(fila["Hora inici"])[:5]
                hora_fi = str(fila["Hora fi"])[:5]

                icona = icona_categoria(fila["Origen"])

                estat = str(
                    fila.get("Estat", "ACTIVA")
                ).strip().upper()

                organitza = str(fila.get("Organitza", "")).strip()
                coordinacio = str(fila.get("Coordinació", "")).strip()
                material = str(fila.get("Material", "")).strip()
                tasques = str(fila.get("Tasques", "")).strip()

                files_informe.append({
                    "Dia": noms_dies[dia.weekday()],
                    "Data": dia.strftime("%d/%m/%Y"),
                    "Hora inici": hora_inici,
                    "Hora fi": hora_fi,
                    "Activitat": fila["Activitat"],
                    "Espai": fila["Espai"],
                    "Organitza": organitza,
                    "Coordinació": coordinacio,
                    "Material": material,
                    "Tasques": tasques,
                    "Categoria": fila["Origen"],
                    "Estat": estat,
                })

                contingut = f"""
{icona} **{hora_inici} - {hora_fi}**

**{fila['Activitat']}**

📍 {fila['Espai']}

👥 {organitza}
"""

                if estat == "PENDENT D'APROVACIÓ":
                    contingut += "\n\n⏳ **Pendent d'aprovació**"

                if coordinacio and coordinacio.lower() != "nan":
                    contingut += f"\n\n🏛️ Coordinació: {coordinacio}"

                if material and material.lower() != "nan":
                    contingut += f"\n\n🧰 Material: {material}"

                if tasques and tasques.lower() != "nan":
                    contingut += f"\n\n📝 Tasques: {tasques}"

                with st.container(border=True):
                    st.markdown(contingut)

    df_informe = pd.DataFrame(files_informe)

    if not df_informe.empty:
        buffer = BytesIO()

        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df_informe.to_excel(
                writer,
                index=False,
                sheet_name="INFORME_SETMANAL"
            )

        st.download_button(
            label="📄 Descarregar informe Excel",
            data=buffer.getvalue(),
            file_name=nom_fitxer,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )