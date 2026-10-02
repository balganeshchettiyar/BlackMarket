const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const dom = new JSDOM(html, {
  url: "http://localhost/",
  runScripts: "dangerously",
  resources: "usable"
});

const window = dom.window;

// Setup mock for localStorage
window.localStorage = {
  getItem: () => null,
  setItem: () => {},
  removeItem: () => {}
};

// Catch errors
window.addEventListener("error", (event) => {
  console.error("PAGE ERROR:", event.error);
});
window.addEventListener("unhandledrejection", (event) => {
  console.error("PROMISE REJECTION:", event.reason);
});

setTimeout(() => {
  console.log("DOM loaded state after 2 seconds:");
  console.log("appState.mode =", window.appState ? window.appState.mode : "not set");
  const investScreen = window.document.getElementById('invest-screen');
  console.log("invest-screen display:", investScreen ? investScreen.style.display : "not found");
  
  process.exit(0);
}, 2000);
