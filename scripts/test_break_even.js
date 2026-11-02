"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

const html = fs.readFileSync("break-even-calculator/index.html", "utf8");
const code = html.match(/<script>([\s\S]*?)<\/script>/);
assert.ok(code, "Missing calculator script");

const nodes = Object.fromEntries(
  ["fixed", "price", "variable", "quantity", "answer", "metrics",
   "revenue", "contribution", "profit", "calculator"]
    .map(id => [id, {value: "", textContent: "", hidden: false, addEventListener() {}}])
);
Object.assign(nodes.fixed, {value: "3000"});
Object.assign(nodes.price, {value: "50"});
Object.assign(nodes.variable, {value: "20"});
Object.assign(nodes.quantity, {value: "150"});

const context = vm.createContext({
  document: {getElementById: id => {
    assert.ok(nodes[id], "Unknown element: " + id);
    return nodes[id];
  }},
});
vm.runInContext(code[1], context, {timeout: 1000});
const rerun = () => vm.runInContext("calc()", context, {timeout: 1000});

assert.equal(nodes.answer.textContent, "100 units to break even");
assert.equal(nodes.revenue.textContent, "$5,000.00");
assert.equal(nodes.contribution.textContent, "$30.00");
assert.equal(nodes.profit.textContent, "$1,500.00");
assert.equal(nodes.metrics.hidden, false);

nodes.price.value = "20";
rerun();
assert.match(nodes.answer.textContent, /No break-even point/);
assert.equal(nodes.metrics.hidden, true);

nodes.price.value = "50";
nodes.quantity.value = "1.5";
rerun();
assert.match(nodes.answer.textContent, /whole numbers/);
assert.equal(nodes.metrics.hidden, true);

nodes.quantity.value = "150";
nodes.fixed.value = "0";
rerun();
assert.equal(nodes.answer.textContent, "0 units to break even");

nodes.fixed.value = "1e308";
nodes.price.value = "1";
nodes.variable.value = "0";
rerun();
assert.match(nodes.answer.textContent, /too large/);
assert.equal(nodes.metrics.hidden, true);

console.log("PASS: break-even calculator default results and edge cases");
