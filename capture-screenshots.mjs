// =============================================================
//  Upro Capital · DeFi Mastery — Screenshot-Generator
//  Erstellt echte Screenshots der DeFi-Plattformen mit Playwright
//  und legt sie in ./screenshots/ ab. Das Dashboard lädt sie
//  danach automatisch (Mockups dienen nur als Fallback).
//
//  Nutzung:
//    npm install
//    npx playwright install chromium
//    node capture-screenshots.mjs
// =============================================================

import { chromium } from 'playwright';
import { mkdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUT = join(__dirname, 'screenshots');

// Welche Seiten geschossen werden. "name" MUSS zu den Dateinamen
// im Dashboard (Objekt SHOTS) passen. fullPage=false -> nur Viewport.
const TARGETS = [
  { name: 'wallet-metamask.png', url: 'https://metamask.io/',                fullPage: false, wait: 2500 },
  { name: 'coinbase-signup.png', url: 'https://www.coinbase.com/signup',     fullPage: false, wait: 3000 },
  { name: 'lido.png',            url: 'https://stake.lido.fi/',              fullPage: false, wait: 4000 },
  { name: 'uniswap.png',         url: 'https://app.uniswap.org/swap',        fullPage: false, wait: 4000 },
  { name: 'aave-supply.png',     url: 'https://app.aave.com/markets/',       fullPage: false, wait: 5000 },
  { name: 'aave-dashboard.png',  url: 'https://app.aave.com/',               fullPage: false, wait: 5000 },
  { name: 'revoke.png',          url: 'https://revoke.cash/',                fullPage: false, wait: 3500 },
  { name: 'defillama.png',       url: 'https://defillama.com/',              fullPage: true,  wait: 3500 },
];

// Typische Cookie-/Consent-Buttons wegklicken (best effort, mehrsprachig).
const CONSENT = [
  'button:has-text("Accept all")', 'button:has-text("Accept All")',
  'button:has-text("Alle akzeptieren")', 'button:has-text("Akzeptieren")',
  'button:has-text("I agree")', 'button:has-text("Got it")',
  'button:has-text("Agree")', 'button:has-text("Allow all")',
  'button:has-text("Accept cookies")', '[id*="accept" i] button',
];

async function dismissBanners(page) {
  for (const sel of CONSENT) {
    try {
      const el = page.locator(sel).first();
      if (await el.isVisible({ timeout: 800 })) {
        await el.click({ timeout: 1500 }).catch(() => {});
        await page.waitForTimeout(400);
      }
    } catch { /* ignorieren */ }
  }
}

async function main() {
  await mkdir(OUT, { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 2, // gestochen scharf (Retina)
    userAgent:
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ' +
      '(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    locale: 'de-DE',
  });

  let ok = 0, fail = 0;

  for (const t of TARGETS) {
    const page = await context.newPage();
    try {
      process.stdout.write(`→ ${t.name.padEnd(24)} ${t.url} ... `);
      await page.goto(t.url, { waitUntil: 'domcontentloaded', timeout: 45000 });
      await page.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {});
      await dismissBanners(page);
      await page.waitForTimeout(t.wait || 2500);
      await page.screenshot({ path: join(OUT, t.name), fullPage: !!t.fullPage });
      console.log('OK');
      ok++;
    } catch (err) {
      console.log('FEHLER:', err.message.split('\n')[0]);
      fail++;
    } finally {
      await page.close();
    }
  }

  await browser.close();
  console.log(`\nFertig: ${ok} erstellt, ${fail} fehlgeschlagen.`);
  console.log(`Screenshots liegen in: ${OUT}`);
  console.log('Öffne nun Upro_Capital_DeFi_Mastery.html im Browser — die Bilder erscheinen automatisch.');

  // Hinweis zu login-geschützten Screens:
  console.log(
    '\nHinweis: "Konto-Sicherheit/2FA" (Coinbase-Einstellungen) und der generische\n' +
    '"Börse-Trade"-Screen sind login-geschützt und werden NICHT automatisch geschossen.\n' +
    'Diese behalten den stilisierten Mockup. Wenn du sie eingeloggt selbst aufnimmst,\n' +
    'speichere sie als screenshots/coinbase-security.png bzw. screenshots/boerse-trade.png\n' +
    'und ergänze die Dateinamen im SHOTS-Objekt am Ende der HTML-Datei.'
  );
}

main().catch((e) => { console.error(e); process.exit(1); });
