# tests/dashboard.test.cjs

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/dashboard.test.cjs)। Snapshot 2026-10-04; 117 lines; SHA-256 `59e1ce32c7530fca926b7c66987b734555abef340ab2802124828dbc6eaafa80`।

## Function / object / element inventory

### `dashboard()` — L6

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

## সম্পূর্ণ original source

```javascript
const assert = require("node:assert/strict");
const { test } = require("node:test");
const fs = require("node:fs");
const vm = require("node:vm");

function dashboard() {
  const nodes = {};
  const $ = (key) => (nodes[key] ||= { innerHTML: "", textContent: "" });
  class Clock extends Date {
    static now() {
      return Date.UTC(2026, 9, 4, 6);
    }
  }
  const state = {
    books: [{ quantity: 10, available_quantity: 5 }],
    students: [
      { student_id: 1, membership_status: "ACTIVE" },
      { student_id: 2, membership_status: "DISABLED" },
    ],
    reservations: [{ status: "ACTIVE" }],
    meta: { authors: [{ id: 1 }], categories: [{ id: 1 }] },
    issues: [
      {
        issue_id: 1,
        student_id: 1,
        student: "Upcoming member",
        title: "Algorithms",
        status: "ISSUED",
        due_date: "2026-10-07",
        copy_no: 2,
        overdue_days: 0,
      },
      {
        issue_id: 2,
        student_id: 1,
        student: "Overdue member",
        title: "Java",
        status: "ISSUED",
        due_date: "2026-10-01",
        overdue_days: 3,
        current_fine: 30,
      },
      {
        issue_id: 3,
        student_id: 2,
        title: "Future book",
        status: "ISSUED",
        due_date: "2026-10-10",
        overdue_days: 0,
      },
      {
        issue_id: 4,
        student_id: 2,
        title: "Returned book",
        status: "RETURNED",
        due_date: "2026-10-05",
      },
    ],
    fines: [
      {
        fine_id: 1,
        issue_id: 5,
        student_id: 1,
        student: "Fine member",
        title: "Database",
        amount: 100,
        paid_amount: 20,
        balance: 80,
        payment_status: "UNPAID",
      },
    ],
  };
  const context = vm.createContext({
    window: {},
    Date: Clock,
    Intl,
    LibraryApp: {
      $,
      state,
      loadData: (render) => render(),
      sortIssues: (rows) => rows,
      issueRows: () => "",
      table: (headers, rows) => rows.join(""),
      escapeHtml: String,
      memberId: (id) => `PSTU-${id}`,
    },
  });
  vm.runInContext(fs.readFileSync("frontend/notifications.js", "utf8"), context);
  const render = () => vm.runInContext(fs.readFileSync("frontend/dashboard.js", "utf8"), context);
  render();
  return { nodes, state, render };
}

test("dashboard shows detailed counts, upcoming borrowers and recorded plus estimated fines", () => {
  const p = dashboard();
  assert.match(p.nodes["#stats"].innerHTML, /1 due within 3 days/);
  assert.match(p.nodes["#stats"].innerHTML, /1 disabled memberships/);
  assert.match(p.nodes["#stats"].innerHTML, /Tk 110 combined outstanding/);
  assert.match(
    p.nodes["#dueSoonTable"].innerHTML,
    /Upcoming member.*Algorithms.*2026-10-07.*3 days left/,
  );
  assert.doesNotMatch(p.nodes["#dueSoonTable"].innerHTML, /Future book|Returned book/);
  assert.match(p.nodes["#fineAttentionTable"].innerHTML, /Fine member.*Tk 80.*Unpaid fine/);
  assert.match(p.nodes["#fineAttentionTable"].innerHTML, /Overdue member.*Tk 30.*Overdue estimate/);
});

test("recorded fines replace estimates rather than counting the same loan twice", () => {
  const p = dashboard();
  p.state.fines[0].issue_id = 2;
  p.render();
  assert.equal(p.nodes["#fineAttentionTotal"].textContent, "Tk 80 recorded + estimated");
  assert.doesNotMatch(p.nodes["#fineAttentionTable"].innerHTML, /Overdue estimate/);
  p.state.fines[0].payment_status = "PAID";
  p.render();
  assert.equal(p.nodes["#fineAttentionTotal"].textContent, "Tk 0 recorded + estimated");
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
| 6 | <code>function dashboard() {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 7 | <code>  const nodes = {};</code> | Local state, DOM reference বা callback/result assign করে। |
| 8 | <code>  const $ = (key) =&gt; (nodes[key] &#124;&#124;= { innerHTML: &quot;&quot;, textContent: &quot;&quot; });</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 9 | <code>  class Clock extends Date {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 10 | <code>    static now() {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 11 | <code>      return Date.UTC(2026, 9, 4, 6);</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 12 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 13 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 14 | <code>  const state = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 15 | <code>    books: [{ quantity: 10, available_quantity: 5 }],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 16 | <code>    students: [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 17 | <code>      { student_id: 1, membership_status: &quot;ACTIVE&quot; },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 18 | <code>      { student_id: 2, membership_status: &quot;DISABLED&quot; },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 19 | <code>    ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 20 | <code>    reservations: [{ status: &quot;ACTIVE&quot; }],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 21 | <code>    meta: { authors: [{ id: 1 }], categories: [{ id: 1 }] },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 22 | <code>    issues: [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 23 | <code>      {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 24 | <code>        issue_id: 1,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 25 | <code>        student_id: 1,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 26 | <code>        student: &quot;Upcoming member&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 27 | <code>        title: &quot;Algorithms&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 28 | <code>        status: &quot;ISSUED&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 29 | <code>        due_date: &quot;2026-10-07&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 30 | <code>        copy_no: 2,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 31 | <code>        overdue_days: 0,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 32 | <code>      },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 33 | <code>      {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 34 | <code>        issue_id: 2,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 35 | <code>        student_id: 1,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 36 | <code>        student: &quot;Overdue member&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 37 | <code>        title: &quot;Java&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 38 | <code>        status: &quot;ISSUED&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 39 | <code>        due_date: &quot;2026-10-01&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 40 | <code>        overdue_days: 3,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 41 | <code>        current_fine: 30,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 42 | <code>      },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 43 | <code>      {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 44 | <code>        issue_id: 3,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 45 | <code>        student_id: 2,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 46 | <code>        title: &quot;Future book&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 47 | <code>        status: &quot;ISSUED&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 48 | <code>        due_date: &quot;2026-10-10&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 49 | <code>        overdue_days: 0,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 50 | <code>      },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 51 | <code>      {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 52 | <code>        issue_id: 4,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 53 | <code>        student_id: 2,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 54 | <code>        title: &quot;Returned book&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 55 | <code>        status: &quot;RETURNED&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 56 | <code>        due_date: &quot;2026-10-05&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 57 | <code>      },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 58 | <code>    ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 59 | <code>    fines: [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 60 | <code>      {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 61 | <code>        fine_id: 1,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 62 | <code>        issue_id: 5,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 63 | <code>        student_id: 1,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 64 | <code>        student: &quot;Fine member&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 65 | <code>        title: &quot;Database&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 66 | <code>        amount: 100,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 67 | <code>        paid_amount: 20,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 68 | <code>        balance: 80,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 69 | <code>        payment_status: &quot;UNPAID&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 70 | <code>      },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 71 | <code>    ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 72 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 73 | <code>  const context = vm.createContext({</code> | Local state, DOM reference বা callback/result assign করে। |
| 74 | <code>    window: {},</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 75 | <code>    Date: Clock,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 76 | <code>    Intl,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 77 | <code>    LibraryApp: {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 78 | <code>      $,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 79 | <code>      state,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 80 | <code>      loadData: (render) =&gt; render(),</code> | Local state, DOM reference বা callback/result assign করে। |
| 81 | <code>      sortIssues: (rows) =&gt; rows,</code> | Local state, DOM reference বা callback/result assign করে। |
| 82 | <code>      issueRows: () =&gt; &quot;&quot;,</code> | Local state, DOM reference বা callback/result assign করে। |
| 83 | <code>      table: (headers, rows) =&gt; rows.join(&quot;&quot;),</code> | Local state, DOM reference বা callback/result assign করে। |
| 84 | <code>      escapeHtml: String,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 85 | <code>      memberId: (id) =&gt; `PSTU-${id}`,</code> | Local state, DOM reference বা callback/result assign করে। |
| 86 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 87 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 88 | <code>  vm.runInContext(fs.readFileSync(&quot;frontend/notifications.js&quot;, &quot;utf8&quot;), context);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 89 | <code>  const render = () =&gt; vm.runInContext(fs.readFileSync(&quot;frontend/dashboard.js&quot;, &quot;utf8&quot;), context);</code> | Local state, DOM reference বা callback/result assign করে। |
| 90 | <code>  render();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 91 | <code>  return { nodes, state, render };</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 92 | <code>}</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 93 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 94 | <code>test(&quot;dashboard shows detailed counts, upcoming borrowers and recorded plus estimated fines&quot;, () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 95 | <code>  const p = dashboard();</code> | Local state, DOM reference বা callback/result assign করে। |
| 96 | <code>  assert.match(p.nodes[&quot;#stats&quot;].innerHTML, /1 due within 3 days/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 97 | <code>  assert.match(p.nodes[&quot;#stats&quot;].innerHTML, /1 disabled memberships/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 98 | <code>  assert.match(p.nodes[&quot;#stats&quot;].innerHTML, /Tk 110 combined outstanding/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 99 | <code>  assert.match(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 100 | <code>    p.nodes[&quot;#dueSoonTable&quot;].innerHTML,</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 101 | <code>    /Upcoming member.*Algorithms.*2026-10-07.*3 days left/,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 102 | <code>  );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 103 | <code>  assert.doesNotMatch(p.nodes[&quot;#dueSoonTable&quot;].innerHTML, /Future book&#124;Returned book/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 104 | <code>  assert.match(p.nodes[&quot;#fineAttentionTable&quot;].innerHTML, /Fine member.*Tk 80.*Unpaid fine/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 105 | <code>  assert.match(p.nodes[&quot;#fineAttentionTable&quot;].innerHTML, /Overdue member.*Tk 30.*Overdue estimate/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 106 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 107 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 108 | <code>test(&quot;recorded fines replace estimates rather than counting the same loan twice&quot;, () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 109 | <code>  const p = dashboard();</code> | Local state, DOM reference বা callback/result assign করে। |
| 110 | <code>  p.state.fines[0].issue_id = 2;</code> | Local state, DOM reference বা callback/result assign করে। |
| 111 | <code>  p.render();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 112 | <code>  assert.equal(p.nodes[&quot;#fineAttentionTotal&quot;].textContent, &quot;Tk 80 recorded + estimated&quot;);</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 113 | <code>  assert.doesNotMatch(p.nodes[&quot;#fineAttentionTable&quot;].innerHTML, /Overdue estimate/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 114 | <code>  p.state.fines[0].payment_status = &quot;PAID&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 115 | <code>  p.render();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 116 | <code>  assert.equal(p.nodes[&quot;#fineAttentionTotal&quot;].textContent, &quot;Tk 0 recorded + estimated&quot;);</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 117 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
