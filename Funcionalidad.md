# ACTIVITATS2026 - ESTAT DEL PROJECTE

## Situació actual

Activitats2026 ha evolucionat d'una aplicació basada en Excel a una aplicació de gestió d'activitats municipals basada en PostgreSQL.

La base de dades és actualment la font principal de dades.

---

## Arquitectura

PostgreSQL
↓
Streamlit
↓
Vistes de consulta i administració

L'Excel queda com:

* Exportació
* Còpia de seguretat
* Recuperació de dades puntual

---

## Funcionalitats operatives

### Consulta

* Vista pública
* Vista interna
* Calendari mensual
* Agenda setmanal
* Ocupació d'espais

### Administració

* Crear activitats
* Editar activitats
* Eliminar activitats
* Cercar activitats
* Exportar a Excel

### Validacions

* Control de solapaments
* Control d'espais
* Validació de dates
* Validació d'hores

---

## Millores implementades

### Refactorització

L'aplicació està dividida en mòduls:

* vista_publica.py
* vista_interna.py
* vista_calendari.py
* vista_setmanal.py
* vista_espais.py
* vista_admin.py
* db.py
* utils.py

app.py ha passat de més de 700 línies a aproximadament 160 línies.

### Espais

S'ha creat la taula:

espais

Els espais es gestionen des de PostgreSQL.

Els formularis utilitzen llistes oficials d'espais.

### Dies de la setmana

Nova activitat:

* Selecció múltiple de dies
* Eliminació d'errors d'escriptura

Editar activitat:

* Selecció múltiple de dies
* Modificació simplificada

### Experiència d'usuari

* Missatges de confirmació
* Actualització automàtica de dades
* Reinicialització del formulari després de guardar

---

## Aspectes pendents

### Solapaments recurrents

Millorar la detecció de conflictes tenint en compte:

* dies_setmana
* activitats recurrents
* activitats de diversos dies

### Calendari

Revisar activitats recurrents de diversos dies per assegurar una visualització correcta.

### Seguretat

Implementar sistema de còpies de seguretat PostgreSQL.

---

## Properes actuacions

1. Primer backup PostgreSQL.
2. Publicació del projecte a GitHub.
3. Dockerització de l'aplicació.
4. Documentació definitiva.
5. Revisió funcional completa.

---

## Estat general

Fase actual:

Aplicació funcional en producció interna.

Nivell d'avanç estimat:

85%-90%

Les funcionalitats principals estan implementades i la fase actual és principalment de validació, correcció de casos especials i millora de l'experiència d'usuari.


El proyecto ya no está en fase de desarrollo inicial. Está en fase de consolidación y pruebas reales. La arquitectura está decidida (PostgreSQL + Streamlit), el CRUD funciona y los próximos pasos son robustez, copias de seguridad, GitHub y Docker. 🚀
