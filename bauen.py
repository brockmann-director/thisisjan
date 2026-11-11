#!/usr/bin/env python3
"""Baut die Webseite aus inhalt/*.json in den Ordner public/.

    python3 bauen.py          -> fertige Seite für das Hosting (schöne Adressen wie /bmw-art-car/)
    python3 bauen.py --lokal  -> Vorschau zum Doppelklicken auf public/index.html

Neues Projekt: in inhalt/projekte.json einen Block kopieren und anpassen.
Die Reihenfolge in der Datei ist die Reihenfolge auf der Seite.
Eigene Bilder: als bilder/<slug>.jpg ablegen, dann werden sie statt des Links benutzt.
"""
import html
import json
import shutil
import sys
from datetime import date
from pathlib import Path

HIER = Path(__file__).resolve().parent
RAUS = HIER / "public"
LOKAL = "--lokal" in sys.argv

seite = json.loads((HIER / "inhalt" / "seite.json").read_text(encoding="utf-8"))
projekte = json.loads((HIER / "inhalt" / "projekte.json").read_text(encoding="utf-8"))

e = html.escape
import hashlib
VERSION = hashlib.md5((HIER / "vorlage" / "stil.css").read_bytes()).hexdigest()[:8]  # neue Version = Browser lädt neu


def link(ziel, tiefe):
    """ziel: '' (Start) oder 'about' usw. tiefe: wie viele Ordner die Seite tief liegt."""
    hoch = "../" * tiefe
    if LOKAL:
        return f"{hoch}{ziel + '/' if ziel else ''}index.html"
    return hoch + (ziel + "/" if ziel else "") if (hoch or ziel) else "./"


def bild(p, tiefe):
    for endung in ("jpg", "jpeg", "png", "webp"):
        datei = HIER / "bilder" / f"{p['slug']}.{endung}"
        if datei.exists():
            return "../" * tiefe + f"bilder/{datei.name}"
    return p["bild"]


def rahmen(titel, inhalt, tiefe, aktiv="", beschreibung=None, og_bild=None):
    css = "../" * tiefe + "stil.css"
    menue = "".join(
        f'<a href="{link(z, tiefe)}"{" aria-current=\"page\"" if aktiv == z else ""}><span class="eng">{n}</span></a>'
        for z, n in (("", "work"), ("about", "about"))
    )
    og = f'<meta property="og:image" content="{e(og_bild)}">' if og_bild else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titel)}</title>
<meta name="description" content="{e(beschreibung or seite['beschreibung'])}">
<meta property="og:title" content="{e(titel)}">
{og}
<link rel="preload" href="{css.replace('stil.css', 'schrift/bagel-fat-one.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{css}?v={VERSION}">
</head>
<body>
<header class="kopf">
  <a class="name" href="{link('', tiefe)}"><span class="eng">{e(seite['name'])}</span></a>
  <button class="menueknopf" aria-label="Menü" aria-expanded="false"><span></span><span></span><span></span></button>
  <nav class="menue">{menue}</nav>
</header>
<main>
{inhalt}
</main>
<footer class="fuss">
  <div class="symbole">
    <a href="{e(seite['instagram'])}" target="_blank" rel="noopener" aria-label="Instagram">{INSTAGRAM}</a>
    <a href="mailto:{e(seite['email'])}" aria-label="E-Mail">{MAIL}</a>
  </div>
  <small>© {date.today().year} Jan Brockmann | <a href="{link('impressum', tiefe)}">impressum</a> | <a href="{link('datenschutz', tiefe)}">datenschutz</a></small>
</footer>
<script>
// Menü am Handy
var kopf = document.querySelector('.kopf'), knopf = document.querySelector('.menueknopf');
knopf.addEventListener('click', function () {{
  var auf = kopf.classList.toggle('offen');
  knopf.setAttribute('aria-expanded', auf);
}});
// Am Handy zeigt die Kachel in der Bildschirmmitte ihren Titel
if (window.matchMedia('(hover: none)').matches && 'IntersectionObserver' in window) {{
  var io = new IntersectionObserver(function (es) {{
    es.forEach(function (x) {{ x.target.classList.toggle('mitte', x.isIntersecting); }});
  }}, {{ rootMargin: '-49% 0px -49% 0px' }});
  document.querySelectorAll('.kachel').forEach(function (k) {{ io.observe(k); }});
}}
// YouTube lädt erst nach Klick (keine Cookies vorher, daher kein Cookie-Banner nötig)
document.querySelectorAll('.video button').forEach(function (b) {{
  b.addEventListener('click', function () {{
    var f = document.createElement('iframe');
    f.src = 'https://www.youtube-nocookie.com/embed/' + b.dataset.id + '?autoplay=1&rel=0';
    f.allow = 'autoplay; fullscreen; picture-in-picture';
    f.allowFullscreen = true;
    f.title = b.getAttribute('aria-label');
    b.replaceWith(f);
  }});
}});
</script>
</body>
</html>
"""


INSTAGRAM = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.8.1 3.3.1 4.8 1.7 4.9 4.9.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 3.2-1.7 4.8-4.9 4.9-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-3.3-.1-4.8-1.7-4.9-4.9C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8C2.4 3.9 3.9 2.4 7.2 2.3 8.4 2.2 8.8 2.2 12 2.2zM12 0C8.7 0 8.3 0 7.1.1 2.7.3.3 2.7.1 7.1 0 8.3 0 8.7 0 12s0 3.7.1 4.9c.2 4.4 2.6 6.8 7 7 1.2.1 1.6.1 4.9.1s3.7 0 4.9-.1c4.4-.2 6.8-2.6 7-7 .1-1.2.1-1.6.1-4.9s0-3.7-.1-4.9c-.2-4.4-2.6-6.8-7-7C15.7 0 15.3 0 12 0zm0 5.8a6.2 6.2 0 1 0 0 12.4 6.2 6.2 0 0 0 0-12.4zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.4-11.8a1.4 1.4 0 1 0 0 2.9 1.4 1.4 0 0 0 0-2.9z"/></svg>'
MAIL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M0 4.5v.4l12 8.6 12-8.6v-.4C24 3.7 23.3 3 22.5 3h-21C.7 3 0 3.7 0 4.5zm0 2.9V19.5c0 .8.7 1.5 1.5 1.5h21c.8 0 1.5-.7 1.5-1.5V7.4l-12 8.6L0 7.4z"/></svg>'


def schreibe(pfad, text):
    ziel = RAUS / pfad / "index.html"
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(text, encoding="utf-8")


def kachel_titel(p):
    t = e(p["titel"])
    return f'{t} <span class="kunde">{e(p["kunde"])}</span>' if t else f'<span class="kunde">{e(p["kunde"])}</span>'


def startseite(tiefe=0):
    kacheln = "\n".join(
        f"""<li class="kachel"><a href="{link(p['slug'], tiefe)}">
  <img src="{e(bild(p, tiefe))}" alt="{e(p['ueberschrift'])}" loading="{'eager' if i < 4 else 'lazy'}">
  <span class="titel">{''.join(f'<span class="eng">{e(x)}</span>' for x in (p['titel'], p['kunde']) if x)}</span>
</a></li>"""
        for i, p in enumerate(projekte)
    )
    return rahmen("Jan Brockmann", f'<ul class="raster">\n{kacheln}\n</ul>', tiefe, aktiv="",
                  og_bild=projekte[0]["bild"] if projekte else None)


def projektseite(i, p):
    videos = "\n".join(
        f"""<div class="video"><button data-id="{e(v)}" aria-label="Video abspielen: {e(p['ueberschrift'])}">
  <img src="{e(bild(p, 1))}" alt=""><span class="play"></span>
  <span class="hinweis">Abspielen lädt YouTube</span>
</button></div>"""
        for v in p["videos"]
    )
    def credit(c):
        if ":" in c:
            a, b = c.split(":", 1)
            return f"<li>{e(a)}: <b>{e(b.strip())}</b></li>"
        return f"<li>{e(c)}</li>"
    credits = "".join(credit(c) for c in p["credits"])
    if " - " in p["ueberschrift"]:
        a, b = p["ueberschrift"].split(" - ", 1)
        kopfzeile = f"<b>{e(a)}</b> - {e(b)}"
    else:
        kopfzeile = f"<b>{e(p['ueberschrift'])}</b>"
    def bildpfad(x):
        return x if x.startswith("http") else "../bilder/" + x
    stills = "".join(
        f'<img src="{e(bildpfad(x))}" alt="" loading="lazy"{" class=\"breit\"" if x in p.get("breit", []) else ""}>'
        for x in p.get("stills", []))
    if not stills and seite.get("platzhalter"):
        stills = '<div class="platz">Still</div>' * 4 + '<div class="platz breit">Still breit</div>'
    stills = f'<div class="stills">{stills}</div>' if stills else ""
    making = "".join(f'<img src="{e(bildpfad(x))}" alt="" loading="lazy">' for x in p.get("making", []))
    if not making and seite.get("platzhalter"):
        making = "".join(f'<div class="platz" style="width:{w}px">Making-of</div>' for w in (420, 260, 360, 300, 380, 240, 330))
    making = f'<div class="making">{making}</div>' if making else ""
    zitat = f'<p class="zitat">{e(p["text"])}</p>' if p.get("text") else ""
    vor = projekte[i - 1] if i > 0 else None
    nach = projekte[i + 1] if i + 1 < len(projekte) else None
    blaettern = (
        f'<a href="{link(vor["slug"], 1)}">← {kachel_titel(vor)}</a>' if vor else "<span></span>"
    ) + (
        f'<a href="{link(nach["slug"], 1)}">{kachel_titel(nach)} →</a>' if nach else "<span></span>"
    )
    inhalt = f"""<article class="projekt">
{videos}
<div class="angaben">
  <h1>{kopfzeile}</h1>
  <ul class="credits">{credits}</ul>
  {zitat}
</div>
{stills}
</article>
{making}
<nav class="blaettern">{blaettern}</nav>"""
    titel = f"Jan Brockmann - {(p['titel'] + ' ' + p['kunde']).strip()}"
    return rahmen(titel, inhalt, 1, aktiv="", beschreibung=p["ueberschrift"], og_bild=p["bild"])


def aboutseite():
    absaetze = "".join(f"<p>{e(a)}</p>" for a in seite["about"])
    bild_html = f'<img src="{e(seite["about_bild"])}" alt="Jan Brockmann">' if seite.get("about_bild") else ""
    inhalt = f"""<div class="text">
  {bild_html}
  <div class="gross">{absaetze}</div>
  <p class="kontakt"><a href="mailto:{e(seite['email'])}">{e(seite['email'])}</a><br><a href="tel:{e(seite['telefon'].replace(' ', ''))}">{e(seite['telefon'])}</a></p>
</div>"""
    return rahmen("Jan Brockmann - about", inhalt, 1, aktiv="about")


def impressum():
    i = seite["impressum"]
    inhalt = f"""<div class="recht">
<h1>Impressum</h1>
<p>Angaben gemäß § 5 DDG</p>
<p>{e(i['name'])}<br>{e(i['strasse'])}<br>{e(i['ort'])}</p>
<h2>Kontakt</h2>
<p>E-Mail: {e(seite['email'])}</p>
<h2>Berufsbezeichnung</h2>
<p>{e(i['beruf'])}</p>
<h2>Haftung für Inhalte</h2>
<p>Die Inhalte dieser Seite wurden mit Sorgfalt erstellt. Für Richtigkeit, Vollständigkeit und Aktualität wird keine Gewähr übernommen. Als Diensteanbieter bin ich gemäß § 7 Abs. 1 DDG für eigene Inhalte nach den allgemeinen Gesetzen verantwortlich, nach §§ 8 bis 10 DDG aber nicht verpflichtet, übermittelte oder gespeicherte fremde Informationen zu überwachen.</p>
<h2>Haftung für Links</h2>
<p>Diese Seite enthält Links zu externen Webseiten, auf deren Inhalte ich keinen Einfluss habe. Für diese Inhalte ist der jeweilige Anbieter verantwortlich. Bei Bekanntwerden von Rechtsverletzungen werden solche Links umgehend entfernt.</p>
<h2>Urheberrecht</h2>
<p>Die Filme, Bilder und Texte auf dieser Seite unterliegen dem deutschen Urheberrecht. Vervielfältigung oder Verwendung außerhalb der Grenzen des Urheberrechts bedarf der Zustimmung des jeweiligen Rechteinhabers.</p>
</div>"""
    return rahmen("Jan Brockmann - Impressum", inhalt, 1, aktiv="impressum")


def datenschutz():
    i = seite["impressum"]
    inhalt = f"""<div class="recht">
<h1>Datenschutz</h1>
<h2>Verantwortlich</h2>
<p>{e(i['name'])}, {e(i['strasse'])}, {e(i['ort'])}, {e(seite['email'])}</p>
<h2>Keine Cookies, kein Tracking</h2>
<p>Diese Seite setzt keine Cookies und verwendet keine Analyse- oder Tracking-Werkzeuge.</p>
<h2>Hosting</h2>
<p>Beim Aufruf der Seite verarbeitet der Hosting-Anbieter technisch notwendige Daten (z. B. IP-Adresse, Zeitpunkt, aufgerufene Seite), um die Seite auszuliefern und vor Missbrauch zu schützen (Art. 6 Abs. 1 lit. f DSGVO).</p>
<h2>YouTube-Videos</h2>
<p>Die Filme sind bei YouTube (Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland) gespeichert. Ein Video wird erst geladen, wenn du auf „Abspielen“ klickst. Erst dann werden Daten wie deine IP-Adresse an YouTube übertragen. Wir nutzen dafür den erweiterten Datenschutzmodus (youtube-nocookie.com). Mehr dazu in der Datenschutzerklärung von Google: <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">policies.google.com/privacy</a>.</p>
<h2>Deine Rechte</h2>
<p>Du hast das Recht auf Auskunft, Berichtigung, Löschung und Einschränkung der Verarbeitung deiner Daten sowie ein Beschwerderecht bei einer Datenschutz-Aufsichtsbehörde. Schreib dafür einfach an {e(seite['email'])}.</p>
</div>"""
    return rahmen("Jan Brockmann - Datenschutz", inhalt, 1, aktiv="datenschutz")


def main():
    if RAUS.exists():
        shutil.rmtree(RAUS)
    RAUS.mkdir()
    shutil.copy(HIER / "vorlage" / "stil.css", RAUS / "stil.css")
    shutil.copytree(HIER / "schrift", RAUS / "schrift")
    if (HIER / "CNAME").exists():
        shutil.copy(HIER / "CNAME", RAUS / "CNAME")
    if (HIER / "bilder").exists():
        shutil.copytree(HIER / "bilder", RAUS / "bilder")
    schreibe("", startseite())
    schreibe("work-1", startseite(1))
    for i, p in enumerate(projekte):
        schreibe(p["slug"], projektseite(i, p))
    schreibe("about", aboutseite())
    schreibe("impressum", impressum())
    schreibe("datenschutz", datenschutz())
    (RAUS / "404.html").write_text(
        rahmen("Jan Brockmann", f'<div class="text gross"><p>Diese Seite gibt es nicht. <a href="{link("", 0)}">Zu den Filmen</a></p></div>', 0),
        encoding="utf-8")
    print(f"Fertig: {len(projekte)} Filme -> {RAUS}{' (lokale Vorschau)' if LOKAL else ''}")


if __name__ == "__main__":
    main()
