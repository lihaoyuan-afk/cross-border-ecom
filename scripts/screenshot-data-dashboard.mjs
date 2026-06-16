import { chromium } from 'playwright';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SCREENSHOTS_DIR = path.join(__dirname, '..', 'docs', 'screenshots');
const BASE_URL = 'http://localhost:5174';

async function waitForECharts(page) {
  await page.waitForFunction(() => {
    const canvases = document.querySelectorAll('canvas');
    return canvases.length > 0;
  }, { timeout: 10000 }).catch(() => {});
  await page.waitForTimeout(2500);
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1440, height: 900 });

  console.log('Loading data-dashboard...');
  await page.goto(`${BASE_URL}/`, { waitUntil: 'networkidle' });
  await waitForECharts(page);

  // 1. Home (KPI cards + sales trend)
  console.log('Screenshotting home...');
  await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'data-dashboard-home.png'), fullPage: false });
  console.log('  -> data-dashboard-home.png done');

  // 2. ACoS chart - scroll into view
  console.log('Screenshotting ads chart...');
  try {
    const chartRows = await page.$$('.chart-row');
    if (chartRows.length >= 1) {
      const firstRowCards = await chartRows[0].$$('.chart-card, .el-card');
      // ACoS chart is the second card in the first chart-row
      if (firstRowCards.length >= 2) {
        await firstRowCards[1].scrollIntoViewIfNeeded();
        await page.waitForTimeout(600);
        await firstRowCards[1].screenshot({ path: path.join(SCREENSHOTS_DIR, 'data-dashboard-ads.png') });
      } else {
        await page.evaluate(() => window.scrollTo(0, 500));
        await page.waitForTimeout(600);
        await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'data-dashboard-ads.png') });
      }
    } else {
      await page.evaluate(() => window.scrollTo(0, 500));
      await page.waitForTimeout(600);
      await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'data-dashboard-ads.png') });
    }
  } catch (e) {
    console.warn('ACoS card not found:', e.message);
    await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'data-dashboard-ads.png') });
  }
  console.log('  -> data-dashboard-ads.png done');

  // Scroll to second chart-row for funnel + inventory
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(800);

  const chartRows = await page.$$('.chart-row');

  // 3. Funnel
  console.log('Screenshotting funnel...');
  try {
    if (chartRows.length >= 2) {
      const cards = await chartRows[1].$$('.chart-card, .el-card');
      if (cards.length >= 1) {
        await cards[0].screenshot({ path: path.join(SCREENSHOTS_DIR, 'data-dashboard-funnel.png') });
      } else {
        await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'data-dashboard-funnel.png') });
      }
    } else {
      await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'data-dashboard-funnel.png') });
    }
  } catch (e) {
    await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'data-dashboard-funnel.png') });
  }
  console.log('  -> data-dashboard-funnel.png done');

  // 4. Inventory table
  console.log('Screenshotting inventory...');
  try {
    if (chartRows.length >= 2) {
      const cards = await chartRows[1].$$('.chart-card, .el-card');
      if (cards.length >= 2) {
        await cards[1].screenshot({ path: path.join(SCREENSHOTS_DIR, 'data-dashboard-inventory.png') });
      } else {
        await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'data-dashboard-inventory.png') });
      }
    } else {
      await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'data-dashboard-inventory.png') });
    }
  } catch (e) {
    await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'data-dashboard-inventory.png') });
  }
  console.log('  -> data-dashboard-inventory.png done');

  await browser.close();
  console.log('All data-dashboard screenshots done.');
})();
