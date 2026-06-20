# ACTIVITATS2026 - ESTAT DEL PROJECTE (20/06/2026)

## Situació actual

L'aplicació ha deixat de dependre d'Excel i funciona principalment sobre PostgreSQL.

Les activitats es gestionen des de la pròpia aplicació i la base de dades és la font oficial de la informació.

Actualment el projecte es troba en fase de consolidació, validació i preparació per a producció.

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

✅ Agenda pública setmanal

✅ Gestió interna

✅ Calendari mensual

✅ Agenda setmanal

✅ Gestió d'espais

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

Sistema implementat mitjançant selecció múltiple:

✅ Dilluns

✅ Dimarts

✅ Dimecres

✅ Dijous

✅ Divendres

✅ Dissabte

✅ Diumenge

Ja no es depèn de textos lliures.

---

## Solapaments

Implementat:

✅ Control de solapaments en crear activitats

✅ Control de solapaments en editar activitats

S'ha eliminat la comprovació redundant de solapaments a la vista interna.

Pendent:

🔲 Revisar possibles casos especials de recurrències llargues si apareixen durant les proves reals.

---

## Qualitat de les dades

Corregits:

✅ Biodansa

✅ Caliu

✅ Tipus unificats

✅ Categories normalitzades

✅ Dies setmana normalitzats

Les dades actuals es consideren consistents.

---

## Interfície

Implementat:

✅ Capçalera institucional

✅ Favicon

✅ Logotips corporatius

✅ Menú reorganitzat

✅ Nomenclatura simplificada

✅ Agenda pública redissenyada

✅ Agenda setmanal millorada

✅ Ordenació per dia i hora

✅ Organitzador visible a les activitats

✅ Cercador a la gestió interna

✅ Millora de la visualització general

✅ Calendari mensual adaptat per a dispositius mòbils

✅ Eliminació de l'any fix 2026

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

✅ Repositori local operatiu

### GitHub

✅ Repositori sincronitzat

https://github.com/ic4rus19/activitats2026

Commits realitzats correctament.

Push validat correctament.

---

## Millores pendents

### Interfície

🔲 Revisió final de la vista Administració

🔲 Revisar textos, icones i missatges

🔲 Revisar formularis

🔲 Revisar experiència d'usuari

🔲 Revisar visualització en pantalles petites

### Validació

🔲 Fer proves amb 1 o 2 usuaris reals

🔲 Corregir incidències detectades

### Documentació

🔲 Actualitzar requirements.txt definitiu

🔲 Revisar documentació funcional

🔲 Documentació tècnica final

### Infraestructura

🔲 Dockerització de l'aplicació

🔲 Preparació del desplegament VPS

---

## Producció

Encara NO.

Abans del desplegament:

1. Revisió visual final.
2. Proves amb usuaris.
3. Correcció d'incidències.
4. Dockerització.
5. Desplegament VPS.
6. Posada en producció.

---

## Estat general

Fase actual:

CONSOLIDACIÓ I PREPARACIÓ PER A VALIDACIÓ D'USUARIS

Nivell estimat d'avanç:

97%

L'aplicació és estable, funcional i disposa de:

✅ PostgreSQL

✅ Backup validat

✅ Git

✅ GitHub

✅ Exportació Excel

✅ Control de solapaments

✅ Interfície consolidada

El mòdul d'estadístiques ha estat retirat del projecte i es replantejarà en una futura versió si apareixen necessitats reals d'explotació de dades.

El risc tècnic actual és baix i les tasques pendents són principalment de validació, documentació i desplegament.
