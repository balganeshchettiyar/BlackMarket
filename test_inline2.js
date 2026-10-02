const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf8');
const configJs = fs.readFileSync('js/config.js', 'utf8');
const teamServiceJs = fs.readFileSync('js/teamService.js', 'utf8');
const marketplaceJs = fs.readFileSync('js/marketplace.js', 'utf8');
let scriptJs = fs.readFileSync('script.js', 'utf8');

scriptJs = scriptJs.replace(
  "marketplace = new Marketplace();",
  "console.log('Before Marketplace'); marketplace = new Marketplace(); console.log('After Marketplace');"
);
scriptJs = scriptJs.replace(
  "if (state.blackMarketUnlocked) {",
  "console.log('checking blackMarketUnlocked:', state.blackMarketUnlocked); if (state.blackMarketUnlocked) {"
);
scriptJs = scriptJs.replace(
  "appState.mode = 'success';",
  "appState.mode = 'success'; console.log('Set to success');"
);

const cleanedHtml = html.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');

const dom = new JSDOM(cleanedHtml, {
  url: "http://localhost/",
  runScripts: "dangerously",
  resources: "usable",
  beforeParse(window) {
    const storage = new Map();
    const teamState = {
        teamName: "Test",
        money: 500,
        blackMarketUnlocked: true,
        purchasedItems: [],
        inventory: { hints: [], mystery: [] },
        puzzleProgress: { cluesFound: [], riddleSolved: false, finalCodeEntered: false },
        codeAttempts: 0
    };
    storage.set('currentTeamId', 'TEAM_07');
    storage.set('blackMarketState_TEAM_07', JSON.stringify(teamState));

    window.localStorage = {
      getItem: (k) => storage.get(k) || null,
      setItem: (k, v) => storage.set(k, v),
      removeItem: (k) => storage.delete(k)
    };
    window.fetch = async () => ({ json: async () => ({}) });
    window.requestAnimationFrame = setTimeout;
  }
});

const window = dom.window;
window.addEventListener("error", (event) => console.error("PAGE ERROR:", event.error));
window.addEventListener("unhandledrejection", (event) => console.error("PROMISE REJECTION:", event.reason));

const loadScript = (content, name) => {
  try {
    const script = window.document.createElement("script");
    script.textContent = content;
    window.document.body.appendChild(script);
  } catch(e) {
    console.error(`Failed to load ${name}:`, e.message);
  }
};

window.HTMLCanvasElement.prototype.getContext = () => ({
  setTransform: () => {}, fillRect: () => {}, clearRect: () => {}, save: () => {},
  restore: () => {}, beginPath: () => {}, arc: () => {}, fill: () => {},
  stroke: () => {}, moveTo: () => {}, lineTo: () => {}, clip: () => {}
});

loadScript(configJs, 'config.js');
loadScript(teamServiceJs, 'teamService.js');
loadScript(marketplaceJs, 'marketplace.js');
loadScript(scriptJs, 'script.js');

const event = window.document.createEvent('Event');
event.initEvent('DOMContentLoaded', true, true);
window.document.dispatchEvent(event);

setTimeout(() => {
  console.log("hub display:", window.document.getElementById('black-market-hub').style.display);
  process.exit(0);
}, 2000);
