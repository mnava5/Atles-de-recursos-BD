# Atles internacional de benestar digital — versió 0.10

## Contingut
- `index.html`: portada.
- `cataleg.html`: 74 targetes educatives amb filtres per país, temàtica, tipus, etapa i cerca textual.
- `recursos/`: una fitxa HTML completa per cadascun dels 74 recursos.
- `paisos/`: una pàgina específica per país o organisme.
- `capitols/`: deu capítols navegables per etapa, famílies, organismes, índex geogràfic i metodologia.
- `dades/recursos.json`: font estructurada de fitxes, temàtiques i personatges.
- `dades/cobertura-paisos.csv`: registre ISO heretat; encara no confirma recerca completa.
- `assets/estils.css`: CSS original sense Bootstrap ni dependències externes.
- `assets/filtres.js`: script progressiu només per al catàleg.

## Com publicar a Odissea — recurs Llibre
1. Crea un Llibre i capítols amb els títols de `capitols/`. Afegeix o copia el contingut d'aquests capítols en mode HTML. Les fitxes llargues poden ser subcapítols natius, si això facilita la navegació.
2. Comprova en un capítol pilot si Moodle conserva `class`, `style`, `data-*`, els enllaços relatius i els elements `details`/`summary`. Alguns editors eliminen scripts i fulls d'estil enllaçats.
3. **No confiïs que Moodle executarà `filtres.js` dins dels capítols del Llibre.** Si el script no s'executa, els recursos segueixen accessibles a través dels capítols estàtics i l'índex de països.
4. Per conservar el filtratge, publica el directori íntegre com a fitxers de Moodle (fitxer principal `index.html`, si l'administració ho permet) o en un espai web autoritzat, i enllaça el catàleg HTML des del Llibre. No totes les instàncies permeten HTML enllaçat amb JavaScript.
5. Confirma el funcionament final amb un usuari docent i un alumne de prova, incloent el mòbil, la impressió i la navegació amb teclat.

## Actualització
Modifica `dades/recursos.json` i regenera l'HTML amb un script de construcció. Les temàtiques són una classificació editorial; si s'afegeixen, cal actualitzar el camp `tematiques`. No copiïs materials originals (imatges, vídeos o PDF) si la seva llicència no permet redistribuir-los.

## Referència de disseny
El catàleg s'inspira en l'arquitectura de **targetes, filtres i camins d'aprenentatge** de Common Sense Education, però no en reprodueix el codi, els gràfics ni la identitat visual.
URL de referència: https://www.commonsense.org/education/digital-literacy/grades-9-12?field_term_lesson_resources_target_id=121574

## Limitacions
- No està acreditada una investigació exhaustiva dels 249 estats o territoris ISO.
- Hi ha fitxes heretades amb metadades individuals pendents de revisió.
- Les etiquetes temàtiques s'han assignat editorialment a partir de les descripcions; cal revisar-les en materials que cobreixen molts àmbits.
- Alguns recursos disposen de guies amb accés restringit, subscripció o limitacions geogràfiques.
- La importació real al Llibre d'Odissea i una auditoria completa WCAG 2.2 AA continuen pendents.


## Novetat v0.11 — personatges i episodis

La secció «Personatges i funcions» disposa d'un dels tres estats: «Personatges identificats», «Sense personatges narratius» o «Pendent de verificació». Les sèries analitzades contenen taules amb personatges i desplegables natius per als episodis amb conflictes, aprenentatges, temàtiques i enllaços originals.

Dades estructurades: `dades/recursos.json` i `dades/personatges-i-episodis.csv`. Consulteu `informe-revisio-personatges.md` abans de publicar. La informació s'ha revisat el 2026-10-17. No s'han modificat les llicències ni els recursos externs.


## Actualització v0.12 · fonts aportades

- `fonts-aportades.html` detalla les set adreces facilitades, estat de consulta i enllaç a la fitxa.
- `dades/urls-aportades.csv` registra l’estat tècnic de la comprovació.
- S’han incorporat les fitxes `recursos/eavi-balance.html` i `recursos/uy-intro.html`.
- L’enllaç directe d’EAVI a *The Art of Living in the Digital Environment* ha retornat HTTP 406, i el de Ceibal institucional HTTP 403; **no s'han presentat com a accessibles verificats**.
- La compatibilitat amb el recurs Llibre d’Odissea encara no està validada.
