#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build self-contained interactive time-line maps of the fallen (Hebrew + English).
Reads Database_enriched.csv, embeds data + Leaflet inline, writes into ../docs/:
  docs/oct7_map.html      (Hebrew UI)
  docs/oct7_map.en.html   (English UI)
Includes an always-on reference layer (Gaza border line + place labels) so the
map is legible even without online tiles.
"""
import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "Database_enriched.csv")
VENDOR = os.path.join(HERE, "vendor")
DOCS = os.path.normpath(os.path.join(HERE, "..", "docs"))
os.makedirs(DOCS, exist_ok=True)

LEAFLET_JS = open(os.path.join(VENDOR, "leaflet.js"), encoding="utf-8").read()
LEAFLET_CSS = open(os.path.join(VENDOR, "leaflet.css"), encoding="utf-8").read()
rows = list(csv.DictReader(open(SRC, encoding="utf-8")))

def num(x):
    try: return float(x)
    except: return None

hours = [int(num(r["Time"])) for r in rows if num(r["Time"]) is not None]
MAXH = max(hours)

recs, loc_agg = [], {}
for r in rows:
    lat, lon = num(r["Latitude"]), num(r["Longitude"])
    if lat is None or lon is None:
        continue
    t = num(r["Time"])
    hour = int(t) if t is not None else MAXH
    recs.append({
        "name": r["Name"], "lat": lat, "lon": lon, "hour": hour,
        "time_known": t is not None, "branch": r["Branch"],
        "joined": (r["Joined"] == "1"), "sof": (r["SOF"] == "1"),
        "age": r["Age"] or "", "loc": r["Location"], "loctype": r["Location_type"],
    })
    k = r["Location"]
    a = loc_agg.setdefault(k, {"loc": k, "lat": lat, "lon": lon, "n": 0})
    a["n"] += 1

# place labels for the reference layer: locations with >=4 fatalities
LABELS = sorted([v for v in loc_agg.values() if v["n"] >= 4],
                key=lambda x: -x["n"])
# approximate Gaza border polyline (N->S)
BORDER = [[31.585,34.519],[31.520,34.477],[31.430,34.398],[31.330,34.328],[31.226,34.266]]

# ---- localization ----------------------------------------------------------
L10N = {
 "he": {
  "dir":"rtl","lang":"he",
  "title":"מפת זמן — נופלי כוחות הביטחון ב‑7 באוקטובר 2023",
  "subtitle":"כל נקודה = מיקום נפילה. השתמשו במחוון או בכפתור ההפעלה כדי לעקוב, שעה אחר שעה, אחר התפרסות הלחימה.",
  "play":"▶ הפעל","pause":"⏸ עצור","cumulative":"מצטבר","colorby":"צבע לפי:",
  "opt_branch":"ענף","opt_wave":"גל (מוצב/מצטרף)","reflayer":"שכבת ייחוס",
  "fallen_until":"נפלו עד שעה זו","branch_filter":"סינון ענף",
  "hour_tpl":"שעה {H} מתחילת המתקפה  (≈ {C}:29)",
  "fallen_n":"{n} נופלים","of_joined":"מתוכם מצטרפים (גל 2)","of_sof":'מתוכם יחב"מ',
  "sof_mark":'יחב"מ',"hour_word":"שעה",
  "legend":"<b>מקרא:</b> גודל העיגול ∝ מספר הנופלים במיקום. צבע לפי הבחירה למעלה.",
  "note":('נכללים {N} נופלים בעלי קואורדינטות (2 ללא מיקום הושמטו). '
          'שעה = שעות מתחילת המתקפה (06:29). נופלים ללא שעה ידועה מוצגים בשעה {MAXH} ומסומנים "?". '
          'הגיל אותר ממקורות פתוחים — לבדיקה לפני פרסום.'),
  "branch":{"Military":"צבא","Police":"משטרה",
            "Emergency Response Team":"כיתת כוננות","Shin Bet":'שב"כ'},
  "switch":"English","switch_href":"oct7_map.en.html",
 },
 "en": {
  "dir":"ltr","lang":"en",
  "title":"Timeline map — fallen security personnel, October 7, 2023",
  "subtitle":"Each dot = a place where personnel fell. Use the slider or Play to watch the fighting spread, hour by hour.",
  "play":"▶ Play","pause":"⏸ Pause","cumulative":"Cumulative","colorby":"Color by:",
  "opt_branch":"Branch","opt_wave":"Wave (on-duty/joined)","reflayer":"Reference layer",
  "fallen_until":"Fallen by this hour","branch_filter":"Filter by branch",
  "hour_tpl":"Hour {H} of the attack  (≈ {C}:29)",
  "fallen_n":"{n} fallen","of_joined":"of them joiners (wave 2)","of_sof":"of them SOF",
  "sof_mark":"SOF","hour_word":"hour",
  "legend":"<b>Legend:</b> circle size ∝ number of fallen at the location. Color per selector above.",
  "note":('Includes {N} fallen with coordinates (2 without location omitted). '
          'Hour = hours since the attack began (06:29). Fallen with unknown time are shown at hour {MAXH}, marked "?". '
          'Ages were sourced from open sources — verify before publication.'),
  "branch":{"Military":"Military","Police":"Police",
            "Emergency Response Team":"Emergency Response Team","Shin Bet":"Shin Bet"},
  "switch":"עברית","switch_href":"oct7_map.html",
 },
}

TEMPLATE = """<!DOCTYPE html>
<html lang="@LANG@" dir="@DIR@">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>@TITLE@</title>
<style>
@LEAFLET_CSS@
:root{--ink:#1f2d3d;--accent:#1f4e79;}
*{box-sizing:border-box}
html,body{margin:0;height:100%;font-family:'Segoe UI',Arial,Helvetica,sans-serif;color:var(--ink)}
#app{display:flex;flex-direction:column;height:100vh}
header{background:#11212f;color:#fff;padding:10px 16px;display:flex;justify-content:space-between;align-items:center;gap:10px}
header h1{margin:0;font-size:18px}
header p{margin:2px 0 0;font-size:12px;color:#b9c6d2}
header a.lang{color:#9ad0ff;font-size:13px;text-decoration:none;white-space:nowrap}
#main{flex:1;display:flex;min-height:0}
#map{flex:1;background:#dfe7ee}
#side{width:300px;background:#f4f6f8;border-inline-start:1px solid #d9e0e6;padding:12px;overflow:auto;font-size:13px}
#controls{background:#1b2c3a;color:#fff;padding:10px 16px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
#controls button{background:var(--accent);color:#fff;border:0;border-radius:6px;padding:6px 12px;cursor:pointer;font-size:14px}
#controls button:hover{background:#2a63a0}
#slider{flex:1;min-width:200px}
.hourlab{font-variant-numeric:tabular-nums;font-weight:700;min-width:150px}
.statbig{font-size:30px;font-weight:800;color:var(--accent)}
.row{display:flex;justify-content:space-between;padding:3px 0;border-bottom:1px dashed #dde3e8}
.swatch{display:inline-block;width:12px;height:12px;border-radius:50%;margin-inline-end:6px;vertical-align:-1px}
.legend{margin-top:10px}
fieldset{border:1px solid #d9e0e6;border-radius:8px;margin:10px 0}
legend{font-weight:700;padding:0 6px}
label.chk{display:block;padding:2px 0;cursor:pointer}
.note{font-size:11px;color:#667;margin-top:10px;line-height:1.5}
.leaflet-popup-content{font-size:12px;max-height:240px;overflow:auto}
.pname{font-weight:700}
select{padding:4px;border-radius:6px}
.placelbl{font-size:11px;color:#33485c;font-weight:600;text-shadow:0 0 3px #fff,0 0 3px #fff,0 0 3px #fff;white-space:nowrap}
</style>
</head>
<body>
<div id="app">
  <header>
    <div><h1>@TITLE@</h1><p>@SUBTITLE@</p></div>
    <a class="lang" href="@SWITCH_HREF@">@SWITCH@</a>
  </header>
  <div id="controls">
    <button id="play">@PLAY@</button>
    <span class="hourlab" id="hourlab"></span>
    <input id="slider" type="range" min="1" value="1" step="1"/>
    <label style="font-size:13px"><input type="checkbox" id="cumul" checked/> @CUMULATIVE@</label>
    <label style="font-size:13px">@COLORBY@
      <select id="colorby"><option value="branch">@OPT_BRANCH@</option><option value="wave">@OPT_WAVE@</option></select>
    </label>
    <label style="font-size:13px"><input type="checkbox" id="reflayer" checked/> @REFLAYER@</label>
  </div>
  <div id="main">
    <div id="map"></div>
    <div id="side">
      <div>@FALLEN_UNTIL@</div>
      <div class="statbig" id="cum_total">0</div>
      <div id="bystat"></div>
      <fieldset><legend>@BRANCH_FILTER@</legend><div id="branchfilter"></div></fieldset>
      <div class="legend" id="legend"></div>
      <div class="note" id="note"></div>
    </div>
  </div>
</div>
<script>
@LEAFLET_JS@
</script>
<script>
const DATA = @DATA@;
const MAXH = @MAXH@;
const LABELS = @LABELS@;
const BORDER = @BORDER@;
const L10N = @L10N@;

const BRANCH_COLORS={"Military":"#1f4e79","Police":"#c0392b","Emergency Response Team":"#2e8b57","Shin Bet":"#d4a017"};
const WAVE_COLORS={"joined":"#c0392b","onduty":"#1f4e79"};
const BHE=L10N.branch;
function t(k){return L10N[k];}

const map=L.map('map',{scrollWheelZoom:true}).setView([31.42,34.49],11);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:18,attribution:'© OpenStreetMap'}).addTo(map);

// reference layer: border + place labels
const refLayer=L.layerGroup().addTo(map);
L.polyline(BORDER,{color:'#7a5230',weight:2,dashArray:'5,5',opacity:.8}).addTo(refLayer);
LABELS.forEach(p=>{
  L.marker([p.lat,p.lon],{interactive:false,icon:L.divIcon({className:'',
    html:'<div class="placelbl">'+p.loc+'</div>',iconSize:[0,0]})}).addTo(refLayer);
});
document.getElementById('reflayer').addEventListener('change',e=>{
  e.target.checked?map.addLayer(refLayer):map.removeLayer(refLayer);
});

const layer=L.layerGroup().addTo(map);
const branches=[...new Set(DATA.map(d=>d.branch))];
const activeBranches=new Set(branches);
const bf=document.getElementById('branchfilter');
branches.forEach(b=>{
  const lab=document.createElement('label');lab.className='chk';
  lab.innerHTML='<input type="checkbox" checked/> <span class="swatch" style="background:'+BRANCH_COLORS[b]+'"></span>'+(BHE[b]||b);
  bf.appendChild(lab);
  lab.querySelector('input').addEventListener('change',e=>{e.target.checked?activeBranches.add(b):activeBranches.delete(b);render();});
});
function colorFor(d){
  if(document.getElementById('colorby').value==='wave') return d.joined?WAVE_COLORS.joined:WAVE_COLORS.onduty;
  return BRANCH_COLORS[d.branch]||'#666';
}
function dominant(list,key){const c={};list.forEach(d=>{const k=key(d);c[k]=(c[k]||0)+1;});return Object.entries(c).sort((a,b)=>b[1]-a[1])[0][0];}

function render(){
  const H=+document.getElementById('slider').value;
  const cumul=document.getElementById('cumul').checked;
  document.getElementById('hourlab').textContent=t('hour_tpl').replace('{H}',H).replace('{C}',(6+H)%24);
  const shown=DATA.filter(d=>activeBranches.has(d.branch)&&(cumul?d.hour<=H:d.hour===H));
  const groups={};
  shown.forEach(d=>{const k=d.lat.toFixed(4)+','+d.lon.toFixed(4);(groups[k]=groups[k]||[]).push(d);});
  layer.clearLayers();
  Object.entries(groups).forEach(([k,list])=>{
    const [lat,lon]=k.split(',').map(Number);
    const r=6+3*Math.sqrt(list.length);
    const col=colorFor(list.length>1?{branch:dominant(list,d=>d.branch),joined:dominant(list,d=>d.joined?'1':'0')==='1'}:list[0]);
    const m=L.circleMarker([lat,lon],{radius:r,color:'#222',weight:1,fillColor:col,fillOpacity:.8});
    const names=list.sort((a,b)=>a.hour-b.hour).map(d=>
      '<div class="row"><span class="pname">'+d.name+'</span><span>'+(BHE[d.branch]||d.branch)+
      (d.age?', '+d.age:'')+(d.sof?' · '+t('sof_mark'):'')+' · '+t('hour_word')+' '+d.hour+(d.time_known?'':'?')+'</span></div>').join('');
    m.bindPopup('<b>'+list[0].loc+'</b> — '+t('fallen_n').replace('{n}',list.length)+'<br><small>'+list[0].loctype+'</small><hr style="margin:4px 0">'+names);
    layer.addLayer(m);
  });
  const cum=DATA.filter(d=>activeBranches.has(d.branch)&&d.hour<=H);
  document.getElementById('cum_total').textContent=cum.length;
  const by={};cum.forEach(d=>by[d.branch]=(by[d.branch]||0)+1);
  document.getElementById('bystat').innerHTML=branches.map(b=>
    '<div class="row"><span><span class="swatch" style="background:'+BRANCH_COLORS[b]+'"></span>'+(BHE[b]||b)+'</span><b>'+(by[b]||0)+'</b></div>').join('')+
    '<div class="row"><span>'+t('of_joined')+'</span><b>'+cum.filter(d=>d.joined).length+'</b></div>'+
    '<div class="row"><span>'+t('of_sof')+'</span><b>'+cum.filter(d=>d.sof).length+'</b></div>';
}
document.getElementById('legend').innerHTML=t('legend');
document.getElementById('note').innerHTML=t('note').replace('{N}',DATA.length).replace('{MAXH}',MAXH);
const slider=document.getElementById('slider');slider.max=MAXH;
slider.addEventListener('input',render);
document.getElementById('cumul').addEventListener('change',render);
document.getElementById('colorby').addEventListener('change',render);
let timer=null;
document.getElementById('play').addEventListener('click',function(){
  if(timer){clearInterval(timer);timer=null;this.textContent=t('play');return;}
  this.textContent=t('pause');
  if(+slider.value>=MAXH)slider.value=1;
  timer=setInterval(()=>{
    if(+slider.value>=MAXH){clearInterval(timer);timer=null;document.getElementById('play').textContent=t('play');return;}
    slider.value=+slider.value+1;render();
  },900);
});
render();
</script>
</body>
</html>
"""

def build(lang):
    s = L10N[lang]
    html = TEMPLATE
    repl = {
        "@LANG@": s["lang"], "@DIR@": s["dir"], "@TITLE@": s["title"],
        "@SUBTITLE@": s["subtitle"], "@PLAY@": s["play"], "@CUMULATIVE@": s["cumulative"],
        "@COLORBY@": s["colorby"], "@OPT_BRANCH@": s["opt_branch"], "@OPT_WAVE@": s["opt_wave"],
        "@REFLAYER@": s["reflayer"], "@FALLEN_UNTIL@": s["fallen_until"],
        "@BRANCH_FILTER@": s["branch_filter"], "@SWITCH@": s["switch"],
        "@SWITCH_HREF@": s["switch_href"],
        "@LEAFLET_CSS@": LEAFLET_CSS, "@LEAFLET_JS@": LEAFLET_JS,
        "@DATA@": json.dumps(recs, ensure_ascii=False),
        "@LABELS@": json.dumps(LABELS, ensure_ascii=False),
        "@BORDER@": json.dumps(BORDER),
        "@L10N@": json.dumps(s, ensure_ascii=False),
        "@MAXH@": str(MAXH),
    }
    for k, v in repl.items():
        html = html.replace(k, v)
    out = os.path.join(DOCS, "oct7_map.html" if lang == "he" else "oct7_map.en.html")
    open(out, "w", encoding="utf-8").write(html)
    print("Wrote", out)

build("he")
build("en")
print(f"{len(recs)} mapped records, {len(LABELS)} place labels, max hour {MAXH}")
