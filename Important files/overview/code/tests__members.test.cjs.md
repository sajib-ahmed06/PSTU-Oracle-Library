# tests/members.test.cjs

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/members.test.cjs)। Snapshot 2026-10-04; 66 lines; SHA-256 `1a1f6648c9a0a4e01da31543ca13c3d38a9848b69b94b195d22d0f3383c357f8`।

## Function / object / element inventory

## সম্পূর্ণ original source

```javascript
const assert = require("node:assert/strict");
const { test } = require("node:test");
const fs = require("node:fs");
const vm = require("node:vm");

test("membership table displays and searches roll and registration", () => {
  const nodes = {
    "#studentSearch": { value: "" },
    "#studentCount": {},
    "#studentTable": {},
    "#studentModal form": {},
    "#identityModal form": {},
  };
  const members = [
    {
      student_id: 1,
      name: "First",
      department: "CSE",
      phone: "01700000001",
      email: "first@example.com",
      membership_status: "ACTIVE",
      roll_no: "001-AB",
      registration_no: "REG-001",
      academic_session: "2023-2024",
    },
    {
      student_id: 2,
      name: "Legacy",
      department: "CSE",
      phone: "01700000002",
      email: "legacy@example.com",
      membership_status: "ACTIVE",
      roll_no: null,
      registration_no: null,
    },
  ];
  const app = {
    $: (key) => nodes[key],
    $$: () => [],
    state: { students: members },
    escapeHtml: (value) => String(value),
    memberId: (id) => `PSTU-${id}`,
    table: (headers, rows) => headers.join("|") + rows.join(""),
    toast() {},
    api() {},
    loadData: (render) => render(),
    postForm() {},
    openRequestedModal() {},
    openModal() {},
  };
  vm.runInNewContext(fs.readFileSync("frontend/students.js", "utf8"), { LibraryApp: app });
  assert.match(nodes["#studentTable"].innerHTML, /001-AB/);
  assert.match(nodes["#studentTable"].innerHTML, /REG-001/);
  assert.match(nodes["#studentTable"].innerHTML, /Not assigned/);
  assert.match(nodes["#studentTable"].innerHTML, /2023-2024/);
  nodes["#studentSearch"].value = "2023-2024";
  nodes["#studentSearch"].oninput();
  assert.equal(nodes["#studentCount"].textContent, "1 member");
  nodes["#studentSearch"].value = "reg-001";
  nodes["#studentSearch"].oninput();
  assert.equal(nodes["#studentCount"].textContent, "1 member");
  assert.doesNotMatch(nodes["#studentTable"].innerHTML, /Legacy/);
  nodes["#studentSearch"].value = "001-ab";
  nodes["#studentSearch"].oninput();
  assert.equal(nodes["#studentCount"].textContent, "1 member");
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
| 6 | <code>test(&quot;membership table displays and searches roll and registration&quot;, () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 7 | <code>  const nodes = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 8 | <code>    &quot;#studentSearch&quot;: { value: &quot;&quot; },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 9 | <code>    &quot;#studentCount&quot;: {},</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 10 | <code>    &quot;#studentTable&quot;: {},</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 11 | <code>    &quot;#studentModal form&quot;: {},</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 12 | <code>    &quot;#identityModal form&quot;: {},</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 13 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 14 | <code>  const members = [</code> | Local state, DOM reference বা callback/result assign করে। |
| 15 | <code>    {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 16 | <code>      student_id: 1,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 17 | <code>      name: &quot;First&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 18 | <code>      department: &quot;CSE&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 19 | <code>      phone: &quot;01700000001&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 20 | <code>      email: &quot;first@example.com&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 21 | <code>      membership_status: &quot;ACTIVE&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 22 | <code>      roll_no: &quot;001-AB&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 23 | <code>      registration_no: &quot;REG-001&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 24 | <code>      academic_session: &quot;2023-2024&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 25 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 26 | <code>    {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 27 | <code>      student_id: 2,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 28 | <code>      name: &quot;Legacy&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 29 | <code>      department: &quot;CSE&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 30 | <code>      phone: &quot;01700000002&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 31 | <code>      email: &quot;legacy@example.com&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 32 | <code>      membership_status: &quot;ACTIVE&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 33 | <code>      roll_no: null,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 34 | <code>      registration_no: null,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 35 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 36 | <code>  ];</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 37 | <code>  const app = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 38 | <code>    $: (key) =&gt; nodes[key],</code> | Local state, DOM reference বা callback/result assign করে। |
| 39 | <code>    $$: () =&gt; [],</code> | Local state, DOM reference বা callback/result assign করে। |
| 40 | <code>    state: { students: members },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 41 | <code>    escapeHtml: (value) =&gt; String(value),</code> | Local state, DOM reference বা callback/result assign করে। |
| 42 | <code>    memberId: (id) =&gt; `PSTU-${id}`,</code> | Local state, DOM reference বা callback/result assign করে। |
| 43 | <code>    table: (headers, rows) =&gt; headers.join(&quot;&#124;&quot;) + rows.join(&quot;&quot;),</code> | Local state, DOM reference বা callback/result assign করে। |
| 44 | <code>    toast() {},</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 45 | <code>    api() {},</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 46 | <code>    loadData: (render) =&gt; render(),</code> | Local state, DOM reference বা callback/result assign করে। |
| 47 | <code>    postForm() {},</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 48 | <code>    openRequestedModal() {},</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 49 | <code>    openModal() {},</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 50 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 51 | <code>  vm.runInNewContext(fs.readFileSync(&quot;frontend/students.js&quot;, &quot;utf8&quot;), { LibraryApp: app });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 52 | <code>  assert.match(nodes[&quot;#studentTable&quot;].innerHTML, /001-AB/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 53 | <code>  assert.match(nodes[&quot;#studentTable&quot;].innerHTML, /REG-001/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 54 | <code>  assert.match(nodes[&quot;#studentTable&quot;].innerHTML, /Not assigned/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 55 | <code>  assert.match(nodes[&quot;#studentTable&quot;].innerHTML, /2023-2024/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 56 | <code>  nodes[&quot;#studentSearch&quot;].value = &quot;2023-2024&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 57 | <code>  nodes[&quot;#studentSearch&quot;].oninput();</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 58 | <code>  assert.equal(nodes[&quot;#studentCount&quot;].textContent, &quot;1 member&quot;);</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 59 | <code>  nodes[&quot;#studentSearch&quot;].value = &quot;reg-001&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 60 | <code>  nodes[&quot;#studentSearch&quot;].oninput();</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 61 | <code>  assert.equal(nodes[&quot;#studentCount&quot;].textContent, &quot;1 member&quot;);</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 62 | <code>  assert.doesNotMatch(nodes[&quot;#studentTable&quot;].innerHTML, /Legacy/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 63 | <code>  nodes[&quot;#studentSearch&quot;].value = &quot;001-ab&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 64 | <code>  nodes[&quot;#studentSearch&quot;].oninput();</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 65 | <code>  assert.equal(nodes[&quot;#studentCount&quot;].textContent, &quot;1 member&quot;);</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 66 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
