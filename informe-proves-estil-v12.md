# Validació de la versió 0.13 amb disseny 0.12

**Data de preparació:** 18 d'octubre de 2026.

## Comprovacions satisfactòries

- `dades/`: comparació binària contra la v0.13 adjunta; **tots els fitxers de dades són idèntics**.
- Catàleg HTML: **84 targetes**, una per cada entrada de `recursos.json`, amb identificadors únics.
- Personatges: preservats els **72 registres** de les dades originals. També es mantenen **17 famílies de sèries** i **56 episodis i registres narratius** de la v0.13.
- Fitxes HTML: comprovació del text original de cada pàgina i del text de la versió redissenyada; no s'ha detectat pèrdua del contingut textual de les fitxes originals.
- Pàgines: revisió estàtica dels atributs `lang`, encapçalaments principals i rutes relatives locals. **Cap enllaç intern trencat** entre els fitxers revisats.
- Filtrat: proves del JavaScript real amb elements simulats. Han passat: primer recompte de 84, selecció d'Austràlia (8 fitxes), combinació Austràlia + Primària (4), Ciberassetjament (8), Ciberassetjament + personatges recurrents (5), cerca per «Vinz», resultats buits i restabliment.
- Països i etapes: llistes regenerades a partir de les etiquetes editorials de la v0.13, sense reclassificar recursos.
- Llibre d'Odissea: capítols HTML sense JavaScript, amb els estils en línia recolorits a la paleta v0.12, i ZIP d'importació independent.

## Limitacions i proves pendents

- **Proves amb navegador real:** Chromium, executat amb Playwright sobre un servidor local, ha retornat `net::ERR_BLOCKED_BY_ADMINISTRATOR`. Les proves visuals a 375 i 1440 píxels i les interaccions reals de teclat continuen pendents. Les proves del JavaScript sense navegador no substitueixen aquestes comprovacions.
- **Accessibilitat:** s'ha preservat HTML semàntic, labels dels filtres i focus visible. No s'ha completat una auditoria WCAG 2.2 AA amb lector de pantalla.
- **Odissea/Moodle:** no s'ha accedit a cap curs real. Moodle pot filtrar scripts i estils en copiar HTML al Llibre. Els filtres dinàmics només estan garantits dins del paquet HTML autònom sota un navegador que permeti JavaScript.
- **Fonts externes:** no s'han verificat novament els enllaços públics ni les dades de les fonts; es conserven literalment les verificacions, advertiments i limitacions de la v0.13.
- **Conversió de format:** el document integral d'un sol HTML i la importació Moodle tenen la paleta v0.12; no són una implementació del filtratge interactiu.
