# thisisjan.com

Die Seite baut sich bei jeder Änderung auf `main` automatisch (GitHub Actions) und geht über GitHub Pages online.

**Inhalte ändern:**
- Filme: `inhalt/projekte.json`. Die Reihenfolge in der Datei ist die Reihenfolge auf der Seite; für einen neuen Film einen Block kopieren.
  - `videos`: YouTube-ID(s), der Teil nach `youtu.be/` bzw. `v=`
  - `bild`: Vorschaubild (Format 5:4). Eigene Bilder als `bilder/<slug>.jpg` ablegen.
  - `stills`: Screengrabs unter dem Text (Dateinamen in `bilder/`), `breit`: welche davon groß über die ganze Breite
  - `making`: Making-of-Fotos ganz unten
- About, Kontakt, Impressum: `inhalt/seite.json`
- Farben und Schrift: `vorlage/stil.css`

**Lokal ansehen:** `python3 bauen.py --lokal`, dann `public/index.html` öffnen.

Videos laden erst nach Klick (youtube-nocookie), deshalb gibt es keine Cookies und keinen Cookie-Banner.
Schriften: Modak (Name, Menü, Kacheln) und DM Sans (Text), beide SIL Open Font License, liegen in `schrift/`.
