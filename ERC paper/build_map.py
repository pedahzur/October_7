#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a self-contained interactive time-line map of the fallen.
Reads Database_enriched.csv, embeds the data inline, writes ./oct7_map.html
(no server / no external data files needed; Leaflet loaded from CDN).
"""
import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "Database_enriched.csv")
OUT = os.path.join(HERE, "oct7_map.html")

rows = list(csv.DictReader(open(SRC, encoding="utf-8")))

# Inline Leaflet (no CDN dependency -> fully self-contained, works offline).
LEAFLET_DIR = os.path.join(HERE, "vendor")
LEAFLET_JS = open(os.path.join(LEAFLET_DIR, "leaflet.js"), encoding="utf-8").read()
LEAFLET_CSS = open(os.path.join(LEAFLET_DIR, "leaflet.css"), encoding="utf-8").read()

def num(x):
    try: return float(x)
    except: return None

# observed integer hours (for slider bounds / unknown-time placement)
hours = [int(num(r["Time"])) for r in rows if num(r["Time"]) is not None]
MAXH = max(hours)

recs = []
for r in rows:
    lat, lon = num(r["Latitude"]), num(r["Longitude"])
    if lat is None or lon is None:
        continue  # 2 rows lack coordinates -> not mappable
    t = num(r["Time"])
    hour = int(t) if t is not None else MAXH       # unknown time -> placed at end
    recs.append({
        "id": r["ID"],
        "name": r["Name"],
        "lat": lat, "lon": lon,
        "hour": hour,
        "time_known": t is not None,
        "branch": r["Branch"],
        "joined": (r["Joined"] == "1"),
        "sof": (r["SOF"] == "1"),
        "officer": (r["Officer"] == "1"),
        "age": r["Age"] or "",
        "rank": r["Rank"],
        "role": r["Role"],
        "unit": r["Unit"],
        "loc": r["Location"],
        "loctype": r["Location_type"],
        "dist": r["Distance_from_border_km"],
    })

data_json = json.dumps(recs, ensure_ascii=False)

HTML = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>מפת זמן — נופלי כוחות הביטחון, 7 באוקטובר 2023</title>
<style>
/* ---- Leaflet (embedded) ---- */
__LEAFLET_CSS__
/* ---- page styles ---- */
  :root{--ink:#1f2d3d;--accent:#1f4e79;}
  *{box-sizing:border-box}
  html,body{margin:0;height:100%;font-family:'Segoe UI',Arial,Helvetica,sans-serif;color:var(--ink)}
  #app{display:flex;flex-direction:column;height:100vh}
  header{background:#11212f;color:#fff;padding:10px 16px}
  header h1{margin:0;font-size:18px}
  header p{margin:2px 0 0;font-size:12px;color:#b9c6d2}
  #main{flex:1;display:flex;min-height:0}
  #map{flex:1}
  #side{width:300px;background:#f4f6f8;border-inline-start:1px solid #d9e0e6;
        padding:12px;overflow:auto;font-size:13px}
  #controls{background:#1b2c3a;color:#fff;padding:10px 16px;display:flex;
            align-items:center;gap:14px;flex-wrap:wrap}
  #controls button{background:var(--accent);color:#fff;border:0;border-radius:6px;
            padding:6px 12px;cursor:pointer;font-size:14px}
  #controls button:hover{background:#2a63a0}
  #slider{flex:1;min-width:220px}
  .hourlab{font-variant-numeric:tabular-nums;font-weight:700;min-width:150px}
  .statbig{font-size:30px;font-weight:800;color:var(--accent)}
  .row{display:flex;justify-content:space-between;padding:3px 0;border-bottom:1px dashed #dde3e8}
  .swatch{display:inline-block;width:12px;height:12px;border-radius:50%;margin-inline-end:6px;vertical-align:-1px}
  .legend{margin-top:10px}
  fieldset{border:1px solid #d9e0e6;border-radius:8px;margin:10px 0}
  legend{font-weight:700;padding:0 6px}
  label.chk{display:block;padding:2px 0;cursor:pointer}
  .note{font-size:11px;color:#667;margin-top:10px;line-height:1.5}
  .leaflet-popup-content{font-size:12px;max-height:240px;overflow:auto;direction:rtl}
  .pname{font-weight:700}
  select{padding:4px;border-radius:6px}
</style>
</head>
<body>
<div id="app">
  <header>
    <h1>מפת זמן — נופלי כוחות הביטחון ב‑7 באוקטובר 2023</h1>
    <p>כל נקודה = מיקום נפילה. השתמשו במחוון או בכפתור ההפעלה כדי לעקוב, שעה אחר שעה, אחר התפרסות הלחימה.</p>
  </header>

  <div id="controls">
    <button id="play">▶ הפעל</button>
    <span class="hourlab" id="hourlab"></span>
    <input id="slider" type="range" min="1" value="1" step="1"/>
    <label style="font-size:13px"><input type="checkbox" id="cumul" checked/> מצטבר</label>
    <label style="font-size:13px">צבע לפי:
      <select id="colorby">
        <option value="branch">ענף</option>
        <option value="wave">גל (מוצב/מצטרף)</option>
      </select>
    </label>
  </div>

  <div id="main">
    <div id="map"></div>
    <div id="side">
      <div>נפלו עד שעה זו</div>
      <div class="statbig" id="cum_total">0</div>
      <div id="bystat"></div>
      <fieldset>
        <legend>סינון ענף</legend>
        <div id="branchfilter"></div>
      </fieldset>
      <div class="legend" id="legend"></div>
      <div class="note" id="note"></div>
    </div>
  </div>
</div>

<script>
__LEAFLET_JS__
</script>
<script>
const DATA = __DATA__;
const MAXH = __MAXH__;

const BRANCH_COLORS = {
  "Military":"#1f4e79", "Police":"#c0392b",
  "Emergency Response Team":"#2e8b57", "Shin Bet":"#d4a017"
};
const WAVE_COLORS = {"joined":"#c0392b","onduty":"#1f4e79"};
const BRANCH_HE = {"Military":"צבא","Police":"משטרה",
  "Emergency Response Team":"כיתת כוננות","Shin Bet":"שב\\u05f4כ"};

const map = L.map('map',{scrollWheelZoom:true}).setView([31.42,34.49],11);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  {maxZoom:18, attribution:'© OpenStreetMap'}).addTo(map);
const layer = L.layerGroup().addTo(map);

const branches = [...new Set(DATA.map(d=>d.branch))];
const activeBranches = new Set(branches);

// build branch filter + legend
const bf = document.getElementById('branchfilter');
branches.forEach(b=>{
  const id='b_'+b.replace(/\\W/g,'');
  const lab=document.createElement('label'); lab.className='chk';
  lab.innerHTML=`<input type="checkbox" id="${id}" checked/> `+
    `<span class="swatch" style="background:${BRANCH_COLORS[b]}"></span>${BRANCH_HE[b]||b}`;
  bf.appendChild(lab);
  lab.querySelector('input').addEventListener('change',e=>{
    e.target.checked?activeBranches.add(b):activeBranches.delete(b); render();
  });
});

function colorFor(d){
  if(document.getElementById('colorby').value==='wave')
    return d.joined?WAVE_COLORS.joined:WAVE_COLORS.onduty;
  return BRANCH_COLORS[d.branch]||'#666';
}
function dominant(list,key){
  const c={}; list.forEach(d=>{const k=key(d);c[k]=(c[k]||0)+1;});
  return Object.entries(c).sort((a,b)=>b[1]-a[1])[0][0];
}

function render(){
  const H=+document.getElementById('slider').value;
  const cumul=document.getElementById('cumul').checked;
  document.getElementById('hourlab').textContent =
    `שעה ${H} מתחילת המתקפה  (≈ ${(6+H)%24}:29)`;
  const shown = DATA.filter(d=> activeBranches.has(d.branch) &&
      (cumul ? d.hour<=H : d.hour===H));
  // group by location
  const groups={};
  shown.forEach(d=>{const k=d.lat.toFixed(4)+','+d.lon.toFixed(4);
    (groups[k]=groups[k]||[]).push(d);});
  layer.clearLayers();
  Object.entries(groups).forEach(([k,list])=>{
    const [lat,lon]=k.split(',').map(Number);
    const r=6+3*Math.sqrt(list.length);
    const col = colorFor(list.length>1?{branch:dominant(list,d=>d.branch),
                 joined:dominant(list,d=>d.joined?'1':'0')==='1'}:list[0]);
    const m=L.circleMarker([lat,lon],{radius:r,color:'#222',weight:1,
        fillColor:col,fillOpacity:.8});
    const names=list.sort((a,b)=>a.hour-b.hour).map(d=>
      `<div class="row"><span class="pname">${d.name}</span>`+
      `<span>${BRANCH_HE[d.branch]||d.branch}${d.age?', '+d.age:''}`+
      `${d.sof?' · יחב\\u05f4מ':''} · שעה ${d.hour}${d.time_known?'':'?'}</span></div>`).join('');
    m.bindPopup(`<b>${list[0].loc}</b> — ${list.length} נופלים<br>`+
      `<small>${list[0].loctype}</small><hr style="margin:4px 0">${names}`);
    layer.addLayer(m);
  });
  // side stats (always cumulative up to H, regardless of per-hour toggle)
  const cum = DATA.filter(d=> activeBranches.has(d.branch) && d.hour<=H);
  document.getElementById('cum_total').textContent = cum.length;
  const by={}; cum.forEach(d=>by[d.branch]=(by[d.branch]||0)+1);
  document.getElementById('bystat').innerHTML = branches.map(b=>
    `<div class="row"><span><span class="swatch" style="background:${BRANCH_COLORS[b]}"></span>`+
    `${BRANCH_HE[b]||b}</span><b>${by[b]||0}</b></div>`).join('') +
    `<div class="row"><span>מתוכם מצטרפים (גל 2)</span><b>${cum.filter(d=>d.joined).length}</b></div>`+
    `<div class="row"><span>מתוכם יחב\\u05f4מ</span><b>${cum.filter(d=>d.sof).length}</b></div>`;
}

// legend
document.getElementById('legend').innerHTML =
  '<b>מקרא:</b> גודל העיגול ∝ מספר הנופלים במיקום. צבע לפי הבחירה למעלה.';
document.getElementById('note').innerHTML =
  `נכללים ${DATA.length} נופלים בעלי קואורדינטות (2 ללא מיקום הושמטו). `+
  `שעה = שעות מתחילת המתקפה (06:29). נופלים ללא שעה ידועה מוצגים בשעה ${MAXH} ומסומנים "?". `+
  `הגיל אותר ממקורות פתוחים — לבדיקה לפני פרסום.`;

// controls
const slider=document.getElementById('slider'); slider.max=MAXH;
['input'].forEach(ev=>slider.addEventListener(ev,render));
document.getElementById('cumul').addEventListener('change',render);
document.getElementById('colorby').addEventListener('change',render);

let timer=null;
document.getElementById('play').addEventListener('click',function(){
  if(timer){clearInterval(timer);timer=null;this.textContent='▶ הפעל';return;}
  this.textContent='⏸ עצור';
  if(+slider.value>=MAXH) slider.value=1;
  timer=setInterval(()=>{
    if(+slider.value>=MAXH){clearInterval(timer);timer=null;
      document.getElementById('play').textContent='▶ הפעל';return;}
    slider.value=+slider.value+1; render();
  },900);
});

render();
</script>
</body>
</html>
"""

html = (HTML.replace("__LEAFLET_CSS__", LEAFLET_CSS)
            .replace("__LEAFLET_JS__", LEAFLET_JS)
            .replace("__DATA__", data_json)
            .replace("__MAXH__", str(MAXH)))
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Wrote {OUT} with {len(recs)} mapped records (max hour {MAXH}).")
