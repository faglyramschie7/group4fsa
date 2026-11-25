#!/usr/bin/env node
/**
 * Capture crisp screenshots of all 20 presentation slides (Slides 1-14 + Appendix A1-A6)
 * and their GlassInsightModal popups (including Slide 5's dual popups) using headless Chromium CDP.
 */

import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';

const LANG = process.argv.includes('--lang=id') ? 'id' : 'en';
const DIST_DIR = path.resolve('goto-fsa-study/dist');
const OUT_DIR = path.resolve(
  LANG === 'id' ? 'outputs/speaker-notes-screenshots-id' : 'outputs/speaker-notes-screenshots'
);
const CHROME_BIN =
  '/Users/kodex/Library/Caches/ms-playwright/chromium-1234/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';
const PORT = 4179;
const CDP_PORT = 9229;

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
};

function startStaticServer() {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      const reqPath = decodeURIComponent((req.url || '/').split('?')[0]);
      let filePath = path.join(DIST_DIR, reqPath === '/' ? 'index.html' : reqPath);
      if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
        filePath = path.join(DIST_DIR, 'index.html');
      }
      const ext = path.extname(filePath).toLowerCase();
      res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
      fs.createReadStream(filePath).pipe(res);
    });
    server.listen(PORT, '127.0.0.1', () => resolve(server));
  });
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

class CDPClient {
  constructor(wsUrl) {
    this.ws = new WebSocket(wsUrl);
    this.id = 0;
    this.pending = new Map();
    this.ready = new Promise((resolve, reject) => {
      this.ws.addEventListener('open', resolve);
      this.ws.addEventListener('error', reject);
    });
    this.ws.addEventListener('message', (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        if (msg.error) reject(new Error(msg.error.message));
        else resolve(msg.result);
      }
    });
  }

  async send(method, params = {}) {
    await this.ready;
    const id = ++this.id;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async eval(expression) {
    const res = await this.send('Runtime.evaluate', {
      expression,
      returnByValue: true,
      awaitPromise: true,
    });
    if (res.exceptionDetails) {
      throw new Error(JSON.stringify(res.exceptionDetails));
    }
    return res.result?.value;
  }

  async screenshotClip(selector, outFile, pad = 4) {
    const box = await this.eval(`(() => {
      const el = document.querySelector(${JSON.stringify(selector)});
      if (!el) return null;
      const r = el.getBoundingClientRect();
      return { x: r.left, y: r.top, width: r.width, height: r.height };
    })()`);
    if (!box || box.width < 10 || box.height < 10) {
      throw new Error(`Element not found or invisible for selector: ${selector}`);
    }
    const { data } = await this.send('Page.captureScreenshot', {
      format: 'png',
      clip: {
        x: Math.max(0, box.x - pad),
        y: Math.max(0, box.y - pad),
        width: box.width + pad * 2,
        height: box.height + pad * 2,
        scale: 1,
      },
    });
    fs.writeFileSync(outFile, Buffer.from(data, 'base64'));
  }

  close() {
    this.ws.close();
  }
}

async function waitForCdpTarget() {
  for (let i = 0; i < 40; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${CDP_PORT}/json/list`);
      const list = await res.json();
      const page = list.find((t) => t.type === 'page');
      if (page?.webSocketDebuggerUrl) return page.webSocketDebuggerUrl;
    } catch {
      // retry
    }
    await sleep(250);
  }
  throw new Error('Timed out waiting for Chrome CDP target');
}

async function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const server = await startStaticServer();
  const userDataDir = `/tmp/chrome-cdp-speaker-${Date.now()}`;
  const chrome = spawn(
    CHROME_BIN,
    [
      '--headless=new',
      '--disable-gpu',
      '--no-sandbox',
      `--remote-debugging-port=${CDP_PORT}`,
      `--user-data-dir=${userDataDir}`,
      '--window-size=1480,960',
      '--force-device-scale-factor=1.5',
      `http://127.0.0.1:${PORT}/`,
    ],
    { stdio: 'ignore' }
  );

  let cdp;
  try {
    const wsUrl = await waitForCdpTarget();
    cdp = new CDPClient(wsUrl);
    await cdp.send('Page.enable');
    await cdp.send('Runtime.enable');
    await cdp.send('Emulation.setDeviceMetricsOverride', {
      width: 1480,
      height: 960,
      deviceScaleFactor: 1.5,
      mobile: false,
    });

    await sleep(900);

    // Force requested language, Presentation tab, Restated Final Report mode, Slide 1
    await cdp.eval(`(() => {
      localStorage.setItem('goto-fsa-lang', ${JSON.stringify(LANG)});
      localStorage.setItem('goto-fsa-active-tab', 'presentation');
      localStorage.setItem('goto_fsa_report_view_mode', 'restated');
      localStorage.setItem('goto-fsa-pres-slide', '1');
      return true;
    })()`);
    await cdp.send('Page.reload', { ignoreCache: true });
    await sleep(1400);

    // Ensure Presentation mode & requested language & Restated are active in live DOM
    await cdp.eval(`(() => {
      const targetRegex = ${LANG === 'id' ? '/indonesia|\\bid\\b/i' : '/english|\\ben\\b/i'};
      const btn = Array.from(document.querySelectorAll('.lang-btn')).find(b => targetRegex.test(b.textContent || ''));
      if (btn && !btn.classList.contains('active')) btn.click();
      return true;
    })()`);
    await sleep(300);

    const clickNavSlide = async (idx) => {
      const ok = await cdp.eval(`(() => {
        const items = document.querySelectorAll('.pres-nav-item');
        if (!items[${idx}]) return false;
        items[${idx}].scrollIntoView({ block: 'center' });
        items[${idx}].click();
        return true;
      })()`);
      if (!ok) throw new Error(`Could not click .pres-nav-item[${idx}]`);
      await sleep(750);
    };

    const ensureRestated = async () => {
      await cdp.eval(`(() => {
        const pills = Array.from(document.querySelectorAll('.restatement-pill'));
        const restatedBtn = pills.find(p => /Final Report|Laporan Akhir/i.test(p.textContent || ''));
        if (restatedBtn && !restatedBtn.classList.contains('active')) {
          restatedBtn.click();
          return 'clicked';
        }
        return 'ok';
      })()`);
      await sleep(350);
    };

    const openAndCapturePopup = async (clickExpr, outFile, postClickWait = 650) => {
      const clicked = await cdp.eval(clickExpr);
      if (!clicked) throw new Error(`Failed clickExpr for ${outFile}: ${clickExpr}`);
      await sleep(postClickWait);
      await cdp.screenshotClip('.glass-modal-panel', path.join(OUT_DIR, outFile), 6);
      await cdp.eval(`(() => {
        const btn = document.querySelector('.glass-close-btn');
        if (btn) btn.click();
        return true;
      })()`);
      await sleep(350);
    };

    for (let slideNum = 1; slideNum <= 20; slideNum++) {
      const idx = slideNum - 1;
      await clickNavSlide(idx);
      await ensureRestated();

      const slidePad = String(slideNum).padStart(2, '0');
      const slideFile = `slide_${slidePad}.png`;
      await cdp.screenshotClip('.slide-sheet', path.join(OUT_DIR, slideFile), 4);
      console.log(`Captured ${slideFile}`);

      if (slideNum === 1) {
        // Slide 1 does not need a popup screenshot in the speaker notes (opening slide)
        continue;
      }

      if (slideNum === 2) {
        await openAndCapturePopup(
          `(() => { const el = document.querySelector('.slide-editorial-row'); if (el) { el.click(); return true; } return false; })()`,
          'popup_02.png'
        );
      } else if (slideNum === 3) {
        await openAndCapturePopup(
          `(() => { const el = document.querySelector('.slide-forces-table tbody tr'); if (el) { el.click(); return true; } return false; })()`,
          'popup_03.png'
        );
      } else if (slideNum === 5) {
        // Capture BOTH Slide 5 popups: 05a (Current Ratio / Liquidity cards) and 05b (Altman Z-Score)
        await openAndCapturePopup(
          `(() => { const el = document.querySelectorAll('.slide-editorial-row')[0]; if (el) { el.click(); return true; } return false; })()`,
          'popup_05a.png'
        );
        await openAndCapturePopup(
          `(() => { const el = document.querySelectorAll('.slide-editorial-row')[2]; if (el) { el.click(); return true; } return false; })()`,
          'popup_05b.png'
        );
      } else if (slideNum === 6 || slideNum === 12) {
        await openAndCapturePopup(
          `(() => { const el = document.querySelector('.slide-editorial-row'); if (el) { el.click(); return true; } return false; })()`,
          `popup_${slidePad}.png`
        );
      } else {
        // Slides 4, 7, 8, 9, 10, 11, 13, 14, and Appendix A1-A6 (15..20)
        // For Slide 9, click row 4 (WACC) so it opens directly on the centerpiece 5. WACC (7.761%) walkthrough tab
        const rowIndex = slideNum === 9 ? 4 : 0;
        await openAndCapturePopup(
          `(() => { const rows = document.querySelectorAll('.slide-financial-table tbody tr'); const el = rows[${rowIndex}] || rows[0]; if (el) { el.click(); return true; } return false; })()`,
          `popup_${slidePad}.png`
        );
      }
      console.log(`Captured popup for Slide ${slideNum}`);
    }

    console.log('Done capturing all slide & popup screenshots!');
  } finally {
    if (cdp) cdp.close();
    chrome.kill('SIGTERM');
    server.close();
    fs.rmSync(userDataDir, { recursive: true, force: true });
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
