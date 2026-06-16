import { chromium } from 'playwright';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SCREENSHOTS_DIR = path.join(__dirname, '..', 'docs', 'screenshots');
const BASE_URL = 'http://localhost:8501';

async function waitForStreamlit(page) {
  await page.waitForSelector('[data-testid="stAppViewContainer"]', { timeout: 20000 }).catch(() => {});
  await page.waitForFunction(() => {
    const spinner = document.querySelector('[data-testid="stStatusWidget"]');
    return !spinner || spinner.style.display === 'none';
  }, { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(2500);
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1440, height: 900 });

  console.log('Loading product-research...');
  await page.goto(BASE_URL, { waitUntil: 'networkidle', timeout: 30000 });
  await waitForStreamlit(page);

  // 1. 市场概览 (first tab, default)
  console.log('Screenshotting overview...');
  await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'product-research-overview.png'), fullPage: false });
  console.log('  -> product-research-overview.png done');

  // 2. 选品评分 tab
  console.log('Clicking 选品评分 tab...');
  try {
    await page.getByText('选品评分').first().click();
    await page.waitForTimeout(2000);
  } catch (e) {
    console.warn('Tab not found:', e.message);
  }
  await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'product-research-scoring.png'), fullPage: false });
  console.log('  -> product-research-scoring.png done');

  // 3. 关键词分析 tab
  console.log('Clicking 关键词分析 tab...');
  try {
    await page.getByText('关键词分析').first().click();
    await page.waitForTimeout(2000);
  } catch (e) {
    console.warn('Tab not found:', e.message);
  }
  await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'product-research-keywords.png'), fullPage: false });
  console.log('  -> product-research-keywords.png done');

  // 4. 竞争度分析 tab
  console.log('Clicking 竞争度分析 tab...');
  try {
    await page.getByText('竞争度分析').first().click();
    await page.waitForTimeout(2000);
  } catch (e) {
    console.warn('Tab not found:', e.message);
  }
  await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'product-research-competition.png'), fullPage: false });
  console.log('  -> product-research-competition.png done');

  await browser.close();
  console.log('All product-research screenshots done.');
})();
