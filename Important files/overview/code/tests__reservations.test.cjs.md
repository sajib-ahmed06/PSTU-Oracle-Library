# tests/reservations.test.cjs

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/reservations.test.cjs)। Snapshot 2026-10-04; 218 lines; SHA-256 `133758eb160ca6f4758c5122f4337f5f40e09efb71e2fa24004c54e848c7ab7a`।

## Function / object / element inventory

### `page(snapshot, role = "student")` — L6

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

## সম্পূর্ণ original source

```javascript
const assert = require("node:assert/strict");
const { test } = require("node:test");
const fs = require("node:fs");
const vm = require("node:vm");

async function page(snapshot, role = "student") {
  const nodes = {};
  const button = { disabled: false, dataset: { reserve: "3" } };
  const requests = [];
  const state = { online: false, ...snapshot };
  const collectButton = { disabled: false, dataset: { collect: "12" } };
  const $ = (selector) =>
    (nodes[selector] ||= {
      value: "",
      textContent: "",
      innerHTML: "",
      classList: { add() {}, remove() {} },
    });
  const app = {
    $,
    $$: (selector) => {
      if (selector === "[data-reserve]") return [button];
      if (selector === "[data-collect]" && role !== "student") return [collectButton];
      return [];
    },
    state,
    escapeHtml: String,
    memberId: (id) => `PSTU-${id}`,
    table: (headers, rows) => rows.join(""),
    toast() {},
    loadData: async (render) => {
      state.online = true;
      await render();
    },
    api: async (path, options) => {
      requests.push({ path, options });
      return options ? { message: "Reserved" } : snapshot;
    },
  };
  vm.runInNewContext(
    fs.readFileSync("frontend/notifications.js", "utf8") +
      "\n" +
      fs.readFileSync("frontend/member-dashboard.js", "utf8") +
      "\n" +
      fs.readFileSync("frontend/reservation-desk.js", "utf8") +
      "\n" +
      fs.readFileSync("frontend/reservations.js", "utf8"),
    {
      LibraryApp: app,
      document: { body: { dataset: { page: role } }, hidden: false },
      window: { setInterval() {} },
      confirm: () => true,
      URLSearchParams,
    },
  );
  await $("#refreshButton").onclick();
  return { nodes, button, collectButton, requests };
}

const snapshot = () => ({
  member: { student_id: 17, name: "Member", roll_no: "007", registration_no: "009" },
  books: [
    {
      book_id: 3,
      title: "Book",
      author_name: "Author",
      category_name: "Science",
      quantity: 2,
      available_quantity: 1,
    },
  ],
  reservations: [],
  issues: [],
  fines: [],
});

test("student catalogue reserves a book without sending a member identity", async () => {
  const p = await page(snapshot());
  assert.match(p.nodes["#catalogueTable"].innerHTML, /Reserve for 3 days/);
  await p.button.onclick();
  const request = p.requests.find((r) => r.options);
  assert.equal(request.path, "/reservations");
  assert.equal(request.options.body.get("bookId"), "3");
  assert.equal(request.options.body.has("studentId"), false);
});

test("member dashboard prominently shows personal due reminders and unpaid fine details", async () => {
  const data = snapshot();
  const due = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Asia/Dhaka",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(new Date(Date.now() + 2 * 86400000));
  data.issues = [
    {
      issue_id: 19,
      student_id: 17,
      title: "Upcoming return",
      status: "ISSUED",
      due_date: due,
      copy_no: 3,
    },
  ];
  data.fines = [
    {
      fine_id: 9,
      issue_id: 20,
      student_id: 17,
      title: "Unpaid book",
      amount: 50,
      paid_amount: 0,
      balance: 50,
      payment_status: "UNPAID",
    },
  ];
  const p = await page(data);
  assert.match(p.nodes["#memberAlerts"].innerHTML, /Book return is due in 2 days/);
  assert.match(p.nodes["#memberAlerts"].innerHTML, /Upcoming return.*Copy #3/);
  assert.match(p.nodes["#memberAlerts"].innerHTML, /Tk 50 outstanding/);
  assert.match(p.nodes["#memberAlerts"].innerHTML, /href="\/student#loans"/);
  assert.match(p.nodes["#memberAlerts"].innerHTML, /href="\/student#fines"/);
});

test("active hold displays deadline and prevents duplicate title reservations", async () => {
  const data = snapshot();
  data.reservations = [
    {
      reservation_id: 1,
      book_id: 3,
      title: "Book",
      copy_no: 2,
      reserved_at: "2026-10-04 12:00:00",
      expires_at: "2026-10-07 12:00:00",
      status: "ACTIVE",
    },
  ];
  const p = await page(data);
  assert.match(p.nodes["#reservationTable"].innerHTML, /2026-10-07 12:00:00/);
  assert.match(p.nodes["#catalogueTable"].innerHTML, /disabled>Already reserved/);
  assert.doesNotMatch(p.nodes["#reservationTable"].innerHTML, /data-collect/);
});

test("expired holds release reservation allowance and overdue fines remain visible", async () => {
  const data = snapshot();
  data.reservations = [{ reservation_id: 1, book_id: 3, title: "Book", status: "EXPIRED" }];
  data.issues = [
    { issue_id: 1, title: "Loan", status: "ISSUED", current_fine: 30, due_date: "2026-10-01" },
  ];
  const p = await page(data);
  assert.match(p.nodes["#studentStats"].innerHTML, /Tk 30/);
  assert.match(p.nodes["#loanTable"].innerHTML, /2026-10-01/);
  assert.match(p.nodes["#catalogueTable"].innerHTML, /Reserve for 3 days/);
  assert.doesNotMatch(p.nodes["#reservationTable"].innerHTML, /data-cancel/);
});

test("available-book filter excludes out-of-stock titles without fetching again", async () => {
  const data = snapshot();
  data.books.push({
    book_id: 4,
    title: "Unavailable title",
    author_name: "Author",
    category_name: "Science",
    quantity: 1,
    available_quantity: 0,
  });
  const p = await page(data);
  const requests = p.requests.length;
  p.nodes["#availabilityFilter"].value = "available";
  p.nodes["#availabilityFilter"].onchange();
  assert.doesNotMatch(p.nodes["#catalogueTable"].innerHTML, /Unavailable title/);
  assert.match(p.nodes["#catalogueCount"].textContent, /1 of 2 titles/);
  assert.equal(p.requests.length, requests);
});

test("borrowing filter separates returned books from current loans", async () => {
  const data = snapshot();
  data.issues = [
    { issue_id: 1, title: "Current book", status: "ISSUED" },
    { issue_id: 2, title: "Returned book", status: "RETURNED" },
  ];
  const p = await page(data);
  p.nodes["#loanFilter"].value = "RETURNED";
  p.nodes["#loanFilter"].onchange();
  assert.match(p.nodes["#loanTable"].innerHTML, /Returned book/);
  assert.doesNotMatch(p.nodes["#loanTable"].innerHTML, /Current book/);
});

test("staff desk lists active members and available books without member dashboard reads", async () => {
  const data = snapshot();
  data.students = [
    { student_id: 17, name: "Active member", membership_status: "ACTIVE" },
    { student_id: 18, name: "Disabled member", membership_status: "DISABLED" },
  ];
  data.books.push({ book_id: 4, title: "Unavailable book", available_quantity: 0 });
  const p = await page(data, "reservations");
  assert.match(p.nodes["#reserveMember"].innerHTML, /Active member/);
  assert.doesNotMatch(p.nodes["#reserveMember"].innerHTML, /Disabled member/);
  assert.match(p.nodes["#reserveBook"].innerHTML, /Book/);
  assert.doesNotMatch(p.nodes["#reserveBook"].innerHTML, /Unavailable book/);
  assert.equal(
    p.requests.some((request) => request.path === "/student/dashboard"),
    false,
  );
});

test("staff can collect a reserved copy through the shared action coordinator", async () => {
  const data = snapshot();
  data.students = [];
  data.reservations = [{ reservation_id: 12, student_id: 17, title: "Book", status: "ACTIVE" }];
  const p = await page(data, "reservations");
  assert.match(p.nodes["#reservationTable"].innerHTML, /data-collect="12"/);
  await p.collectButton.onclick();
  const request = p.requests.find((item) => item.options);
  assert.equal(request.path, "/reservations/12/collect");
  assert.equal(request.options.method, "POST");
  assert.equal(p.collectButton.disabled, false);
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
| 6 | <code>async function page(snapshot, role = &quot;student&quot;) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 7 | <code>  const nodes = {};</code> | Local state, DOM reference বা callback/result assign করে। |
| 8 | <code>  const button = { disabled: false, dataset: { reserve: &quot;3&quot; } };</code> | Local state, DOM reference বা callback/result assign করে। |
| 9 | <code>  const requests = [];</code> | Local state, DOM reference বা callback/result assign করে। |
| 10 | <code>  const state = { online: false, ...snapshot };</code> | Local state, DOM reference বা callback/result assign করে। |
| 11 | <code>  const collectButton = { disabled: false, dataset: { collect: &quot;12&quot; } };</code> | Local state, DOM reference বা callback/result assign করে। |
| 12 | <code>  const $ = (selector) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 13 | <code>    (nodes[selector] &#124;&#124;= {</code> | Local state, DOM reference বা callback/result assign করে। |
| 14 | <code>      value: &quot;&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 15 | <code>      textContent: &quot;&quot;,</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 16 | <code>      innerHTML: &quot;&quot;,</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 17 | <code>      classList: { add() {}, remove() {} },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 18 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 19 | <code>  const app = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 20 | <code>    $,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 21 | <code>    $$: (selector) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 22 | <code>      if (selector === &quot;[data-reserve]&quot;) return [button];</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 23 | <code>      if (selector === &quot;[data-collect]&quot; &amp;&amp; role !== &quot;student&quot;) return [collectButton];</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 24 | <code>      return [];</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 25 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 26 | <code>    state,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 27 | <code>    escapeHtml: String,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 28 | <code>    memberId: (id) =&gt; `PSTU-${id}`,</code> | Local state, DOM reference বা callback/result assign করে। |
| 29 | <code>    table: (headers, rows) =&gt; rows.join(&quot;&quot;),</code> | Local state, DOM reference বা callback/result assign করে। |
| 30 | <code>    toast() {},</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 31 | <code>    loadData: async (render) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 32 | <code>      state.online = true;</code> | Local state, DOM reference বা callback/result assign করে। |
| 33 | <code>      await render();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 34 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 35 | <code>    api: async (path, options) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 36 | <code>      requests.push({ path, options });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 37 | <code>      return options ? { message: &quot;Reserved&quot; } : snapshot;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 38 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 39 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 40 | <code>  vm.runInNewContext(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 41 | <code>    fs.readFileSync(&quot;frontend/notifications.js&quot;, &quot;utf8&quot;) +</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 42 | <code>      &quot;\n&quot; +</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 43 | <code>      fs.readFileSync(&quot;frontend/member-dashboard.js&quot;, &quot;utf8&quot;) +</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 44 | <code>      &quot;\n&quot; +</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 45 | <code>      fs.readFileSync(&quot;frontend/reservation-desk.js&quot;, &quot;utf8&quot;) +</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 46 | <code>      &quot;\n&quot; +</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 47 | <code>      fs.readFileSync(&quot;frontend/reservations.js&quot;, &quot;utf8&quot;),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 48 | <code>    {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 49 | <code>      LibraryApp: app,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 50 | <code>      document: { body: { dataset: { page: role } }, hidden: false },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 51 | <code>      window: { setInterval() {} },</code> | Timeout/reconnection/search debounce timer শুরু বা বন্ধ করে। |
| 52 | <code>      confirm: () =&gt; true,</code> | Local state, DOM reference বা callback/result assign করে। |
| 53 | <code>      URLSearchParams,</code> | Form fields বা filters URL-encoded request body/query parameters-এ রূপান্তর করে। |
| 54 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 55 | <code>  );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 56 | <code>  await $(&quot;#refreshButton&quot;).onclick();</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 57 | <code>  return { nodes, button, collectButton, requests };</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 58 | <code>}</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 59 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 60 | <code>const snapshot = () =&gt; ({</code> | Local state, DOM reference বা callback/result assign করে। |
| 61 | <code>  member: { student_id: 17, name: &quot;Member&quot;, roll_no: &quot;007&quot;, registration_no: &quot;009&quot; },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 62 | <code>  books: [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 63 | <code>    {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 64 | <code>      book_id: 3,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 65 | <code>      title: &quot;Book&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 66 | <code>      author_name: &quot;Author&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 67 | <code>      category_name: &quot;Science&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 68 | <code>      quantity: 2,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 69 | <code>      available_quantity: 1,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 70 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 71 | <code>  ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 72 | <code>  reservations: [],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 73 | <code>  issues: [],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 74 | <code>  fines: [],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 75 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 76 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 77 | <code>test(&quot;student catalogue reserves a book without sending a member identity&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 78 | <code>  const p = await page(snapshot());</code> | Local state, DOM reference বা callback/result assign করে। |
| 79 | <code>  assert.match(p.nodes[&quot;#catalogueTable&quot;].innerHTML, /Reserve for 3 days/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 80 | <code>  await p.button.onclick();</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 81 | <code>  const request = p.requests.find((r) =&gt; r.options);</code> | Local state, DOM reference বা callback/result assign করে। |
| 82 | <code>  assert.equal(request.path, &quot;/reservations&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 83 | <code>  assert.equal(request.options.body.get(&quot;bookId&quot;), &quot;3&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 84 | <code>  assert.equal(request.options.body.has(&quot;studentId&quot;), false);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 85 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 86 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 87 | <code>test(&quot;member dashboard prominently shows personal due reminders and unpaid fine details&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 88 | <code>  const data = snapshot();</code> | Local state, DOM reference বা callback/result assign করে। |
| 89 | <code>  const due = new Intl.DateTimeFormat(&quot;en-CA&quot;, {</code> | Local state, DOM reference বা callback/result assign করে। |
| 90 | <code>    timeZone: &quot;Asia/Dhaka&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 91 | <code>    year: &quot;numeric&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 92 | <code>    month: &quot;2-digit&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 93 | <code>    day: &quot;2-digit&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 94 | <code>  }).format(new Date(Date.now() + 2 * 86400000));</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 95 | <code>  data.issues = [</code> | Local state, DOM reference বা callback/result assign করে। |
| 96 | <code>    {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 97 | <code>      issue_id: 19,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 98 | <code>      student_id: 17,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 99 | <code>      title: &quot;Upcoming return&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 100 | <code>      status: &quot;ISSUED&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 101 | <code>      due_date: due,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 102 | <code>      copy_no: 3,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 103 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 104 | <code>  ];</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 105 | <code>  data.fines = [</code> | Local state, DOM reference বা callback/result assign করে। |
| 106 | <code>    {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 107 | <code>      fine_id: 9,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 108 | <code>      issue_id: 20,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 109 | <code>      student_id: 17,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 110 | <code>      title: &quot;Unpaid book&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 111 | <code>      amount: 50,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 112 | <code>      paid_amount: 0,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 113 | <code>      balance: 50,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 114 | <code>      payment_status: &quot;UNPAID&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 115 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 116 | <code>  ];</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 117 | <code>  const p = await page(data);</code> | Local state, DOM reference বা callback/result assign করে। |
| 118 | <code>  assert.match(p.nodes[&quot;#memberAlerts&quot;].innerHTML, /Book return is due in 2 days/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 119 | <code>  assert.match(p.nodes[&quot;#memberAlerts&quot;].innerHTML, /Upcoming return.*Copy #3/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 120 | <code>  assert.match(p.nodes[&quot;#memberAlerts&quot;].innerHTML, /Tk 50 outstanding/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 121 | <code>  assert.match(p.nodes[&quot;#memberAlerts&quot;].innerHTML, /href=&quot;\/student#loans&quot;/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 122 | <code>  assert.match(p.nodes[&quot;#memberAlerts&quot;].innerHTML, /href=&quot;\/student#fines&quot;/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 123 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 124 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 125 | <code>test(&quot;active hold displays deadline and prevents duplicate title reservations&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 126 | <code>  const data = snapshot();</code> | Local state, DOM reference বা callback/result assign করে। |
| 127 | <code>  data.reservations = [</code> | Local state, DOM reference বা callback/result assign করে। |
| 128 | <code>    {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 129 | <code>      reservation_id: 1,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 130 | <code>      book_id: 3,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 131 | <code>      title: &quot;Book&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 132 | <code>      copy_no: 2,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 133 | <code>      reserved_at: &quot;2026-10-04 12:00:00&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 134 | <code>      expires_at: &quot;2026-10-07 12:00:00&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 135 | <code>      status: &quot;ACTIVE&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 136 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 137 | <code>  ];</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 138 | <code>  const p = await page(data);</code> | Local state, DOM reference বা callback/result assign করে। |
| 139 | <code>  assert.match(p.nodes[&quot;#reservationTable&quot;].innerHTML, /2026-10-07 12:00:00/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 140 | <code>  assert.match(p.nodes[&quot;#catalogueTable&quot;].innerHTML, /disabled&gt;Already reserved/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 141 | <code>  assert.doesNotMatch(p.nodes[&quot;#reservationTable&quot;].innerHTML, /data-collect/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 142 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 143 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 144 | <code>test(&quot;expired holds release reservation allowance and overdue fines remain visible&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 145 | <code>  const data = snapshot();</code> | Local state, DOM reference বা callback/result assign করে। |
| 146 | <code>  data.reservations = [{ reservation_id: 1, book_id: 3, title: &quot;Book&quot;, status: &quot;EXPIRED&quot; }];</code> | Local state, DOM reference বা callback/result assign করে। |
| 147 | <code>  data.issues = [</code> | Local state, DOM reference বা callback/result assign করে। |
| 148 | <code>    { issue_id: 1, title: &quot;Loan&quot;, status: &quot;ISSUED&quot;, current_fine: 30, due_date: &quot;2026-10-01&quot; },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 149 | <code>  ];</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 150 | <code>  const p = await page(data);</code> | Local state, DOM reference বা callback/result assign করে। |
| 151 | <code>  assert.match(p.nodes[&quot;#studentStats&quot;].innerHTML, /Tk 30/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 152 | <code>  assert.match(p.nodes[&quot;#loanTable&quot;].innerHTML, /2026-10-01/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 153 | <code>  assert.match(p.nodes[&quot;#catalogueTable&quot;].innerHTML, /Reserve for 3 days/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 154 | <code>  assert.doesNotMatch(p.nodes[&quot;#reservationTable&quot;].innerHTML, /data-cancel/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 155 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 156 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 157 | <code>test(&quot;available-book filter excludes out-of-stock titles without fetching again&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 158 | <code>  const data = snapshot();</code> | Local state, DOM reference বা callback/result assign করে। |
| 159 | <code>  data.books.push({</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 160 | <code>    book_id: 4,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 161 | <code>    title: &quot;Unavailable title&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 162 | <code>    author_name: &quot;Author&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 163 | <code>    category_name: &quot;Science&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 164 | <code>    quantity: 1,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 165 | <code>    available_quantity: 0,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 166 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 167 | <code>  const p = await page(data);</code> | Local state, DOM reference বা callback/result assign করে। |
| 168 | <code>  const requests = p.requests.length;</code> | Local state, DOM reference বা callback/result assign করে। |
| 169 | <code>  p.nodes[&quot;#availabilityFilter&quot;].value = &quot;available&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 170 | <code>  p.nodes[&quot;#availabilityFilter&quot;].onchange();</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 171 | <code>  assert.doesNotMatch(p.nodes[&quot;#catalogueTable&quot;].innerHTML, /Unavailable title/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 172 | <code>  assert.match(p.nodes[&quot;#catalogueCount&quot;].textContent, /1 of 2 titles/);</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 173 | <code>  assert.equal(p.requests.length, requests);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 174 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 175 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 176 | <code>test(&quot;borrowing filter separates returned books from current loans&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 177 | <code>  const data = snapshot();</code> | Local state, DOM reference বা callback/result assign করে। |
| 178 | <code>  data.issues = [</code> | Local state, DOM reference বা callback/result assign করে। |
| 179 | <code>    { issue_id: 1, title: &quot;Current book&quot;, status: &quot;ISSUED&quot; },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 180 | <code>    { issue_id: 2, title: &quot;Returned book&quot;, status: &quot;RETURNED&quot; },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 181 | <code>  ];</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 182 | <code>  const p = await page(data);</code> | Local state, DOM reference বা callback/result assign করে। |
| 183 | <code>  p.nodes[&quot;#loanFilter&quot;].value = &quot;RETURNED&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 184 | <code>  p.nodes[&quot;#loanFilter&quot;].onchange();</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 185 | <code>  assert.match(p.nodes[&quot;#loanTable&quot;].innerHTML, /Returned book/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 186 | <code>  assert.doesNotMatch(p.nodes[&quot;#loanTable&quot;].innerHTML, /Current book/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 187 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 188 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 189 | <code>test(&quot;staff desk lists active members and available books without member dashboard reads&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 190 | <code>  const data = snapshot();</code> | Local state, DOM reference বা callback/result assign করে। |
| 191 | <code>  data.students = [</code> | Local state, DOM reference বা callback/result assign করে। |
| 192 | <code>    { student_id: 17, name: &quot;Active member&quot;, membership_status: &quot;ACTIVE&quot; },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 193 | <code>    { student_id: 18, name: &quot;Disabled member&quot;, membership_status: &quot;DISABLED&quot; },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 194 | <code>  ];</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 195 | <code>  data.books.push({ book_id: 4, title: &quot;Unavailable book&quot;, available_quantity: 0 });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 196 | <code>  const p = await page(data, &quot;reservations&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 197 | <code>  assert.match(p.nodes[&quot;#reserveMember&quot;].innerHTML, /Active member/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 198 | <code>  assert.doesNotMatch(p.nodes[&quot;#reserveMember&quot;].innerHTML, /Disabled member/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 199 | <code>  assert.match(p.nodes[&quot;#reserveBook&quot;].innerHTML, /Book/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 200 | <code>  assert.doesNotMatch(p.nodes[&quot;#reserveBook&quot;].innerHTML, /Unavailable book/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 201 | <code>  assert.equal(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 202 | <code>    p.requests.some((request) =&gt; request.path === &quot;/student/dashboard&quot;),</code> | Local state, DOM reference বা callback/result assign করে। |
| 203 | <code>    false,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 204 | <code>  );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 205 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 206 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 207 | <code>test(&quot;staff can collect a reserved copy through the shared action coordinator&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 208 | <code>  const data = snapshot();</code> | Local state, DOM reference বা callback/result assign করে। |
| 209 | <code>  data.students = [];</code> | Local state, DOM reference বা callback/result assign করে। |
| 210 | <code>  data.reservations = [{ reservation_id: 12, student_id: 17, title: &quot;Book&quot;, status: &quot;ACTIVE&quot; }];</code> | Local state, DOM reference বা callback/result assign করে। |
| 211 | <code>  const p = await page(data, &quot;reservations&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 212 | <code>  assert.match(p.nodes[&quot;#reservationTable&quot;].innerHTML, /data-collect=&quot;12&quot;/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 213 | <code>  await p.collectButton.onclick();</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 214 | <code>  const request = p.requests.find((item) =&gt; item.options);</code> | Local state, DOM reference বা callback/result assign করে। |
| 215 | <code>  assert.equal(request.path, &quot;/reservations/12/collect&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 216 | <code>  assert.equal(request.options.method, &quot;POST&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 217 | <code>  assert.equal(p.collectButton.disabled, false);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 218 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
