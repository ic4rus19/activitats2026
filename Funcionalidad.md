# ACTIVITATS2026 - ESTAT DEL PROJECTE (18/06/2026)

## Situació actual

L'aplicació ha deixat de dependre d'Excel i funciona principalment sobre PostgreSQL.

Les activitats es gestionen des de la pròpia aplicació i la base de dades és la font oficial de la informació.

---

## Arquitectura

PostgreSQL
↓
Streamlit
↓
Vistes de consulta i administració

L'Excel queda com:

* Exportació
* Recuperació puntual de dades
* Còpia de seguretat complementària

---

## Funcionalitats operatives

### Consulta

✅ Agenda pública

✅ Vista interna

✅ Calendari mensual

✅ Agenda setmanal

✅ Ocupació d'espais

### Administració

✅ Crear activitats

✅ Editar activitats

✅ Eliminar activitats

✅ Cercar activitats

✅ Exportar activitats a Excel

---

## Base de dades

✅ PostgreSQL operatiu

✅ Taula activitats

✅ Taula espais

✅ Gestió d'espais des de PostgreSQL

Els espais es seleccionen mitjançant desplegables oficials.

---

## Dies de la setmana

Nou sistema implementat mitjançant selecció múltiple:

✅ Dilluns

✅ Dimarts

✅ Dimecres

✅ Dijous

✅ Divendres

✅ Dissabte

✅ Diumenge

Ja no es depèn de textos lliures com:

* Cap de setmana
* Dilluns a Divendres

---

## Solapaments

Implementat:

✅ Control de solapaments en crear activitats

✅ Control de solapaments en editar activitats

Pendent:

🔲 Revisar possibles casos especials de recurrències llargues si apareixen durant les proves reals.

---

## Qualitat de les dades

Corregits:

✅ Biodansa

✅ Caliu

✅ Tipus unificats

✅ Dies setmana normalitzats

Les dades actuals es consideren consistents.

---

## Seguretat

### Backup PostgreSQL

✅ Realitzat correctament

Fitxer:

BACKUPS/activitats2026_2026-06-18.backup

### Exportació Excel

✅ Operativa

✅ Validada correctament

---

## Control de versions

### Git

✅ Repositori local creat

### GitHub

✅ Repositori creat

https://github.com/ic4rus19/activitats2026

✅ Primer commit

✅ Primer push

Repositori sincronitzat correctament.

---

## Millores visuals pendents

Abans de producció:

🔲 Revisar distribució de Vista Administració

🔲 Millorar capçaleres i icones

🔲 Revisar textos i missatges

🔲 Revisar formularis

🔲 Revisar experiència d'usuari

🔲 Revisar visualització en pantalles petites

---

## Producció

Encara NO.

Abans del desplegament:

1. Millores visuals.
2. Proves amb 1 o 2 usuaris reals.
3. Correcció d'incidències detectades.
4. Dockerització de l'aplicació.
5. Desplegament definitiu.

---

## Properes actuacions

### Prioritat alta

🔲 Revisió visual completa

🔲 Proves amb usuaris

### Prioritat mitjana

🔲 Dockerització de l'aplicació

🔲 Documentació tècnica

### Prioritat baixa

🔲 Estadístiques avançades

🔲 Funcionalitats addicionals

---

## Estat general

Fase actual:

CONSOLIDACIÓ I VALIDACIÓ

Nivell estimat d'avanç:

95%

L'aplicació és funcional, estable i ja disposa de base de dades PostgreSQL, còpies de seguretat, control de versions amb Git i repositori GitHub operatiu.
