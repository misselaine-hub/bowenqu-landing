#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BO Wenqu — Back-to-School flyer builder
Outputs:
  BOWenqu_BackToSchool_Flyer_A4.pdf / .png       (A4 print, vector)
  BOWenqu_BackToSchool_Flyer_Social.pdf / .png   (1080x1350, 4:5 social)
"""
import base64
import io
import os
import subprocess

OUT = os.path.dirname(os.path.abspath(__file__))
LANDING = "https://bowenqu.com/backtoschool"

# ---------------------------------------------------------------- icons
# 48x48 viewBox. WeasyPrint does not resolve <use>, so path data is expanded inline.
ICONS = {
    "notebook": '<rect x="10" y="6" width="28" height="36" rx="3" fill="currentColor" opacity=".12"/>'
                '<rect x="10" y="6" width="28" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="2.2"/>'
                '<path d="M16 6v36" stroke="currentColor" stroke-width="2.2"/>'
                '<path d="M22 15h11M22 21h11M22 27h11M22 33h7" stroke="currentColor" stroke-width="2" stroke-linecap="round" opacity=".45"/>',
    "pen": '<path d="M13 34l3-8 16-16a3 3 0 014 0l1 1a3 3 0 010 4L21 31l-8 3z" fill="currentColor"/>'
           '<path d="M13 34l1.5 5 5-1.5" fill="currentColor" opacity=".55"/>'
           '<path d="M30 11l5 5" stroke="#fff" stroke-width="2" opacity=".5" stroke-linecap="round"/>',
    "eraser": '<rect x="7" y="19" width="34" height="17" rx="3.5" fill="currentColor" opacity=".35"/>'
              '<rect x="7" y="19" width="34" height="8" rx="3.5" fill="currentColor"/>'
              '<path d="M7 27h34" stroke="#fff" stroke-width="2.4"/>',
    "ruler": '<rect x="5" y="17" width="38" height="14" rx="2.5" fill="currentColor"/>'
             '<path d="M12 17v6M18 17v8M24 17v6M30 17v8M36 17v6" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/>',
    "case": '<rect x="4" y="17" width="40" height="18" rx="6" fill="currentColor"/>'
            '<path d="M4 26h40" stroke="#fff" stroke-width="2.4"/>'
            '<circle cx="26" cy="26" r="3.2" fill="#fff" opacity=".85"/>',
    "label": '<path d="M6 15h28a2 2 0 012 2v14a2 2 0 01-2 2H6a2 2 0 01-2-2V17a2 2 0 012-2z" fill="currentColor" opacity=".35"/>'
             '<path d="M34 15l8 9-8 9z" fill="currentColor"/>'
             '<path d="M11 22h14M11 27h9" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/>',
    "unicorn": '<path d="M24 3l4.6 11.4h-9.2z" fill="#FFD84D"/>'
               '<path d="M13.5 18.5L11 9.5l8 4.5z" fill="#fff" stroke="currentColor" stroke-width="2"/>'
               '<path d="M34.5 18.5L37 9.5l-8 4.5z" fill="#fff" stroke="currentColor" stroke-width="2"/>'
               '<ellipse cx="24" cy="28" rx="11" ry="12" fill="#fff" stroke="currentColor" stroke-width="2.2"/>'
               '<path d="M13.6 21.5C6 25 5.6 35.6 10.8 41c-.6-6.6 1-11.4 4-14.4z" fill="#FF6FA5"/>'
               '<path d="M18.6 27.2q2.2 2.2 4.4 0" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/>'
               '<path d="M25 27.2q2.2 2.2 4.4 0" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/>'
               '<path d="M21 33.6q3 2.6 6 0" stroke="#FF6FA5" stroke-width="2.2" fill="none" stroke-linecap="round"/>',
    "dino": '<path d="M5 35c0-10 8.5-16 18.5-16 8 0 11 5 13 9l7-5-1 7 6 4-9 3c-4 5-11 7-19 7-9 0-15.5-4-15.5-9z" fill="currentColor"/>'
            '<path d="M13 21l2-6 3 6 3-6 3 6" fill="none" stroke="#fff" stroke-width="2.4" opacity=".8" stroke-linejoin="round"/>'
            '<circle cx="32" cy="27" r="2.6" fill="#fff"/><circle cx="32.8" cy="27" r="1.3" fill="#171634"/>'
            '<path d="M35 32q3 1.2 5.5-1" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" opacity=".8"/>',
    "shield": '<path d="M24 5l15 5v12c0 10-7 17-15 21-8-4-15-11-15-21V10z" fill="currentColor" opacity=".14"/>'
              '<path d="M24 5l15 5v12c0 10-7 17-15 21-8-4-15-11-15-21V10z" fill="none" stroke="currentColor" stroke-width="2.2"/>'
              '<path d="M16.5 24l5.5 5.5L32 19" stroke="currentColor" stroke-width="3.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
    "star": '<path d="M24 5l5.5 11.6L42 18l-9 8.8 2.1 12.4L24 33.6 12.9 39.2 15 26.8 6 18l12.5-1.4z" fill="currentColor"/>',
    "check": '<circle cx="24" cy="24" r="18" fill="currentColor" opacity=".14"/>'
             '<path d="M15 24.5l6 6 12-13" stroke="currentColor" stroke-width="3.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
    "gift": '<path d="M4 13h40v11H4z" fill="currentColor"/><path d="M2 26h44v20H2z" fill="currentColor" opacity=".72"/>'
            '<path d="M24 13v33" stroke="#fff" stroke-width="3"/>'
            '<path d="M24 13c-6-9-16-8-16-3 0 3 6 3 16 3zm0 0c6-9 16-8 16-3 0 3-6 3-16 3z" fill="currentColor"/>',
    "books": '<rect x="6" y="12" width="36" height="8" rx="2" fill="#fff"/>'
             '<rect x="9" y="22" width="30" height="8" rx="2" fill="#fff"/>'
             '<rect x="12" y="32" width="24" height="8" rx="2" fill="#fff"/>',
    "confetti": '<circle cx="12" cy="12" r="5" fill="currentColor"/>'
                '<rect x="26" y="4" width="10" height="10" rx="2" fill="currentColor" transform="rotate(20 31 9)"/>'
                '<circle cx="38" cy="24" r="4" fill="currentColor"/>',
}


def icon(name, size, color="currentColor", extra=""):
    return (f'<svg class="ic" viewBox="0 0 48 48" width="{size}" height="{size}" '
            f'style="color:{color};{extra}">{ICONS[name]}</svg>')


def qr_data_uri(url, scale=8):
    import segno
    qr = segno.make(url, error="m")
    buf = io.BytesIO()
    qr.save(buf, kind="png", scale=scale, border=2, dark="#171634", light="#ffffff")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


# ---------------------------------------------------------------- content
LOGO_MARK = '<span class="logo-mark">' + icon("star", "6.2mm", "#fff") + '</span>'

CHIPS = [("notebook", "6 notebooks"), ("pen", "8 pens"), ("label", "name labels"),
         ("eraser", "erasers"), ("ruler", "ruler"), ("case", "pencil case")]

PARENTS_ITEMS = [
    "The whole list, one box — no more “we forgot the glue stick”",
    "100gsm paper — fountain pens don’t bleed through",
    "EN71 &amp; ASTM D-4236 certified, non-toxic, rounded corners",
    "1-year replacement guarantee — no receipt needed",
]
KIDS_ITEMS = [
    "Unicorn notebooks &amp; dinosaur pens, <b>6 characters</b> to collect",
    "Name labels, so nothing comes home missing",
    "A pencil case that gets you borrowed pens",
    "Everything that makes school a little magical",
]


def item_list(items, color):
    return "".join(
        f'<li>{icon("check", "3.6mm", color)}<span>{t}</span></li>' for t in items)


# ---------------------------------------------------------------- A4 CSS
CSS_A4 = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 210mm; height: 297mm; }
body {
  font-family: 'Nunito', 'DejaVu Sans', sans-serif;
  background: #FFFDF7; color: #171634; position: relative; overflow: hidden;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
.ic { display: inline-block; vertical-align: middle; }

/* ---------- hero 0-104mm ---------- */
.hero { position:absolute; top:0; left:0; width:210mm; height:104mm;
        background: linear-gradient(135deg, #6C4CF1 0%, #7B5CF5 42%, #5233D6 100%); }
.blob { position:absolute; border-radius:50%; }
.blob1 { width:112mm; height:112mm; right:-32mm; top:-44mm; background:rgba(255,255,255,.10); }
.blob2 { width:58mm; height:58mm; right:26mm; top:52mm; background:rgba(255,138,61,.28); }
.blob3 { width:24mm; height:24mm; left:-8mm; top:80mm; background:rgba(255,216,77,.28); }
.logo { position:absolute; left:13mm; top:10mm; display:flex; align-items:center; }
.logo-mark { width:10.5mm; height:10.5mm; border-radius:3.6mm;
             background:linear-gradient(135deg,#FF6FA5,#FF8A3D); display:flex;
             align-items:center; justify-content:center; }
.logo-mark svg { width:6.2mm; height:6.2mm; color:#fff; }
.logo-txt { font-family:'Fredoka',sans-serif; font-weight:600; font-size:12.4pt;
            color:#fff; letter-spacing:1.6pt; margin-left:3.4mm; }
.pill { position:absolute; right:13mm; top:11.6mm; padding:1.5mm 4.2mm;
        border:0.35mm solid rgba(255,255,255,.55); border-radius:20mm;
        font-size:8pt; font-weight:800; letter-spacing:1.4pt; color:#fff; white-space:nowrap; }
.eyebrow { position:absolute; left:13mm; top:24mm; font-size:8.4pt; font-weight:800;
           letter-spacing:2.3pt; color:#CFC2FF; }
h1 { position:absolute; left:12.4mm; top:28.6mm; font-family:'Fredoka',sans-serif;
     font-weight:700; font-size:34pt; line-height:.96; color:#fff; letter-spacing:-.3pt;
     white-space:nowrap; }
h1 .gold { color:#FFD84D; }
.sub { position:absolute; left:13mm; top:58mm; width:100mm; font-size:11pt;
       line-height:1.45; color:#DCD3FF; }
.slogan { position:absolute; left:13mm; top:78mm; background:#fff; border-radius:16mm;
          padding:2.9mm 6.6mm; font-family:'Fredoka',sans-serif; font-weight:600;
          font-size:12pt; color:#5233D6; white-space:nowrap; }
.deco { position:absolute; }
.deco-uni { right:19mm; top:20mm; }
.deco-dino { right:5mm; top:50mm; color:#2BC48A; }
.deco-nb { right:62mm; top:52mm; color:#FF8A3D; transform:rotate(-8deg); }
.deco-pen { right:42mm; top:72mm; color:#FF6FA5; transform:rotate(14deg); }
.deco-star { right:66mm; top:8mm; color:#FFD84D; }
.deco-star2 { right:12mm; top:66mm; color:#fff; opacity:.85; }
.deco-conf { right:56mm; top:36mm; color:#FFD84D; opacity:.9; }

/* ---------- offer card 92-140mm ---------- */
.offer { position:absolute; left:12mm; top:92mm; width:186mm; height:48mm;
         background:#fff; border-radius:6mm; border:0.3mm solid #ECE7F5; }
.offer-left { position:absolute; left:9mm; top:7mm; width:80mm; }
.klabel { font-size:7.8pt; font-weight:800; letter-spacing:1.8pt; color:#8282A6; }
.price { font-family:'Fredoka',sans-serif; font-weight:700; font-size:33pt; color:#171634;
         line-height:1.05; margin-top:1mm; white-space:nowrap; }
.price .was { font-size:12pt; font-weight:500; color:#8282A6; text-decoration:line-through;
              margin-left:4mm; letter-spacing:0; }
.price .save { font-size:10pt; font-weight:800; color:#2BC48A; margin-left:4mm; letter-spacing:0; }
.badge { display:inline-block; margin-top:4mm; background:#FF8A3D; color:#fff;
         border-radius:3.2mm; padding:2mm 4.6mm; font-size:8.4pt; font-weight:800;
         letter-spacing:.5pt; white-space:nowrap; }
.offer-right { position:absolute; left:96mm; top:7mm; width:82mm; }
.count { font-family:'Fredoka',sans-serif; font-weight:700; font-size:23pt; color:#6C4CF1;
         line-height:1; white-space:nowrap; }
.count span { font-size:9.5pt; color:#4A4A6A; font-weight:800; letter-spacing:.4pt; }
.chips { margin-top:3.4mm; }
.chip { display:inline-block; margin:0 1.5mm 1.6mm 0; padding:1.3mm 3mm;
        background:#F6F3FF; border-radius:10mm; font-size:8.2pt; font-weight:700; color:#4A4A6A; }
.chip svg { width:3.2mm; height:3.2mm; margin-right:1.3mm; }

/* ---------- dual line 145-227mm ---------- */
.dual { position:absolute; left:12mm; top:145mm; width:186mm; height:82mm; }
.col { position:absolute; top:0; height:82mm; border-radius:5mm; padding:6mm 6.5mm; }
.col-p { left:0; width:91mm; background:#F1ECFF; }
.col-k { right:0; width:91mm; background:#FFEFF5; }
.col-head { display:flex; align-items:center; font-family:'Fredoka',sans-serif; font-weight:700;
            font-size:12.4pt; letter-spacing:.3pt; }
.col-head svg { width:5.4mm; height:5.4mm; margin-right:2.3mm; }
.col-p .col-head { color:#5233D6; }
.col-k .col-head { color:#D63C7E; }
ul { list-style:none; margin-top:3.2mm; }
li { position:relative; padding-left:5.2mm; font-size:9.1pt; line-height:1.4;
     color:#3C3C5C; margin-bottom:1.7mm; }
li svg { position:absolute; left:0; top:0.35mm; width:3.5mm; height:3.5mm; }
li b { color:#171634; }
.quote { position:absolute; left:6.5mm; bottom:5.5mm; width:78mm; font-family:'Fredoka',sans-serif;
         font-weight:600; font-size:10.4pt; line-height:1.25; }
.col-p .quote { color:#5233D6; }
.col-k .quote { color:#D63C7E; }

/* ---------- gifts 232-246mm ---------- */
.gifts { position:absolute; left:12mm; top:232mm; width:186mm; height:14mm;
         background:#E9F9F2; border-radius:4mm; display:flex; align-items:center;
         padding:0 6mm; white-space:nowrap; overflow:hidden; }
.gifts svg { width:6mm; height:6mm; color:#2BC48A; margin-right:2.6mm; flex:none; }
.gifts .txt { font-size:8.6pt; letter-spacing:.1pt; }
.gifts b { color:#171634; }
.gifts .sep { color:#BFD8CD; margin:0 2.4mm; }

/* ---------- footer 252-297mm ---------- */
.foot { position:absolute; left:0; top:252mm; width:210mm; height:45mm;
        background:#171634; }
.foot-in { position:absolute; left:13mm; top:7mm; width:184mm; }
.cta { display:inline-block; background:#FF8A3D; color:#fff; font-family:'Fredoka',sans-serif;
       font-weight:700; font-size:12.6pt; letter-spacing:.4pt; border-radius:3.4mm;
       padding:2.6mm 6.4mm; white-space:nowrap; }
.cta .arr { margin-left:2.2mm; }
.url { font-size:9.4pt; color:#B9B7D6; margin-left:5mm; letter-spacing:.3pt; white-space:nowrap; }
.qr { position:absolute; right:0; top:-3mm; width:19mm; height:19mm;
      border-radius:2.5mm; background:#fff; padding:1.1mm; }
.qr img { width:16.8mm; height:16.8mm; }
.foot-right { position:absolute; right:13mm; top:30mm; width:160mm; text-align:right; }
.tags { font-size:7.4pt; color:#FF6FA5; font-weight:800; letter-spacing:.3pt; }
.fine { font-size:6.8pt; color:#9A98BE; margin-top:1.3mm; }
.disclaimer { font-size:6.2pt; color:#6E6C90; margin-top:1.1mm; }
"""

HERO = f"""
<div class="hero">
  <div class="blob blob1"></div><div class="blob blob2"></div><div class="blob blob3"></div>
  <div class="logo">{LOGO_MARK}<span class="logo-txt">BO WENQU</span></div>
  <div class="pill">BACK-TO-SCHOOL EVENT</div>
  <div class="eyebrow">THE WHOLE CLASS LIST, ONE BOX</div>
  <h1>BACK-TO-SCHOOL,<br><span class="gold">SORTED.</span></h1>
  <div class="sub">Unicorn notebooks. Dinosaur pens. And everything else on that
      impossible class list.</div>
  <div class="slogan">Cute gear. Serious school days.</div>
  <div class="deco deco-uni">{icon("unicorn", "28mm", "#6C4CF1")}</div>
  <div class="deco deco-dino">{icon("dino", "25mm", "#2BC48A")}</div>
  <div class="deco deco-nb">{icon("notebook", "21mm", "#FF8A3D")}</div>
  <div class="deco deco-pen">{icon("pen", "16mm", "#FF6FA5")}</div>
  <div class="deco deco-star">{icon("star", "8.5mm", "#FFD84D")}</div>
  <div class="deco deco-star2">{icon("star", "5mm", "#fff")}</div>
  <div class="deco deco-conf">{icon("confetti", "11mm", "#FFD84D")}</div></div>
"""

OFFER = f"""
<div class="offer">
  <div class="offer-left">
    <div class="klabel">BACK-TO-SCHOOL BUNDLE</div>
    <div class="price">$59<span class="was">$79</span><span class="save">you save $20</span></div>
    <div class="badge">EARLY-BIRD 20% OFF &nbsp;·&nbsp; ENDS AUG 22</div>
  </div>
  <div class="offer-right">
    <div class="count">24 <span>PIECES IN ONE BOX</span></div>
    <div class="chips">{''.join(f'<span class="chip">{icon(k, "3.2mm", "#6C4CF1")}{t}</span>' for k, t in CHIPS)}</div>
  </div>
</div>
"""

DUAL = f"""
<div class="dual">
  <div class="col col-p">
    <div class="col-head">{icon("shield", "5.4mm", "#6C4CF1")}FOR PARENTS</div>
    <ul>{item_list(PARENTS_ITEMS, "#2BC48A")}</ul>
    <div class="quote">Everything on the list. Nothing to worry about.</div>
  </div>
  <div class="col col-k">
    <div class="col-head">{icon("unicorn", "5.4mm", "#FF6FA5")}FOR KIDS</div>
    <ul>{item_list(KIDS_ITEMS, "#FF6FA5")}</ul>
    <div class="quote">Your school stuff, but make it magical.</div>
  </div>
</div>
"""

GIFTS = f"""
<div class="gifts">
  {icon("gift", "6mm", "#2BC48A")}
  <span class="txt"><b>Spend $39</b> &rarr; free unicorn sticker pack<span class="sep">|</span>
  <b>Spend $69</b> &rarr; free dino pencil case<span class="sep">|</span>
  Free shipping</span>
</div>
"""

FOOT = f"""
<div class="foot">
  <div class="foot-in">
    <span class="cta">SHOP THE LIST <span class="arr">&rarr;</span></span>
    <span class="url">{LANDING.replace("https://", "")}</span>
    <div class="qr"><img src="{qr_data_uri(LANDING)}" alt="QR"></div>
  </div>
  <div class="foot-right">
    <div class="tags">#BOWenqu&nbsp;&nbsp;#BackToSchool&nbsp;&nbsp;#SchoolSupplies&nbsp;&nbsp;#StationeryAddict</div>
    <div class="fine">EN71 &amp; ASTM D-4236 certified · Ships within 48 hours · Ages 6+ · 1-year replacement guarantee</div>
    <div class="disclaimer">Sample pricing, dates and certification claims shown for layout only — verify before printing. © BO Wenqu</div>
  </div>
</div>
"""

HTML_A4 = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>BO Wenqu — Back-to-School Flyer (A4)</title>
<style>{CSS_A4}</style></head>
<body>{HERO}{OFFER}{DUAL}{GIFTS}{FOOT}</body></html>"""


# ---------------------------------------------------------------- social 4:5
CSS_SOCIAL = open(os.path.join(OUT, "_social.css"), encoding="utf-8").read()

HTML_SOCIAL = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>BO Wenqu — Back-to-School Flyer (Social 4:5)</title>
<style>{CSS_SOCIAL}</style></head>
<body>{HERO}{OFFER}{DUAL}{GIFTS}{FOOT}</body></html>"""


def main():
    from weasyprint import HTML as WHTML

    html_a4 = os.path.join(OUT, "flyer_a4.html")
    html_social = os.path.join(OUT, "flyer_social.html")
    open(html_a4, "w", encoding="utf-8").write(HTML_A4)
    open(html_social, "w", encoding="utf-8").write(HTML_SOCIAL)

    jobs = [
        (html_a4, os.path.join(OUT, "BOWenqu_BackToSchool_Flyer_A4.pdf"),
         os.path.join(OUT, "BOWenqu_BackToSchool_Flyer_A4.png"), 160),
        (html_social, os.path.join(OUT, "BOWenqu_BackToSchool_Flyer_Social.pdf"),
         os.path.join(OUT, "BOWenqu_BackToSchool_Flyer_Social.png"), 120),
    ]
    for src, pdf, png, dpi in jobs:
        WHTML(filename=src).write_pdf(pdf)
        subprocess.run(["pdftoppm", "-png", "-r", str(dpi), "-singlefile", pdf, png[:-4]], check=True)
        print("built", os.path.basename(pdf), "|", os.path.basename(png))


if __name__ == "__main__":
    main()
