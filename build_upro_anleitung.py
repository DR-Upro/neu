#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut die UPRO-gebrandete Version der Anleitung
"Claude Cowork & Claude Code" als PDF.
Design: Upro-Capital-/AI-World-Stil – Schwarz + Gold (Luxury).
Quelle-Inhalt: Herr-Tech-Original -> Re-Brand.
"""

from fpdf import FPDF

# ---------------------------------------------------------------------------
# UPRO Design-System  (Schwarz + Gold)
# ---------------------------------------------------------------------------
BG       = (12, 12, 12)       # #0C0C0C  Seiten-Hintergrund
PANEL    = (26, 26, 26)       # #1A1A1A  Karten
PANEL2   = (20, 20, 20)       # #141414  Prompt-/Boxen-Fill
GOLD     = (228, 184, 121)    # #E4B879  Akzent / Headlines
GOLD_DIM = (122, 98, 54)      # #7A6236  Rahmen / Linien (gedämpft)
LINE     = (58, 50, 38)       # #3A3226  sehr subtile Linien
TEXT     = (206, 206, 206)    # #CECECE  Fliesstext
MUTED    = (140, 140, 140)    # #8C8C8C  Sekundärtext
WHITE    = (244, 244, 244)    # #F4F4F4  Titel
DARK     = (12, 12, 12)       # Text auf Gold

BRAND_L1 = "Upro Capital"
BRAND_L2 = ". AI World"
SITE     = "hub.upro-capital.com"
AUTOR    = "Dr. Upro"
VERSION  = "Version: Juni 2026"

PAGE_W, PAGE_H = 210, 297          # A4
M = 16
CW = PAGE_W - 2 * M

FREG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FBLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FMON = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FSER = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FSEB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
ASSET = "/home/user/neu/assets/"


class UPRO(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(False)
        self.set_margins(M, M, M)
        self.add_font("DJ", "", FREG)
        self.add_font("DJ", "B", FBLD)
        self.add_font("MO", "", FMON)
        self.add_font("SE", "", FSER)
        self.add_font("SE", "B", FSEB)

    # -- Voller schwarzer Hintergrund + Kopf-/Fusszeile ---------------------
    def header(self):
        self.set_fill_color(*BG)
        self.rect(0, 0, PAGE_W, PAGE_H, style="F")
        if self.page_no() == 1:
            return
        # Wortmarke oben rechts
        self.set_font("SE", "B", 9.5)
        self.set_text_color(*GOLD)
        self.set_xy(M, 9)
        self.cell(CW, 5, BRAND_L1, align="R")
        self.set_font("DJ", "", 7)
        self.set_text_color(*GOLD_DIM)
        self.set_xy(M, 14)
        self.cell(CW, 4, BRAND_L2, align="R")

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_draw_color(*LINE)
        self.set_line_width(0.3)
        self.line(M, PAGE_H - 14, PAGE_W - M, PAGE_H - 14)
        self.set_font("DJ", "", 8)
        self.set_text_color(*MUTED)
        self.set_xy(M, PAGE_H - 12)
        self.cell(CW / 2, 5, SITE, align="L")
        self.set_xy(M + CW / 2, PAGE_H - 12)
        self.cell(CW / 2, 5, f"Seite {self.page_no()}", align="R")

    # -- Bausteine -----------------------------------------------------------
    def rrect(self, x, y, w, h, r, fill=None, draw=None, lw=0.4):
        style = ""
        if fill is not None:
            self.set_fill_color(*fill)
            style += "F"
        if draw is not None:
            self.set_draw_color(*draw)
            self.set_line_width(lw)
            style += "D"
        self.rect(x, y, w, h, style=style, round_corners=True, corner_radius=r)

    def card(self, x, y, w, h, r=2.5):
        """Dunkle Karte mit goldener Oberkante."""
        self.rrect(x, y, w, h, r, fill=PANEL)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.7)
        self.line(x + r, y + 0.35, x + w - r, y + 0.35)

    def gold_num(self, n, x, y, d=7):
        self.set_fill_color(*GOLD)
        self.ellipse(x, y, d, d, style="F")
        self.set_font("DJ", "B", 9)
        self.set_text_color(*DARK)
        self.set_xy(x, y + 0.4)
        self.cell(d, d, str(n), align="C")

    def kicker(self, txt):
        self.set_font("DJ", "B", 8.5)
        self.set_text_color(*GOLD_DIM)
        self.cell(0, 5, txt.upper(), align="L", new_x="LMARGIN", new_y="NEXT")

    def h1(self, txt):
        self.set_font("DJ", "B", 22)
        self.set_text_color(*GOLD)
        self.cell(0, 11, txt, align="L", new_x="LMARGIN", new_y="NEXT")

    def lead(self, txt):
        self.set_font("DJ", "", 10.5)
        self.set_text_color(*MUTED)
        self.multi_cell(CW, 5.6, txt, align="L", new_x="LMARGIN", new_y="NEXT")

    def h2(self, txt):
        self.set_font("DJ", "B", 13.5)
        self.set_text_color(*GOLD)
        self.cell(0, 8, txt, align="L", new_x="LMARGIN", new_y="NEXT")

    def body(self, txt, w=CW, gap=5.2, size=10):
        self.set_font("DJ", "", size)
        self.set_text_color(*TEXT)
        self.multi_cell(w, gap, txt, align="L", new_x="LMARGIN", new_y="NEXT")


def diamond(pdf, cx, cy, r, lw=0.5):
    pdf.set_draw_color(*GOLD_DIM)
    pdf.set_line_width(lw)
    pdf.line(cx, cy - r, cx + r, cy)
    pdf.line(cx + r, cy, cx, cy + r)
    pdf.line(cx, cy + r, cx - r, cy)
    pdf.line(cx - r, cy, cx, cy - r)


def diamond_cluster(pdf, x, y):
    """Geometrisches Rauten-Motiv wie auf dem UPRO-Cover."""
    diamond(pdf, x, y, 13)
    diamond(pdf, x + 17, y + 5, 9)
    diamond(pdf, x - 9, y + 16, 7)
    diamond(pdf, x + 11, y + 21, 5)


def numbered_step(pdf, n, title, txt, x, y, w):
    d = 7.5
    pdf.gold_num(n, x, y, d)
    tx = x + d + 4
    tw = w - d - 4
    pdf.set_xy(tx, y - 0.5)
    pdf.set_font("DJ", "B", 10.5)
    pdf.set_text_color(*WHITE)
    pdf.multi_cell(tw, 5.2, title, align="L", new_x="LEFT", new_y="NEXT")
    pdf.set_x(tx)
    pdf.set_font("DJ", "", 9.3)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(tw, 4.8, txt, align="L", new_x="LMARGIN", new_y="NEXT")
    return max(pdf.get_y(), y + d) + 3.5


def figure(pdf, img, ratio, img_w, caption, top=None):
    """Gerahmter Screenshot mit Bildunterschrift. Gibt neue y zurück."""
    if top is None:
        top = pdf.get_y()
    pad = 3
    h = img_w * ratio
    fw = img_w + 2 * pad
    fh = h + 2 * pad
    fx = M + (CW - fw) / 2
    pdf.rrect(fx, top, fw, fh, 2.5, fill=PANEL2, draw=GOLD_DIM, lw=0.4)
    pdf.image(img, fx + pad, top + pad, img_w, h)
    pdf.set_xy(M, top + fh + 2.5)
    pdf.set_font("DJ", "", 8.2)
    pdf.set_text_color(*MUTED)
    pdf.cell(CW, 4, caption, align="C")
    return top + fh + 9


def step_line(pdf, n, txt, x, w):
    """Kompakte nummerierte Zeile (für Prompt-Workflows)."""
    cy = pdf.get_y()
    pdf.set_font("DJ", "B", 8.8)
    pdf.set_text_color(*GOLD)
    pdf.set_xy(x, cy)
    pdf.cell(6, 4.8, str(n) + ".")
    pdf.set_xy(x + 6, cy)
    pdf.set_font("DJ", "", 9.3)
    pdf.set_text_color(*TEXT)
    pdf.multi_cell(w - 6, 4.8, txt, align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(0.8)


def bullet(pdf, txt, x, w, mark=">"):
    cy = pdf.get_y()
    pdf.set_text_color(*GOLD)
    pdf.set_font("DJ", "B", 9.5)
    pdf.set_xy(x, cy)
    pdf.cell(5, 4.9, mark)
    pdf.set_xy(x + 5, cy)
    pdf.set_font("DJ", "", 9.6)
    pdf.set_text_color(*TEXT)
    pdf.multi_cell(w - 5, 4.9, txt, align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1.1)


def wrap_mono(pdf, text, max_w):
    pdf.set_font("MO", "", 8.4)
    out, cur = [], ""
    for wd in text.split(" "):
        test = (cur + " " + wd).strip()
        if pdf.get_string_width(test) <= max_w:
            cur = test
        else:
            if cur:
                out.append(cur)
            cur = wd
    if cur:
        out.append(cur)
    return out or [""]


def prompt_box(pdf, lines, x, y, w, label="PROMPT"):
    inner = w - 12
    wrapped = []
    for ln in lines:
        wrapped += wrap_mono(pdf, ln, inner)
    line_h = 4.4
    h = 8.5 + len(wrapped) * line_h + 4
    pdf.rrect(x, y, w, h, 2.5, fill=PANEL2, draw=GOLD_DIM, lw=0.4)
    pdf.set_xy(x + 6, y + 3)
    pdf.set_font("DJ", "B", 7.8)
    pdf.set_text_color(*GOLD)
    pdf.cell(0, 4, label.upper())
    yy = y + 8.5
    pdf.set_font("MO", "", 8.4)
    pdf.set_text_color(*TEXT)
    for ln in wrapped:
        pdf.set_xy(x + 6, yy)
        pdf.cell(inner, line_h, ln)
        yy += line_h
    return y + h + 4


def tip(pdf, label, txt, x, y, w):
    pdf.set_font("DJ", "", 9.3)
    lines = pdf.multi_cell(w - 12, 4.7, txt, align="L", dry_run=True, output="LINES")
    h = 9.5 + len(lines) * 4.7 + 3
    pdf.rrect(x, y, w, h, 2.5, fill=PANEL2, draw=GOLD_DIM, lw=0.4)
    pdf.set_xy(x + 6, y + 3)
    pdf.set_font("DJ", "B", 7.8)
    pdf.set_text_color(*GOLD)
    pdf.cell(0, 4, label.upper())
    pdf.set_xy(x + 6, y + 8.5)
    pdf.set_font("DJ", "", 9.3)
    pdf.set_text_color(*TEXT)
    pdf.multi_cell(w - 12, 4.7, txt, align="L")
    return y + h + 4


# ===========================================================================
pdf = UPRO()

# ---------- SEITE 1 : COVER ------------------------------------------------
pdf.add_page()
pdf.set_fill_color(*BG)
pdf.rect(0, 0, PAGE_W, PAGE_H, style="F")
diamond_cluster(pdf, 168, 30)
diamond_cluster(pdf, 36, 232)

# Wortmarke
pdf.set_xy(0, 66)
pdf.set_font("SE", "B", 27)
wU = pdf.get_string_width("Upro ")
wC = pdf.get_string_width("Capital")
pdf.set_font("DJ", "", 13)
wAI = pdf.get_string_width(" · AI World")
pdf.set_font("SE", "B", 27)
total = wU + wC + wAI
sx = (PAGE_W - total) / 2
pdf.set_xy(sx, 66)
pdf.set_text_color(*GOLD)
pdf.cell(wU, 13, "Upro ")
pdf.set_x(sx + wU)
pdf.set_text_color(228, 200, 150)
pdf.cell(wC, 13, "Capital")
pdf.set_font("DJ", "", 13)
pdf.set_text_color(*GOLD)
pdf.set_xy(sx + wU + wC, 69.5)
pdf.cell(wAI, 9, " · AI World")
# Tagline THE AI ADVANTAGE (gesperrt)
pdf.set_font("DJ", "", 8)
pdf.set_text_color(*GOLD_DIM)
pdf.set_xy(M, 82)
pdf.cell(CW, 5, "T H E   A I   A D V A N T A G E", align="C")

# Tagline-Zeile
pdf.set_font("DJ", "", 11)
pdf.set_text_color(*MUTED)
pdf.set_xy(M, 100)
pdf.cell(CW, 6, "Understand   .   Predict   .   Research   .   Own", align="C")
# Gold-Divider
pdf.set_draw_color(*GOLD)
pdf.set_line_width(0.6)
pdf.line(PAGE_W / 2 - 28, 113, PAGE_W / 2 + 28, 113)

# Titel
pdf.set_xy(M, 120)
pdf.set_font("DJ", "B", 36)
pdf.set_text_color(*WHITE)
pdf.cell(CW, 16, "Claude Cowork", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_x(M)
pdf.cell(CW, 16, "& Claude Code", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(3)
pdf.set_x(M)
pdf.set_font("DJ", "", 14)
pdf.set_text_color(*GOLD)
pdf.cell(CW, 9, "Dein neues Betriebssystem. Punkt.", align="C")

# Fuss
pdf.set_xy(M, 250)
pdf.set_font("DJ", "", 10)
pdf.set_text_color(*MUTED)
pdf.cell(CW, 6, f"Erstellt von {AUTOR}   |   {VERSION}", align="C",
         new_x="LMARGIN", new_y="NEXT")
pdf.ln(1)
pdf.set_x(M)
pdf.set_font("DJ", "B", 10)
pdf.set_text_color(*GOLD)
pdf.cell(CW, 6, SITE, align="C")

# ---------- SEITE 2 : Was ist Claude --------------------------------------
pdf.add_page()
pdf.set_y(24)
pdf.kicker("Grundlagen")
pdf.h1("Was ist Claude?")
pdf.lead("Claude ist der KI-Agent von Anthropic. Nicht ChatGPT, nicht Gemini – "
         "Claude. Das Werkzeug, das gerade alles verändert. Drei Bereiche "
         "musst du kennen:")
pdf.ln(2)

cards = [
    ("1", "Chat", "Wie ChatGPT – nur besser",
     "Texte, Fragen, Konversation. Dein täglicher KI-Assistent."),
    ("2", "Cowork", "Dein Agent auf deinem Rechner",
     "Erstellt Dateien, recherchiert, automatisiert. Greift auf deine "
     "Ordner zu. Arbeitet für dich."),
    ("3", "Claude Code", "Dein eigener Entwickler",
     "Baut Websites, Tools und komplette Anwendungen. Null Code von dir nötig."),
]
cy = pdf.get_y()
gap = 5
cw = (CW - 2 * gap) / 3
ch = 52
for i, (n, t, sub, d) in enumerate(cards):
    cx = M + i * (cw + gap)
    pdf.card(cx, cy, cw, ch)
    pdf.gold_num(n, cx + 5, cy + 6)
    pdf.set_xy(cx + 15, cy + 6.6)
    pdf.set_font("DJ", "B", 11)
    pdf.set_text_color(*GOLD)
    pdf.cell(0, 6, t)
    pdf.set_xy(cx + 5, cy + 16)
    pdf.set_font("DJ", "B", 8.4)
    pdf.set_text_color(*WHITE)
    pdf.multi_cell(cw - 10, 4.2, sub, align="L")
    pdf.set_xy(cx + 5, cy + 25)
    pdf.set_font("DJ", "", 8.6)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(cw - 10, 4.3, d, align="L")
pdf.set_y(cy + ch + 6)

pdf.set_y(tip(pdf, "Tipp · Einfach fragen",
              "Wenn du nicht weiterkommst: Frag Claude direkt. Beschreibe dein "
              "Problem in normaler Sprache – Claude hilft dir sofort. Kein "
              "langes Rätseln, kein Googeln.", M, pdf.get_y(), CW))

pdf.ln(1)
pdf.h2("Warum Claude und nicht ChatGPT?")
for b in [
    "Claude führt Code aus, bearbeitet Dateien, greift auf dein System zu – nicht nur Text.",
    "Cowork arbeitet für dich, nicht nur mit dir.",
    "Claude Code ersetzt einen Entwickler: keine Wartezeiten, keine 5-stelligen Rechnungen.",
    "Anthropic wächst schneller als OpenAI. Kein Hype – das ist Momentum.",
]:
    bullet(pdf, b, M, CW)

pdf.ln(1)
pdf.set_y(tip(pdf, "Ziel dieser Anleitung",
              "Du richtest Claude Cowork + Claude Code als dein neues "
              "Betriebssystem ein. Schritt für Schritt. Nach 20 Minuten bist "
              "du live.", M, pdf.get_y(), CW))

# ---------- SEITE 3 : Cowork einrichten -----------------------------------
pdf.add_page()
pdf.set_y(24)
pdf.kicker("Setup")
pdf.h1("Claude Cowork einrichten")
pdf.lead("Zwei Dinge brauchst du: die Desktop-App und einen bezahlten Plan. "
         "5 Minuten – dann läuft es.")
pdf.ln(2)
pdf.h2("Schritt-für-Schritt Setup")
y = pdf.get_y() + 1
steps = [
    ("App herunterladen", "claude.com/download → Desktop-App für Mac oder Windows laden und installieren."),
    ("Pro Plan buchen", "Mindestens Pro ($20/Monat). Für intensive Nutzung: Max ($100/Monat)."),
    ("Cowork-Tab öffnen", "Desktop-App öffnen → drei Tabs oben: Chat, Cowork, Code → auf „Cowork“ klicken."),
    ("Ordner auswählen", "Lege einen Ordner „Claude Cowork“ auf dem Desktop an und wähle ihn in der App aus – Claude greift dann darauf zu."),
    ("Modell wählen", "Komplexe Aufgaben: „Opus 4.6“. Einfache Tasks: „Sonnet 4.6“ (spart Credits)."),
]
for i, (t, d) in enumerate(steps, 1):
    y = numbered_step(pdf, i, t, d, M, y, CW)
pdf.set_y(y + 1)

pdf.h2("Welcher Plan ist der richtige?")
py = pdf.get_y()
pw = (CW - 6) / 2
ph = 48
for col, (name, price, items, hot) in enumerate([
    ("Pro Plan", "$20/Monat",
     ["Cowork & Claude Code verfügbar", "Sonnet- + Opus-Modelle",
      "Begrenzte Credits täglich", "Ideal zum Starten"], False),
    ("Max Plan", "$100/Monat",
     ["Alles aus Pro", "Deutlich mehr Credit-Kapazität",
      "Prioritäts-Zugang", "Für intensive tägliche Nutzung"], True),
]):
    cx = M + col * (pw + 6)
    pdf.rrect(cx, py, pw, ph, 3, fill=PANEL if hot else PANEL2,
              draw=GOLD if hot else GOLD_DIM, lw=0.5 if hot else 0.4)
    pdf.set_xy(cx, py + 6)
    pdf.set_font("DJ", "B", 12)
    pdf.set_text_color(*WHITE)
    pdf.cell(pw, 6, name, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(cx)
    pdf.set_font("DJ", "B", 19)
    pdf.set_text_color(*GOLD)
    pdf.cell(pw, 11, price, align="C")
    iy = py + 27
    for it in items:
        pdf.set_xy(cx + 8, iy)
        pdf.set_font("DJ", "B", 9)
        pdf.set_text_color(*GOLD)
        pdf.cell(4, 4.6, "+")
        pdf.set_xy(cx + 13, iy)
        pdf.set_font("DJ", "", 8.8)
        pdf.set_text_color(*TEXT)
        pdf.cell(pw - 18, 4.6, it)
        iy += 5.2

pdf.set_y(py + ph + 8)
figure(pdf, ASSET + "shot_cowork.png", 0.65, 88,
       "So sieht die Ordner-Auswahl in Claude Cowork aus")

# ---------- SEITE 4 : Ordnerstruktur --------------------------------------
pdf.add_page()
pdf.set_y(24)
pdf.kicker("Struktur")
pdf.h1("Die Ordnerstruktur")
pdf.lead("Dein Ordner ist das Herzstück. Wie du ihn aufbaust, entscheidet, wie "
         "gut Claude für dich arbeitet. Hier die Struktur, die funktioniert:")
pdf.ln(2)

folders = [
    ("ABOUT ME", "Wichtigste! Claude liest diese Dateien vor jeder Aufgabe.", True),
    ("OUTPUTS", "Hier speichert Claude alle Ergebnisse und Deliverables.", False),
    ("TEMPLATES", "Deine besten Vorlagen – Claude speichert sie auf Abruf.", False),
]
fy = pdf.get_y()
for name, desc, star in folders:
    pdf.rrect(M, fy, CW, 13, 2.5, fill=PANEL)
    pdf.set_fill_color(*GOLD)
    pdf.rect(M, fy + 2, 2.4, 9, style="F")
    pdf.set_xy(M + 8, fy + 2.4)
    pdf.set_font("DJ", "B", 10.5)
    pdf.set_text_color(*GOLD)
    pdf.cell(45, 4.5, (("★ " if star else "") + name + "/"))
    pdf.set_xy(M + 62, fy + 2.4)
    pdf.set_font("DJ", "", 9)
    pdf.set_text_color(*TEXT)
    pdf.multi_cell(CW - 70, 4.5, desc, align="L")
    fy += 16
pdf.set_y(fy)

pdf.h2("ABOUT ME – Die drei Kern-Dateien")
pdf.body("In diesem Ordner liegen genau drei Dateien. Sie sind die einzigen, "
         "die Claude automatisch vor jeder Session liest:")
pdf.ln(1)
files = [
    ("about-me.md", "Wer du bist, wie du arbeitest, was gute Ergebnisse für dich bedeuten."),
    ("anti-ai-writing-style.md", "Dein Schreibstil: verbotene Wörter, Muster und Formatierungsregeln."),
    ("my-company.md", "Deine Ziele, Strategie und Fokus – was du gerade anstrebst."),
]
fy = pdf.get_y()
fw = (CW - 2 * 5) / 3
fh = 35
for i, (fn, d) in enumerate(files):
    fx = M + i * (fw + 5)
    pdf.card(fx, fy, fw, fh)
    pdf.set_xy(fx + 4, fy + 6)
    pdf.set_font("MO", "", 8.0)
    pdf.set_text_color(*GOLD)
    pdf.multi_cell(fw - 8, 4.2, fn)
    pdf.set_xy(fx + 4, fy + 15)
    pdf.set_font("DJ", "", 8.4)
    pdf.set_text_color(*TEXT)
    pdf.multi_cell(fw - 8, 4.1, d)
pdf.set_y(fy + fh + 5)

pdf.set_y(tip(pdf, "Wichtig · Kurz & präzise halten",
              "Claude liest den ABOUT-ME-Ordner vor JEDER Aufgabe. Halte die "
              "Gesamtgröße unter 6.000 Zeichen (ca. 3 Seiten Text). Je kürzer "
              "und präziser, desto besser versteht Claude dich.",
              M, pdf.get_y(), CW))
pdf.ln(1)
figure(pdf, ASSET + "shot_finder.png", 0.4667, 120,
       "Dein Claude Cowork Ordner im Finder mit den drei Unterordnern")

# ---------- SEITE 5 : Kern-Dateien Teil 1 ---------------------------------
pdf.add_page()
pdf.set_y(24)
pdf.kicker("Kern-Dateien · Teil 1")
pdf.h1("about-me.md & Schreibstil")
pdf.ln(1)
pdf.h2("Datei 1: about-me.md")
pdf.body("Die wichtigste Datei. Wer du bist, wie du arbeitest, was gute "
         "Ergebnisse für dich bedeuten. Claude liest sie vor jeder Aufgabe – "
         "dein digitales Briefing.")
pdf.ln(1.5)
pdf.set_font("DJ", "B", 9.5)
pdf.set_text_color(*WHITE)
pdf.cell(0, 5.5, "So erstellst du deine about-me.md:", new_x="LMARGIN", new_y="NEXT")
pdf.ln(1)
step_line(pdf, 1, "Öffne eine neue Cowork-Session (Opus 4.6 + Extended Thinking wählen).", M, CW)
step_line(pdf, 2, "Füge folgenden Prompt ein und lass Claude dich interviewen:", M, CW)
pdf.set_y(prompt_box(pdf, [
    "Baue meine about-me.md Datei für meinen Cowork-Ordner.",
    "Interviewe mich mit 20 Fragen (eine nach der anderen).",
    "Fasse meine Antworten danach in einer kompakten Datei",
    "unter 6.000 Zeichen zusammen.",
    "Speichere sie als about-me.md im Ordner ABOUT ME/.",
], M, pdf.get_y(), CW, label="Prompt · about-me.md"))
step_line(pdf, 3, "Beantworte die Fragen per Sprache oder tippe sie ein.", M, CW)
step_line(pdf, 4, "Claude erstellt die fertige Datei direkt in deinem ABOUT-ME-Ordner.", M, CW)

pdf.ln(1)
pdf.h2("Datei 2: anti-ai-writing-style.md")
pdf.body("Du hasst KI-Texte. Wir auch. Diese Datei definiert verbotene Wörter, "
         "störende Satzmuster und Formatierungsregeln. Damit schreibt Claude "
         "wie du – nicht wie ein Roboter.")
pdf.ln(1)
pdf.set_font("DJ", "B", 9.5)
pdf.set_text_color(*WHITE)
pdf.cell(0, 5.5, "Was rein gehört:", new_x="LMARGIN", new_y="NEXT")
pdf.ln(1)
for b in [
    "Verbotene Wörter (z. B. „synergieren“, „nahtlos“, „revolutionär“, „transformativ“)",
    "Verbotene Muster (z. B. „Das ist nicht X – das ist Y.“, „In einer Welt, in der…“)",
    "Formatierungsregeln (z. B. max. 3 Sätze pro Absatz, keine Bullet-Points ohne Kontext)",
    "Dein bevorzugter Ton (direkt, locker, wie eine WhatsApp an einen CEO)",
]:
    bullet(pdf, b, M, CW)

pdf.ln(1)
pdf.set_y(tip(pdf, "Tipp · Einfach anfangen",
              "Schreibe 10 Wörter auf, die dich in KI-Texten am meisten "
              "stören. Ergänze die Datei schrittweise. Je mehr drinsteht, "
              "desto mehr klingt Claude wie du.", M, pdf.get_y(), CW))

# ---------- SEITE 6 : Kern-Dateien Teil 2 ---------------------------------
pdf.add_page()
pdf.set_y(24)
pdf.kicker("Kern-Dateien · Teil 2")
pdf.h1("my-company.md & Global Instructions")
pdf.ln(1)
pdf.h2("Datei 3: my-company.md")
pdf.body("Deine Ziele, Strategie, Fokus. Was willst du dieses Jahr? Welche "
         "Plattformen? Wozu sagst du „Nein“? Ohne Kontext gibt Claude "
         "generische Antworten – mit Kontext wird es dein Sparring-Partner.")
pdf.ln(1)
pdf.set_font("DJ", "B", 9.5)
pdf.set_text_color(*WHITE)
pdf.cell(0, 5.5, "Erstellen in der gleichen Session wie about-me:",
         new_x="LMARGIN", new_y="NEXT")
pdf.ln(1)
py = pdf.get_y()
left_w = CW * 0.5 - 3
prompt_box(pdf, [
    "Erstelle jetzt meine my-company.md Datei.",
    "Stelle mir 6–8 Fragen zu meinen Zielen,",
    "meiner Strategie und meinem aktuellen Fokus.",
    "Halte die Datei unter 3.000 Zeichen.",
    "Speichere als my-company.md in ABOUT ME/.",
], M, py, left_w, label="Prompt · my-company.md")
tiles = [
    ("Ziele", "Top 2–3 Ziele mit konkreten Zahlen."),
    ("Fokus jetzt", "Womit verbringst du gerade die meiste Energie?"),
    ("Nein sagen", "Trends & Anfragen, die du aktiv ablehnst."),
    ("Deine Wette", "Worauf setzt du, was andere noch nicht sehen?"),
]
tx = M + CW * 0.5 + 3
tw = (CW * 0.5 - 3 - 4) / 2
th = 19
for i, (t, d) in enumerate(tiles):
    r, c = divmod(i, 2)
    cx = tx + c * (tw + 4)
    cyy = py + r * (th + 4)
    pdf.card(cx, cyy, tw, th, r=2)
    pdf.set_xy(cx + 3, cyy + 3)
    pdf.set_font("DJ", "B", 9)
    pdf.set_text_color(*GOLD)
    pdf.cell(0, 4, t)
    pdf.set_xy(cx + 3, cyy + 7.5)
    pdf.set_font("DJ", "", 7.8)
    pdf.set_text_color(*TEXT)
    pdf.multi_cell(tw - 6, 3.7, d)
pdf.set_y(py + 50)

pdf.h2("Global Instructions einrichten")
pdf.body("Einmal einrichten, für immer profitieren. Global Instructions sind "
         "dein permanentes Briefing – Claude liest sie vor jeder Aufgabe. "
         "Öffne: Einstellungen → Cowork → Global Instructions.")
pdf.ln(1)
pdf.set_y(prompt_box(pdf, [
    "Lies vor jeder Aufgabe alle Dateien in ABOUT ME/.",
    "Lies OUTPUTS/ und TEMPLATES/ NUR auf expliziten Verweis.",
    "Speichere Ergebnisse in OUTPUTS/ (Unterordner).",
    "Bei unklarem Auftrag: Frage nach, bevor du startest.",
], M, pdf.get_y(), CW, label="Global Instructions"))
pdf.ln(1)
figure(pdf, ASSET + "shot_p6.png", 0.5826, 100,
       "Einstellungen → Cowork → Global Instructions")

# ---------- SEITE 7 : Credits sparen --------------------------------------
pdf.add_page()
pdf.set_y(24)
pdf.kicker("Effizienz")
pdf.h1("Credits clever sparen")
pdf.lead("Credits sind dein Guthaben bei Claude. Lange Konversationen werden "
         "exponentiell teurer. Diese 6 Tricks sparen dir bis zu 80 % deiner "
         "Kosten.")
pdf.ln(2)
tricks = [
    ("Konversation neustarten", "Jede Nachricht lässt Claude die ganze Historie neu lesen. „Restart from here“ statt unten weiterschreiben.", "bis zu 95 % in langen Sessions"),
    ("Neue Session alle 20 Nachrichten", "Zusammenfassung erstellen lassen, kopieren, neu starten und als erste Nachricht einfügen. Kontext bleibt, Aufblähung ist weg.", "eliminiert Kontext-Aufblähung"),
    ("Aufgaben bündeln", "Drei Prompts = dreifache Kontext-Ladung. Ein Prompt mit drei Aufgaben = einmalige Ladung.", "bis zu 3× weniger Verbrauch"),
    ("Sonnet für einfache Tasks", "Grammatik, Brainstorming, Formatierung → Sonnet. Opus nur für tiefes Denken. Sonnet kostet 60–80 % weniger.", "bis zu 80 % Kostenersparnis"),
    ("ABOUT ME kurz halten", "Über 6.000 Zeichen liest Claude nur Zusammenfassungen. Ziel: alle Dateien zusammen darunter.", "bessere Qualität + weniger Kosten"),
    ("Arbeit über den Tag verteilen", "Claude nutzt ein rollendes 5-Stunden-Fenster. 2–3 Sessions verteilt maximieren dein Tageslimit.", "maximale tägliche Kapazität"),
]
gy = pdf.get_y()
gw = (CW - 6) / 2
gh = 36
for i, (t, d, save) in enumerate(tricks):
    r, c = divmod(i, 2)
    cx = M + c * (gw + 6)
    cyy = gy + r * (gh + 5)
    pdf.card(cx, cyy, gw, gh)
    pdf.gold_num(i + 1, cx + 5, cyy + 6)
    pdf.set_xy(cx + 15, cyy + 5)
    pdf.set_font("DJ", "B", 10)
    pdf.set_text_color(*GOLD)
    pdf.multi_cell(gw - 20, 4.6, t)
    pdf.set_xy(cx + 5, cyy + 15)
    pdf.set_font("DJ", "", 8.4)
    pdf.set_text_color(*TEXT)
    pdf.multi_cell(gw - 10, 4.0, d)
    pdf.set_font("DJ", "B", 7.6)
    pw_pill = min(pdf.get_string_width("→ " + save) + 6, gw - 10)
    pdf.rrect(cx + 5, cyy + gh - 8, pw_pill, 5.5, 2.2, fill=PANEL2, draw=GOLD_DIM, lw=0.3)
    pdf.set_xy(cx + 5, cyy + gh - 8)
    pdf.set_text_color(*GOLD)
    pdf.cell(pw_pill, 5.5, "→ " + save, align="C")

# ---------- SEITE 8 : Claude Code -----------------------------------------
pdf.add_page()
pdf.set_y(24)
pdf.kicker("Build")
pdf.h1("Claude Code – dein Entwickler")
pdf.lead("Was früher Zehntausende Euro und Monate kostete, baust du jetzt in "
         "20 Minuten – ganz ohne Programmierkenntnisse. Du beschreibst, "
         "Claude baut.")
pdf.ln(1)
pdf.h2("Was du damit bauen kannst")
for b in [
    "Websites & Landing Pages – mit Design, Formularen und Funktionen.",
    "Custom Tools – maßgeschneiderte Anwendungen nach deiner Beschreibung.",
    "Automatisierungen – Daten verarbeiten, APIs verbinden, Workflows steuern.",
    "Komplette Systeme – Datenbanken, Dashboards, Reports per Beschreibung.",
]:
    bullet(pdf, b, M, CW)
pdf.ln(1)
pdf.h2("Einrichtung & Nutzung")
y = pdf.get_y() + 1
code_steps = [
    ("Tab „Code“ öffnen", "In der Desktop-App auf den dritten Tab klicken – beim ersten Mal wirst du durch das Setup geführt."),
    ("Terminal-Zugriff erlauben", "Claude Code braucht Zugriff auf dein Terminal. Die App fragt automatisch – einfach bestätigen."),
    ("Projekt-Ordner wählen", "Ordner auf dem Desktop anlegen (z. B. „Mein Projekt“) und auswählen. Claude legt dort alles an."),
    ("Beschreibe, was du brauchst", "So detailliert wie möglich – Deutsch oder Englisch. Je mehr Kontext, desto besser."),
    ("Claude baut automatisch", "Claude schreibt Code, richtet Dateien ein und startet die Anwendung – selbstständig."),
    ("Testen & verfeinern", "Direkt im Browser testen. Passt etwas nicht: in normaler Sprache Feedback geben."),
]
half = CW / 2 - 3
col_y = [y, y]
for i, (t, d) in enumerate(code_steps):
    c = i % 2
    cx = M + c * (half + 6)
    col_y[c] = numbered_step(pdf, i + 1, t, d, cx, col_y[c], half)
pdf.set_y(max(col_y) + 1)

pdf.set_y(prompt_box(pdf, [
    "Hey Claude, ich brauche ein Tool, in das ich einen",
    "Video-Link einfügen kann und das das Video 1:1 nachbaut –",
    "mit Transkript, Screenshots, Szenen-Vorschlägen und",
    "fertiger Video-Generierung.",
], M, pdf.get_y(), CW, label="Beispiel-Prompt"))
pdf.set_y(tip(pdf, "Das Ergebnis",
              "Vollständige Webanwendung – kein Coding, kein Entwickler, null "
              "Agentur-Kosten. Früher: 8 Wochen + 5-stelliger Betrag. Heute: "
              "1 Prompt, 20 Minuten.", M, pdf.get_y(), CW))

# ---------- SEITE 9 : Erste 20 Minuten ------------------------------------
pdf.add_page()
pdf.set_y(24)
pdf.kicker("Los geht's")
pdf.h1("Deine ersten 20 Minuten")
pdf.lead("20 Minuten. Jetzt. Blocke sie in deinem Kalender. Hier ist, was du "
         "tust:")
pdf.ln(2)
blocks = [
    ("Min 0 – 5", "App & Ordner einrichten", [
        "Desktop-App laden: claude.com/download",
        "Pro Plan buchen ($20 oder $100/Monat)",
        "Ordner „Claude Cowork/“ mit ABOUT ME/, OUTPUTS/, TEMPLATES/ anlegen",
        "App öffnen → Tab „Cowork“ → Ordner auswählen",
    ]),
    ("Min 5 – 12", "Die 3 Kern-Dateien erstellen", [
        "Neue Cowork-Session: Opus 4.6 + Extended Thinking",
        "about-me.md-Prompt einfügen → Fragen beantworten",
        "Direkt weiter: my-company.md erstellen",
        "anti-ai-writing-style.md: 10 Störwörter aufschreiben",
    ]),
    ("Min 12 – 14", "Global Instructions", [
        "Einstellungen → Cowork → Global Instructions",
        "Vorlage von Seite 6 kopieren und anpassen",
    ]),
    ("Min 14 – 20", "Erste echte Session", [
        "Neue Aufgabe starten und Auftrag beschreiben",
        "Claude liest deine Dateien, fragt nach, baut das Ergebnis",
        "Zufrieden? „Speichere das als Template in TEMPLATES/“",
    ]),
]
by = pdf.get_y()
for tag, title, items in blocks:
    h = 11 + len(items) * 4.8 + 3
    pdf.rrect(M, by, CW, h, 2.5, fill=PANEL)
    pdf.set_fill_color(*GOLD)
    pdf.rect(M, by + 2, 2.4, h - 4, style="F")
    pdf.set_font("DJ", "B", 8.5)
    pw_pill = pdf.get_string_width(tag) + 8
    pdf.rrect(M + 7, by + 3, pw_pill, 5.6, 2.5, fill=PANEL2, draw=GOLD_DIM, lw=0.3)
    pdf.set_xy(M + 7, by + 3)
    pdf.set_text_color(*GOLD)
    pdf.cell(pw_pill, 5.6, tag, align="C")
    pdf.set_xy(M + 13 + pw_pill, by + 2.6)
    pdf.set_font("DJ", "B", 10.5)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 6, title)
    iy = by + 11
    for it in items:
        pdf.set_xy(M + 9, iy)
        pdf.set_font("DJ", "B", 9)
        pdf.set_text_color(*GOLD)
        pdf.cell(4, 4.6, ">")
        pdf.set_xy(M + 13, iy)
        pdf.set_font("DJ", "", 8.8)
        pdf.set_text_color(*TEXT)
        pdf.multi_cell(CW - 19, 4.6, it)
        iy = pdf.get_y()
    by += h + 4

pdf.ln(1)
banner_y = pdf.get_y()
bh = 26
pdf.rrect(M, banner_y, CW, bh, 3, fill=PANEL, draw=GOLD, lw=0.6)
pdf.set_xy(M, banner_y + 6)
pdf.set_font("DJ", "B", 15)
pdf.set_text_color(*GOLD)
pdf.cell(CW, 8, "Du bist bereit.", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_x(M)
pdf.set_font("DJ", "", 11)
pdf.set_text_color(*TEXT)
pdf.cell(CW, 6, "Dein neues Betriebssystem wartet.   ·   " + SITE, align="C")

pdf.output("/home/user/neu/Claude_Cowork_Code_Anleitung_UPRO.pdf")
print("OK -> Claude_Cowork_Code_Anleitung_UPRO.pdf")
