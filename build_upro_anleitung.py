#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut die UPRO-gebrandete Version der Anleitung
"Claude Cowork & Claude Code" als PDF.
Quelle: Herr-Tech-Original -> Re-Brand im Upro-Capital-/AI-World-Stil.
"""

from fpdf import FPDF

# ---------------------------------------------------------------------------
# UPRO Design-System
# ---------------------------------------------------------------------------
NAVY      = (11, 31, 58)      # #0B1F3A  Midnight / Capital
BLAU      = (31, 78, 120)     # #1F4E78  Primaer
BLAU_HELL = (46, 109, 180)    # #2E6DB4  Akzent blau
GOLD      = (201, 162, 39)    # #C9A227  Premium-Akzent
GOLD_HELL = (245, 236, 205)   # #F5ECCD
TEXT      = (26, 35, 50)      # #1A2332
MUTED     = (107, 114, 128)   # #6B7280
LINIE     = (214, 219, 227)   # #D6DBE3
BG_KARTE  = (255, 255, 255)
BG_SOFT   = (244, 246, 250)   # #F4F6FA
BG_NAVY_SOFT = (235, 240, 248)
WEISS     = (255, 255, 255)

TAGLINE   = "Understand   ·   Predict   ·   Research   ·   Own"
BRAND     = "Upro Capital · AI World"
SITE      = "hub.upro-capital.com"
AUTOR     = "Dr. Upro"
VERSION   = "Version: Juni 2026"

PAGE_W, PAGE_H = 210, 297          # A4
M = 16                              # Seitenrand
CW = PAGE_W - 2 * M                 # Inhaltsbreite

FREG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FBLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FMON = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


class UPRO(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(False)
        self.set_margins(M, M, M)
        self.add_font("DJ", "", FREG)
        self.add_font("DJ", "B", FBLD)
        self.add_font("MO", "", FMON)
        self.seite = 0

    # -- Kopf-/Fusszeile -----------------------------------------------------
    def header(self):
        if self.page_no() == 1:           # Cover hat eigenen Kopf
            return
        self.set_xy(M, 10)
        self.set_font("DJ", "B", 9)
        self.set_text_color(*BLAU)
        self.cell(self.get_string_width("Upro Capital") + 0.5, 5, "Upro Capital",
                  align="L", new_x="RIGHT", new_y="TOP")
        self.set_text_color(*GOLD)
        self.set_font("DJ", "", 9)
        self.cell(0, 5, " · AI World", align="L")
        self.set_xy(M, 10)
        self.set_font("DJ", "", 8)
        self.set_text_color(*MUTED)
        self.cell(CW, 5, SITE, align="R")
        self.set_draw_color(*LINIE)
        self.set_line_width(0.3)
        self.line(M, 17, PAGE_W - M, 17)

    def footer(self):
        if self.page_no() == 1:           # Cover bleibt clean
            return
        self.set_y(-14)
        self.set_draw_color(*LINIE)
        self.set_line_width(0.3)
        self.line(M, self.get_y(), PAGE_W - M, self.get_y())
        self.set_y(-11)
        self.set_font("DJ", "", 8)
        self.set_text_color(*MUTED)
        self.cell(CW / 2, 5, BRAND, align="L")
        self.set_x(M + CW / 2)
        self.cell(CW / 2, 5, f"Seite {self.page_no()}", align="R")

    # -- Bausteine -----------------------------------------------------------
    def rrect(self, x, y, w, h, r, fill, draw=None, lw=0.3):
        self.set_fill_color(*fill)
        if draw:
            self.set_draw_color(*draw)
            self.set_line_width(lw)
            style = "DF"
        else:
            style = "F"
        self.rect(x, y, w, h, style=style, round_corners=True, corner_radius=r)

    def kicker(self, txt):
        """Kleine goldene Sektions-Vorzeile."""
        self.set_font("DJ", "B", 8.5)
        self.set_text_color(*GOLD)
        self.cell(0, 5, txt.upper(), align="L", new_x="LMARGIN", new_y="NEXT")

    def h1(self, txt):
        self.set_font("DJ", "B", 21)
        self.set_text_color(*NAVY)
        self.cell(0, 10, txt, align="L", new_x="LMARGIN", new_y="NEXT")

    def lead(self, txt):
        self.set_font("DJ", "", 10.5)
        self.set_text_color(*MUTED)
        self.multi_cell(CW, 5.6, txt, align="L", new_x="LMARGIN", new_y="NEXT")

    def h2(self, txt, color=BLAU):
        self.set_font("DJ", "B", 13.5)
        self.set_text_color(*color)
        self.cell(0, 8, txt, align="L", new_x="LMARGIN", new_y="NEXT")

    def body(self, txt, w=CW, gap=5.2, size=10):
        self.set_font("DJ", "", size)
        self.set_text_color(*TEXT)
        self.multi_cell(w, gap, txt, align="L", new_x="LMARGIN", new_y="NEXT")


def chip_row(pdf, y):
    """Tagline-Chips fuer das Cover."""
    parts = ["Understand", "Predict", "Research", "Own"]
    pdf.set_font("DJ", "B", 9)
    gap = 4
    widths = [pdf.get_string_width(p) + 12 for p in parts]
    total = sum(widths) + gap * (len(parts) - 1)
    x = (PAGE_W - total) / 2
    for p, w in zip(parts, widths):
        pdf.set_fill_color(*NAVY)
        pdf.rect(x, y, w, 8, style="F", round_corners=True, corner_radius=4)
        pdf.set_text_color(*GOLD)
        pdf.set_xy(x, y)
        pdf.cell(w, 8, p, align="C")
        x += w + gap


def numbered_step(pdf, n, title, txt, x, y, w):
    """Schritt mit goldener Nummernscheibe. Gibt neue y-Position zurueck."""
    d = 8
    pdf.set_fill_color(*BLAU)
    pdf.ellipse(x, y, d, d, style="F")
    pdf.set_font("DJ", "B", 10)
    pdf.set_text_color(*WEISS)
    pdf.set_xy(x, y + 0.4)
    pdf.cell(d, d, str(n), align="C")
    tx = x + d + 4
    tw = w - d - 4
    pdf.set_xy(tx, y - 0.5)
    pdf.set_font("DJ", "B", 10.5)
    pdf.set_text_color(*NAVY)
    pdf.multi_cell(tw, 5.2, title, align="L", new_x="LEFT", new_y="NEXT")
    pdf.set_x(tx)
    pdf.set_font("DJ", "", 9.3)
    pdf.set_text_color(*TEXT)
    pdf.multi_cell(tw, 4.8, txt, align="L", new_x="LMARGIN", new_y="NEXT")
    return max(pdf.get_y(), y + d) + 3.5


def bullet(pdf, txt, x, w, gold=False):
    cy = pdf.get_y()
    pdf.set_text_color(*(GOLD if gold else BLAU_HELL))
    pdf.set_font("DJ", "B", 10)
    pdf.set_xy(x, cy)
    pdf.cell(5, 4.9, "›")
    pdf.set_xy(x + 5, cy)
    pdf.set_font("DJ", "", 9.6)
    pdf.set_text_color(*TEXT)
    pdf.multi_cell(w - 5, 4.9, txt, align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1.1)


def prompt_box(pdf, lines, x, y, w, label="PROMPT"):
    """Terminal-artige Prompt-Box. Gibt neue y-Position zurueck."""
    pdf.set_font("MO", "", 8.6)
    line_h = 4.4
    inner = w - 10
    wrapped = []
    for ln in lines:
        wrapped += wrap_mono(pdf, ln, inner)
    h = 9 + len(wrapped) * line_h + 4
    pdf.rrect(x, y, w, h, 2.5, NAVY)
    pdf.set_fill_color(*GOLD)
    pdf.rect(x, y, w, 6.5, style="F", round_corners=True, corner_radius=2.5)
    pdf.rect(x, y + 3.5, w, 3, style="F")
    pdf.set_xy(x + 4, y + 0.5)
    pdf.set_font("DJ", "B", 7.5)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 5.5, label)
    pdf.set_xy(x, y + 0.5)
    pdf.set_font("MO", "", 7.5)
    pdf.cell(w - 4, 5.5, "claude", align="R")
    yy = y + 8.5
    pdf.set_font("MO", "", 8.6)
    pdf.set_text_color(245, 247, 250)
    for ln in wrapped:
        pdf.set_xy(x + 5, yy)
        pdf.cell(inner, line_h, ln)
        yy += line_h
    return y + h + 4


def wrap_mono(pdf, text, max_w):
    pdf.set_font("MO", "", 8.6)
    words = text.split(" ")
    out, cur = [], ""
    for wd in words:
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


def tip(pdf, title, txt, x, y, w):
    """Goldene Tipp-Box. Gibt neue y zurueck."""
    pdf.set_font("DJ", "", 9.3)
    lines = pdf.multi_cell(w - 12, 4.7, txt, align="L", dry_run=True, output="LINES")
    h = 10 + len(lines) * 4.7 + 3
    pdf.rrect(x, y, w, h, 2.5, GOLD_HELL, draw=GOLD, lw=0.4)
    pdf.set_fill_color(*GOLD)
    pdf.rect(x, y, 2.4, h, style="F")
    pdf.set_xy(x + 6, y + 3)
    pdf.set_font("DJ", "B", 9.6)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 5, title)
    pdf.set_xy(x + 6, y + 9)
    pdf.set_font("DJ", "", 9.3)
    pdf.set_text_color(*TEXT)
    pdf.multi_cell(w - 12, 4.7, txt, align="L")
    return y + h + 4


# ===========================================================================
pdf = UPRO()

# ---------- SEITE 1 : COVER ------------------------------------------------
pdf.add_page()
pdf.set_fill_color(*NAVY)
pdf.rect(0, 0, PAGE_W, PAGE_H, style="F")
# Akzentbalken
pdf.set_fill_color(*GOLD)
pdf.rect(0, 0, PAGE_W, 3, style="F")

chip_row(pdf, 30)

pdf.set_xy(M, 92)
pdf.set_font("DJ", "B", 40)
pdf.set_text_color(*WEISS)
pdf.cell(0, 18, "Claude Cowork", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_x(M)
pdf.set_text_color(*GOLD)
pdf.cell(0, 18, "& Claude Code", align="C", new_x="LMARGIN", new_y="NEXT")

pdf.ln(4)
pdf.set_font("DJ", "", 14)
pdf.set_text_color(220, 226, 236)
pdf.cell(0, 9, "Dein neues Betriebssystem. Punkt.", align="C",
         new_x="LMARGIN", new_y="NEXT")

# Trennlinie
pdf.set_draw_color(*GOLD)
pdf.set_line_width(0.5)
pdf.line(PAGE_W / 2 - 25, 168, PAGE_W / 2 + 25, 168)

# Autor / Version Block
pdf.set_xy(M, 246)
pdf.set_font("DJ", "B", 11)
pdf.set_text_color(*WEISS)
pdf.cell(0, 6, f"Erstellt von {AUTOR}", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_x(M)
pdf.set_font("DJ", "", 10)
pdf.set_text_color(180, 190, 205)
pdf.cell(0, 6, VERSION, align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)
pdf.set_x(M)
pdf.set_font("DJ", "B", 11)
pdf.set_text_color(*GOLD)
pdf.cell(0, 6, SITE, align="C", new_x="LMARGIN", new_y="NEXT")

pdf.set_fill_color(*GOLD)
pdf.rect(0, PAGE_H - 3, PAGE_W, 3, style="F")

# ---------- SEITE 2 : Was ist Claude --------------------------------------
pdf.add_page()
pdf.set_y(24)
pdf.kicker("Grundlagen")
pdf.h1("Was ist Claude?")
pdf.lead("Claude ist der KI-Agent von Anthropic. Nicht ChatGPT, nicht Gemini – "
         "Claude. Das Werkzeug, das gerade alles verändert. Drei Bereiche "
         "musst du kennen:")
pdf.ln(2)

# 3 Karten nebeneinander
cards = [
    ("1", "Chat", "Wie ChatGPT – nur besser. Texte, Fragen, Konversation. "
                   "Dein täglicher KI-Assistent."),
    ("2", "Cowork", "Dein Agent auf deinem Rechner. Erstellt Dateien, "
                    "recherchiert, automatisiert. Arbeitet für dich."),
    ("3", "Claude Code", "Dein eigener Entwickler. Baut Websites, Tools und "
                         "komplette Anwendungen. Null Code von dir nötig."),
]
cy = pdf.get_y()
gap = 5
cw = (CW - 2 * gap) / 3
ch = 46
for i, (n, t, d) in enumerate(cards):
    cx = M + i * (cw + gap)
    pdf.rrect(cx, cy, cw, ch, 3, BG_SOFT, draw=LINIE, lw=0.3)
    pdf.set_fill_color(*GOLD)
    pdf.ellipse(cx + 5, cy + 5, 7, 7, style="F")
    pdf.set_font("DJ", "B", 9)
    pdf.set_text_color(*NAVY)
    pdf.set_xy(cx + 5, cy + 5.3)
    pdf.cell(7, 7, n, align="C")
    pdf.set_xy(cx + 5, cy + 14)
    pdf.set_font("DJ", "B", 11)
    pdf.set_text_color(*BLAU)
    pdf.cell(0, 6, t)
    pdf.set_xy(cx + 5, cy + 21)
    pdf.set_font("DJ", "", 8.6)
    pdf.set_text_color(*TEXT)
    pdf.multi_cell(cw - 10, 4.3, d, align="L")
pdf.set_y(cy + ch + 6)

pdf.set_y(tip(pdf, "Wichtiger Tipp: Einfach fragen!",
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
ph = 44
# Pro
pdf.rrect(M, py, pw, ph, 3, BG_SOFT, draw=LINIE)
pdf.set_xy(M + 6, py + 5)
pdf.set_font("DJ", "B", 12)
pdf.set_text_color(*BLAU)
pdf.cell(0, 6, "Pro Plan")
pdf.set_xy(M + 6, py + 5)
pdf.set_font("DJ", "B", 11)
pdf.set_text_color(*GOLD)
pdf.cell(pw - 12, 6, "$20/Monat", align="R")
pdf.set_xy(M + 6, py + 14)
pdf.set_font("DJ", "", 9)
pdf.set_text_color(*TEXT)
pdf.multi_cell(pw - 12, 5,
    "+  Cowork & Claude Code verfügbar\n"
    "+  Sonnet- + Opus-Modelle\n"
    "+  Begrenzte Credits täglich\n"
    "→  Ideal zum Starten")
# Max
mx = M + pw + 6
pdf.rrect(mx, py, pw, ph, 3, BG_NAVY_SOFT, draw=BLAU_HELL, lw=0.4)
pdf.set_xy(mx + 6, py + 5)
pdf.set_font("DJ", "B", 12)
pdf.set_text_color(*NAVY)
pdf.cell(0, 6, "Max Plan")
pdf.set_xy(mx + 6, py + 5)
pdf.set_font("DJ", "B", 11)
pdf.set_text_color(*GOLD)
pdf.cell(pw - 12, 6, "$100/Monat", align="R")
pdf.set_xy(mx + 6, py + 14)
pdf.set_font("DJ", "", 9)
pdf.set_text_color(*TEXT)
pdf.multi_cell(pw - 12, 5,
    "+  Alles aus Pro\n"
    "+  Deutlich mehr Credit-Kapazität\n"
    "+  Prioritäts-Zugang\n"
    "→  Für intensive tägliche Nutzung")

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
    pdf.rrect(M, fy, CW, 13, 2.5, BG_SOFT, draw=LINIE)
    pdf.set_fill_color(*(GOLD if star else BLAU))
    pdf.rect(M, fy, 2.4, 13, style="F")
    pdf.set_xy(M + 7, fy + 2.4)
    pdf.set_font("DJ", "B", 10.5)
    pdf.set_text_color(*NAVY)
    label = ("★ " if star else "") + name + "/"
    pdf.cell(45, 4.5, label)
    pdf.set_xy(M + 60, fy + 2.4)
    pdf.set_font("DJ", "", 9)
    pdf.set_text_color(*TEXT)
    pdf.multi_cell(CW - 66, 4.5, desc, align="L")
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
fh = 34
for i, (fn, d) in enumerate(files):
    fx = M + i * (fw + 5)
    pdf.rrect(fx, fy, fw, fh, 3, WEISS, draw=LINIE)
    pdf.set_fill_color(*BLAU)
    pdf.rect(fx, fy, fw, 2.4, style="F", round_corners=True, corner_radius=3)
    pdf.rect(fx, fy + 1, fw, 1.4, style="F")
    pdf.set_xy(fx + 4, fy + 5)
    pdf.set_font("MO", "", 8.2)
    pdf.set_text_color(*BLAU)
    pdf.multi_cell(fw - 8, 4.2, fn)
    pdf.set_xy(fx + 4, fy + 14)
    pdf.set_font("DJ", "", 8.4)
    pdf.set_text_color(*TEXT)
    pdf.multi_cell(fw - 8, 4.1, d)
pdf.set_y(fy + fh + 5)

pdf.set_y(tip(pdf, "Dateien kurz und präzise halten!",
              "Claude liest den ABOUT-ME-Ordner vor JEDER Aufgabe. Halte die "
              "Gesamtgröße unter 6.000 Zeichen (ca. 3 Seiten Text). Je kürzer "
              "und präziser, desto besser versteht Claude dich.",
              M, pdf.get_y(), CW))

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
pdf.ln(1)
pdf.set_y(prompt_box(pdf, [
    "Baue meine about-me.md Datei für meinen Cowork-Ordner.",
    "Interviewe mich mit 20 Fragen (eine nach der anderen).",
    "Fasse meine Antworten in einer kompakten Datei unter",
    "6.000 Zeichen zusammen und speichere sie als",
    "about-me.md im Ordner ABOUT ME/.",
], M, pdf.get_y(), CW))

pdf.ln(1)
pdf.h2("Datei 2: anti-ai-writing-style.md")
pdf.body("Du hasst KI-Texte. Wir auch. Diese Datei definiert verbotene Wörter, "
         "störende Satzmuster und Formatierungsregeln. Damit schreibt Claude "
         "wie du – nicht wie ein Roboter.")
pdf.ln(1)
pdf.set_font("DJ", "B", 9.5)
pdf.set_text_color(*NAVY)
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
pdf.set_y(tip(pdf, "Tipp: Einfach anfangen",
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
# Prompt + 4 Mini-Kacheln nebeneinander
py = pdf.get_y()
left_w = CW * 0.5 - 3
prompt_box(pdf, [
    "Erstelle jetzt meine my-company.md Datei.",
    "Stelle mir 6–8 Fragen zu meinen Zielen,",
    "meiner Strategie und meinem aktuellen Fokus.",
    "Halte die Datei unter 3.000 Zeichen.",
    "Speichere als my-company.md in ABOUT ME/.",
], M, py, left_w)
# Mini-Kacheln rechts
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
    pdf.rrect(cx, cyy, tw, th, 2.5, BG_SOFT, draw=LINIE)
    pdf.set_xy(cx + 3, cyy + 2.5)
    pdf.set_font("DJ", "B", 9)
    pdf.set_text_color(*BLAU)
    pdf.cell(0, 4, t)
    pdf.set_xy(cx + 3, cyy + 7)
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
], M, pdf.get_y(), CW))

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
    ("Neue Session alle 20 Nachrichten", "Zusammenfassung erstellen lassen, kopieren, neu starten, als erste Nachricht einfügen. Kontext bleibt, Ballast weg.", "eliminiert Kontext-Aufblähung"),
    ("Aufgaben bündeln", "Drei Prompts = dreifache Kontext-Ladung. Ein Prompt mit drei Aufgaben = einmalige Ladung.", "bis zu 3× weniger Verbrauch"),
    ("Sonnet für einfache Tasks", "Grammatik, Brainstorming, Formatierung → Sonnet. Opus nur für tiefes Denken. Sonnet kostet 60–80 % weniger.", "bis zu 80 % Kostenersparnis"),
    ("ABOUT ME kurz halten", "Über 6.000 Zeichen liest Claude nur Zusammenfassungen. Ziel: alle Dateien zusammen darunter.", "bessere Qualität + weniger Kosten"),
    ("Arbeit über den Tag verteilen", "Claude nutzt ein rollendes 5-Stunden-Fenster. 2–3 Sessions verteilt maximieren dein Tageslimit.", "maximale tägliche Kapazität"),
]
gy = pdf.get_y()
gw = (CW - 6) / 2
gh = 35
for i, (t, d, save) in enumerate(tricks):
    r, c = divmod(i, 2)
    cx = M + c * (gw + 6)
    cyy = gy + r * (gh + 5)
    pdf.rrect(cx, cyy, gw, gh, 3, WEISS, draw=LINIE)
    pdf.set_fill_color(*BLAU)
    pdf.ellipse(cx + 5, cyy + 5, 7, 7, style="F")
    pdf.set_font("DJ", "B", 9)
    pdf.set_text_color(*WEISS)
    pdf.set_xy(cx + 5, cyy + 5.3)
    pdf.cell(7, 7, str(i + 1), align="C")
    pdf.set_xy(cx + 15, cyy + 4.5)
    pdf.set_font("DJ", "B", 10)
    pdf.set_text_color(*NAVY)
    pdf.multi_cell(gw - 20, 4.6, t)
    pdf.set_xy(cx + 5, cyy + 14)
    pdf.set_font("DJ", "", 8.4)
    pdf.set_text_color(*TEXT)
    pdf.multi_cell(gw - 10, 4.0, d)
    # Save-Pill
    pdf.set_font("DJ", "B", 7.6)
    pw_pill = pdf.get_string_width("→ " + save) + 6
    pdf.set_fill_color(*GOLD_HELL)
    pdf.rect(cx + 5, cyy + gh - 8, min(pw_pill, gw - 10), 5.5, style="F",
             round_corners=True, corner_radius=2.5)
    pdf.set_xy(cx + 5, cyy + gh - 8)
    pdf.set_text_color(*NAVY)
    pdf.cell(min(pw_pill, gw - 10), 5.5, "→ " + save, align="C")

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
for i, (t, d) in enumerate(code_steps):
    r, c = divmod(i, 2)
    if c == 0 and r > 0:
        pass
# zweispaltig manuell
ys = [y, y, y]
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
], M, pdf.get_y(), CW, label="BEISPIEL-PROMPT"))
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
    pdf.rrect(M, by, CW, h, 3, BG_SOFT, draw=LINIE)
    pdf.set_fill_color(*GOLD)
    pdf.rect(M, by, 2.4, h, style="F")
    # Tag-Pill
    pdf.set_font("DJ", "B", 8.5)
    pw_pill = pdf.get_string_width(tag) + 8
    pdf.set_fill_color(*NAVY)
    pdf.rect(M + 6, by + 3, pw_pill, 5.6, style="F", round_corners=True, corner_radius=2.8)
    pdf.set_xy(M + 6, by + 3)
    pdf.set_text_color(*GOLD)
    pdf.cell(pw_pill, 5.6, tag, align="C")
    pdf.set_xy(M + 12 + pw_pill, by + 2.6)
    pdf.set_font("DJ", "B", 10.5)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 6, title)
    iy = by + 11
    for it in items:
        pdf.set_xy(M + 8, iy)
        pdf.set_font("DJ", "B", 9)
        pdf.set_text_color(*GOLD)
        pdf.cell(4, 4.6, "›")
        pdf.set_xy(M + 12, iy)
        pdf.set_font("DJ", "", 8.8)
        pdf.set_text_color(*TEXT)
        pdf.multi_cell(CW - 18, 4.6, it)
        iy = pdf.get_y()
    by += h + 4

# Abschluss-Banner
pdf.ln(1)
banner_y = pdf.get_y()
bh = 26
pdf.rrect(M, banner_y, CW, bh, 4, NAVY)
pdf.set_fill_color(*GOLD)
pdf.rect(M, banner_y, CW, 2.2, style="F", round_corners=True, corner_radius=4)
pdf.rect(M, banner_y + 1, CW, 1.2, style="F")
pdf.set_xy(M, banner_y + 6)
pdf.set_font("DJ", "B", 15)
pdf.set_text_color(*WEISS)
pdf.cell(CW, 8, "Du bist bereit.", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_x(M)
pdf.set_font("DJ", "", 11)
pdf.set_text_color(*GOLD)
pdf.cell(CW, 6, "Dein neues Betriebssystem wartet.  ·  " + SITE, align="C")

pdf.output("/home/user/neu/Claude_Cowork_Code_Anleitung_UPRO.pdf")
print("OK -> Claude_Cowork_Code_Anleitung_UPRO.pdf")
