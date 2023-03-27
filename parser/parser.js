const _puppeteer = require('puppeteer');
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth')
puppeteer.use(StealthPlugin())

const keywords = [
    "Neomorph",
    "Button",
    "Input",
    "Checkbox",
    "Radio button",
    "Select box",
    "Datepicker",
    "Slider",
    "Tooltip",
    "Modal",
    "Progress bar",
    "Spinner",
    "Alert",
    "Tab",
    "Accordion",
    "Menu",
    "Navbar",
    "Dropdown",
    "Toast",
    "Popover",
    "Carousel",
    "Toggle button",
    "Pagination",
    "Rating system",
    "Search bar",
    "Stepper",
    "Tree view",
    "Video player",
    "Audio player",
    "Tooltipster",
    "Timepicker",
    "Drag and drop",
    "Tooltipster",
    "File uploader",
    "Context menu",
    "Contextual feedback",
    "Form validation",
    "Typeahead",
    "Social media sharing buttons",
    "Code editor",
    "Lightbox",
    "Magnifier"
];

const getPosts = async () => {
    console.log('Running parser...')
    const browser = await puppeteer.launch({
        headless: true,
        executablePath: _puppeteer.executablePath(),
    });
    const page = await browser.newPage();
    const keyword = keywords[Math.floor(Math.random() * keywords.length)];

    try {
        await page.setViewport({
            width: 1100,
            height: 870
        });
        await page.goto(`https://codepen.io/search/pens?q=${keyword}`, {waitUntil: 'networkidle2'});
        // await new Promise(r => setTimeout(r, 5000))
        const result = []
        await page.waitForSelector('.item-grid [data-component="Item"]')
        const pens = await page.$$('.item-grid [data-component="Item"]');

        for (const pen of pens) {
            const image = await pen.$eval('picture img', el => el.src);
            const link = await pen.$eval('span.visually-hidden', (span) => span.parentNode.href);
            const name = await pen.$eval('header>div>h2', el => el.textContent);
            const likes = await pen.$eval('[title="Love"]', el => el.textContent.replace('Love', ''));
            const author = await pen.$eval('header>div>address>a', el => el.textContent);
            result.push({image, name, likes, link, author});
        }
        console.log('Finished parser...', result)
        return result;
    } catch (e) {
        console.log(e)
    } finally {
        // await browser.close();
    }
};

module.exports = {
    getPosts,
}
