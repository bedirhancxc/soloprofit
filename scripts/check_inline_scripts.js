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
  // Verify same-page and cross-page navigation fragments actually exist.
  for (const [, href] of html.matchAll(/<a\b[^>]*\bhref="([^"]+)"/g)) {
    if (!href.includes("#") || /^(?:https?:|mailto:|tel:)/i.test(href)) continue;
    const resolved = new URL(href, url);
    if (resolved.origin !== new URL(url).origin || !resolved.pathname.startsWith("/soloprofit/")) continue;
    const targetPath = resolved.pathname.slice("/soloprofit/".length);
    const targetFile = path.join(targetPath, "index.html");
    assert.ok(fs.existsSync(targetFile), "Broken navigation destination: " + href + " in " + file);
    const fragment = decodeURIComponent(resolved.hash.slice(1));
    if (!fragment) continue;
    const targetHtml = fs.readFileSync(targetFile, "utf8");
    assert.ok(targetHtml.includes('id="' + fragment + '"') || targetHtml.includes("id='" + fragment + "'"),
      "Broken navigation fragment #" + fragment + " in " + file);
  }
  console.log("PASS: " + file);
}
console.log("PASS: all " + urls.length + " pages have valid inline JavaScript and responsive navigation.");

const css = fs.readFileSync("assets/site.css", "utf8");
assert.match(css, /@media\s*\(max-width:\s*620px\)/, "Missing phone layout breakpoint");
assert.match(css, /@media\s*\(min-width:\s*621px\)\s*and\s*\(max-width:\s*900px\)/, "Missing tablet layout breakpoint");
assert.match(css, /\.calculator-layout\s*\{grid-template-columns:1fr\}/, "Tablet calculator layout must not be cramped");
assert.match(css, /\.calc-tabs\s*\{display:grid;grid-template-columns:repeat\(2,minmax\(0,1fr\)\)/, "Phone calculator tabs need two columns");
assert.match(css, /\.inner-page \.card form\s*\{grid-template-columns:1fr\}/, "Phone detail forms need one column");
assert.match(css, /\[hidden\]\s*\{display:none!important\}/, "Hidden result panels must stay hidden");
console.log("PASS: navigation fragments and static phone/tablet CSS checks");
