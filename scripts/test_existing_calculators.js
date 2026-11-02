"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

// Exercise the scripts embedded in the actual published HTML, not a copy of their formulas.
function calculator(file, values) {
  const html = fs.readFileSync(file, "utf8");
  const match = html.match(/<script>([\s\S]*?)<\/script>/);
  assert.ok(match, "Missing embedded calculator script in " + file);
  const elements = Object.entries(values).map(([name, value]) => ({
    name, value: String(value), validity: {valid: true}, invalid: false,
    setAttribute(key, val) {if(key==="aria-invalid")this.invalid=val==="true"},
    removeAttribute(key) {if(key==="aria-invalid")this.invalid=false},
    closest() {return {firstChild:{textContent: this.name}}}
  }));
  const form = {elements, addEventListener() {}};
  elements.namedItem = name => elements.find(el => el.name === name);
  const answer = {textContent: ""};
  const context = vm.createContext({
    document: {getElementById: id => ({calculator: form, answer})[id]}
  });
  vm.runInContext(match[1], context, {timeout: 1000});
  return {
    answer,
    isInvalid(name) {return elements.find(el=>el.name===name).invalid},
    set(name, value) {
      const input = elements.find(el => el.name === name);
      assert.ok(input, "Missing field: " + name);
      input.value = String(value);
      vm.runInContext("calc()", context, {timeout: 1000});
      return answer.textContent;
    }
  };
}

const freelance = calculator("freelance-hourly-rate/index.html", {
  income: 80000, expenses: 10000, hours: 25, weeks: 46
});
assert.equal(freelance.answer.textContent, "$78.26 per billable hour");
assert.match(freelance.set("hours", 0), /greater than zero/i);
assert.equal(freelance.isInvalid("hours"),true);
assert.match(freelance.set("hours", ""), /hours/i);
freelance.set("hours", 25);
assert.equal(freelance.isInvalid("hours"),false);
assert.match(freelance.set("weeks", 53), /no more than 52/i);
freelance.set("weeks", 46);
freelance.set("income", "1e308");
assert.match(freelance.set("expenses", "1e308"), /too large/i);

const margin = calculator("profit-margin/index.html", {
  revenue: 10000, cost: 7000
});
assert.equal(margin.answer.textContent, "30% profit margin");
assert.equal(margin.set("cost", 12000), "-20% profit margin (loss)");
assert.match(margin.set("revenue", 0), /greater than \$0/i);
assert.equal(margin.isInvalid("revenue"),true);
assert.match(margin.set("revenue", ""), /total revenue.*valid non-negative/i);
assert.equal(margin.isInvalid("revenue"),true);
margin.set("revenue", 10000);
assert.equal(margin.isInvalid("revenue"),false);
assert.match(margin.set("cost", ""), /total costs.*valid non-negative/i);
assert.equal(margin.isInvalid("cost"),true);
margin.set("cost", 7000);
assert.equal(margin.isInvalid("cost"),false);

const subscription = calculator("subscription-break-even/index.html", {
  price: 29, variable: 4, fixed: 1200
});
assert.equal(subscription.answer.textContent, "48 subscribers to break even");
assert.match(subscription.set("fixed", ""), /monthly fixed costs/i);
subscription.set("fixed", 1200);
assert.match(subscription.set("price", 4), /(?:must exceed|must be higher than)/i);
subscription.set("price", 29);
assert.equal(subscription.set("fixed", 0), "0 subscribers to break even");
subscription.set("fixed", "1e308");
subscription.set("variable", 28.999999999999996);
assert.match(subscription.answer.textContent, /too large/i);

console.log("PASS: three existing calculator scripts, currency output and edge cases");
