const puppeteer = require('puppeteer');

(async () => {
    try {
        const browser = await puppeteer.launch({ headless: "new" });
        const page = await browser.newPage();

        page.on('console', msg => console.log('PAGE LOG:', msg.text()));
        page.on('pageerror', error => console.log('PAGE ERROR:', error.message));
        page.on('requestfailed', request =>
            console.log('REQUEST FAILED:', request.url(), request.failure().errorText)
        );

        await page.goto('http://localhost:8080', { waitUntil: 'networkidle2' });
        
        // Wait a bit to let any animations or delayed scripts run
        await page.waitForTimeout(2000);

        // Take a screenshot to see what it looks like
        await page.screenshot({ path: 'screenshot.png' });

        await browser.close();
    } catch (e) {
        console.error('Puppeteer Error:', e);
    }
})();
