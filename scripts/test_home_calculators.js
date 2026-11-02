"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

const html = fs.readFileSync("index.html","utf8");
const match = html.match(/<script>([\s\S]*?)<\/script>/);
assert.ok(match,"Missing homepage calculator script");
const inputs = {};
const events = {};
const node = () => ({textContent:"",dataset:{},disabled:false,
  addEventListener(name,callback){events[name]=callback;},
  setAttribute(){},removeAttribute(){},
});
const nodes = Object.fromEntries(["copyStatus","heading","explain","note","result","resultBox","copy","csv","year"]
  .map(id=>[id,node()]));
nodes.fields = {
  replaceChildren(){for(const key of Object.keys(inputs))delete inputs[key]},
  append(label){const input=label.input;inputs[input.id]=input;}
};
nodes.tabs = {children:[],addEventListener(){}};
const doc = {
  getElementById(id){const el=nodes[id]||inputs[id];assert.ok(el,"Unknown element: "+id);return el;},
  createElement(tag){
    if(tag==="label")return {textContent:"",append(input){this.input=input}};
    if(tag==="input"){const input={...node(),id:"",validity:{valid:true}};let stored="";Object.defineProperty(input,"value",{get(){return stored},set(v){stored=String(v)}});return input;}
    throw Error("Unexpected element: "+tag);
  }
};
const context = vm.createContext({document:doc,Date,Intl});
const run = text => vm.runInContext(text,context,{timeout:1000});
run(match[1]);
assert.equal(nodes.result.textContent,"$78.26/ hour");
assert.equal(nodes.copy.disabled,false);

function select(name){run('active='+JSON.stringify(name)+';render()')}
function edit(name,value){assert.ok(inputs[name],"Unknown field: "+name);inputs[name].value=String(value);run("compute()");return nodes.result.textContent}

select("project");
assert.equal(nodes.result.textContent,"$4,571.43 project quote");
assert.match(edit("margin",100),/below 100%/);
assert.equal(nodes.csv.disabled,true);
assert.equal(nodes.resultBox.dataset.invalid,"true");

select("subscription");
assert.equal(nodes.result.textContent,"$7,550.00 / month");
assert.match(edit("customers",1.5),/whole number/);
edit("customers",350);
edit("price",4);
edit("cost",29);
assert.equal(nodes.result.textContent,"-$9,950.00 / month");

select("target");
assert.equal(nodes.result.textContent,"440 customers");
assert.match(edit("price",4),/must exceed/);
edit("price",29);
assert.match(edit("fixed",""),/valid, non-negative/);
assert.equal(nodes.copy.disabled,true);


// A browser without Clipboard API must still explain why copying failed.
select("freelance");
assert.equal(nodes.copy.disabled,false);
assert.equal(typeof events.click,"function");
events.click();
assert.match(nodes.copyStatus.textContent,/Clipboard unavailable/);

console.log("PASS: homepage's four existing calculator formulas, error states and currency formatting");
