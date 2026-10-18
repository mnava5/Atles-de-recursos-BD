# Atles de benestar digital · Dades v0.13 amb disseny v0.12

**Aquesta edició conserva íntegrament el corpus editorial v0.13 (84 recursos), els registres d'episodis, personatges, fonts, auditoria i altres dades.** Només s'ha canviat la presentació HTML i el CSS per adoptar el disseny de la v0.12. No s'han afegit recursos ni s'han verificat novament URLs externes.

- `index.html`: portada de l'estil v0.12.
- `cataleg.html`: targetes amb portada de color i filtres v0.12 (país, temàtica, tipus, etapa, cerca). Es conserva com a filtre addicional opcional l'estat dels personatges.
- `recursos/`: fitxes completes v0.13, amb capçalera, seccions i barra lateral v0.12.
- `paisos/` i `capitols/`: inventaris presentats amb targetes v0.12; els altres capítols conserven el contingut revisat de la v0.13.
- `personatges.html`, `episodis.html`: contingut v0.13 amb aparença v0.12.
- `dades/`: **dades v0.13 sense modificar**.
- `assets/estils.css`: CSS de la v0.12 amb complement de compatibilitat.
- `assets/filtres.js`: filtres de la v0.12, progressius i sense llibreries externes.
- `odissea/` i `importacio-odissea-v0.13-estil-v12.zip`: fitxers HTML preparats per copiar al Llibre de Moodle, amb colorimetria v0.12. Aquest format no incorpora filtres interactius dins del Llibre.
- `Atles_internacional_benestar_digital_v0.13.html`: document integral original de la v0.13, conservat sense alterar-ne el contingut.

**Per veure el disseny nou**, descomprimeix el ZIP i obre `index.html`, o directament `cataleg.html`, al navegador. Mantingues l'estructura de carpetes.

**Per publicar a Odissea**, crea un recurs Llibre i copia els capítols/subcapítols de `odissea/` amb l'editor HTML. El catàleg autònom amb filtres depèn de `assets/filtres.js`, i Moodle pot eliminar scripts quan s'enganxen dins del Llibre. Si es vol conservar la cerca interactiva, publica el catàleg autònom com a recurs de fitxer HTML autoritzat, o enllaça'l des del Llibre després de provar-ho en el teu curs real.

`build_v13.py` és el generador original de la v0.13, conservat com a referència. **No l'executis directament sobre aquest paquet**, perquè regeneraria les pàgines amb l'estil anterior de la v0.13. La transformació s’ha executat sobre una còpia del corpus i s’ha conservat la traçabilitat dels fitxers font.

Les fitxes indiquen l'abast real de la verificació de les fonts, com a la v0.13. Aquesta transformació no substitueix una auditoria completa WCAG 2.2 AA ni la prova d'importació al servidor real d'Odissea.

---

# Atles internacional de benestar digital · versió 0.13

Base: paquet complet 0.12. Revisió: 17/10/2026.

## Contingut

- `index.html`: portada del catàleg autònom.
- `cataleg.html`: 84 fitxes amb cerca i filtres progressius, inclòs l’estat dels personatges.
- `personatges.html`: 17 famílies examinades; 14 amb un nucli o figura recurrent documentats.
- `episodis.html`: 56 registres únics, diferenciats per tipus.
- `Atles_internacional_benestar_digital_v0.13.html`: llibre complet en un sol HTML, sense scripts ni recursos locals externs.
- `odissea/`: 12 capítols i 84 fitxes com a subcapítols, amb estils en línia.
- `importacio-odissea-v0.13.zip`: només els HTML destinats al recurs Llibre.
- `dades/`: dades de fitxes, sèries, personatges, episodis, auditoria i cerques.
- `informe-revisio-v13.md`: canvis editorials i límits.
- `informe-validacio.md`: comprovacions efectuades en aquesta versió.
- `arxiu-v12/`: dades i informes anteriors, conservats com a antecedents, no com a contingut vigent.

## Importació prevista al Llibre d’Odissea

1. Crear un recurs Llibre en un espai de prova.
2. A l’administració del Llibre, utilitzar l’opció d’importar capítols, si està habilitada.
3. Seleccionar `importacio-odissea-v0.13.zip` i l’opció en què cada fitxer HTML representa un capítol.
4. Els noms numèrics ordenen la lectura. Les fitxes acaben en `_sub.html` perquè es tractin com a subcapítols de “Catàleg complet”.
5. Comprovar que els enllaços relatius es converteixen en enllaços de capítol i que es mantenen els identificadors, `details` i `summary`.
6. Revisar com a docent i participant, amb teclat, en pantalla estreta i en impressió.

Referència oficial consultada: https://docs.moodle.org/402/en/Book_settings#Importing_chapters

La documentació de Moodle descriu el mecanisme; no acredita la versió ni les opcions habilitades d’Odissea. No s’ha importat el paquet en un curs real. Si l’editor elimina `details`, la informació es pot convertir en subapartats oberts; no s’ha d’introduir dependència de JavaScript per llegir-la.

## Regeneració

Editar les dades editorials revisades de `dades/` i executar `python3 build_v13.py`. El script necessita Python 3 i lxml. No fa cerques ni infereix automàticament temes o personatges. Cal mantenir coherent `resum-revisio.json` quan canviï l’inventari.

## Abast

S’han revisat les fonts principals del corpus heretat i s’ha aprofundit en les afirmacions narratives. No s’han llegit tots els annexos ni visionat tots els vídeos. L’ampliació internacional és dirigida; el registre de 249 territoris no representa una recerca mundial acabada. Les llicències individuals dels materials externs s’han de comprovar abans de reproduir-los.


## Ampliació 0.14 · Youth Law Australia (18/10/2026)

S’han afegit 6 fitxes d’orientació jurídica, amb aplicació d’aula editorial i advertiment sobre la normativa del Territori del Nord. Les pàgines originals i l’índex temàtic han estat consultats a la web; no es presenten com a seqüències didàctiques oficials, ni es documenten personatges ficticis o rúbriques que no hi són. S’han mantingut les 84 fitxes de la v0.13. La interfície HTML ha estat ampliada sense alterar les dades dels registres anteriors. El fitxer llibre únic i els fitxers d’importació nativa d’Odissea de la versió 0.13 es conserven com a antecedent, NO incorporen les fitxes noves. Per regenerar-los cal adaptar el generador a la v0.14.
