# tests/notifications.test.cjs

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/notifications.test.cjs)। Snapshot 2026-10-04; 265 lines; SHA-256 `b38dfed0cde9b48b1fa93541ae80514b8c203677b3aa86eebd29610713e0f45a`।

## Function / object / element inventory

### `notifications(storage = new Map()` — L6

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

## সম্পূর্ণ original source

```javascript
const assert = require("node:assert/strict");
const { test } = require("node:test");
const fs = require("node:fs");
const vm = require("node:vm");

function notifications(storage = new Map()) {
  const nodes = new Map();
  const buttons = ["all", "reservation", "fine"].map((filter) => ({
    dataset: { alertFilter: filter },
    setAttribute() {},
  }));
  const $ = (selector) => {
    if (!nodes.has(selector))
      nodes.set(selector, {
        hidden: selector === "#notificationPanel",
        textContent: "",
        innerHTML: "",
        disabled: false,
        setAttribute(name, value) {
          this[name] = value;
        },
        querySelectorAll: (selector) => (selector === "[data-alert-filter]" ? buttons : []),
        contains: () => true,
        focus() {},
      });
    return nodes.get(selector);
  };
  const messages = [];
  const window = {
    localStorage: {
      getItem: (key) => storage.get(key),
      setItem: (key, value) => storage.set(key, value),
    },
  };
  vm.runInNewContext(fs.readFileSync("frontend/notifications.js", "utf8"), {
    window,
    document: { addEventListener() {} },
    Date,
    Intl,
  });
  const manager = window.LibraryNotifications.create({
    $,
    escapeHtml: String,
    toast: (message) => messages.push(message),
  });
  return { library: window.LibraryNotifications, manager, $, messages, buttons, storage };
}

const staff = { user_id: 1, username: "admin", user_type: "ADMIN" };

test("daily overdue updates show today's fine, daily rate and return/payment action", () => {
  const p = notifications();
  const member = { user_type: "STUDENT", student_id: 2 };
  const data = {
    issues: [
      {
        issue_id: 18,
        student_id: 2,
        status: "ISSUED",
        title: "Java",
        due_date: "2026-10-01",
        overdue_days: 3,
        current_fine: 30,
      },
    ],
  };
  const first = p.library.buildItems(data, member, Date.UTC(2026, 9, 4, 6))[0];
  assert.match(first.note, /Tk 30 estimated today.*3 overdue day.*Tk 10\/day until return/);
  assert.match(first.note, /Return the book and pay the final fine/);
  data.issues[0].overdue_days = 4;
  data.issues[0].current_fine = 40;
  const next = p.library.buildItems(data, member, Date.UTC(2026, 9, 5, 6))[0];
  assert.match(next.note, /Tk 40 estimated today/);
  assert.notEqual(first.key, next.key);
});

test("urgent overdue and unpaid fines outrank newer reservations and due reminders", () => {
  const p = notifications();
  const data = snapshot();
  data.reservations[0].reservation_id = 999;
  data.issues = [
    { issue_id: 1, status: "ISSUED", current_fine: 50, due_date: "2026-10-01" },
    { issue_id: 100, status: "ISSUED", due_date: "2026-10-07" },
  ];
  const alerts = p.library.buildItems(data, staff, Date.UTC(2026, 9, 4, 6));
  assert.deepEqual(
    Array.from(alerts, (item) => item.key.split(":")[0]),
    ["overdue", "fine", "due", "reservation"],
  );
});

test("return reminders start exactly three Dhaka calendar days before the due date", () => {
  const p = notifications();
  const data = {
    issues: [
      {
        issue_id: 15,
        student_id: 2,
        student: "Rahim",
        title: "Algorithms",
        status: "ISSUED",
        due_date: "2026-10-07",
        issue_date: "2026-09-22",
        copy_no: 4,
      },
    ],
  };
  assert.equal(p.library.buildItems(data, staff, Date.UTC(2026, 9, 3, 17, 59, 59)).length, 0);
  const alerts = p.library.buildItems(data, staff, Date.UTC(2026, 9, 3, 18));
  assert.equal(alerts.length, 1);
  assert.equal(alerts[0].type, "due");
  assert.match(alerts[0].title, /3 days/);
  assert.match(alerts[0].detail, /Rahim.*Algorithms.*Copy #4/);
  assert.match(alerts[0].note, /2026-09-22.*2026-10-07/);
  assert.equal(alerts[0].href, "/circulation");
});

test("due-day reminders become overdue fine alerts and returned loans disappear", () => {
  const p = notifications();
  const now = Date.UTC(2026, 9, 4, 6);
  const issue = {
    issue_id: 15,
    student_id: 2,
    title: "Algorithms",
    status: "ISSUED",
    due_date: "2026-10-04",
  };
  const member = { user_type: "STUDENT", student_id: 2 };
  let alerts = p.library.buildItems({ issues: [issue] }, member, now);
  assert.match(alerts[0].title, /due today/);
  assert.equal(alerts[0].href, "/student#loans");
  issue.due_date = "2026-10-03";
  issue.current_fine = 10;
  alerts = p.library.buildItems({ issues: [issue] }, member, now);
  assert.equal(alerts.length, 1);
  assert.equal(alerts[0].type, "fine");
  issue.status = "RETURNED";
  assert.equal(p.library.buildItems({ issues: [issue] }, member, now).length, 0);
  issue.status = "ISSUED";
  issue.student_id = 3;
  assert.equal(p.library.buildItems({ issues: [issue] }, member, now).length, 0);
});

test("invalid dates are ignored and reminders distinguish each day of the window", () => {
  const p = notifications();
  assert.equal(p.library.daysUntilDue("2026-02-30"), null);
  assert.equal(p.library.daysUntilDue(null), null);
  const data = { issues: [{ issue_id: 7, status: "ISSUED", due_date: "2026-10-07" }] };
  const early = p.library.buildItems(data, staff, Date.UTC(2026, 9, 4))[0];
  const next = p.library.buildItems(data, staff, Date.UTC(2026, 9, 5))[0];
  assert.notEqual(early.key, next.key);
  assert.match(next.title, /2 days/);
});
const snapshot = () => ({
  reservations: [
    {
      reservation_id: 8,
      student_id: 2,
      student: "Rahim",
      title: "Clean Code",
      copy_no: 3,
      status: "ACTIVE",
      expires_at: "2099-10-07 12:00:00",
    },
  ],
  fines: [
    {
      fine_id: 4,
      issue_id: 9,
      student_id: 2,
      student: "Rahim",
      title: "Database",
      amount: 100,
      paid_amount: 20,
      balance: 80,
      payment_status: "UNPAID",
    },
  ],
  issues: [],
});

test("alerts show active holds and remaining fines, excluding paid and expired records", () => {
  const p = notifications();
  const data = snapshot();
  data.reservations.push({
    ...data.reservations[0],
    reservation_id: 9,
    expires_at: "2000-01-01 12:00:00",
  });
  data.fines.push({ ...data.fines[0], fine_id: 5, payment_status: "PAID", balance: 0 });
  const alerts = p.library.buildItems(data, staff);
  assert.equal(alerts.length, 2);
  assert.match(alerts.find((alert) => alert.type === "fine").note, /Tk 80 outstanding/);
  assert.equal(alerts.find((alert) => alert.type === "reservation").href, "/reservations");
});

test("student alerts are scoped to their own member ID and dashboard sections", () => {
  const p = notifications();
  const data = snapshot();
  data.reservations.push({ ...data.reservations[0], reservation_id: 10, student_id: 3 });
  data.fines.push({ ...data.fines[0], fine_id: 6, student_id: 3 });
  const alerts = p.library.buildItems(data, { user_type: "STUDENT", student_id: 2 });
  assert.equal(alerts.length, 2);
  assert.ok(alerts.every((alert) => alert.href.startsWith("/student#")));
  assert.ok(alerts.every((alert) => !alert.detail.includes("Rahim")));
});

test("overdue estimates appear without double counting a recorded fine", () => {
  const p = notifications();
  const data = snapshot();
  data.issues = [
    { issue_id: 9, status: "ISSUED", current_fine: 80 },
    { issue_id: 10, status: "ISSUED", current_fine: 30, title: "Java", student: "Karim" },
    { issue_id: 11, status: "RETURNED", current_fine: 50 },
  ];
  const alerts = p.library.buildItems(data, staff);
  assert.equal(alerts.length, 3);
  assert.match(alerts.find((alert) => alert.key.startsWith("overdue:")).note, /Tk 30 estimated/);
});

test("read status survives navigation and stays separate for different accounts", () => {
  const storage = new Map();
  const first = notifications(storage);
  first.manager.setSession(staff);
  first.manager.update(snapshot());
  assert.equal(first.$("#notificationBadge").textContent, "2");
  first.$("#notificationReadAll").onclick();
  assert.equal(first.$("#notificationBadge").hidden, true);
  assert.match(first.$("#notificationList").innerHTML, /Clean Code/);
  assert.ok([...storage.values()].every((value) => !value.includes("Rahim")));
  const second = notifications(storage);
  second.manager.setSession(staff);
  second.manager.update(snapshot());
  assert.equal(second.$("#notificationBadge").hidden, true);
  second.manager.setSession({ ...staff, user_id: 2 });
  assert.equal(second.$("#notificationBadge").textContent, "2");
});

test("new requests announce once and resolved records disappear after refresh", () => {
  const p = notifications();
  p.manager.setSession(staff);
  p.manager.update(snapshot());
  assert.equal(p.messages.length, 0);
  const data = snapshot();
  data.reservations.push({ ...data.reservations[0], reservation_id: 12 });
  p.manager.update(data);
  p.manager.update(data);
  assert.equal(p.messages.length, 1);
  data.reservations = [];
  data.fines = [];
  p.manager.update(data);
  assert.equal(p.$("#notificationBadge").hidden, true);
});

test("offline state retains alerts and shows their freshness clearly", () => {
  const p = notifications();
  p.manager.setSession(staff);
  p.manager.update(snapshot());
  p.manager.update({}, false);
  assert.equal(p.$("#notificationBadge").textContent, "2");
  assert.match(p.$("#notificationFreshness").textContent, /Connection lost/);
  p.buttons[2].onclick();
  assert.doesNotMatch(p.$("#notificationList").innerHTML, /Clean Code/);
  assert.match(p.$("#notificationList").innerHTML, /Database/);
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
| 6 | <code>function notifications(storage = new Map()) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 7 | <code>  const nodes = new Map();</code> | Local state, DOM reference বা callback/result assign করে। |
| 8 | <code>  const buttons = [&quot;all&quot;, &quot;reservation&quot;, &quot;fine&quot;].map((filter) =&gt; ({</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 9 | <code>    dataset: { alertFilter: filter },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 10 | <code>    setAttribute() {},</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 11 | <code>  }));</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 12 | <code>  const $ = (selector) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 13 | <code>    if (!nodes.has(selector))</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 14 | <code>      nodes.set(selector, {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 15 | <code>        hidden: selector === &quot;#notificationPanel&quot;,</code> | Local state, DOM reference বা callback/result assign করে। |
| 16 | <code>        textContent: &quot;&quot;,</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 17 | <code>        innerHTML: &quot;&quot;,</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 18 | <code>        disabled: false,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 19 | <code>        setAttribute(name, value) {</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 20 | <code>          this[name] = value;</code> | Local state, DOM reference বা callback/result assign করে। |
| 21 | <code>        },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 22 | <code>        querySelectorAll: (selector) =&gt; (selector === &quot;[data-alert-filter]&quot; ? buttons : []),</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 23 | <code>        contains: () =&gt; true,</code> | Local state, DOM reference বা callback/result assign করে। |
| 24 | <code>        focus() {},</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 25 | <code>      });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 26 | <code>    return nodes.get(selector);</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 27 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 28 | <code>  const messages = [];</code> | Local state, DOM reference বা callback/result assign করে। |
| 29 | <code>  const window = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 30 | <code>    localStorage: {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 31 | <code>      getItem: (key) =&gt; storage.get(key),</code> | Local state, DOM reference বা callback/result assign করে। |
| 32 | <code>      setItem: (key, value) =&gt; storage.set(key, value),</code> | Local state, DOM reference বা callback/result assign করে। |
| 33 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 34 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 35 | <code>  vm.runInNewContext(fs.readFileSync(&quot;frontend/notifications.js&quot;, &quot;utf8&quot;), {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 36 | <code>    window,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 37 | <code>    document: { addEventListener() {} },</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 38 | <code>    Date,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 39 | <code>    Intl,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 40 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 41 | <code>  const manager = window.LibraryNotifications.create({</code> | Local state, DOM reference বা callback/result assign করে। |
| 42 | <code>    $,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 43 | <code>    escapeHtml: String,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 44 | <code>    toast: (message) =&gt; messages.push(message),</code> | Local state, DOM reference বা callback/result assign করে। |
| 45 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 46 | <code>  return { library: window.LibraryNotifications, manager, $, messages, buttons, storage };</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 47 | <code>}</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 48 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 49 | <code>const staff = { user_id: 1, username: &quot;admin&quot;, user_type: &quot;ADMIN&quot; };</code> | Local state, DOM reference বা callback/result assign করে। |
| 50 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 51 | <code>test(&quot;daily overdue updates show today&#x27;s fine, daily rate and return/payment action&quot;, () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 52 | <code>  const p = notifications();</code> | Local state, DOM reference বা callback/result assign করে। |
| 53 | <code>  const member = { user_type: &quot;STUDENT&quot;, student_id: 2 };</code> | Local state, DOM reference বা callback/result assign করে। |
| 54 | <code>  const data = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 55 | <code>    issues: [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 56 | <code>      {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 57 | <code>        issue_id: 18,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 58 | <code>        student_id: 2,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 59 | <code>        status: &quot;ISSUED&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 60 | <code>        title: &quot;Java&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 61 | <code>        due_date: &quot;2026-10-01&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 62 | <code>        overdue_days: 3,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 63 | <code>        current_fine: 30,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 64 | <code>      },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 65 | <code>    ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 66 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 67 | <code>  const first = p.library.buildItems(data, member, Date.UTC(2026, 9, 4, 6))[0];</code> | Local state, DOM reference বা callback/result assign করে। |
| 68 | <code>  assert.match(first.note, /Tk 30 estimated today.*3 overdue day.*Tk 10\/day until return/);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 69 | <code>  assert.match(first.note, /Return the book and pay the final fine/);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 70 | <code>  data.issues[0].overdue_days = 4;</code> | Local state, DOM reference বা callback/result assign করে। |
| 71 | <code>  data.issues[0].current_fine = 40;</code> | Local state, DOM reference বা callback/result assign করে। |
| 72 | <code>  const next = p.library.buildItems(data, member, Date.UTC(2026, 9, 5, 6))[0];</code> | Local state, DOM reference বা callback/result assign করে। |
| 73 | <code>  assert.match(next.note, /Tk 40 estimated today/);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 74 | <code>  assert.notEqual(first.key, next.key);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 75 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 76 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 77 | <code>test(&quot;urgent overdue and unpaid fines outrank newer reservations and due reminders&quot;, () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 78 | <code>  const p = notifications();</code> | Local state, DOM reference বা callback/result assign করে। |
| 79 | <code>  const data = snapshot();</code> | Local state, DOM reference বা callback/result assign করে। |
| 80 | <code>  data.reservations[0].reservation_id = 999;</code> | Local state, DOM reference বা callback/result assign করে। |
| 81 | <code>  data.issues = [</code> | Local state, DOM reference বা callback/result assign করে। |
| 82 | <code>    { issue_id: 1, status: &quot;ISSUED&quot;, current_fine: 50, due_date: &quot;2026-10-01&quot; },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 83 | <code>    { issue_id: 100, status: &quot;ISSUED&quot;, due_date: &quot;2026-10-07&quot; },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 84 | <code>  ];</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 85 | <code>  const alerts = p.library.buildItems(data, staff, Date.UTC(2026, 9, 4, 6));</code> | Local state, DOM reference বা callback/result assign করে। |
| 86 | <code>  assert.deepEqual(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 87 | <code>    Array.from(alerts, (item) =&gt; item.key.split(&quot;:&quot;)[0]),</code> | Local state, DOM reference বা callback/result assign করে। |
| 88 | <code>    [&quot;overdue&quot;, &quot;fine&quot;, &quot;due&quot;, &quot;reservation&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 89 | <code>  );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 90 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 91 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 92 | <code>test(&quot;return reminders start exactly three Dhaka calendar days before the due date&quot;, () =&gt; {</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 93 | <code>  const p = notifications();</code> | Local state, DOM reference বা callback/result assign করে। |
| 94 | <code>  const data = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 95 | <code>    issues: [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 96 | <code>      {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 97 | <code>        issue_id: 15,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 98 | <code>        student_id: 2,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 99 | <code>        student: &quot;Rahim&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 100 | <code>        title: &quot;Algorithms&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 101 | <code>        status: &quot;ISSUED&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 102 | <code>        due_date: &quot;2026-10-07&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 103 | <code>        issue_date: &quot;2026-09-22&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 104 | <code>        copy_no: 4,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 105 | <code>      },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 106 | <code>    ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 107 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 108 | <code>  assert.equal(p.library.buildItems(data, staff, Date.UTC(2026, 9, 3, 17, 59, 59)).length, 0);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 109 | <code>  const alerts = p.library.buildItems(data, staff, Date.UTC(2026, 9, 3, 18));</code> | Local state, DOM reference বা callback/result assign করে। |
| 110 | <code>  assert.equal(alerts.length, 1);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 111 | <code>  assert.equal(alerts[0].type, &quot;due&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 112 | <code>  assert.match(alerts[0].title, /3 days/);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 113 | <code>  assert.match(alerts[0].detail, /Rahim.*Algorithms.*Copy #4/);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 114 | <code>  assert.match(alerts[0].note, /2026-09-22.*2026-10-07/);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 115 | <code>  assert.equal(alerts[0].href, &quot;/circulation&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 116 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 117 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 118 | <code>test(&quot;due-day reminders become overdue fine alerts and returned loans disappear&quot;, () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 119 | <code>  const p = notifications();</code> | Local state, DOM reference বা callback/result assign করে। |
| 120 | <code>  const now = Date.UTC(2026, 9, 4, 6);</code> | Local state, DOM reference বা callback/result assign করে। |
| 121 | <code>  const issue = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 122 | <code>    issue_id: 15,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 123 | <code>    student_id: 2,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 124 | <code>    title: &quot;Algorithms&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 125 | <code>    status: &quot;ISSUED&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 126 | <code>    due_date: &quot;2026-10-04&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 127 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 128 | <code>  const member = { user_type: &quot;STUDENT&quot;, student_id: 2 };</code> | Local state, DOM reference বা callback/result assign করে। |
| 129 | <code>  let alerts = p.library.buildItems({ issues: [issue] }, member, now);</code> | Local state, DOM reference বা callback/result assign করে। |
| 130 | <code>  assert.match(alerts[0].title, /due today/);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 131 | <code>  assert.equal(alerts[0].href, &quot;/student#loans&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 132 | <code>  issue.due_date = &quot;2026-10-03&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 133 | <code>  issue.current_fine = 10;</code> | Local state, DOM reference বা callback/result assign করে। |
| 134 | <code>  alerts = p.library.buildItems({ issues: [issue] }, member, now);</code> | Local state, DOM reference বা callback/result assign করে। |
| 135 | <code>  assert.equal(alerts.length, 1);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 136 | <code>  assert.equal(alerts[0].type, &quot;fine&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 137 | <code>  issue.status = &quot;RETURNED&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 138 | <code>  assert.equal(p.library.buildItems({ issues: [issue] }, member, now).length, 0);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 139 | <code>  issue.status = &quot;ISSUED&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 140 | <code>  issue.student_id = 3;</code> | Local state, DOM reference বা callback/result assign করে। |
| 141 | <code>  assert.equal(p.library.buildItems({ issues: [issue] }, member, now).length, 0);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 142 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 143 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 144 | <code>test(&quot;invalid dates are ignored and reminders distinguish each day of the window&quot;, () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 145 | <code>  const p = notifications();</code> | Local state, DOM reference বা callback/result assign করে। |
| 146 | <code>  assert.equal(p.library.daysUntilDue(&quot;2026-02-30&quot;), null);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 147 | <code>  assert.equal(p.library.daysUntilDue(null), null);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 148 | <code>  const data = { issues: [{ issue_id: 7, status: &quot;ISSUED&quot;, due_date: &quot;2026-10-07&quot; }] };</code> | Local state, DOM reference বা callback/result assign করে। |
| 149 | <code>  const early = p.library.buildItems(data, staff, Date.UTC(2026, 9, 4))[0];</code> | Local state, DOM reference বা callback/result assign করে। |
| 150 | <code>  const next = p.library.buildItems(data, staff, Date.UTC(2026, 9, 5))[0];</code> | Local state, DOM reference বা callback/result assign করে। |
| 151 | <code>  assert.notEqual(early.key, next.key);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 152 | <code>  assert.match(next.title, /2 days/);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 153 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 154 | <code>const snapshot = () =&gt; ({</code> | Local state, DOM reference বা callback/result assign করে। |
| 155 | <code>  reservations: [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 156 | <code>    {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 157 | <code>      reservation_id: 8,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 158 | <code>      student_id: 2,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 159 | <code>      student: &quot;Rahim&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 160 | <code>      title: &quot;Clean Code&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 161 | <code>      copy_no: 3,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 162 | <code>      status: &quot;ACTIVE&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 163 | <code>      expires_at: &quot;2099-10-07 12:00:00&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 164 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 165 | <code>  ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 166 | <code>  fines: [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 167 | <code>    {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 168 | <code>      fine_id: 4,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 169 | <code>      issue_id: 9,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 170 | <code>      student_id: 2,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 171 | <code>      student: &quot;Rahim&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 172 | <code>      title: &quot;Database&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 173 | <code>      amount: 100,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 174 | <code>      paid_amount: 20,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 175 | <code>      balance: 80,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 176 | <code>      payment_status: &quot;UNPAID&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 177 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 178 | <code>  ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 179 | <code>  issues: [],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 180 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 181 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 182 | <code>test(&quot;alerts show active holds and remaining fines, excluding paid and expired records&quot;, () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 183 | <code>  const p = notifications();</code> | Local state, DOM reference বা callback/result assign করে। |
| 184 | <code>  const data = snapshot();</code> | Local state, DOM reference বা callback/result assign করে। |
| 185 | <code>  data.reservations.push({</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 186 | <code>    ...data.reservations[0],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 187 | <code>    reservation_id: 9,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 188 | <code>    expires_at: &quot;2000-01-01 12:00:00&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 189 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 190 | <code>  data.fines.push({ ...data.fines[0], fine_id: 5, payment_status: &quot;PAID&quot;, balance: 0 });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 191 | <code>  const alerts = p.library.buildItems(data, staff);</code> | Local state, DOM reference বা callback/result assign করে। |
| 192 | <code>  assert.equal(alerts.length, 2);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 193 | <code>  assert.match(alerts.find((alert) =&gt; alert.type === &quot;fine&quot;).note, /Tk 80 outstanding/);</code> | Local state, DOM reference বা callback/result assign করে। |
| 194 | <code>  assert.equal(alerts.find((alert) =&gt; alert.type === &quot;reservation&quot;).href, &quot;/reservations&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 195 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 196 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 197 | <code>test(&quot;student alerts are scoped to their own member ID and dashboard sections&quot;, () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 198 | <code>  const p = notifications();</code> | Local state, DOM reference বা callback/result assign করে। |
| 199 | <code>  const data = snapshot();</code> | Local state, DOM reference বা callback/result assign করে। |
| 200 | <code>  data.reservations.push({ ...data.reservations[0], reservation_id: 10, student_id: 3 });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 201 | <code>  data.fines.push({ ...data.fines[0], fine_id: 6, student_id: 3 });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 202 | <code>  const alerts = p.library.buildItems(data, { user_type: &quot;STUDENT&quot;, student_id: 2 });</code> | Local state, DOM reference বা callback/result assign করে। |
| 203 | <code>  assert.equal(alerts.length, 2);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 204 | <code>  assert.ok(alerts.every((alert) =&gt; alert.href.startsWith(&quot;/student#&quot;)));</code> | Local state, DOM reference বা callback/result assign করে। |
| 205 | <code>  assert.ok(alerts.every((alert) =&gt; !alert.detail.includes(&quot;Rahim&quot;)));</code> | Local state, DOM reference বা callback/result assign করে। |
| 206 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 207 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 208 | <code>test(&quot;overdue estimates appear without double counting a recorded fine&quot;, () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 209 | <code>  const p = notifications();</code> | Local state, DOM reference বা callback/result assign করে। |
| 210 | <code>  const data = snapshot();</code> | Local state, DOM reference বা callback/result assign করে। |
| 211 | <code>  data.issues = [</code> | Local state, DOM reference বা callback/result assign করে। |
| 212 | <code>    { issue_id: 9, status: &quot;ISSUED&quot;, current_fine: 80 },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 213 | <code>    { issue_id: 10, status: &quot;ISSUED&quot;, current_fine: 30, title: &quot;Java&quot;, student: &quot;Karim&quot; },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 214 | <code>    { issue_id: 11, status: &quot;RETURNED&quot;, current_fine: 50 },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 215 | <code>  ];</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 216 | <code>  const alerts = p.library.buildItems(data, staff);</code> | Local state, DOM reference বা callback/result assign করে। |
| 217 | <code>  assert.equal(alerts.length, 3);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 218 | <code>  assert.match(alerts.find((alert) =&gt; alert.key.startsWith(&quot;overdue:&quot;)).note, /Tk 30 estimated/);</code> | Local state, DOM reference বা callback/result assign করে। |
| 219 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 220 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 221 | <code>test(&quot;read status survives navigation and stays separate for different accounts&quot;, () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 222 | <code>  const storage = new Map();</code> | Local state, DOM reference বা callback/result assign করে। |
| 223 | <code>  const first = notifications(storage);</code> | Local state, DOM reference বা callback/result assign করে। |
| 224 | <code>  first.manager.setSession(staff);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 225 | <code>  first.manager.update(snapshot());</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 226 | <code>  assert.equal(first.$(&quot;#notificationBadge&quot;).textContent, &quot;2&quot;);</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 227 | <code>  first.$(&quot;#notificationReadAll&quot;).onclick();</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 228 | <code>  assert.equal(first.$(&quot;#notificationBadge&quot;).hidden, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 229 | <code>  assert.match(first.$(&quot;#notificationList&quot;).innerHTML, /Clean Code/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 230 | <code>  assert.ok([...storage.values()].every((value) =&gt; !value.includes(&quot;Rahim&quot;)));</code> | Local state, DOM reference বা callback/result assign করে। |
| 231 | <code>  const second = notifications(storage);</code> | Local state, DOM reference বা callback/result assign করে। |
| 232 | <code>  second.manager.setSession(staff);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 233 | <code>  second.manager.update(snapshot());</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 234 | <code>  assert.equal(second.$(&quot;#notificationBadge&quot;).hidden, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 235 | <code>  second.manager.setSession({ ...staff, user_id: 2 });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 236 | <code>  assert.equal(second.$(&quot;#notificationBadge&quot;).textContent, &quot;2&quot;);</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 237 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 238 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 239 | <code>test(&quot;new requests announce once and resolved records disappear after refresh&quot;, () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 240 | <code>  const p = notifications();</code> | Local state, DOM reference বা callback/result assign করে। |
| 241 | <code>  p.manager.setSession(staff);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 242 | <code>  p.manager.update(snapshot());</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 243 | <code>  assert.equal(p.messages.length, 0);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 244 | <code>  const data = snapshot();</code> | Local state, DOM reference বা callback/result assign করে। |
| 245 | <code>  data.reservations.push({ ...data.reservations[0], reservation_id: 12 });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 246 | <code>  p.manager.update(data);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 247 | <code>  p.manager.update(data);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 248 | <code>  assert.equal(p.messages.length, 1);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 249 | <code>  data.reservations = [];</code> | Local state, DOM reference বা callback/result assign করে। |
| 250 | <code>  data.fines = [];</code> | Local state, DOM reference বা callback/result assign করে। |
| 251 | <code>  p.manager.update(data);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 252 | <code>  assert.equal(p.$(&quot;#notificationBadge&quot;).hidden, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 253 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 254 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 255 | <code>test(&quot;offline state retains alerts and shows their freshness clearly&quot;, () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 256 | <code>  const p = notifications();</code> | Local state, DOM reference বা callback/result assign করে। |
| 257 | <code>  p.manager.setSession(staff);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 258 | <code>  p.manager.update(snapshot());</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 259 | <code>  p.manager.update({}, false);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 260 | <code>  assert.equal(p.$(&quot;#notificationBadge&quot;).textContent, &quot;2&quot;);</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 261 | <code>  assert.match(p.$(&quot;#notificationFreshness&quot;).textContent, /Connection lost/);</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 262 | <code>  p.buttons[2].onclick();</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 263 | <code>  assert.doesNotMatch(p.$(&quot;#notificationList&quot;).innerHTML, /Clean Code/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 264 | <code>  assert.match(p.$(&quot;#notificationList&quot;).innerHTML, /Database/);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 265 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
