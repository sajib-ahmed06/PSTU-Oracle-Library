# tests/circulation.test.cjs

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/circulation.test.cjs)। Snapshot 2026-10-04; 87 lines; SHA-256 `fe0346fce7e752b24e969e5b114c0b11e55e561296926282b0c74c95ef25f148`।

## Function / object / element inventory

### `setup(state, values = {})` — L6

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

## সম্পূর্ণ original source

```javascript
const assert = require("node:assert/strict");
const { test } = require("node:test");
const fs = require("node:fs");
const vm = require("node:vm");

function setup(state, values = {}) {
  const nodes = {};
  const messages = [];
  let submitted = 0;
  const app = {
    state,
    $: (key) => (nodes[key] ||= { value: "", innerHTML: "", addEventListener() {} }),
    $$: () => [],
    escapeHtml: String,
    memberId: (id) => `Member-${id}`,
    toast: (text) => messages.push(text),
    api: async () => [],
    loadData: (fn) => fn(),
    sortIssues: (items) => items,
    issueRows: () => "",
    postForm: async () => {
      submitted++;
      return false;
    },
    openRequestedModal() {},
  };
  app.$("#issueFilter").value = "ALL";
  vm.runInNewContext(fs.readFileSync("frontend/circulation.js", "utf8"), {
    LibraryApp: app,
    window: { setTimeout() {} },
    FormData: function () {
      return Object.entries(values);
    },
  });
  return {
    nodes,
    messages,
    get submitted() {
      return submitted;
    },
  };
}

test("members with two active loans remain eligible but members with three do not", () => {
  const state = {
    online: true,
    books: [],
    fines: [],
    students: [
      { student_id: 1, name: "Two loans", department: "QA" },
      { student_id: 2, name: "Three loans", department: "QA" },
    ],
    issues: [1, 1, 2, 2, 2].map((id) => ({ student_id: id, status: "ISSUED" })),
  };
  const result = setup(state);
  assert.match(result.nodes["#studentOptions"].innerHTML, /Two loans/);
  assert.doesNotMatch(result.nodes["#studentOptions"].innerHTML, /Three loans/);
});

test("duplicate physical copies are rejected before submission", async () => {
  const result = setup(
    { online: true, books: [], students: [], fines: [], issues: [] },
    { studentId: "1", bookId: "1", copyId: "2", bookId2: "1", copyId2: "2" },
  );
  await result.nodes["#issueModal form"].onsubmit({ preventDefault() {} });
  assert.equal(result.submitted, 0);
  assert.match(result.messages.join(" "), /different copies/);
});

test("selected copies cannot exceed remaining loan allowance", async () => {
  const result = setup(
    {
      online: true,
      books: [],
      students: [],
      fines: [],
      issues: [
        { student_id: 1, status: "ISSUED" },
        { student_id: 1, status: "ISSUED" },
      ],
    },
    { studentId: "1", bookId: "1", copyId: "2", bookId2: "1", copyId2: "3" },
  );
  await result.nodes["#issueModal form"].onsubmit({ preventDefault() {} });
  assert.equal(result.submitted, 0);
  assert.match(result.messages.join(" "), /1 more copies/);
});
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>const assert = require(&quot;node:assert/strict&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 2 | <code>const { test } = require(&quot;node:test&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 3 | <code>const fs = require(&quot;node:fs&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 4 | <code>const vm = require(&quot;node:vm&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 5 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 6 | <code>function setup(state, values = {}) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 7 | <code>  const nodes = {};</code> | Local state, DOM reference বা callback/result assign করে। |
| 8 | <code>  const messages = [];</code> | Local state, DOM reference বা callback/result assign করে। |
| 9 | <code>  let submitted = 0;</code> | Local state, DOM reference বা callback/result assign করে। |
| 10 | <code>  const app = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 11 | <code>    state,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 12 | <code>    $: (key) =&gt; (nodes[key] &#124;&#124;= { value: &quot;&quot;, innerHTML: &quot;&quot;, addEventListener() {} }),</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 13 | <code>    $$: () =&gt; [],</code> | Local state, DOM reference বা callback/result assign করে। |
| 14 | <code>    escapeHtml: String,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 15 | <code>    memberId: (id) =&gt; `Member-${id}`,</code> | Local state, DOM reference বা callback/result assign করে। |
| 16 | <code>    toast: (text) =&gt; messages.push(text),</code> | Local state, DOM reference বা callback/result assign করে। |
| 17 | <code>    api: async () =&gt; [],</code> | Local state, DOM reference বা callback/result assign করে। |
| 18 | <code>    loadData: (fn) =&gt; fn(),</code> | Local state, DOM reference বা callback/result assign করে। |
| 19 | <code>    sortIssues: (items) =&gt; items,</code> | Local state, DOM reference বা callback/result assign করে। |
| 20 | <code>    issueRows: () =&gt; &quot;&quot;,</code> | Local state, DOM reference বা callback/result assign করে। |
| 21 | <code>    postForm: async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 22 | <code>      submitted++;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 23 | <code>      return false;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 24 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 25 | <code>    openRequestedModal() {},</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 26 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 27 | <code>  app.$(&quot;#issueFilter&quot;).value = &quot;ALL&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 28 | <code>  vm.runInNewContext(fs.readFileSync(&quot;frontend/circulation.js&quot;, &quot;utf8&quot;), {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 29 | <code>    LibraryApp: app,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 30 | <code>    window: { setTimeout() {} },</code> | Timeout/reconnection/search debounce timer শুরু বা বন্ধ করে। |
| 31 | <code>    FormData: function () {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 32 | <code>      return Object.entries(values);</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 33 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 34 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 35 | <code>  return {</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 36 | <code>    nodes,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 37 | <code>    messages,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 38 | <code>    get submitted() {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 39 | <code>      return submitted;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 40 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 41 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 42 | <code>}</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 43 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 44 | <code>test(&quot;members with two active loans remain eligible but members with three do not&quot;, () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 45 | <code>  const state = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 46 | <code>    online: true,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 47 | <code>    books: [],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 48 | <code>    fines: [],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 49 | <code>    students: [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 50 | <code>      { student_id: 1, name: &quot;Two loans&quot;, department: &quot;QA&quot; },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 51 | <code>      { student_id: 2, name: &quot;Three loans&quot;, department: &quot;QA&quot; },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 52 | <code>    ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 53 | <code>    issues: [1, 1, 2, 2, 2].map((id) =&gt; ({ student_id: id, status: &quot;ISSUED&quot; })),</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 54 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 55 | <code>  const result = setup(state);</code> | Local state, DOM reference বা callback/result assign করে। |
| 56 | <code>  assert.match(result.nodes[&quot;#studentOptions&quot;].innerHTML, /Two loans/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 57 | <code>  assert.doesNotMatch(result.nodes[&quot;#studentOptions&quot;].innerHTML, /Three loans/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 58 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 59 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 60 | <code>test(&quot;duplicate physical copies are rejected before submission&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 61 | <code>  const result = setup(</code> | Local state, DOM reference বা callback/result assign করে। |
| 62 | <code>    { online: true, books: [], students: [], fines: [], issues: [] },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 63 | <code>    { studentId: &quot;1&quot;, bookId: &quot;1&quot;, copyId: &quot;2&quot;, bookId2: &quot;1&quot;, copyId2: &quot;2&quot; },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 64 | <code>  );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 65 | <code>  await result.nodes[&quot;#issueModal form&quot;].onsubmit({ preventDefault() {} });</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 66 | <code>  assert.equal(result.submitted, 0);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 67 | <code>  assert.match(result.messages.join(&quot; &quot;), /different copies/);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 68 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 69 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 70 | <code>test(&quot;selected copies cannot exceed remaining loan allowance&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 71 | <code>  const result = setup(</code> | Local state, DOM reference বা callback/result assign করে। |
| 72 | <code>    {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 73 | <code>      online: true,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 74 | <code>      books: [],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 75 | <code>      students: [],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 76 | <code>      fines: [],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 77 | <code>      issues: [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 78 | <code>        { student_id: 1, status: &quot;ISSUED&quot; },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 79 | <code>        { student_id: 1, status: &quot;ISSUED&quot; },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 80 | <code>      ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 81 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 82 | <code>    { studentId: &quot;1&quot;, bookId: &quot;1&quot;, copyId: &quot;2&quot;, bookId2: &quot;1&quot;, copyId2: &quot;3&quot; },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 83 | <code>  );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 84 | <code>  await result.nodes[&quot;#issueModal form&quot;].onsubmit({ preventDefault() {} });</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 85 | <code>  assert.equal(result.submitted, 0);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 86 | <code>  assert.match(result.messages.join(&quot; &quot;), /1 more copies/);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 87 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
