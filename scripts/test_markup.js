"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs");
const vm=require("node:vm");
const html=fs.readFileSync("markup-calculator/index.html","utf8");
assert.match(html,/id="cost"[^>]*inputmode="decimal"/);
assert.match(html,/id="markup"[^>]*inputmode="decimal"/);
assert.match(html,/id="result"[^>]*aria-atomic="true"/);
const match=html.match(/<script>([\s\S]*?)<\/script>/);
assert.ok(match);
const input=value=>({
 value:String(value),validity:{valid:true},attributes:{},
 addEventListener(){},
 setAttribute(k,v){this.attributes[k]=v},
 removeAttribute(k){delete this.attributes[k]}
});
const c=input(40),m=input(50),o={textContent:""};
const context=vm.createContext({document:{getElementById(id){return {cost:c,markup:m,result:o}[id]}}});
vm.runInContext(match[1],context,{timeout:1000});
assert.match(o.textContent,/Selling price: \$60\.00/);
assert.match(o.textContent,/Gross profit: \$20\.00/);
assert.match(o.textContent,/Gross margin: 33\.33%/);
c.value="";vm.runInContext("calc()",context);assert.equal(c.attributes["aria-invalid"],"true");
c.value="0";vm.runInContext("calc()",context);assert.match(o.textContent,/greater than/);
c.value="40";m.value="-2";vm.runInContext("calc()",context);assert.equal(m.attributes["aria-invalid"],"true");
m.value="0";vm.runInContext("calc()",context);assert.match(o.textContent,/Selling price: \$40\.00/);assert.equal(m.attributes["aria-invalid"],undefined);
c.value="1e308";m.value="1e308";vm.runInContext("calc()",context);assert.match(o.textContent,/too large/);assert.equal(c.attributes["aria-invalid"],"true");assert.equal(m.attributes["aria-invalid"],"true");
c.value="40";m.value="50";vm.runInContext("calc()",context);assert.match(o.textContent,/Selling price: \\$60\\.00/);assert.equal(c.attributes["aria-invalid"],undefined);assert.equal(m.attributes["aria-invalid"],undefined);
console.log("PASS: markup calculator formula, validation and mobile input semantics");
