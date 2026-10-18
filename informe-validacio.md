# Validació de l’Atles · versió 0.13

Data: 17/10/2026.

## Comprovacions executades

- 227 documents HTML analitzats; zero enllaços interns a fitxers o fragments inexistents.
- Zero identificadors duplicats dins de cada document.
- 84 identificadors de recurs, 17 de família i 56 de registre narratiu únics.
- Catàleg amb 84 fitxes; recompte geogràfic separat en 24 països i 6 organismes.
- ZIP d’importació llegible i íntegre: 96 HTML, amb 84 noms acabats en `_sub.html`.
- Capítols d’importació sense scripts, formularis, iframes, estils externs ni contingut ocult dependent de scripts.
- Llibre complet sense scripts ni dependències locals externes: 84 fitxes i 56 identificadors d’episodi.
- Desplegables inicialment tancats; etiquetes de formulari vinculades als controls.
- Sintaxi de `assets/filtres.js` comprovada amb `node --check`.
- Vuit comprovacions de la lògica dels filtres amb els atributs reals de les 84 fitxes: país, personatge, combinació, restabliment, conjunt buit i cerca sense diacrítics.

Les comprovacions dels filtres utilitzen un adaptador de DOM per executar el script. No es presenten com una prova de navegador real.

## Proves no executades

- Prova gràfica en ordinador, mòbil i impressió: no s’ha pogut executar, perquè l’entorn no disposa d’un executable de navegador. No s’ha produït cap captura vàlida.
- Navegació real amb teclat i lector de pantalla.
- Auditoria integral de contrast i WCAG.
- Importació i vista de participant al Llibre d’Odissea.
- Funcionament de tots els vídeos, jocs, comptes i descàrregues externs.

La compatibilitat real amb Odissea continua pendent. No s’afirma que el paquet s’hagi importat ni que s’hagi validat visualment a la plataforma.
