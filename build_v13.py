#!/usr/bin/env python3
"""Regenera l’Atles exclusivament a partir de dades editorials revisades.
No cerca fonts, no infereix personatges i no reclassifica temes per paraules clau.
Ús: python3 build_v13.py
"""
from pathlib import Path
from collections import Counter, defaultdict
from html import escape as H
from urllib.parse import urlsplit, unquote
import csv, json, re, shutil, unicodedata, zipfile
from lxml import html as LH

ROOT=Path(__file__).resolve().parent
def read(n): return json.loads((ROOT/'dades'/n).read_text())
R=read('recursos.json'); S=read('series.json'); E=read('episodis.json'); ST=read('resum-revisio.json')
BY={r['id']:r for r in R}; SB={s['id']:s for s in S}; EB={e['id']:e for e in E}
ALIASES=read('aliases.json'); DATE=ST['data']; VERSION=ST['versio']
STAT={
 'recurrents':'Repartiment recurrent documentat',
 'mascotes_recurrents':'Mascotes o figures recurrents',
 'conte_recurrents':'Conté programes amb personatges recurrents',
 'narratius_recurrencia_no_confirmada':'Narració; recurrència no confirmada',
 'repositori_per_desglossar':'Repositori: cal revisar cada material',
 'pendent_acces':'Contingut no recuperat',
 'pendent_material':'Material intern pendent de revisió',
 'no_identificats_fitxa':'No identificats a la fitxa principal'
}
FSTAT={'recurrent':'Recurrència documentada','mascota_recurrent':'Figura recurrent en diversos materials','no_confirmada':'Recurrència entre històries no confirmada'}
def clean(x): return str(x or '').replace(' — ',' · ').replace('«','“').replace('»','”')
def txt(x): return H(clean(x))
def slug(s):
    t=''.join(c for c in unicodedata.normalize('NFD',s.lower()) if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+','-',t).strip('-')
def link(u,label): return f'<a href="{H(u,quote=True)}">{txt(label)}</a>'
def ul(items): return '<ul>'+''.join('<li>'+i+'</li>' for i in items)+'</ul>'
def badge(status): return f'<span class="badge {status}">{txt(STAT.get(status,FSTAT.get(status,status)))}</span>'
def note(s): return '<aside class="info"><p>'+txt(s)+'</p></aside>'
def table(headers,rows,caption):
    return '<div class="table-wrap" role="region" aria-label="'+H(caption,quote=True)+'" tabindex="0"><table><caption>'+txt(caption)+'</caption><thead><tr>'+''.join('<th scope="col">'+txt(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(c)+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'

for f in ['assets','recursos','paisos','capitols','odissea']:
    d=ROOT/f
    if f!='assets' and d.exists(): shutil.rmtree(d)
    d.mkdir(exist_ok=True)

CSS="""
:root{--bg:#fff;--text:#3f3f3f;--heading:#477a57;--muted:#5c635f;--line:#dce5dd;--pale:#f4f8f4;--focus:#9a4200;--info:#f1f7fc}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#fff;color:var(--text);font:1rem/1.65 'Segoe UI',Arial,sans-serif}a{color:#255f3a;text-decoration-thickness:1px;text-underline-offset:.18em}a:hover{color:#133e23}a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible,[tabindex]:focus-visible{outline:3px solid var(--focus);outline-offset:4px}h1,h2,h3,h4{color:var(--heading);line-height:1.25;font-weight:500;overflow-wrap:anywhere}h1{font-size:clamp(2rem,4vw,3.45rem);max-width:24ch;margin:.4em 0}h2{font-size:1.65rem;margin:1.8rem 0 .8rem}h3{font-size:1.18rem}h4{font-size:1.1rem}p{margin:.6em 0 1em}small,.secondary{color:var(--muted)}.container{width:min(1180px,calc(100% - 48px));margin-inline:auto}.site-header{border-bottom:1px solid var(--line);background:white}.header-inner{display:flex;justify-content:space-between;gap:24px;align-items:center;padding-block:18px}.brand{font-size:.85rem;font-weight:700;letter-spacing:.08em;text-decoration:none}.mainnav{display:flex;gap:20px;flex-wrap:wrap;font-size:.9rem}.skip{position:absolute;left:12px;top:-100px;background:#fff;padding:12px;z-index:5}.skip:focus{top:6px}.hero{background:var(--pale);padding:46px 0 38px;border-bottom:1px solid var(--line)}.eyebrow{text-transform:uppercase;letter-spacing:.13em;font-size:.76rem;font-weight:600;color:#477052}.lead{font-size:1.13rem;max-width:76ch}.hero-caps{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}.hero-caps span,.pill{background:white;border:1px solid var(--line);padding:5px 12px;border-radius:99px;font-size:.85rem}.main{padding-block:26px 60px}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin-block:20px}.card{border:1px solid var(--line);border-radius:12px;padding:22px;background:#fff;display:flex;flex-direction:column;gap:7px;min-width:0}.card h2,.card h3{font-size:1.18rem;margin:0 0 4px}.card p{font-size:.94rem;margin:0 0 8px}.card .action{margin-top:auto;padding-top:10px}.meta{font-size:.8rem;color:var(--muted)}.badge{display:inline-block;border:1px solid #d4ded6;border-radius:7px;padding:3px 8px;font-size:.77rem;line-height:1.4;color:#38473d;background:#f5f8f5;align-self:flex-start}.recurrents,.recurrent{background:#e9f6ea;border-color:#bad5bd}.mascotes_recurrents,.mascota_recurrent{background:#eef5fa;border-color:#caddea}.pendent_acces{background:#fff5eb;border-color:#e5d2c2}.info{padding:14px 20px;background:var(--info);border-left:6px solid #4b97d1;border-radius:12px;margin-block:20px}.info p:last-child{margin-bottom:0}.controls{padding:24px;background:#f8faf8;border:1px solid var(--line);border-radius:12px;margin-block:24px}.controls-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.control label{display:block;font-size:.87rem;font-weight:600;margin-bottom:5px}input,select,button{font:inherit}input,select{width:100%;min-height:44px;border:1px solid #aebbb1;border-radius:6px;background:#fff;padding:8px 10px;color:#3f3f3f}.searchfield{grid-column:1/-1}.filter-bottom{display:flex;gap:18px;align-items:center;justify-content:space-between;margin-top:16px}button{padding:8px 15px;background:white;color:#255f3a;border:1px solid #8ca792;border-radius:7px;cursor:pointer}details{background:#f8f9fa;border:1px solid #dee2e6;border-radius:8px;margin:12px 0}summary{cursor:pointer;padding:13px 16px;font-weight:600;color:#303a33}details>div{padding:0 18px 18px}details[open]>summary{border-bottom:1px solid #dee2e6;margin-bottom:12px}.table-wrap{max-width:100%;overflow-x:auto;margin:18px 0}table{width:100%;border-collapse:collapse;font-size:.9rem}caption{text-align:left;font-weight:600;color:#477a57;padding-bottom:8px}th,td{padding:12px 14px;border:1px solid #dce5dd;vertical-align:top;overflow-wrap:anywhere}th{background:#f4f8f4;text-align:left}dl{display:grid;grid-template-columns:minmax(130px,180px) minmax(0,1fr);gap:9px 16px}dt{font-weight:600}dd{margin:0}footer{border-top:1px solid var(--line);padding:26px 0;font-size:.82rem;color:var(--muted)}.breadcrumbs{font-size:.85rem;margin-bottom:20px}.topic-list{display:flex;gap:6px;flex-wrap:wrap}.topic-list span{font-size:.77rem;border:1px solid #dde5df;padding:2px 7px;border-radius:5px}.family{border-top:1px solid var(--line);padding-top:16px;margin-top:26px}.episode-source{font-size:.83rem;overflow-wrap:anywhere}.chapter-nav{display:flex;justify-content:space-between;gap:22px;border-top:1px solid var(--line);padding-top:18px;margin-top:28px}.toc{columns:2;column-gap:42px}.toc li{break-inside:avoid;margin-bottom:8px}.book-header{padding:35px 0;border-bottom:1px solid var(--line)}.book{width:min(1040px,calc(100% - 48px));margin:auto}.book-chapter{padding:20px 0 35px;border-top:2px solid #dce5dd;margin-top:36px}.book-resource{padding-top:16px;margin-top:28px;border-top:1px solid #dce5dd}.book-back{font-size:.85rem}.backline{margin-bottom:15px}.empty{padding:25px;border:1px solid var(--line);border-radius:8px}.print-note{font-size:.85rem;color:var(--muted)}[hidden]{display:none!important}@media(max-width:850px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}.header-inner{align-items:flex-start;flex-direction:column;gap:10px}.controls-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:560px){.container,.book{width:calc(100% - 32px)}.grid,.controls-grid{grid-template-columns:minmax(0,1fr)}.hero{padding-block:30px}.mainnav{gap:10px 16px}.card{padding:18px}.controls{padding:18px}.toc{columns:1}dl{grid-template-columns:1fr;gap:2px}dd{margin-bottom:10px}.hero-caps{gap:7px}th,td{padding:9px}.filter-bottom{align-items:flex-start;flex-direction:column}.chapter-nav{font-size:.85rem}.searchfield{grid-column:auto}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}@media print{.site-header,.controls,.skip,.chapter-nav,.book-back,.backline{display:none!important}body{font-size:10pt}.container,.book{width:100%}.hero{background:#fff;padding:0 0 15px}.grid{display:block}.card,details{break-inside:avoid;margin-bottom:12px}details>div{display:block!important}details>summary{list-style:none}a{color:#1d4d2d}.book-chapter{break-before:page}h1,h2,h3,h4{break-after:avoid}.table-wrap{overflow:visible}table{font-size:9pt}}
"""
(ROOT/'assets/estils.css').write_text(CSS)
JS="""(() => {
  const panel=document.querySelector('[data-catalogue]'); if(!panel)return;
  const fields=[...panel.querySelectorAll('[data-filter]')];
  const cards=[...document.querySelectorAll('[data-resource]')];
  const count=document.getElementById('result-count'), empty=document.getElementById('no-results');
  const norm=s=>s.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLocaleLowerCase('ca');
  function apply(){let n=0;for(const card of cards){let ok=fields.every(f=>!f.value||(f.dataset.filter==='search'?norm(card.dataset.search).includes(norm(f.value)):(card.dataset[f.dataset.filter]||'').split('|').includes(f.value)));card.hidden=!ok;if(ok)n++;}count.textContent=`${n} de ${cards.length} fitxes`;empty.hidden=n!==0;}
  for(const f of fields)f.addEventListener(f.type==='search'?'input':'change',apply);
  document.getElementById('reset-filters').addEventListener('click',()=>{fields.forEach(f=>f.value='');apply();document.getElementById('free-search').focus();});
  panel.hidden=false;apply();
})();
"""
(ROOT/'assets/filtres.js').write_text(JS)

def shell(title,body,depth=0,active='',script=False):
    p='../'*depth
    nav=[('cataleg.html','Catàleg'),('personatges.html','Personatges'),('episodis.html','Episodis'),('capitols/09-index-geografic.html','Països'),('capitols/10-metodologia.html','Fonts i criteris')]
    return '<!DOCTYPE html>\n<html lang="ca"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>'+txt(title)+' · Atles de benestar digital</title><link rel="stylesheet" href="'+p+'assets/estils.css">'+('<script defer src="'+p+'assets/filtres.js"></script>' if script else '')+'</head><body><a class="skip" href="#contingut">Salta al contingut</a><header class="site-header"><div class="container header-inner"><a class="brand" href="'+p+'index.html">ATLES · BENESTAR DIGITAL</a><nav class="mainnav" aria-label="Navegació principal">'+''.join('<a href="'+p+u+'"'+(' aria-current="page"' if u==active else '')+'>'+label+'</a>' for u,label in nav)+'</nav></div></header><main id="contingut">'+body+'</main><footer><div class="container">Versió '+VERSION+' · Revisió: 17 d’octubre de 2026. Les propostes d’aula són de l’Atles. Fonts originals enllaçades, sense redistribució dels seus materials.</div></footer></body></html>'
def hero(title,lead='',caps=None):
    return '<section class="hero"><div class="container"><p class="eyebrow">Atles internacional · edició '+VERSION+'</p><h1>'+txt(title)+'</h1>'+('<p class="lead">'+txt(lead)+'</p>' if lead else '')+('<div class="hero-caps">'+''.join('<span>'+txt(x)+'</span>' for x in caps)+'</div>' if caps else '')+'</div></section>'

native_names={r['id']:f'12_{i:03}_{r["id"]}_sub.html' for i,r in enumerate(R,1)}
native_ch_names={
 'orient':'01_orientacions.html','person':'02_personatges.html','epis':'03_episodis.html','prim':'04_infantil_primaria.html','sec':'05_secundaria.html','batx':'06_batxillerat_fp.html','uni':'07_universitat.html','doc':'08_formacio_docent.html','fam':'09_families.html','geo':'10_paisos_organismes.html','met':'11_fonts_criteris.html','catalog':'12_cataleg.html'}
def rh(rid,mode='site',depth=0):
    rid=ALIASES.get(rid,rid)
    return native_names[rid] if mode=='native' else '../'*depth+'recursos/'+rid+'.html'
def ch(key,mode='site',depth=0):
    sm={'orient':'capitols/01-com-utilitzar.html','person':'personatges.html','epis':'episodis.html','prim':'capitols/02-primaria.html','sec':'capitols/03-secundaria.html','batx':'capitols/04-batxillerat-fp.html','uni':'capitols/05-universitat.html','doc':'capitols/06-formacio-docent.html','fam':'capitols/07-families.html','geo':'capitols/09-index-geografic.html','met':'capitols/10-metodologia.html','catalog':'cataleg.html'}
    return native_ch_names[key] if mode=='native' else '../'*depth+sm[key]

def epbody(e):
    cast=', '.join(e['personatges']) or 'No concretats individualment a la font consultada.'
    return '<p class="secondary">'+txt(e.get('titol_estat','Títol identificat a la font original.'))+'</p><dl><dt>Personatges documentats</dt><dd>'+txt(cast)+'</dd><dt>Situació o conflicte</dt><dd>'+txt(e['conflicte_documentat'])+'</dd><dt>Aprenentatge documentat</dt><dd>'+txt(e['aprenentatge_documentat'])+'</dd><dt>Abast de la revisió</dt><dd>'+txt(e['abast_verificacio'])+'</dd><dt>Material docent</dt><dd>'+txt(e['guia_estat'])+(' · '+link(e['guia_url'],'Pàgina o document docent') if e['guia_url'] else '')+'</dd><dt>Avaluació</dt><dd>'+txt(e['avaluacio_estat'])+'</dd></dl><p class="episode-source">'+link(e['font'],'Font original')+(' · '+txt(e['localitzador']) if e['localitzador'] else '')+' · Consulta: '+DATE+'</p><p><strong>Proposta de l’Atles:</strong> '+txt(e['proposta_atles'])+'</p>'

def chartable(chars):
    if not chars:return '<p>La font acredita ficció, però no s’ha pogut establir un repartiment individual verificable.</p>'
    return table(['Personatge o figura','Funció documentada','Recurrència individual','Evidència'],[(txt(c['nom']),txt(c['rol']),txt(c['recurrencia']),link(c['font'],c['localitzador'])) for c in chars],'Personatges i funcions segons les fonts')

def resource_body(r,mode='site',depth=1,heading=2):
    sub=f'h{heading}'; rid=r['id']
    out='<p>'+badge(r['personatges_estat'])+'</p><p class="lead">'+txt(r['descripcio'])+'</p>'
    out+='<dl>'+''.join('<dt>'+label+'</dt><dd>'+value+'</dd>' for label,value in [
        ('País o organisme',txt(r['pais_organisme'])),('Entitat',txt(r['entitat'])),('Etapa',txt(' · '.join(r['etapes']))),('Destinataris',txt(r['edat'])),('Llengües',txt(r['idiomes'])),('Formats',txt(' · '.join(r['tipus']))),('Accés',txt(r['format_acces']))])+'</dl>'
    out+='<p>'+link(r['enllac_original'],'Consulta el recurs original')+'</p>'
    out+=f'<{sub}>Personatges i recurrència</{sub}><p>'+txt(r['personatges_observacions'])+'</p>'
    if r['series_ids']:
        out+=ul([link(ch('person',mode,depth)+'#serie-'+sid,SB[sid]['titol']) for sid in r['series_ids']])
    if r['personatges_fitxa']:out+=chartable(r['personatges_fitxa'])
    if r['episodis_ids']:
        out+=f'<{sub}>Episodis i activitats documentats</{sub}><p class="secondary">Les peces es compten una sola vegada al registre general, encara que s’enllacin des de diverses fitxes.</p>'
        for eid in r['episodis_ids']:
            e=EB[eid]
            out+='<details><summary>'+txt(e['titol'])+' <span class="meta">· '+txt(e['tipus'])+'</span></summary><div>'+epbody(e)+'<p>'+link(ch('epis',mode,depth)+'#ep-'+eid,'Ves al registre únic')+'</p></div></details>'
    out+=f'<{sub}>Orientacions pedagògiques</{sub}><dl><dt>Guia o suport docent</dt><dd>'+txt(r['detall'].get('guia','No verificada'))+'</dd><dt>Rúbrica</dt><dd>'+txt(r['detall'].get('rubrica','No verificada'))+'</dd></dl>'
    if r['detall'].get('guia_url'): out+='<p>'+link(r['detall']['guia_url'],'Consulta les orientacions docents')+'</p>'
    out+='<p><strong>Proposta de l’Atles:</strong> '+txt(r['aplicacio'])+'</p>'
    out+=f'<{sub}>Temes</{sub}><div class="topic-list">'+''.join('<span>'+txt(t)+'</span>' for t in r['tematiques'])+'</div><p class="secondary">'+txt(r['tematiques_estat'])+'</p>'
    out+=f'<{sub}>Font, ús i límits</{sub}><p>'+txt(r['verificacio'])+'</p><p>'+txt(r['advertiment'])+'</p><p><strong>Drets d’ús:</strong> '+txt(r['llicencia'])+'</p>'
    return out

def listing(subset,mode='site',depth=0):
    return table(['Recurs','País o organisme','Personatges'],[(link(rh(r['id'],mode,depth),r['titol_original']),txt(r['pais_organisme']),badge(r['personatges_estat'])) for r in subset],'Recursos seleccionats') if subset else '<p>No hi ha cap fitxa específica d’aquesta etapa en la selecció actual.</p>'

def orientations(mode='site',depth=0):
    return '<p>L’Atles ajuda a escollir recursos internacionals per treballar el benestar i la ciutadania digitals. Combina sèries, relats, jocs, guies i marcs de treball.</p>'+note('Un personatge identificat en una història no és necessàriament recurrent. Una guia, una activitat de reflexió i una rúbrica tampoc són equivalents.')+'<h3>Com seleccionar un recurs</h3>'+ul(['Concretar l’objectiu: descans, atenció, relacions, seguretat, privacitat o participació.','Comprovar l’etapa, la llengua i l’accés al material original.','Llegir la fitxa i l’evidència de recurrència, si es vol treballar amb un fil narratiu estable.','Adaptar els exemples al grup i contrastar les orientacions que depenen del context del país.','Valorar què aporta el recurs a les dimensions física, emocional, social i cognitiva, sense confondre una etiqueta temàtica amb una prova d’eficàcia.'])+'<h3>Entrades de lectura</h3>'+ul([link(ch('person',mode,depth),'Personatges i famílies narratives'),link(ch('epis',mode,depth),'Episodis, històries i activitats'),link(ch('geo',mode,depth),'Països i organismes'),link(ch('met',mode,depth),'Fonts, criteris i límits de la recerca'),link(ch('catalog',mode,depth),'Catàleg de recursos')])

def characters(mode='site',depth=0):
    out=note('Hi ha 17 famílies o conjunts narratius examinats: 14 tenen un nucli o una figura recurrent documentats i 3 mantenen la recurrència entre històries sense confirmar. Les mascotes i les personificacions s’identifiquen explícitament.')
    out+=table(['Programa','Origen','Tipus','Conclusió'],[(link('#serie-'+s['id'],s['titol']),txt(s['pais_organisme']),txt(s['tipologia']),txt(FSTAT[s['recurrencia_estat']])) for s in S],'Resultats de la revisió de recurrència')
    for s in S:
        out+='<section class="family" id="serie-'+s['id']+'"><h3>'+txt(s['titol'])+'</h3><p class="meta">'+txt(s['pais_organisme'])+' · '+txt(FSTAT[s['recurrencia_estat']])+'</p><p>'+txt(s['resum'])+'</p>'+chartable(s['personatges'])+'<p>'+txt(s['notes'])+'</p>'
        if s['total_declarat'] is not None:out+='<p><strong>Inventari declarat per la font:</strong> '+txt(s['total_declarat'])+'. <strong>Registres descrits a l’Atles:</strong> '+str(sum(e['serie_id']==s['id'] for e in E))+'. Els dos recomptes poden correspondre a unitats diferents.</p>'
        out+=ul([link(rh(rid,mode,depth),BY[rid]['titol_original']) for rid in s['recursos_ids'] if rid in BY])+'</section>'
    return out

def episode_chapter(mode='site',depth=0):
    out='<p>56 registres únics. S’hi diferencien episodis, històries, situacions, lliçons, jocs i activitats. No tots són vídeos ni tots contenen una trama completa.</p>'+note('Cada entrada indica què s’ha consultat: text original, guia docent o sinopsi. Els aprenentatges de la font i les propostes de l’Atles apareixen separats. Els vídeos no s’han visionat íntegrament.')
    out+=ul([link('#grup-'+s['id'],s['titol']+' ('+str(sum(e['serie_id']==s['id'] for e in E))+')') for s in S if any(e['serie_id']==s['id'] for e in E)])
    for s in S:
        es=[e for e in E if e['serie_id']==s['id']]
        if not es:continue
        out+='<section id="grup-'+s['id']+'"><h3>'+txt(s['titol'])+'</h3>'
        for e in es:out+='<details id="ep-'+e['id']+'"><summary>'+txt(e['titol'])+' <span class="meta">· '+txt(e['tipus'])+'</span></summary><div>'+epbody(e)+'</div></details>'
        out+='</section>'
    return out

def geography(mode='site',depth=0):
    countries=sorted({r['pais_organisme'] for r in R if 'Internacional' not in r['pais_organisme'] and r['pais_organisme'] not in ['Consell d’Europa','Unió Europea']})
    orgs=sorted(set(r['pais_organisme'] for r in R)-set(countries))
    out='<p>La selecció inclou <strong>24 països i 6 etiquetes d’organismes internacionals</strong>. Els organismes no s’afegeixen al recompte de països. El registre de 249 entrades ISO és un instrument de seguiment, no una investigació mundial acabada.</p>'
    for label,tags in [('Països',countries),('Organismes internacionals',orgs)]:
        out+='<h3>'+label+'</h3>'
        for country in tags:
            sub=[r for r in R if r['pais_organisme']==country]
            if mode=='native':out+='<details><summary>'+txt(country)+' · '+str(len(sub))+' fitxes</summary><div>'+listing(sub,mode,depth)+'</div></details>'
            else:out+='<p>'+link('../'*depth+'paisos/'+slug(country)+'.html',country)+' · '+str(len(sub))+' fitxes</p>'
    return out

def methodology(mode='site',depth=0):
    out='<h3>Abast real de la revisió 0.13</h3><p>S’ha intentat recuperar de nou la font principal de les 76 fitxes heretades. S’ha fusionat un duplicat de Better Internet for Kids i s’hi han incorporat 9 fitxes. El catàleg resultant té 84 recursos. La lectura detallada s’ha concentrat en els materials narratius i en les afirmacions sobre personatges, episodis i suport docent.</p>'+note('Aquesta és una revisió completa de les fitxes del corpus a nivell de font principal, amb aprofundiment narratiu i ampliació internacional dirigida. No equival a haver llegit tots els annexos, visionat tots els vídeos ni investigat exhaustivament tots els països.')
    out+='<h3>Com es determina la recurrència</h3>'+ul(['Una font primària declara un repartiment estable, o el mateix personatge està identificat en més d’una història o format.','S’anota per separat la presència puntual, el repartiment recurrent, la mascota i la personificació d’un concepte.','Un programa amb diverses edicions no acredita per si sol la continuïtat del repartiment.','Un nom d’autor, un presentador real o un lloc on transcorre la ficció no es converteixen en personatge o país productor.','L’absència d’un nom a la portada i les cerques sense resultats no acrediten que el material no contingui personatges.'])
    out+='<h3>Nivells d’evidència</h3>'+table(['Nivell','Què permet afirmar','Límit'],[('Text original llegit','Accions i personatges dels passatges indicats.','No equival a haver visionat les adaptacions.'),('Guia o sinopsi oficial','Objectius, premissa i dades explícites.','No s’hi afegeixen diàlegs ni desenllaços.'),('Portada o catàleg','Tipus de recurs i materials anunciats.','No acredita el contingut complet dels annexos.'),('Contingut no recuperat','Constància de l’intent.','No permet afirmar absència de personatges.')],'Criteris de lectura de les fonts')
    out+='<h3>Correccions que afecten la lectura pedagògica</h3>'+ul(['HTML Heroes: incorporats Ruby i Archie i distingides les edicions de 1st–2nd i 3rd–4th Class.','ZigZaga na Net: contrastat el llibre original; títols de la v0.12 no localitzats en aquesta edició retirats de les fitxes actives.','SeguraNet: Pisca i Luzinha confirmats com a mascotes al joc; Pisca també té una col·lecció de relats.','Common Sense: vinculats els rols a cada lliçó; Head treballa verificació a la lliçó específica i curiositat i autoria a la presentació general.','Hector’s World: mantinguts els set episodis i temes acreditats per Netsafe; repartiment secundari i títols individuals no reconfirmats retirats de la presentació activa.','MediaSmarts: guia docent i rúbriques dels Ontario Textbooks acreditades a les fonts oficials; figura House Hippo identificada a la campanya Break the Fake.','Sud-àfrica i Singapur: es confirma la presència de ficció, però no s’inventa recurrència entre volums o edicions.'])
    out+='<h3>Accés i recerca pendent</h3>'+ul(['Always ON: no s’ha recuperat l’URL exacta heretada; no s’ha substituït per un fullet amb un títol semblant.','Ceibal: no s’han recuperat la seqüència REA ni la pàgina institucional facilitada. Sí que s’han llegit les presentacions públiques dels tres cursos EDUx.','Hector’s World: la portada específica no ha ofert contingut llegible; la informació activa prové de Netsafe.','Cyber Ninjas: el PDF gràfic no ha permès una lectura verificable; noms i arguments no s’han completat.','Digiduck: candidat localitzat en la informació indexada de Childnet; accés directe fallit. Es manté fora del catàleg contrastat.','La consulta de recursos de Dinamarca ha estat intermitent; no es declara lectura completa de les descàrregues.'])
    out+='<h3>Com s’ha ampliat la recerca internacional</h3><p>S’han combinat les fonts oficials ja presents amb cerques dirigides en anglès i llengües d’origen. S’han incorporat programes d’Austràlia, Portugal, Polònia, Brasil, Sud-àfrica, Armènia, Singapur i l’ITU. Les cerques al Japó no han produït una fitxa nacional prou contrastada; això no indica que no existeixin recursos. No s’han cobert amb el mateix detall tots els territoris d’Àfrica o Àsia.</p>'
    out+='<h3>Registre de totes les fitxes</h3><p>La columna de personatges expressa una conclusió amb un abast limitat; no és una certificació d’absència en tots els materials.</p>'
    out+=table(['Fitxa','Font principal','Personatges'],[(link(rh(r['id'],mode,depth),r['titol_original']),link(r['enllac_original'],r['entitat']),badge(r['personatges_estat'])) for r in R],'Fonts principals revisades')
    out+='<h3>Drets i criteri d’ús</h3><p>L’Atles conté descripcions i propostes pròpies i enllaça els materials originals. No redistribueix vídeos, il·lustracions, còmic ni guies d’altres entitats. “Públic” o “gratuït” no significa que es pugui modificar o reproduir qualsevol material. La llengua, els drets i la pertinència per al grup s’han de revisar en el recurs concret.</p>'
    return out

STAGES=[('prim','Educació infantil i primària',['Educació infantil','Primària']),('sec','Secundària obligatòria',['Secundària obligatòria']),('batx','Batxillerat i formació professional',['Batxillerat i FP']),('uni','Universitat',['Universitat']),('doc','Formació docent i centre',['Formació docent']),('fam','Famílies i comunitat',['Famílies i comunitat'])]
CHAPTERS=[('orient','Com utilitzar l’Atles',orientations),('person','Personatges i recurrència',characters),('epis','Episodis, històries i activitats',episode_chapter)]
for key,title,stages in STAGES:
    def stagebody(mode='site',depth=0,stages=stages):
        subset=[r for r in R if set(r['etapes'])&set(stages)]
        return '<p>Les etapes són una orientació per a la selecció. La correspondència amb cursos i edats d’altres països s’ha de contrastar a cada fitxa.</p>'+listing(subset,mode,depth)
    CHAPTERS.append((key,title,stagebody))
CHAPTERS += [('geo','Països i organismes',geography),('met','Fonts, criteris i límits',methodology),('catalog','Catàleg complet',lambda mode='site',depth=0:listing(R,mode,depth))]

# Fitxes i pàgines del catàleg autònom.
for r in R:
    body=hero(r['titol_original'],r['pais_organisme']+' · '+r['entitat'])+'<div class="container main"><p class="breadcrumbs">'+link('../cataleg.html','Catàleg')+' / '+txt(r['titol_original'])+'</p>'+resource_body(r)+'</div>'
    (ROOT/'recursos'/f'{r["id"]}.html').write_text(shell(r['titol_original'],body,1))
for old,new in ALIASES.items():
    (ROOT/'recursos'/f'{old}.html').write_text(shell('Fitxa unificada',hero('Fitxa unificada')+'<div class="container main"><p>Aquest recurs duplicava una fitxa del mateix material.</p><p>'+link(new+'.html','Continua a la fitxa vigent')+'</p></div>',1))

chapter_sitepaths={'orient':'01-com-utilitzar','prim':'02-primaria','sec':'03-secundaria','batx':'04-batxillerat-fp','uni':'05-universitat','doc':'06-formacio-docent','fam':'07-families','geo':'09-index-geografic','met':'10-metodologia'}
for i,(key,title,fn) in enumerate(CHAPTERS):
    if key=='catalog':continue
    depth=1 if key in chapter_sitepaths else 0
    path=ROOT/'capitols'/f'{chapter_sitepaths[key]}.html' if depth else ROOT/('personatges.html' if key=='person' else 'episodis.html')
    nav='<nav class="chapter-nav" aria-label="Capítols">'+(link(ch(CHAPTERS[i-1][0],depth=depth),'Anterior: '+CHAPTERS[i-1][1]) if i else '<span></span>')+(link(ch(CHAPTERS[i+1][0],depth=depth),'Següent: '+CHAPTERS[i+1][1]) if i+1<len(CHAPTERS) else '')+'</nav>'
    path.write_text(shell(title,hero(title)+'<div class="container main">'+fn(depth=depth)+nav+'</div>',depth,active=('personatges.html' if key=='person' else 'episodis.html' if key=='epis' else 'capitols/10-metodologia.html' if key=='met' else '')))
(ROOT/'capitols/08-organismes.html').write_text(shell('Organismes internacionals',hero('Organismes internacionals')+'<div class="container main">'+listing([r for r in R if 'Internacional' in r['pais_organisme'] or r['pais_organisme'] in ['Unió Europea','Consell d’Europa']],depth=1)+'</div>',1))
for country in sorted({r['pais_organisme'] for r in R}):
    sub=[r for r in R if r['pais_organisme']==country]
    (ROOT/'paisos'/f'{slug(country)}.html').write_text(shell(country,hero(country,'Selecció de fonts; no inventari exhaustiu del territori o organisme.')+'<div class="container main">'+listing(sub,depth=1)+'</div>',1))

def options(field,values):return ''.join('<option value="'+H(v,quote=True)+'">'+txt(v)+'</option>' for v in values)
filters=[('country','País o organisme',sorted({r['pais_organisme'] for r in R})),('stage','Etapa',sorted({s for r in R for s in r['etapes']})),('topic','Tema',sorted({s for r in R for s in r['tematiques']})),('type','Format',sorted({s for r in R for s in r['tipus']})),('characters','Personatges i evidència',list(STAT))]
panel='<section class="controls" data-catalogue hidden aria-label="Cerca i filtres"><h2>Troba el recurs</h2><div class="controls-grid"><div class="control searchfield"><label for="free-search">Títol, entitat, personatge o paraula clau</label><input type="search" id="free-search" data-filter="search" placeholder="Ex.: Coni, descans, privacitat, Pisca"></div>'
for field,label,values in filters:
    panel+='<div class="control"><label for="filter-'+field+'">'+label+'</label><select id="filter-'+field+'" data-filter="'+field+'"><option value="">Tots</option>'+(''.join('<option value="'+v+'">'+txt(STAT[v])+'</option>' for v in values) if field=='characters' else options(field,values))+'</select></div>'
panel+='</div><div class="filter-bottom"><p id="result-count" role="status" aria-live="polite"></p><button type="button" id="reset-filters">Neteja els filtres</button></div></section>'
cards=''
for r in R:
    data={'country':r['pais_organisme'],'stage':'|'.join(r['etapes']),'topic':'|'.join(r['tematiques']),'type':'|'.join(r['tipus']),'characters':r['personatges_estat'],'search':' '.join([r['titol_original'],r['entitat'],r['pais_organisme'],r['descripcio']]+[c['nom'] for c in r['personatges_fitxa']])}
    cards+='<article class="card" data-resource="'+r['id']+'" '+ ' '.join('data-'+k+'="'+H(v,quote=True)+'"' for k,v in data.items())+'><p class="meta">'+txt(r['pais_organisme'])+' · '+txt(' / '.join(r['etapes']))+'</p><h2>'+link(rh(r['id']),r['titol_original'])+'</h2>'+badge(r['personatges_estat'])+'<p>'+txt(r['descripcio'])+'</p><p class="action">'+link(rh(r['id']),'Obre la fitxa')+'</p></article>'
(ROOT/'cataleg.html').write_text(shell('Catàleg de recursos',hero('Recursos per al benestar digital','Cerca per etapa, tema, país, format i evidència sobre personatges.',[f'{len(R)} fitxes',f'{ST["paisos"]} països + {ST["organismes"]} organismes','Fonts i límits a cada fitxa'])+'<div class="container main">'+panel+'<noscript><p>Les fitxes són totes visibles. Es pot utilitzar la cerca del navegador o els índexs d’etapes i països.</p></noscript><p id="no-results" class="empty" hidden>No hi ha fitxes amb aquesta combinació de filtres.</p><div class="grid">'+cards+'</div></div>',active='cataleg.html',script=True))

home=hero('Atles internacional de benestar digital','Històries, personatges i recursos educatius per escollir amb criteri què es treballa a l’aula.',[f'{len(R)} recursos',f'{ST["families_recurrents"]} famílies amb figures recurrents',f'{len(E)} registres narratius únics'])
home+='<div class="container main"><div class="grid">'
for title,desc,path in [('Escollir un recurs','Etapa, llengua, format, temes i evidència.','cataleg.html'),('Seguir un personatge','Repartiments, mascotes i presències puntuals.','personatges.html'),('Treballar una història','Conflicte, aprenentatge i font de cada peça.','episodis.html')]:
    home+='<article class="card"><h2>'+link(path,title)+'</h2><p>'+desc+'</p></article>'
home+='</div><h2>Una lectura internacional amb fonts explícites</h2><p>La selecció inclou programes d’Europa, Amèrica, Oceania, Àfrica i Àsia, a més d’organismes internacionals. No tots els territoris tenen el mateix grau de cobertura.</p>'+note('La versió 0.13 revisa les 76 fitxes anteriors, fusiona un duplicat i incorpora 9 recursos. Diferencia què diu la font, què proposa l’Atles i què continua sense verificar.')+'<h2>Camins de lectura</h2>'+ul([link(ch(k),t) for k,t,_ in CHAPTERS if k!='catalog'])+'<h2>Lectura en un sol document</h2><p>'+link('Atles_internacional_benestar_digital_v0.13.html','Obre el llibre HTML complet')+'</p></div>'
(ROOT/'index.html').write_text(shell('Atles internacional de benestar digital',home))

provided=list(csv.DictReader((ROOT/'dades/urls-aportades.csv').open(encoding='utf-8-sig')))
(ROOT/'fonts-aportades.html').write_text(shell('Fonts aportades',hero('Fonts aportades')+'<div class="container main">'+table(['Font','Adreça facilitada','Resultat actual','Fitxa'],[(txt(x['font']),link(x['url_original'],'Font aportada'),txt(x['estat_validacio']),link(x['fitxa_local'],'Fitxa relacionada')) for x in provided],'Revisió de les set fonts aportades')+'</div>'))

# HTML d’importació de capítols. No scripts, formularis, estils externs ni límits d’amplada globals.
inline_map={'h2':'color:#477a57;font-weight:400;line-height:1.3;margin:24px 0 16px;', 'h3':'color:#477a57;font-size:1.1rem;line-height:1.3;margin:22px 0 12px;', 'p':'margin:0 0 14px;', 'a':'color:#255f3a;text-decoration:underline;', 'details':'background:#f8f9fa;border:1px solid #dee2e6;border-radius:8px;margin:12px 0;', 'summary':'padding:12px 16px;cursor:pointer;color:#292929;line-height:1.5;', 'table':'width:100%;border-collapse:collapse;', 'th':'border:1px solid #dce5dd;padding:10px;text-align:left;vertical-align:top;background:#f4f8f4;', 'td':'border:1px solid #dce5dd;padding:10px;vertical-align:top;overflow-wrap:anywhere;', 'caption':'text-align:left;font-weight:600;margin-bottom:8px;', 'dt':'font-weight:600;margin-top:10px;', 'dd':'margin:0 0 10px;', 'aside':'background:#f1f7fc;border-left:6px solid #4b97d1;border-radius:12px;padding:16px 20px;margin:20px 0;'}
def inlined(content):
    root=LH.fragment_fromstring(content,create_parent='div')
    for el in root.iter():
        cls=el.get('class','')
        if el.tag in inline_map:el.set('style',inline_map[el.tag])
        if 'table-wrap' in cls:el.set('style','max-width:100%;overflow-x:auto;margin:16px 0;')
        if el.tag=='div' and el.getparent() is not None and el.getparent().tag=='details':el.set('style','padding:12px 16px;')
        for a in list(el.attrib):
            if a=='class' or a.startswith('data-'):del el.attrib[a]
    return ''.join(LH.tostring(e,encoding='unicode') for e in root)
def native_doc(title,content,anchor):
    return '<!DOCTYPE html><html lang="ca"><head><meta charset="utf-8"><title>'+txt(title)+'</title></head><body><section id="'+anchor+'"><h2 style="color:#477a57;font-weight:400;line-height:1.3;">'+txt(title)+'</h2>'+inlined(content)+'</section></body></html>'
anchors={}
for key,title,fn in CHAPTERS:
    name=native_ch_names[key];anchor='cap-'+key;anchors[name]=anchor
    (ROOT/'odissea'/name).write_text(native_doc(title,fn('native'),anchor))
for r in R:
    name=native_names[r['id']];anchor='rec-'+r['id'];anchors[name]=anchor
    (ROOT/'odissea'/name).write_text(native_doc(r['titol_original'],resource_body(r,'native',0,3),anchor))

bookparts=[]
for key,title,fn in CHAPTERS:
    name=native_ch_names[key]
    root=LH.fromstring((ROOT/'odissea'/name).read_text())
    content=root.find('body')[0]
    if key=='catalog':
        for r in R:
            rp=LH.fromstring((ROOT/'odissea'/native_names[r['id']]).read_text()).find('body')[0]
            rp.tag='article';rp.set('class','book-resource')
            # resource title becomes level 3; its subsections level 4 in the combined book.
            for el in rp.iter():
                if el.tag=='h3':el.tag='h4'
                elif el.tag=='h2':el.tag='h3'
            content.append(rp)
    content.set('class','book-chapter')
    back=LH.fromstring('<p class="book-back"><a href="#index-llibre">Torna a l’índex del llibre</a></p>');content.append(back)
    for a in content.xpath('.//a[@href]'):
        u=a.get('href');p=urlsplit(u)
        if p.scheme or p.netloc or not p.path:continue
        if p.path in anchors:a.set('href','#'+(p.fragment or anchors[p.path]))
    bookparts.append(LH.tostring(content,encoding='unicode'))
book='<!DOCTYPE html><html lang="ca"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Atles internacional de benestar digital · v0.13</title><style>'+CSS+'</style></head><body><a class="skip" href="#index-llibre">Salta a l’índex</a><main class="book"><header class="book-header"><p class="eyebrow">Edició 0.13 · 17 d’octubre de 2026</p><h1>Atles internacional de benestar digital</h1><p class="lead">Fonts, personatges i històries per escollir recursos educatius amb criteri.</p><p>84 fitxes · 24 països · 6 organismes · 14 famílies recurrents documentades</p></header><nav id="index-llibre" aria-label="Índex del llibre"><h2>Índex</h2><ol class="toc">'+''.join('<li>'+link('#cap-'+k,t)+'</li>' for k,t,_ in CHAPTERS)+'</ol></nav>'+''.join(bookparts)+'<footer>Atles v0.13 · Fonts consultades el '+DATE+'. Importació i visualització real a Odissea pendents de comprovació.</footer></main></body></html>'
(ROOT/'Atles_internacional_benestar_digital_v0.13.html').write_text(book)

readme='''# Atles internacional de benestar digital · versió 0.13

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
'''
(ROOT/'README.md').write_text(readme)
with zipfile.ZipFile(ROOT/'importacio-odissea-v0.13.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted((ROOT/'odissea').glob('*.html')):z.write(p,p.name)
print(json.dumps({'html_autonom':len(list(ROOT.glob('**/*.html'))),'fitxes':len(R),'families':len(S),'registres_narratius':len(E),'capitols_importacio':len(list((ROOT/'odissea').glob('*.html')))},ensure_ascii=False))
