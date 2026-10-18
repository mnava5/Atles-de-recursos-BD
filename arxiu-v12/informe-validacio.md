# Informe de validació · versió 0.10
Data: 17/10/2026

## Comprovacions efectuades
- 109 documents HTML amb un H1 i `lang="ca"`.
- 74 targetes de catàleg i 74 fitxes independents.
- 23 pàgines de països i organismes.
- 10 capítols estàtics navegables.
- 0 enllaços interns locals inexistents en la inspecció HTML.
- 0 etiquetes de formulari `for` sense control corresponent.
- Identificadors de fitxa únics i correspondència de les etiquetes temàtiques amb el vocabulari controlat.
- `node --check` del fitxer `assets/filtres.js`: sintaxi correcta.
- Les fitxes i portades utilitzen HTML semàntic i CSS propi, sense imatges ni biblioteques de tercers.

## Proves pendents / bloquejades
- Les proves de navegador automatitzat sobre `file://` i `http://127.0.0.1` retornen `net::ERR_BLOCKED_BY_ADMINISTRATOR` a l'entorn actual. Per tant no s'han validat realment el filtre operatiu, el focus amb teclat, la renderització 375/1440 px ni la impressió a Chromium en aquesta versió.
- No s'ha provat la compatibilitat real amb els capítols natius d'Odissea; els filtres requereixen JavaScript i poden no funcionar si Moodle filtra scripts.
- No s'ha fet auditoria completa WCAG 2.2 AA amb lector de pantalla.
- No s'han obert individualment tots els 74 recursos i fitxers descarregables: les fitxes antigues mantenen estat de verificació heretat.
- La llista de 249 territoris ISO és un inventari, no una recerca exhaustiva conclosa.

## Evidències i procedència
- Els nous recursos narratius tenen referències de consulta al fitxer `dades/fonts-consultades.csv`.
- Els rols de personatges són descriptius d'acord amb les fonts consultades, no símbols atribuïts si la font no els defineix.
- Les etiquetes temàtiques assignades a recursos antics són orientatives i s'han de revisar editorialment abans de publicació definitiva.


## Actualització v0.11

- Fitxes HTML analitzades: 109.
- Registres del JSON: 74.
- Episodis descrits en fitxes (repeticions possibles): 33.
- Errors de navegació interna o `<details open>` en inspecció estàtica: 0.
- La verificació funcional al navegador, amb lector de pantalla i a Odissea continua pendent; **aquesta validació és estàtica**.
- Errors: Cap error detectat a les comprovacions indicades.

### Prova gràfica no completada
S'ha intentat obrir una fitxa amb Chromium en mode sense interfície gràfica el 17/10/2026, però el procés ha superat el límit d'execució i no ha produït una captura. En conseqüència **no es declara superada** una prova visual a mòbil, escriptori o lector de pantalla en la versió 0.11.


## Revisió v0.12 — fonts aportades

- Set adreces revisades i documentades a `fonts-aportades.html` i `dades/urls-aportades.csv`.
- Cinc ja estaven representades per fitxes preexistents i s’han relacionat com a fonts complementàries sense duplicar fitxes.
- EAVI: s’ha incorporat un article original d’EAVI que sí ha estat consultat; la pàgina marc facilitada ha retornat HTTP 406 i queda pendent de verificació directa.
- Ceibal: s’ha incorporat una fitxa d’un curs oficial d’introducció, amb informació recuperada de l’índex oficial; la pàgina marc facilitada ha retornat HTTP 403 i la consulta directa del curs no s’ha pogut completar.
- El catàleg HTML autònom pot filtrar amb JavaScript. El Llibre de Moodle necessita una prova de compatibilitat real.
- No s’ha auditat de nou el contingut complet de les 74 fitxes heretades.
