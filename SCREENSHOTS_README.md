# 📸 Echte Screenshots für das DeFi-Mastery-Dashboard

Das Dashboard (`Upro_Capital_DeFi_Mastery.html`) zeigt standardmäßig
stilisierte UI-Nachbauten ("Mockups"). Mit dem mitgelieferten
Playwright-Skript erzeugst du **echte Screenshots** der Plattformen.
Sobald die Bilder im Ordner `screenshots/` liegen, werden sie vom
Dashboard **automatisch** geladen und ersetzen die Mockups – ohne dass
du im HTML etwas ändern musst.

> ⚠️ Warum lokal? Die Cloud-Session, in der das Dashboard gebaut wurde,
> darf aus Sicherheitsgründen keine externen Webseiten aufrufen
> (`host_not_allowed`). Dein eigener Rechner kann das – darum läuft das
> Skript bei dir lokal.

---

## Voraussetzungen
- **Node.js 18+** (`node -v` zum Prüfen)

## In 3 Schritten

```bash
# 1. Ins Projektverzeichnis wechseln
cd /pfad/zu/neu

# 2. Einmalig: Playwright + Chromium installieren
npm run setup
#   (entspricht: npm install && npx playwright install chromium)

# 3. Screenshots erzeugen
npm run shots
#   (entspricht: node capture-screenshots.mjs)
```

Danach `Upro_Capital_DeFi_Mastery.html` im Browser öffnen – die echten
Screenshots erscheinen automatisch an den richtigen Stellen.

---

## Was wird automatisch aufgenommen?

| Datei | Quelle | Modul im Dashboard |
|------|--------|--------------------|
| `wallet-metamask.png` | metamask.io | Krypto-Grundlagen |
| `coinbase-signup.png` | coinbase.com/signup | Plattformen |
| `lido.png` | stake.lido.fi | Staking |
| `uniswap.png` | app.uniswap.org/swap | Liquidity Pools |
| `aave-supply.png` | app.aave.com/markets | Stablecoin-Income |
| `aave-dashboard.png` | app.aave.com | Lending & Borrowing |
| `revoke.png` | revoke.cash | Risikomanagement |
| `defillama.png` | defillama.com | DeFi-Tools |

## Login-geschützte Screens (manuell)
Zwei Ansichten brauchen ein eingeloggtes Konto und werden **nicht**
automatisch geschossen (sie behalten den Mockup):

- **Konto-Sicherheit / 2FA** (Coinbase-Einstellungen)
- **Börse-Trade-Screen** (Kauf-Ansicht)

Wenn du sie selbst aufnehmen willst: eingeloggt einen Screenshot machen,
als `screenshots/coinbase-security.png` bzw. `screenshots/boerse-trade.png`
speichern und die beiden Zeilen im `SHOTS`-Objekt **ganz unten in der
HTML-Datei** ergänzen, z. B.:

```js
'coinbase.com/settings/security' : 'coinbase-security.png',
'app.börse.com/trade'            : 'boerse-trade.png',
```

---

## Tipps & Fehlerbehebung
- **Eine Seite schlägt fehl / Banner stört?** Erhöhe den `wait`-Wert oder
  passe die `CONSENT`-Selektoren in `capture-screenshots.mjs` an.
- **Browser sichtbar laufen lassen** (zum Debuggen): in der Datei
  `chromium.launch({ headless: true })` auf `headless: false` ändern.
- **Andere/zusätzliche Seiten?** Einfach einen Eintrag im `TARGETS`-Array
  ergänzen und denselben Dateinamen ins `SHOTS`-Objekt der HTML schreiben.
- **dApps zeigen "Connect Wallet":** Das ist normal und didaktisch sogar
  gut – die Lernenden sehen genau den Einstiegspunkt. Für Screens nach
  dem Verbinden ggf. manuell aufnehmen (siehe oben).
