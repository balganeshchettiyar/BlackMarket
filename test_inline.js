const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf8');
const configJs = fs.readFileSync('js/config.js', 'utf8');
const teamServiceJs = fs.readFileSync('js/teamService.js', 'utf8');
const marketplaceJs = fs.readFileSync('js/marketplace.js', 'utf8');
const scriptJs = fs.readFileSync('script.js', 'utf8');

// Strip out existing script tags from HTML to prevent duplicate execution errors
const cleanedHtml = html.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');

const dom = new JSDOM(cleanedHtml, {
  url: "http://localhost/",
  runScripts: "dangerously",
  resources: "usable",
  beforeParse(window) {
    const storage = new Map();
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

// Setup error handlers
window.addEventListener("error", (event) => {
  console.error("PAGE ERROR:", event.error ? event.error.message : event.message);
});
window.addEventListener("unhandledrejection", (event) => {
  console.error("PROMISE REJECTION:", event.reason);
});

// Inject scripts in order
const loadScript = (content, name) => {
  try {
    const script = window.document.createElement("script");
    script.textContent = content;
    window.document.body.appendChild(script);
  } catch(e) {
    console.error(`Failed to load ${name}:`, e.message);
  }
};

loadScript(configJs, 'config.js');
loadScript(teamServiceJs, 'teamService.js');
loadScript(marketplaceJs, 'marketplace.js');
loadScript(scriptJs, 'script.js');

// Trigger DOMContentLoaded
const event = window.document.createEvent('Event');
event.initEvent('DOMContentLoaded', true, true);
window.document.dispatchEvent(event);

setTimeout(() => {
  console.log("DOM loaded state after 2 seconds:");
  console.log("appState =", window.appState);
  const investScreen = window.document.getElementById('invest-screen');
  console.log("invest-screen display:", investScreen ? investScreen.style.display : "not found");
  const cinLayer = window.document.getElementById('cinematic-layer');
  console.log("cinematic-layer display:", cinLayer ? cinLayer.style.display : "not found");
  
  process.exit(0);
}, 4500);
