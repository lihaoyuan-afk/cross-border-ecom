import { chromium } from 'playwright';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SCREENSHOTS_DIR = path.join(__dirname, '..', 'docs', 'screenshots');
const BASE_URL = 'http://localhost:5175';
const SAMPLE_ASIN = 'B02DGTFGQ5';

async function waitForECharts(page) {
  await page.waitForFunction(() => {
    const canvases = document.querySelectorAll('canvas');
    return canvases.length > 0;
  }, { timeout: 10000 }).catch(() => {});
  await page.waitForTimeout(1500);
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1440, height: 900 });

  // 1. Dashboard
  console.log('Screenshotting dashboard...');
  await page.goto(`${BASE_URL}/`, { waitUntil: 'networkidle' });
  await waitForECharts(page);
  await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'competitor-monitor-dashboard.png'), fullPage: false });
  console.log('  -> competitor-monitor-dashboard.png done');

  // 2. Product list
  console.log('Screenshotting product list...');
  await page.goto(`${BASE_URL}/products`, { waitUntil: 'networkidle' });
  await page.waitForSelector('table tbody tr', { timeout: 10000 }).catch(() => {});
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'competitor-monitor-products.png'), fullPage: false });
  console.log('  -> competitor-monitor-products.png done');

  // 3. Product detail
  console.log('Screenshotting product detail...');
  await page.goto(`${BASE_URL}/products/${SAMPLE_ASIN}`, { waitUntil: 'networkidle' });
  await waitForECharts(page);
  await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'competitor-monitor-detail.png'), fullPage: false });
  console.log('  -> competitor-monitor-detail.png done');

  // 4. Alert config
  console.log('Screenshotting alert config...');
  await page.goto(`${BASE_URL}/alerts/config`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'competitor-monitor-alerts.png'), fullPage: false });
  console.log('  -> competitor-monitor-alerts.png done');

  await browser.close();
  console.log('All competitor-monitor screenshots done.');
})();
