#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate bilingual landing pages into ../docs/ (index.html, index.en.html)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.normpath(os.path.join(HERE, "..", "docs"))
os.makedirs(DOCS, exist_ok=True)

PAGE = {
 "he": dict(lang="he", dir="rtl", switch="English", switch_href="index.en.html",
   map_href="oct7_map.html", video_src="animation.he.webm",
   title="קיבולת תגובה מוטמעת (ERC) — 7 באוקטובר 2023",
   sub="ניתוח מבוסס‑נתונים של 369 אנשי כוחות הביטחון שנפלו במתקפת חמאס, ככלי פרוקסי למיפוי היחידות והלוחמים שהגיבו תחת קריסת הפיקוד והשליטה.",
   en="Embedded Response Capacity against Swarm Terrorism — an empirical analysis (N=369)",
   tags=["מפת ציר‑זמן אינטראקטיבית","סטטיסטיקה תיאורית","סטטיסטיקה הסקתית"],
   h_arg="הטיעון בקצרה",
   arg="לאחר השלב הראשון של המתקפה, בו לחמו הכוחות שהיו מוצבים בגבול, הופיעו בשטח יחידות ולוחמים נוספים שנכנסו לקרבות ביוזמתם — בהיעדר גורם שניהל את האירוע. בקרב המגיבים קיים ייצוג דיספרופורציונלי ללוחמי יחידות מיוחדות. אנו טוענים שההצלחה החלקית של כוחות הביטחון נבעה מ“קיבולת תגובה מוטמעת”: היכולת לעבור באופן מיידי משגרה למשבר ולפעול בערפל קרב, גם כשמערכות הפיקוד והשליטה משותקות.",
   stats=[("369","נופלים במאגר"),("~42%","מצטרפים (גל שני)"),("16.3%",'לוחמי יחב"מ מההרוגים'),("34.9 / 22.8","גיל ממוצע: מצטרפים / מוצבים")],
   h_video="אנימציה — התפשטות הלחימה",
   video_cap="האנימציה מציגה את הופעת הנופלים, שעה אחר שעה, על מפת עוטף עזה. לאינטראקציה מלאה ראו המפה החיה למטה.",
   dl="⬇ הורדת הווידאו (webm)",
   h_map="מפת ציר‑הזמן — שעה אחר שעה",
   map_intro="כל עיגול מציין מיקום נפילה; גודלו פרופורציוני למספר הנופלים בו. הזיזו את המחוון או לחצו “הפעל” כדי לראות כיצד התפשטה הלחימה במרחב, שעה אחר שעה מתחילת המתקפה (06:29).",
   map_open="פתח במסך מלא ↗", map_bar="מפת זמן אינטראקטיבית",
   h_find="ממצאים מרכזיים",
   finds=[
     "<b>שני גלים מובחנים:</b> המוצבים (גל ראשון) צעירים בהרבה (ממוצע 22.8) מהמצטרפים (34.9); מבחן Mann‑Whitney p≈3×10⁻⁷.",
     "<b>יחב“מ הוא המנבא העצמאי החזק ביותר להצטרפות:</b> ברגרסיה לוגיסטית (Firth) OR≈16.7 (p&lt;0.001); מילואים 8.2; קצין 3.4.",
     "<b>ייצוג‑יתר חסון של יחב“מ:</b> גם בהנחה נדיבה של 5% מהכוח — פי ~3; ב‑1–2% — פי ~8–16.",
     "<b>הסקה לפי ענף ושירות:</b> Cramér's V = 0.64 (שירות) ו‑0.54 (ענף) — אפקטים גדולים.",
   ],
   figs=[("figures/fig1_age_by_wave.png","התפלגות גיל לפי גל — דו‑שיא: מוצבים בני 20, מצטרפים פרוסים על פני הטווח."),
         ("figures/fig3_composition.png",'הרכב הנופלים: ענף, שירות, יחב"מ, וקצונה.'),
         ("figures/fig6_km_by_wave.png","קפלן‑מאייר: זמן עד נפילה לפי גל (אירועים בלבד — אין ניצולים בנתונים)."),
         ("figures/fig4_location_distance.png","נפילות לפי סוג מיקום ולפי מרחק מגבול עזה.")],
   h_meth="מתודולוגיה והסתייגויות",
   meth="המאגר נאסף ממקורות פתוחים רשמיים (צה“ל, משטרה, כאן, Mapping the Massacre) ואומת בהצלבה. הגיל אותר ממקורות פתוחים (בעיקר הספדי Times of Israel) באימות שני מקורות (367/369). המרחק מהגבול והיררכיית היחידה חושבו מהנתונים. הניתוח כולל χ²/Fisher, רגרסיה לוגיסטית (Firth), Kruskal‑Wallis, Kaplan‑Meier ו‑Cox, וטיעון חסם ליחב“מ.",
   note="<b>לפני פרסום:</b> (1) אין ניצולים בנתונים → תוצאות ההישרדות מתארות את הנופלים בלבד; (2) הרוגים חולקים יחידה/מיקום → לשקול clustered SE; (3) תאים קטנים (שב“כ n=7); (4) טענות “ייצוג‑יתר” נשענות על טיעון החסם (מכנה מדויק מסווג); (5) עמודת הגיל לבדיקה ידנית.",
   footer="מאגר וניתוח: פרויקט ERC · נבנה ככלי מחקר. כל הנתונים ממקורות פתוחים.",
 ),
 "en": dict(lang="en", dir="ltr", switch="עברית", switch_href="index.html",
   map_href="oct7_map.en.html", video_src="animation.en.webm",
   title="Embedded Response Capacity (ERC) — October 7, 2023",
   sub="A data-driven analysis of 369 Israeli security personnel killed in the Hamas attack, used as a proxy to map the units and fighters who responded amid the collapse of command and control.",
   en="Embedded Response Capacity against Swarm Terrorism — an empirical analysis (N=369)",
   tags=["Interactive timeline map","Descriptive statistics","Inferential statistics"],
   h_arg="The argument in brief",
   arg="After the first phase of the attack, in which the forces stationed at the border fought, additional units and individual fighters appeared on the scene and entered combat on their own initiative — with no one managing the event. Among the responders there is a disproportionate representation of special-operations personnel. We argue that the security forces' partial success stemmed from “Embedded Response Capacity”: the ability to switch instantly from routine to crisis and to operate in the fog of war even when command-and-control systems are paralyzed.",
   stats=[("369","fallen in dataset"),("~42%","joiners (second wave)"),("16.3%","SOF among the fallen"),("34.9 / 22.8","mean age: joiners / on-duty")],
   h_video="Animation — the spread of the fighting",
   video_cap="The animation shows the fallen appearing, hour by hour, across the Gaza-envelope map. For full interactivity see the live map below.",
   dl="⬇ Download the video (webm)",
   h_map="The timeline map — hour by hour",
   map_intro="Each circle marks a place where personnel fell; its size is proportional to the number of fallen there. Move the slider or press “Play” to see how the fighting spread in space, hour by hour from the start of the attack (06:29).",
   map_open="Open full screen ↗", map_bar="Interactive timeline map",
   h_find="Key findings",
   finds=[
     "<b>Two distinct waves:</b> the on-duty (first wave) are far younger (mean 22.8) than the joiners (34.9); Mann‑Whitney p≈3×10⁻⁷.",
     "<b>SOF is the strongest independent predictor of joining:</b> in a Firth logistic regression OR≈16.7 (p&lt;0.001); Reserves 8.2; Officer 3.4.",
     "<b>Robust SOF over-representation:</b> even assuming a generous 5% of the force — ~3×; at 1–2% — ~8–16×.",
     "<b>Branch & service inference:</b> Cramér's V = 0.64 (service) and 0.54 (branch) — large effects.",
   ],
   figs=[("figures/fig1_age_by_wave.png","Age distribution by wave — bimodal: on-duty aged ~20, joiners spread across the range."),
         ("figures/fig3_composition.png","Composition of the fallen: branch, service, SOF, and officer."),
         ("figures/fig6_km_by_wave.png","Kaplan‑Meier: time to falling by wave (events only — no survivors in the data)."),
         ("figures/fig4_location_distance.png","Fatalities by location type and by distance from the Gaza border.")],
   h_meth="Methodology & caveats",
   meth="The dataset was compiled from official open sources (IDF, Police, Kan, Mapping the Massacre) and cross-verified. Ages were located from open sources (mainly Times of Israel obituaries) verified against two sources (367/369). Distance-from-border and unit hierarchy were computed from the data. The analysis includes χ²/Fisher, Firth logistic regression, Kruskal‑Wallis, Kaplan‑Meier and Cox, and an SOF bounding argument.",
   note="<b>Before publication:</b> (1) no survivors in the data → survival results describe the fallen only; (2) fatalities share unit/location → consider clustered SE; (3) small cells (Shin Bet n=7); (4) over-representation claims rely on the bounding argument (exact denominator classified); (5) the age column should be manually reviewed.",
   footer="Dataset & analysis: the ERC project · built as a research tool. All data from open sources.",
 ),
}

CSS = """
:root{--ink:#1f2d3d;--accent:#1f4e79;--bg:#f4f6f8;--line:#d9e0e6}
*{box-sizing:border-box}
body{margin:0;font-family:'Segoe UI',Arial,Helvetica,sans-serif;color:var(--ink);background:#fff;line-height:1.65}
.wrap{max-width:1100px;margin:0 auto;padding:0 20px}
header.hero{background:linear-gradient(135deg,#11212f,#1f4e79);color:#fff;padding:40px 0 32px;position:relative}
header.hero h1{margin:0 0 6px;font-size:30px}
header.hero .subt{font-size:16px;color:#cdd9e5;max-width:780px}
header.hero .ensub{font-size:13px;color:#9fb3c6;margin-top:6px}
header.hero a.lang{position:absolute;top:16px;inset-inline-end:20px;color:#9ad0ff;font-size:14px;text-decoration:none}
section{padding:32px 0;border-bottom:1px solid var(--line)}
h2{font-size:22px;color:var(--accent);margin:0 0 14px}
p.lead{font-size:16px}
.stats{display:flex;gap:14px;flex-wrap:wrap;margin:18px 0}
.stat{flex:1;min-width:150px;background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:16px;text-align:center}
.stat .n{font-size:28px;font-weight:800;color:var(--accent)}
.stat .l{font-size:13px;color:#5a6b7b;margin-top:4px}
.card{border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:0 6px 24px rgba(0,0,0,.08)}
.card .bar{background:#1b2c3a;color:#fff;padding:10px 16px;font-size:14px;display:flex;justify-content:space-between;align-items:center}
.card .bar a{color:#9ad0ff;text-decoration:none}
iframe.map{width:100%;height:640px;border:0;display:block}
video.anim{width:100%;display:block;background:#dfe7ee}
.figs{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:18px;margin-top:8px}
.fig{border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#fff}
.fig img{width:100%;display:block}
.fig .cap{padding:8px 12px;font-size:13px;color:#5a6b7b}
.findings li{margin:6px 0}
.note{background:#fff8e6;border:1px solid #f0d98a;border-radius:10px;padding:14px;font-size:13px;color:#6b5a23}
footer{padding:24px 0;font-size:12px;color:#8090a0}
.tag{display:inline-block;background:#e9eef4;color:#34557a;border-radius:20px;padding:3px 10px;font-size:12px;margin-inline-end:6px}
"""

def render(s):
    tags = "".join(f'<span class="tag">{x}</span>' for x in s["tags"])
    stats = "".join(f'<div class="stat"><div class="n">{n}</div><div class="l">{l}</div></div>' for n,l in s["stats"])
    finds = "".join(f"<li>{x}</li>" for x in s["finds"])
    figs = "".join(f'<div class="fig"><img src="{src}" alt=""/><div class="cap">{cap}</div></div>' for src,cap in s["figs"])
    return f"""<!DOCTYPE html>
<html lang="{s['lang']}" dir="{s['dir']}">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{s['title']}</title>
<style>{CSS}</style>
</head>
<body>
<header class="hero"><div class="wrap">
  <a class="lang" href="{s['switch_href']}">{s['switch']}</a>
  <h1>{s['title']}</h1>
  <div class="subt">{s['sub']}</div>
  <div class="ensub">{s['en']}</div>
  <div style="margin-top:14px">{tags}</div>
</div></header>

<section><div class="wrap">
  <h2>{s['h_arg']}</h2>
  <p class="lead">{s['arg']}</p>
  <div class="stats">{stats}</div>
</div></section>

<section><div class="wrap">
  <h2>{s['h_video']}</h2>
  <div class="card"><video class="anim" controls autoplay muted loop playsinline poster="figures/fig1_age_by_wave.png">
    <source src="{s['video_src']}" type="video/webm"/></video></div>
  <p class="cap" style="font-size:13px;color:#5a6b7b">{s['video_cap']}
    &nbsp;·&nbsp; <a href="{s['video_src']}" download style="color:#1f4e79;font-weight:600">{s['dl']}</a></p>
</div></section>

<section><div class="wrap">
  <h2>{s['h_map']}</h2>
  <p>{s['map_intro']}</p>
  <div class="card"><div class="bar"><span>{s['map_bar']}</span>
    <a href="{s['map_href']}" target="_blank">{s['map_open']}</a></div>
    <iframe class="map" src="{s['map_href']}" title="map"></iframe></div>
</div></section>

<section><div class="wrap">
  <h2>{s['h_find']}</h2>
  <ul class="findings">{finds}</ul>
  <div class="figs">{figs}</div>
</div></section>

<section><div class="wrap">
  <h2>{s['h_meth']}</h2>
  <p>{s['meth']}</p>
  <div class="note">{s['note']}</div>
</div></section>

<footer><div class="wrap">{s['footer']}</div></footer>
</body></html>
"""

for lang, fn in [("he","index.html"),("en","index.en.html")]:
    open(os.path.join(DOCS, fn), "w", encoding="utf-8").write(render(PAGE[lang]))
    print("Wrote", os.path.join(DOCS, fn))
