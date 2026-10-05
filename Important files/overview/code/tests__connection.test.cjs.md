# tests/connection.test.cjs

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/connection.test.cjs)। Snapshot 2026-10-04; 216 lines; SHA-256 `10f9f8ee6d796f54fa2ad1e0ab613ccd2daaa635e4ec2bf782fbe8722a010b04`।

## Function / object / element inventory

### `app(fetch, options = {})` — L6

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

## সম্পূর্ণ original source

```javascript
const assert = require("node:assert/strict");
const { test } = require("node:test");
const fs = require("node:fs");
const vm = require("node:vm");

function app(fetch, options = {}) {
  const timers = [],
    events = {},
    redirects = [];
  const node = () => ({
    innerHTML: "",
    textContent: "",
    classList: { toggle() {}, add() {} },
    setAttribute() {},
  });
  const nodes = {};
  const document = {
    hidden: false,
    body: { dataset: { page: "overview" } },
    querySelector: (selector) => (nodes[selector] ||= node()),
    querySelectorAll: () => [],
    addEventListener: (name, fn) => {
      events[name] = fn;
    },
  };
  const context = vm.createContext({
    document,
    window: {
      LibraryNotifications: options.notifications,
      location: { replace: (path) => redirects.push(path) },
      setInterval: (fn) => {
        timers.push(fn);
        return 1;
      },
      addEventListener: (name, fn) => {
        events[name] = fn;
      },
    },
    fetch,
    AbortSignal,
    TypeError,
    URLSearchParams,
    Intl,
    Date: options.Date || Date,
    setTimeout: (fn) => {
      fn();
      return 1;
    },
    clearTimeout() {},
  });
  vm.runInContext(fs.readFileSync("frontend/shared.js", "utf8"), context);
  return { library: vm.runInContext("LibraryApp", context), timers, events, redirects };
}
const response = (status, value) => ({ status, ok: status < 400, json: async () => value });

test("circulation sorts overdue and upcoming returns ahead of active loans and returned history", () => {
  const p = app(async (path) => response(200, data(path)));
  const items = [
    { issue_id: 99, status: "RETURNED", issue_date: "2099-01-01" },
    { issue_id: 5, status: "ISSUED", due_date: p.library.dateFromToday(10) },
    { issue_id: 3, status: "ISSUED", due_date: p.library.dateFromToday(-2) },
    { issue_id: 4, status: "ISSUED", due_date: p.library.dateFromToday(2) },
    { issue_id: 2, status: "ISSUED", due_date: p.library.dateFromToday(-10) },
  ];
  assert.deepEqual(
    Array.from(p.library.sortIssues(items), (item) => item.issue_id),
    [2, 3, 4, 5, 99],
  );
  assert.equal(items[0].issue_id, 99);
});
const data = (path) =>
  path === "/api/snapshot"
    ? { books: [], students: [], issues: [], fines: [], meta: { authors: [], categories: [] } }
    : path === "/api/auth/session"
      ? { username: "admin", user_type: "ADMIN" }
      : path === "/api/meta"
        ? { authors: [], categories: [] }
        : [];

test("temporary read failure retries and load becomes connected", async () => {
  let reads = 0;
  const p = app(async (path) =>
    path === "/api/snapshot" && ++reads === 1 ? response(503, {}) : response(200, data(path)),
  );
  assert.equal(await p.library.loadData(() => {}), true);
  assert.equal(reads, 2);
});

test("overlapping refreshes share one data load", async () => {
  let reads = 0,
    renders = 0;
  const p = app(async (path) => {
    if (path === "/api/snapshot") reads++;
    return response(200, data(path));
  });
  await Promise.all([p.library.loadData(() => renders++), p.library.loadData(() => renders++)]);
  assert.equal(reads, 1);
  assert.equal(renders, 1);
});

test("older server without snapshot uses existing routes and stays connected", async () => {
  const paths = [];
  const p = app(async (path) => {
    paths.push(path);
    if (path === "/api/snapshot") return response(404, { detail: "Not Found" });
    return response(200, path === "/api/books" ? [{ book_id: 1 }] : data(path));
  });
  assert.equal(await p.library.loadData(() => {}), true);
  assert.equal(p.library.state.books[0].book_id, 1);
  assert.equal(await p.library.loadData(() => {}), true);
  assert.equal(paths.filter((path) => path === "/api/snapshot").length, 1);
  for (const name of ["books", "students", "issues", "fines", "meta"]) {
    assert.equal(paths.filter((path) => path === `/api/${name}`).length, 2);
  }
});

test("snapshot database errors stay offline without falling back", async () => {
  const paths = [];
  const p = app(async (path) => {
    paths.push(path);
    return path === "/api/auth/session"
      ? response(200, data(path))
      : response(503, { detail: "Unavailable" });
  });
  assert.equal(await p.library.loadData(() => {}), false);
  assert.equal(paths.includes("/api/books"), false);
});

test("mutation failures are not automatically replayed", async () => {
  let writes = 0;
  const p = app(async (path) => {
    if (path === "/api/auth/session") return response(200, data(path));
    writes++;
    return response(503, { detail: "Database unavailable" });
  });
  await assert.rejects(p.library.api("/issues", { method: "POST" }), /Database unavailable/);
  assert.equal(writes, 1);
});

test("monitor restores live data after outage", async () => {
  let offline = true;
  const p = app(async (path) =>
    path !== "/api/auth/session" && offline
      ? response(503, { detail: "Unavailable" })
      : response(200, data(path)),
  );
  assert.equal(await p.library.loadData(() => {}), false);
  offline = false;
  await p.timers[0]();
  assert.equal(p.library.state.online, true);
});

test("live notifications refresh from the shared snapshot after 30 seconds", async () => {
  let now = 0;
  class Clock extends Date {
    static now() {
      return now;
    }
  }
  let reads = 0;
  const updates = [];
  const sessions = [];
  const p = app(
    async (path) => {
      if (path === "/api/snapshot") {
        reads++;
        return response(200, { ...data(path), reservations: [{ reservation_id: reads }] });
      }
      return response(200, data(path));
    },
    {
      Date: Clock,
      notifications: {
        create: () => ({
          setSession: (session) => sessions.push(session),
          update: (snapshot, online) =>
            updates.push({ reservation: snapshot.reservations[0].reservation_id, online }),
        }),
      },
    },
  );
  await p.library.loadData(() => {});
  now = 31000;
  await p.timers[0]();
  assert.equal(reads, 2);
  assert.equal(sessions[0].user_type, "ADMIN");
  assert.deepEqual(updates, [
    { reservation: 1, online: true },
    { reservation: 2, online: true },
  ]);
});

test("notification freshness becomes offline without clearing the last snapshot", async () => {
  let offline = false;
  const updates = [];
  const p = app(
    async (path) => {
      if (offline && path !== "/api/auth/session") return response(503, { detail: "Unavailable" });
      return response(200, { ...data(path), reservations: [{ reservation_id: 8 }] });
    },
    {
      notifications: {
        create: () => ({
          setSession() {},
          update: (snapshot, online) =>
            updates.push({ reservation: snapshot.reservations[0].reservation_id, online }),
        }),
      },
    },
  );
  await p.library.loadData(() => {});
  offline = true;
  await p.timers[0]();
  assert.deepEqual(updates.at(-1), { reservation: 8, online: false });
  assert.equal(p.library.state.reservations[0].reservation_id, 8);
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
| 6 | <code>function app(fetch, options = {}) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 7 | <code>  const timers = [],</code> | Local state, DOM reference বা callback/result assign করে। |
| 8 | <code>    events = {},</code> | Local state, DOM reference বা callback/result assign করে। |
| 9 | <code>    redirects = [];</code> | Local state, DOM reference বা callback/result assign করে। |
| 10 | <code>  const node = () =&gt; ({</code> | Local state, DOM reference বা callback/result assign করে। |
| 11 | <code>    innerHTML: &quot;&quot;,</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 12 | <code>    textContent: &quot;&quot;,</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 13 | <code>    classList: { toggle() {}, add() {} },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 14 | <code>    setAttribute() {},</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 15 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 16 | <code>  const nodes = {};</code> | Local state, DOM reference বা callback/result assign করে। |
| 17 | <code>  const document = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 18 | <code>    hidden: false,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 19 | <code>    body: { dataset: { page: &quot;overview&quot; } },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 20 | <code>    querySelector: (selector) =&gt; (nodes[selector] &#124;&#124;= node()),</code> | Local state, DOM reference বা callback/result assign করে। |
| 21 | <code>    querySelectorAll: () =&gt; [],</code> | Local state, DOM reference বা callback/result assign করে। |
| 22 | <code>    addEventListener: (name, fn) =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 23 | <code>      events[name] = fn;</code> | Local state, DOM reference বা callback/result assign করে। |
| 24 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 25 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 26 | <code>  const context = vm.createContext({</code> | Local state, DOM reference বা callback/result assign করে। |
| 27 | <code>    document,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 28 | <code>    window: {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 29 | <code>      LibraryNotifications: options.notifications,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 30 | <code>      location: { replace: (path) =&gt; redirects.push(path) },</code> | Local state, DOM reference বা callback/result assign করে। |
| 31 | <code>      setInterval: (fn) =&gt; {</code> | Timeout/reconnection/search debounce timer শুরু বা বন্ধ করে। |
| 32 | <code>        timers.push(fn);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 33 | <code>        return 1;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 34 | <code>      },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 35 | <code>      addEventListener: (name, fn) =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 36 | <code>        events[name] = fn;</code> | Local state, DOM reference বা callback/result assign করে। |
| 37 | <code>      },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 38 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 39 | <code>    fetch,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 40 | <code>    AbortSignal,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 41 | <code>    TypeError,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 42 | <code>    URLSearchParams,</code> | Form fields বা filters URL-encoded request body/query parameters-এ রূপান্তর করে। |
| 43 | <code>    Intl,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 44 | <code>    Date: options.Date &#124;&#124; Date,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 45 | <code>    setTimeout: (fn) =&gt; {</code> | Timeout/reconnection/search debounce timer শুরু বা বন্ধ করে। |
| 46 | <code>      fn();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 47 | <code>      return 1;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 48 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 49 | <code>    clearTimeout() {},</code> | Timeout/reconnection/search debounce timer শুরু বা বন্ধ করে। |
| 50 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 51 | <code>  vm.runInContext(fs.readFileSync(&quot;frontend/shared.js&quot;, &quot;utf8&quot;), context);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 52 | <code>  return { library: vm.runInContext(&quot;LibraryApp&quot;, context), timers, events, redirects };</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 53 | <code>}</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 54 | <code>const response = (status, value) =&gt; ({ status, ok: status &lt; 400, json: async () =&gt; value });</code> | Local state, DOM reference বা callback/result assign করে। |
| 55 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 56 | <code>test(&quot;circulation sorts overdue and upcoming returns ahead of active loans and returned history&quot;, () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 57 | <code>  const p = app(async (path) =&gt; response(200, data(path)));</code> | Local state, DOM reference বা callback/result assign করে। |
| 58 | <code>  const items = [</code> | Local state, DOM reference বা callback/result assign করে। |
| 59 | <code>    { issue_id: 99, status: &quot;RETURNED&quot;, issue_date: &quot;2099-01-01&quot; },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 60 | <code>    { issue_id: 5, status: &quot;ISSUED&quot;, due_date: p.library.dateFromToday(10) },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 61 | <code>    { issue_id: 3, status: &quot;ISSUED&quot;, due_date: p.library.dateFromToday(-2) },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 62 | <code>    { issue_id: 4, status: &quot;ISSUED&quot;, due_date: p.library.dateFromToday(2) },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 63 | <code>    { issue_id: 2, status: &quot;ISSUED&quot;, due_date: p.library.dateFromToday(-10) },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 64 | <code>  ];</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 65 | <code>  assert.deepEqual(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 66 | <code>    Array.from(p.library.sortIssues(items), (item) =&gt; item.issue_id),</code> | Local state, DOM reference বা callback/result assign করে। |
| 67 | <code>    [2, 3, 4, 5, 99],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 68 | <code>  );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 69 | <code>  assert.equal(items[0].issue_id, 99);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 70 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 71 | <code>const data = (path) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 72 | <code>  path === &quot;/api/snapshot&quot;</code> | Local state, DOM reference বা callback/result assign করে। |
| 73 | <code>    ? { books: [], students: [], issues: [], fines: [], meta: { authors: [], categories: [] } }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 74 | <code>    : path === &quot;/api/auth/session&quot;</code> | Local state, DOM reference বা callback/result assign করে। |
| 75 | <code>      ? { username: &quot;admin&quot;, user_type: &quot;ADMIN&quot; }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 76 | <code>      : path === &quot;/api/meta&quot;</code> | Local state, DOM reference বা callback/result assign করে। |
| 77 | <code>        ? { authors: [], categories: [] }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 78 | <code>        : [];</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 79 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 80 | <code>test(&quot;temporary read failure retries and load becomes connected&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 81 | <code>  let reads = 0;</code> | Local state, DOM reference বা callback/result assign করে। |
| 82 | <code>  const p = app(async (path) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 83 | <code>    path === &quot;/api/snapshot&quot; &amp;&amp; ++reads === 1 ? response(503, {}) : response(200, data(path)),</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 84 | <code>  );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 85 | <code>  assert.equal(await p.library.loadData(() =&gt; {}), true);</code> | Local state, DOM reference বা callback/result assign করে। |
| 86 | <code>  assert.equal(reads, 2);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 87 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 88 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 89 | <code>test(&quot;overlapping refreshes share one data load&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 90 | <code>  let reads = 0,</code> | Local state, DOM reference বা callback/result assign করে। |
| 91 | <code>    renders = 0;</code> | Local state, DOM reference বা callback/result assign করে। |
| 92 | <code>  const p = app(async (path) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 93 | <code>    if (path === &quot;/api/snapshot&quot;) reads++;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 94 | <code>    return response(200, data(path));</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 95 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 96 | <code>  await Promise.all([p.library.loadData(() =&gt; renders++), p.library.loadData(() =&gt; renders++)]);</code> | Local state, DOM reference বা callback/result assign করে। |
| 97 | <code>  assert.equal(reads, 1);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 98 | <code>  assert.equal(renders, 1);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 99 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 100 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 101 | <code>test(&quot;older server without snapshot uses existing routes and stays connected&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 102 | <code>  const paths = [];</code> | Local state, DOM reference বা callback/result assign করে। |
| 103 | <code>  const p = app(async (path) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 104 | <code>    paths.push(path);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 105 | <code>    if (path === &quot;/api/snapshot&quot;) return response(404, { detail: &quot;Not Found&quot; });</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 106 | <code>    return response(200, path === &quot;/api/books&quot; ? [{ book_id: 1 }] : data(path));</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 107 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 108 | <code>  assert.equal(await p.library.loadData(() =&gt; {}), true);</code> | Local state, DOM reference বা callback/result assign করে। |
| 109 | <code>  assert.equal(p.library.state.books[0].book_id, 1);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 110 | <code>  assert.equal(await p.library.loadData(() =&gt; {}), true);</code> | Local state, DOM reference বা callback/result assign করে। |
| 111 | <code>  assert.equal(paths.filter((path) =&gt; path === &quot;/api/snapshot&quot;).length, 1);</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 112 | <code>  for (const name of [&quot;books&quot;, &quot;students&quot;, &quot;issues&quot;, &quot;fines&quot;, &quot;meta&quot;]) {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 113 | <code>    assert.equal(paths.filter((path) =&gt; path === `/api/${name}`).length, 2);</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 114 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 115 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 116 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 117 | <code>test(&quot;snapshot database errors stay offline without falling back&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 118 | <code>  const paths = [];</code> | Local state, DOM reference বা callback/result assign করে। |
| 119 | <code>  const p = app(async (path) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 120 | <code>    paths.push(path);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 121 | <code>    return path === &quot;/api/auth/session&quot;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 122 | <code>      ? response(200, data(path))</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 123 | <code>      : response(503, { detail: &quot;Unavailable&quot; });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 124 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 125 | <code>  assert.equal(await p.library.loadData(() =&gt; {}), false);</code> | Local state, DOM reference বা callback/result assign করে। |
| 126 | <code>  assert.equal(paths.includes(&quot;/api/books&quot;), false);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 127 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 128 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 129 | <code>test(&quot;mutation failures are not automatically replayed&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 130 | <code>  let writes = 0;</code> | Local state, DOM reference বা callback/result assign করে। |
| 131 | <code>  const p = app(async (path) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 132 | <code>    if (path === &quot;/api/auth/session&quot;) return response(200, data(path));</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 133 | <code>    writes++;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 134 | <code>    return response(503, { detail: &quot;Database unavailable&quot; });</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 135 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 136 | <code>  await assert.rejects(p.library.api(&quot;/issues&quot;, { method: &quot;POST&quot; }), /Database unavailable/);</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 137 | <code>  assert.equal(writes, 1);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 138 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 139 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 140 | <code>test(&quot;monitor restores live data after outage&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 141 | <code>  let offline = true;</code> | Local state, DOM reference বা callback/result assign করে। |
| 142 | <code>  const p = app(async (path) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 143 | <code>    path !== &quot;/api/auth/session&quot; &amp;&amp; offline</code> | Local state, DOM reference বা callback/result assign করে। |
| 144 | <code>      ? response(503, { detail: &quot;Unavailable&quot; })</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 145 | <code>      : response(200, data(path)),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 146 | <code>  );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 147 | <code>  assert.equal(await p.library.loadData(() =&gt; {}), false);</code> | Local state, DOM reference বা callback/result assign করে। |
| 148 | <code>  offline = false;</code> | Local state, DOM reference বা callback/result assign করে। |
| 149 | <code>  await p.timers[0]();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 150 | <code>  assert.equal(p.library.state.online, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 151 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 152 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 153 | <code>test(&quot;live notifications refresh from the shared snapshot after 30 seconds&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 154 | <code>  let now = 0;</code> | Local state, DOM reference বা callback/result assign করে। |
| 155 | <code>  class Clock extends Date {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 156 | <code>    static now() {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 157 | <code>      return now;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 158 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 159 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 160 | <code>  let reads = 0;</code> | Local state, DOM reference বা callback/result assign করে। |
| 161 | <code>  const updates = [];</code> | Local state, DOM reference বা callback/result assign করে। |
| 162 | <code>  const sessions = [];</code> | Local state, DOM reference বা callback/result assign করে। |
| 163 | <code>  const p = app(</code> | Local state, DOM reference বা callback/result assign করে। |
| 164 | <code>    async (path) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 165 | <code>      if (path === &quot;/api/snapshot&quot;) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 166 | <code>        reads++;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 167 | <code>        return response(200, { ...data(path), reservations: [{ reservation_id: reads }] });</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 168 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 169 | <code>      return response(200, data(path));</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 170 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 171 | <code>    {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 172 | <code>      Date: Clock,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 173 | <code>      notifications: {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 174 | <code>        create: () =&gt; ({</code> | Local state, DOM reference বা callback/result assign করে। |
| 175 | <code>          setSession: (session) =&gt; sessions.push(session),</code> | Local state, DOM reference বা callback/result assign করে। |
| 176 | <code>          update: (snapshot, online) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 177 | <code>            updates.push({ reservation: snapshot.reservations[0].reservation_id, online }),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 178 | <code>        }),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 179 | <code>      },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 180 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 181 | <code>  );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 182 | <code>  await p.library.loadData(() =&gt; {});</code> | Local state, DOM reference বা callback/result assign করে। |
| 183 | <code>  now = 31000;</code> | Local state, DOM reference বা callback/result assign করে। |
| 184 | <code>  await p.timers[0]();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 185 | <code>  assert.equal(reads, 2);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 186 | <code>  assert.equal(sessions[0].user_type, &quot;ADMIN&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 187 | <code>  assert.deepEqual(updates, [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 188 | <code>    { reservation: 1, online: true },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 189 | <code>    { reservation: 2, online: true },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 190 | <code>  ]);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 191 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 192 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 193 | <code>test(&quot;notification freshness becomes offline without clearing the last snapshot&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 194 | <code>  let offline = false;</code> | Local state, DOM reference বা callback/result assign করে। |
| 195 | <code>  const updates = [];</code> | Local state, DOM reference বা callback/result assign করে। |
| 196 | <code>  const p = app(</code> | Local state, DOM reference বা callback/result assign করে। |
| 197 | <code>    async (path) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 198 | <code>      if (offline &amp;&amp; path !== &quot;/api/auth/session&quot;) return response(503, { detail: &quot;Unavailable&quot; });</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 199 | <code>      return response(200, { ...data(path), reservations: [{ reservation_id: 8 }] });</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 200 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 201 | <code>    {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 202 | <code>      notifications: {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 203 | <code>        create: () =&gt; ({</code> | Local state, DOM reference বা callback/result assign করে। |
| 204 | <code>          setSession() {},</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 205 | <code>          update: (snapshot, online) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 206 | <code>            updates.push({ reservation: snapshot.reservations[0].reservation_id, online }),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 207 | <code>        }),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 208 | <code>      },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 209 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 210 | <code>  );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 211 | <code>  await p.library.loadData(() =&gt; {});</code> | Local state, DOM reference বা callback/result assign করে। |
| 212 | <code>  offline = true;</code> | Local state, DOM reference বা callback/result assign করে। |
| 213 | <code>  await p.timers[0]();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 214 | <code>  assert.deepEqual(updates.at(-1), { reservation: 8, online: false });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 215 | <code>  assert.equal(p.library.state.reservations[0].reservation_id, 8);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 216 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
