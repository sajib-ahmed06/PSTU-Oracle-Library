# tests/fines.test.cjs

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/fines.test.cjs)। Snapshot 2026-10-04; 184 lines; SHA-256 `f0607cd1c606e67052001a083e6c1e0b3305cfab7745309e60d955f967810ef3`।

## Function / object / element inventory

### `render(
  state,
  collection = { total: 0, today: 0, month: 0, date: "2026-10-05", month_start: "2026-10-01" },
)` — L5

এই page-এর current state ও search/filter থেকে tables/metrics/options তৈরি করে, DOM update করে এবং generated action buttons-এর events bind করে। পাশের পূর্ণ code-এ page-specific fields দেখা যাবে।

## সম্পূর্ণ original source

```javascript
const assert = require("node:assert/strict");
const { test } = require("node:test");
const fs = require("node:fs");
const vm = require("node:vm");
function render(
  state,
  collection = { total: 0, today: 0, month: 0, date: "2026-10-05", month_start: "2026-10-01" },
) {
  const nodes = {};
  const app = {
    state,
    $: (key) => (nodes[key] ||= {}),
    $$: () => [],
    escapeHtml: (value) => String(value ?? ""),
    memberId: (id) => `PSTU-${id}`,
    table: (headers, rows) => rows.join(""),
    toast() {},
    api: async () => collection,
    loadData: (fn) => {
      nodes.ready = fn();
      return nodes.ready;
    },
  };
  vm.runInNewContext(fs.readFileSync("frontend/fines.js", "utf8"), {
    LibraryApp: app,
    window: { setInterval() {} },
    document: { hidden: false },
  });
  return nodes;
}

test("fine collection shows total, today's and current month's actual receipts separately", async () => {
  const nodes = render(
    { students: [], issues: [], fines: [] },
    { total: 1250.5, today: 100, month: 450.5, date: "2026-10-05", month_start: "2026-10-01" },
  );
  await nodes.ready;
  const html = nodes["#fineCollection"].innerHTML;
  assert.match(html, /Total fine collection.*Tk 1,250.5/);
  assert.match(html, /Today’s fine collection.*Tk 100/);
  assert.match(html, /Monthly fine collection.*Tk 450.5/);
  assert.match(html, /2026-10-05/);
});
test("unpaid fines appear before newer paid records, with the largest balance first", () => {
  const nodes = render({
    students: [],
    issues: [],
    fines: [
      {
        fine_id: 999,
        title: "Paid history",
        amount: 200,
        paid_amount: 200,
        balance: 0,
        payment_status: "PAID",
      },
      {
        fine_id: 2,
        title: "Small outstanding",
        amount: 10,
        paid_amount: 0,
        balance: 10,
        payment_status: "UNPAID",
      },
      {
        fine_id: 1,
        title: "Large outstanding",
        amount: 100,
        paid_amount: 0,
        balance: 100,
        payment_status: "UNPAID",
      },
    ],
  });
  const html = nodes["#fineTable"].innerHTML;
  assert.ok(html.indexOf("Large outstanding") < html.indexOf("Small outstanding"));
  assert.ok(html.indexOf("Small outstanding") < html.indexOf("Paid history"));
});

test("overdue loans display return action and combine with unpaid fines", () => {
  const nodes = render({
    students: [],
    issues: [
      {
        issue_id: 1,
        student_id: 1,
        student: "Member",
        title: "Overdue book",
        status: "ISSUED",
        due_date: "2026-10-01",
        overdue_days: 3,
        current_fine: 30,
      },
      { issue_id: 2, status: "ISSUED", overdue_days: 0, current_fine: 0, title: "On time" },
    ],
    fines: [
      {
        fine_id: 1,
        issue_id: 3,
        student_id: 2,
        student: "Returned",
        title: "Returned book",
        amount: 20,
        payment_status: "UNPAID",
      },
      { fine_id: 2, issue_id: 4, amount: 100, payment_status: "PAID" },
    ],
  });
  assert.match(nodes["#fineSummary"].innerHTML, /Tk 50/);
  assert.match(nodes["#overdueTable"].innerHTML, /Return book/);
  assert.match(nodes["#overdueTable"].innerHTML, /3 days/);
  assert.doesNotMatch(nodes["#overdueTable"].innerHTML, /On time/);
});
test("returned overdue book moves to history without changing outstanding total", () => {
  const nodes = render({
    students: [],
    issues: [
      {
        issue_id: 1,
        status: "RETURNED",
        overdue_days: 0,
        current_fine: 0,
        return_date: "2026-10-04",
      },
    ],
    fines: [
      {
        fine_id: 1,
        issue_id: 1,
        student_id: 1,
        student: "Member",
        title: "Book",
        amount: 30,
        payment_status: "UNPAID",
      },
    ],
  });
  assert.match(nodes["#fineSummary"].innerHTML, /Tk 30/);
  assert.match(nodes["#overdueTable"].innerHTML, /No overdue books/);
  assert.match(nodes["#fineTable"].innerHTML, /2026-10-04/);
  assert.match(nodes["#fineTable"].innerHTML, /Pay full fine/);
});

test("legacy partial payments preserve the remaining balance", () => {
  const nodes = render({
    students: [],
    issues: [{ issue_id: 1, status: "RETURNED", copy_no: 2, return_date: "2026-10-04" }],
    fines: [
      {
        fine_id: 1,
        issue_id: 1,
        amount: 100,
        paid_amount: 35.25,
        balance: 64.75,
        payment_status: "UNPAID",
      },
    ],
  });
  assert.match(nodes["#fineSummary"].innerHTML, /Tk 64.75/);
  assert.doesNotMatch(nodes["#fineSummary"].innerHTML, /Tk 100/);
  assert.match(nodes["#fineTable"].innerHTML, /Tk 35.25/);
  assert.match(nodes["#fineTable"].innerHTML, /PARTIAL/);
  assert.match(nodes["#fineTable"].innerHTML, /Copy #2/);
});

test("fully paid fine has zero outstanding and retains receipts", () => {
  const nodes = render({
    students: [],
    issues: [],
    fines: [{ fine_id: 1, amount: 100, paid_amount: 100, balance: 0, payment_status: "PAID" }],
  });
  assert.match(nodes["#fineSummary"].innerHTML, /Tk 0/);
  assert.doesNotMatch(nodes["#fineTable"].innerHTML, /data-pay=/);
  assert.match(nodes["#fineTable"].innerHTML, /Receipts/);
});
test("existing fine for the same issue is not double counted", () => {
  const nodes = render({
    students: [],
    issues: [{ issue_id: 1, student_id: 1, status: "ISSUED", overdue_days: 3, current_fine: 30 }],
    fines: [{ fine_id: 1, issue_id: 1, amount: 30, payment_status: "UNPAID" }],
  });
  assert.match(nodes["#fineSummary"].innerHTML, /Tk 30/);
  assert.doesNotMatch(nodes["#fineSummary"].innerHTML, /Tk 60/);
});
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>const assert = require(&quot;node:assert/strict&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 2 | <code>const { test } = require(&quot;node:test&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 3 | <code>const fs = require(&quot;node:fs&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 4 | <code>const vm = require(&quot;node:vm&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 5 | <code>function render(</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 6 | <code>  state,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 7 | <code>  collection = { total: 0, today: 0, month: 0, date: &quot;2026-10-05&quot;, month_start: &quot;2026-10-01&quot; },</code> | Local state, DOM reference বা callback/result assign করে। |
| 8 | <code>) {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 9 | <code>  const nodes = {};</code> | Local state, DOM reference বা callback/result assign করে। |
| 10 | <code>  const app = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 11 | <code>    state,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 12 | <code>    $: (key) =&gt; (nodes[key] &#124;&#124;= {}),</code> | Local state, DOM reference বা callback/result assign করে। |
| 13 | <code>    $$: () =&gt; [],</code> | Local state, DOM reference বা callback/result assign করে। |
| 14 | <code>    escapeHtml: (value) =&gt; String(value ?? &quot;&quot;),</code> | Local state, DOM reference বা callback/result assign করে। |
| 15 | <code>    memberId: (id) =&gt; `PSTU-${id}`,</code> | Local state, DOM reference বা callback/result assign করে। |
| 16 | <code>    table: (headers, rows) =&gt; rows.join(&quot;&quot;),</code> | Local state, DOM reference বা callback/result assign করে। |
| 17 | <code>    toast() {},</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 18 | <code>    api: async () =&gt; collection,</code> | Local state, DOM reference বা callback/result assign করে। |
| 19 | <code>    loadData: (fn) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 20 | <code>      nodes.ready = fn();</code> | Local state, DOM reference বা callback/result assign করে। |
| 21 | <code>      return nodes.ready;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 22 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 23 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 24 | <code>  vm.runInNewContext(fs.readFileSync(&quot;frontend/fines.js&quot;, &quot;utf8&quot;), {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 25 | <code>    LibraryApp: app,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 26 | <code>    window: { setInterval() {} },</code> | Timeout/reconnection/search debounce timer শুরু বা বন্ধ করে। |
| 27 | <code>    document: { hidden: false },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 28 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 29 | <code>  return nodes;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 30 | <code>}</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 31 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 32 | <code>test(&quot;fine collection shows total, today&#x27;s and current month&#x27;s actual receipts separately&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 33 | <code>  const nodes = render(</code> | Local state, DOM reference বা callback/result assign করে। |
| 34 | <code>    { students: [], issues: [], fines: [] },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 35 | <code>    { total: 1250.5, today: 100, month: 450.5, date: &quot;2026-10-05&quot;, month_start: &quot;2026-10-01&quot; },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 36 | <code>  );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 37 | <code>  await nodes.ready;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 38 | <code>  const html = nodes[&quot;#fineCollection&quot;].innerHTML;</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 39 | <code>  assert.match(html, /Total fine collection.*Tk 1,250.5/);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 40 | <code>  assert.match(html, /Today’s fine collection.*Tk 100/);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 41 | <code>  assert.match(html, /Monthly fine collection.*Tk 450.5/);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 42 | <code>  assert.match(html, /2026-10-05/);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 43 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 44 | <code>test(&quot;unpaid fines appear before newer paid records, with the largest balance first&quot;, () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 45 | <code>  const nodes = render({</code> | Local state, DOM reference বা callback/result assign করে। |
| 46 | <code>    students: [],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 47 | <code>    issues: [],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 48 | <code>    fines: [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 49 | <code>      {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 50 | <code>        fine_id: 999,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 51 | <code>        title: &quot;Paid history&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 52 | <code>        amount: 200,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 53 | <code>        paid_amount: 200,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 54 | <code>        balance: 0,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 55 | <code>        payment_status: &quot;PAID&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 56 | <code>      },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 57 | <code>      {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 58 | <code>        fine_id: 2,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 59 | <code>        title: &quot;Small outstanding&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 60 | <code>        amount: 10,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 61 | <code>        paid_amount: 0,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 62 | <code>        balance: 10,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 63 | <code>        payment_status: &quot;UNPAID&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 64 | <code>      },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 65 | <code>      {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 66 | <code>        fine_id: 1,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 67 | <code>        title: &quot;Large outstanding&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 68 | <code>        amount: 100,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 69 | <code>        paid_amount: 0,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 70 | <code>        balance: 100,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 71 | <code>        payment_status: &quot;UNPAID&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 72 | <code>      },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 73 | <code>    ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 74 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 75 | <code>  const html = nodes[&quot;#fineTable&quot;].innerHTML;</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 76 | <code>  assert.ok(html.indexOf(&quot;Large outstanding&quot;) &lt; html.indexOf(&quot;Small outstanding&quot;));</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 77 | <code>  assert.ok(html.indexOf(&quot;Small outstanding&quot;) &lt; html.indexOf(&quot;Paid history&quot;));</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 78 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 79 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 80 | <code>test(&quot;overdue loans display return action and combine with unpaid fines&quot;, () =&gt; {</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 81 | <code>  const nodes = render({</code> | Local state, DOM reference বা callback/result assign করে। |
| 82 | <code>    students: [],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 83 | <code>    issues: [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 84 | <code>      {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 85 | <code>        issue_id: 1,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 86 | <code>        student_id: 1,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 87 | <code>        student: &quot;Member&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 88 | <code>        title: &quot;Overdue book&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 89 | <code>        status: &quot;ISSUED&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 90 | <code>        due_date: &quot;2026-10-01&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 91 | <code>        overdue_days: 3,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 92 | <code>        current_fine: 30,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 93 | <code>      },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 94 | <code>      { issue_id: 2, status: &quot;ISSUED&quot;, overdue_days: 0, current_fine: 0, title: &quot;On time&quot; },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 95 | <code>    ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 96 | <code>    fines: [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 97 | <code>      {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 98 | <code>        fine_id: 1,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 99 | <code>        issue_id: 3,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 100 | <code>        student_id: 2,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 101 | <code>        student: &quot;Returned&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 102 | <code>        title: &quot;Returned book&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 103 | <code>        amount: 20,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 104 | <code>        payment_status: &quot;UNPAID&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 105 | <code>      },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 106 | <code>      { fine_id: 2, issue_id: 4, amount: 100, payment_status: &quot;PAID&quot; },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 107 | <code>    ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 108 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 109 | <code>  assert.match(nodes[&quot;#fineSummary&quot;].innerHTML, /Tk 50/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 110 | <code>  assert.match(nodes[&quot;#overdueTable&quot;].innerHTML, /Return book/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 111 | <code>  assert.match(nodes[&quot;#overdueTable&quot;].innerHTML, /3 days/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 112 | <code>  assert.doesNotMatch(nodes[&quot;#overdueTable&quot;].innerHTML, /On time/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 113 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 114 | <code>test(&quot;returned overdue book moves to history without changing outstanding total&quot;, () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 115 | <code>  const nodes = render({</code> | Local state, DOM reference বা callback/result assign করে। |
| 116 | <code>    students: [],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 117 | <code>    issues: [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 118 | <code>      {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 119 | <code>        issue_id: 1,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 120 | <code>        status: &quot;RETURNED&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 121 | <code>        overdue_days: 0,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 122 | <code>        current_fine: 0,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 123 | <code>        return_date: &quot;2026-10-04&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 124 | <code>      },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 125 | <code>    ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 126 | <code>    fines: [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 127 | <code>      {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 128 | <code>        fine_id: 1,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 129 | <code>        issue_id: 1,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 130 | <code>        student_id: 1,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 131 | <code>        student: &quot;Member&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 132 | <code>        title: &quot;Book&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 133 | <code>        amount: 30,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 134 | <code>        payment_status: &quot;UNPAID&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 135 | <code>      },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 136 | <code>    ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 137 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 138 | <code>  assert.match(nodes[&quot;#fineSummary&quot;].innerHTML, /Tk 30/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 139 | <code>  assert.match(nodes[&quot;#overdueTable&quot;].innerHTML, /No overdue books/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 140 | <code>  assert.match(nodes[&quot;#fineTable&quot;].innerHTML, /2026-10-04/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 141 | <code>  assert.match(nodes[&quot;#fineTable&quot;].innerHTML, /Pay full fine/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 142 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 143 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 144 | <code>test(&quot;legacy partial payments preserve the remaining balance&quot;, () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 145 | <code>  const nodes = render({</code> | Local state, DOM reference বা callback/result assign করে। |
| 146 | <code>    students: [],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 147 | <code>    issues: [{ issue_id: 1, status: &quot;RETURNED&quot;, copy_no: 2, return_date: &quot;2026-10-04&quot; }],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 148 | <code>    fines: [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 149 | <code>      {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 150 | <code>        fine_id: 1,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 151 | <code>        issue_id: 1,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 152 | <code>        amount: 100,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 153 | <code>        paid_amount: 35.25,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 154 | <code>        balance: 64.75,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 155 | <code>        payment_status: &quot;UNPAID&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 156 | <code>      },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 157 | <code>    ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 158 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 159 | <code>  assert.match(nodes[&quot;#fineSummary&quot;].innerHTML, /Tk 64.75/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 160 | <code>  assert.doesNotMatch(nodes[&quot;#fineSummary&quot;].innerHTML, /Tk 100/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 161 | <code>  assert.match(nodes[&quot;#fineTable&quot;].innerHTML, /Tk 35.25/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 162 | <code>  assert.match(nodes[&quot;#fineTable&quot;].innerHTML, /PARTIAL/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 163 | <code>  assert.match(nodes[&quot;#fineTable&quot;].innerHTML, /Copy #2/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 164 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 165 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 166 | <code>test(&quot;fully paid fine has zero outstanding and retains receipts&quot;, () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 167 | <code>  const nodes = render({</code> | Local state, DOM reference বা callback/result assign করে। |
| 168 | <code>    students: [],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 169 | <code>    issues: [],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 170 | <code>    fines: [{ fine_id: 1, amount: 100, paid_amount: 100, balance: 0, payment_status: &quot;PAID&quot; }],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 171 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 172 | <code>  assert.match(nodes[&quot;#fineSummary&quot;].innerHTML, /Tk 0/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 173 | <code>  assert.doesNotMatch(nodes[&quot;#fineTable&quot;].innerHTML, /data-pay=/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 174 | <code>  assert.match(nodes[&quot;#fineTable&quot;].innerHTML, /Receipts/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 175 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 176 | <code>test(&quot;existing fine for the same issue is not double counted&quot;, () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 177 | <code>  const nodes = render({</code> | Local state, DOM reference বা callback/result assign করে। |
| 178 | <code>    students: [],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 179 | <code>    issues: [{ issue_id: 1, student_id: 1, status: &quot;ISSUED&quot;, overdue_days: 3, current_fine: 30 }],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 180 | <code>    fines: [{ fine_id: 1, issue_id: 1, amount: 30, payment_status: &quot;UNPAID&quot; }],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 181 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 182 | <code>  assert.match(nodes[&quot;#fineSummary&quot;].innerHTML, /Tk 30/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 183 | <code>  assert.doesNotMatch(nodes[&quot;#fineSummary&quot;].innerHTML, /Tk 60/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 184 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
