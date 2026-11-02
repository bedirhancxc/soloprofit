"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const sitemap = fs.readFileSync("sitemap.xml", "utf8");
const urls = [...sitemap.matchAll(/<loc>(.*?)<\/loc>/g)].map(x => x[1]);
assert.ok(urls.length >= 2, "No sitemap pages");
for (const url of urls) {
  const pathname = new URL(url).pathname.replace(/^\/soloprofit\/?/, "");
  const file = path.join(pathname, "index.html");
  const html = fs.readFileSync(file, "utf8");
  const blocks = [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)];
  assert.ok(blocks.length, "Missing page logic: " + file);
  for (const block of blocks) {
    new vm.Script(block[1], {filename: file});
  }
  assert.match(html, /href="#main-content"/, "Missing skip navigation: " + file);
  assert.match(html, /id="main-content"/, "Missing main anchor: " + file);
  assert.match(html, /class="site-header"/, "Missing navigation: " + file);
  assert.match(html, /href="(?:\.\.\/)?assets\/site\.css"/, "Missing shared responsive stylesheet: " + file);
  console.log("PASS: " + file);
}
console.log("PASS: all " + urls.length + " pages have valid inline JavaScript and responsive navigation.");
