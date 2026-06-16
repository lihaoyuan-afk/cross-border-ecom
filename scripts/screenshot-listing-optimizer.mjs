import { chromium } from 'playwright';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SCREENSHOTS_DIR = path.join(__dirname, '..', 'docs', 'screenshots');
const BASE_URL = 'http://localhost:5173';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1440, height: 900 });

  console.log('Loading listing-optimizer...');
  await page.goto(BASE_URL, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  // Click "加载演示数据"
  console.log('Clicking demo data button...');
  try {
    await page.getByText('加载演示数据').first().click();
    await page.waitForTimeout(800);
  } catch (e) {
    console.warn('Demo button not found:', e.message);
  }

  // Click "开始评分"
  console.log('Clicking score button...');
  try {
    await page.getByText('开始评分').first().click();
    await page.waitForTimeout(2500);
  } catch (e) {
    console.warn('Score button not found:', e.message);
  }

  // Wait for radar chart canvas
  try {
    await page.waitForFunction(() => document.querySelectorAll('canvas').length > 0, { timeout: 8000 });
  } catch (e) {}
  await page.waitForTimeout(1000);

  // 1. Scoring screenshot
  console.log('Screenshotting scoring...');
  await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'listing-optimizer-scoring.png'), fullPage: false });
  console.log('  -> listing-optimizer-scoring.png done');

  // Click "获取优化建议" or "刷新建议"
  console.log('Clicking suggestions button...');
  try {
    const btn = page.getByText('获取优化建议').or(page.getByText('刷新建议'));
    await btn.first().click();
    await page.waitForTimeout(2000);
  } catch (e) {
    console.warn('Suggestions button not found:', e.message);
  }

  // 2. Suggestions screenshot
  console.log('Screenshotting suggestions...');
  await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'listing-optimizer-suggestions.png'), fullPage: false });
  console.log('  -> listing-optimizer-suggestions.png done');

  // Click "AI重写" button
  console.log('Clicking AI rewrite button...');
  try {
    await page.locator('button', { hasText: /AI.*重写/ }).first().click();
    await page.waitForTimeout(2500);
  } catch (e) {
    try {
      await page.locator('button', { hasText: /重写/ }).first().click();
      await page.waitForTimeout(2500);
    } catch (e2) {
      console.warn('Rewrite button not found:', e2.message);
    }
  }

  // 3. Rewrite screenshot
  console.log('Screenshotting rewrite...');
  await page.screenshot({ path: path.join(SCREENSHOTS_DIR, 'listing-optimizer-rewrite.png'), fullPage: false });
  console.log('  -> listing-optimizer-rewrite.png done');

  await browser.close();
  console.log('All listing-optimizer screenshots done.');
})();
