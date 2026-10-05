# tests/login.test.cjs

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/login.test.cjs)। Snapshot 2026-10-04; 116 lines; SHA-256 `3a4758bf0861320f1408d41c850247764e74beb5ec861fc983a7b604a8c4b606`।

## Function / object / element inventory

### `page(fetch)` — L7

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

## সম্পূর্ণ original source

```javascript
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const { test } = require("node:test");
const source = fs.readFileSync("frontend/login.js", "utf8");

function page(fetch) {
  const element = (extra = {}) => ({
    textContent: "",
    disabled: false,
    attributes: {},
    setAttribute(key, value) {
      this.attributes[key] = value;
    },
    ...extra,
  });
  const form = element({
    values: { username: " admin ", password: "test1234" },
    elements: { username: { focus() {} } },
  });
  const nodes = {
    "#loginForm": form,
    "#password": element({ type: "password" }),
    "#togglePassword": element(),
    "#loginButton": element(),
    "#loginError": element(),
  };
  const redirects = [];
  const context = {
    document: { querySelector: (selector) => nodes[selector] },
    window: { location: { replace: (path) => redirects.push(path) } },
    FormData: class {
      constructor(form) {
        return Object.entries(form.values);
      }
    },
    URLSearchParams,
    AbortController,
    setTimeout,
    clearTimeout,
    TypeError,
    fetch,
  };
  vm.runInNewContext(source, context);
  return { nodes, redirects, submit: () => form.onsubmit({ preventDefault() {} }) };
}

test("password visibility updates accessible toggle state", () => {
  const { nodes } = page(() => {});
  nodes["#togglePassword"].onclick();
  assert.equal(nodes["#password"].type, "text");
  assert.equal(nodes["#togglePassword"].attributes["aria-pressed"], "true");
  nodes["#togglePassword"].onclick();
  assert.equal(nodes["#password"].type, "password");
});

test("successful login trims username and redirects", async () => {
  const p = page(async (_, options) => {
    assert.equal(options.body.get("username"), "admin");
    return { ok: true, json: async () => ({ username: "admin", user_type: "ADMIN" }) };
  });
  await p.submit();
  assert.deepEqual(p.redirects, ["/"]);
});

test("malformed successful response cannot redirect", async () => {
  const p = page(async () => ({
    ok: true,
    json: async () => {
      throw new Error("Invalid JSON");
    },
  }));
  await p.submit();
  assert.equal(p.redirects.length, 0);
  assert.match(p.nodes["#loginError"].textContent, /unexpected response/);
  assert.equal(p.nodes["#loginButton"].disabled, false);
});

test("student login opens the personal dashboard", async () => {
  const p = page(async () => ({
    ok: true,
    json: async () => ({ username: "studentqa", user_type: "STUDENT" }),
  }));
  await p.submit();
  assert.deepEqual(p.redirects, ["/student"]);
});

test("wrong password and network errors show useful messages", async () => {
  const p = page(async () => ({
    ok: false,
    json: async () => ({ detail: "Incorrect username or password" }),
  }));
  await p.submit();
  assert.equal(p.nodes["#loginError"].textContent, "Incorrect username or password");
  const offline = page(async () => {
    throw new TypeError("Failed to fetch");
  });
  await offline.submit();
  assert.match(offline.nodes["#loginError"].textContent, /Cannot reach the server/);
});

test("repeated submission sends only one pending request", async () => {
  let resolve,
    calls = 0;
  const p = page(() => {
    calls++;
    return new Promise((done) => {
      resolve = done;
    });
  });
  const pending = p.submit();
  await p.submit();
  assert.equal(calls, 1);
  resolve({ ok: true, json: async () => ({ username: "admin", user_type: "ADMIN" }) });
  await pending;
});
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>const assert = require(&quot;node:assert/strict&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 2 | <code>const fs = require(&quot;node:fs&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 3 | <code>const vm = require(&quot;node:vm&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 4 | <code>const { test } = require(&quot;node:test&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 5 | <code>const source = fs.readFileSync(&quot;frontend/login.js&quot;, &quot;utf8&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 6 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 7 | <code>function page(fetch) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 8 | <code>  const element = (extra = {}) =&gt; ({</code> | Local state, DOM reference বা callback/result assign করে। |
| 9 | <code>    textContent: &quot;&quot;,</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 10 | <code>    disabled: false,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 11 | <code>    attributes: {},</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 12 | <code>    setAttribute(key, value) {</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 13 | <code>      this.attributes[key] = value;</code> | Local state, DOM reference বা callback/result assign করে। |
| 14 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 15 | <code>    ...extra,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 16 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 17 | <code>  const form = element({</code> | Local state, DOM reference বা callback/result assign করে। |
| 18 | <code>    values: { username: &quot; admin &quot;, password: &quot;test1234&quot; },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 19 | <code>    elements: { username: { focus() {} } },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 20 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 21 | <code>  const nodes = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 22 | <code>    &quot;#loginForm&quot;: form,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 23 | <code>    &quot;#password&quot;: element({ type: &quot;password&quot; }),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 24 | <code>    &quot;#togglePassword&quot;: element(),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 25 | <code>    &quot;#loginButton&quot;: element(),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 26 | <code>    &quot;#loginError&quot;: element(),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 27 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 28 | <code>  const redirects = [];</code> | Local state, DOM reference বা callback/result assign করে। |
| 29 | <code>  const context = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 30 | <code>    document: { querySelector: (selector) =&gt; nodes[selector] },</code> | Local state, DOM reference বা callback/result assign করে। |
| 31 | <code>    window: { location: { replace: (path) =&gt; redirects.push(path) } },</code> | Local state, DOM reference বা callback/result assign করে। |
| 32 | <code>    FormData: class {</code> | Form fields বা filters URL-encoded request body/query parameters-এ রূপান্তর করে। |
| 33 | <code>      constructor(form) {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 34 | <code>        return Object.entries(form.values);</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 35 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 36 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 37 | <code>    URLSearchParams,</code> | Form fields বা filters URL-encoded request body/query parameters-এ রূপান্তর করে। |
| 38 | <code>    AbortController,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 39 | <code>    setTimeout,</code> | Timeout/reconnection/search debounce timer শুরু বা বন্ধ করে। |
| 40 | <code>    clearTimeout,</code> | Timeout/reconnection/search debounce timer শুরু বা বন্ধ করে। |
| 41 | <code>    TypeError,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 42 | <code>    fetch,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 43 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 44 | <code>  vm.runInNewContext(source, context);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 45 | <code>  return { nodes, redirects, submit: () =&gt; form.onsubmit({ preventDefault() {} }) };</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 46 | <code>}</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 47 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 48 | <code>test(&quot;password visibility updates accessible toggle state&quot;, () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 49 | <code>  const { nodes } = page(() =&gt; {});</code> | Local state, DOM reference বা callback/result assign করে। |
| 50 | <code>  nodes[&quot;#togglePassword&quot;].onclick();</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 51 | <code>  assert.equal(nodes[&quot;#password&quot;].type, &quot;text&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 52 | <code>  assert.equal(nodes[&quot;#togglePassword&quot;].attributes[&quot;aria-pressed&quot;], &quot;true&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 53 | <code>  nodes[&quot;#togglePassword&quot;].onclick();</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 54 | <code>  assert.equal(nodes[&quot;#password&quot;].type, &quot;password&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 55 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 56 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 57 | <code>test(&quot;successful login trims username and redirects&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 58 | <code>  const p = page(async (_, options) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 59 | <code>    assert.equal(options.body.get(&quot;username&quot;), &quot;admin&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 60 | <code>    return { ok: true, json: async () =&gt; ({ username: &quot;admin&quot;, user_type: &quot;ADMIN&quot; }) };</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 61 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 62 | <code>  await p.submit();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 63 | <code>  assert.deepEqual(p.redirects, [&quot;/&quot;]);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 64 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 65 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 66 | <code>test(&quot;malformed successful response cannot redirect&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 67 | <code>  const p = page(async () =&gt; ({</code> | Local state, DOM reference বা callback/result assign করে। |
| 68 | <code>    ok: true,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 69 | <code>    json: async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 70 | <code>      throw new Error(&quot;Invalid JSON&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 71 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 72 | <code>  }));</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 73 | <code>  await p.submit();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 74 | <code>  assert.equal(p.redirects.length, 0);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 75 | <code>  assert.match(p.nodes[&quot;#loginError&quot;].textContent, /unexpected response/);</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 76 | <code>  assert.equal(p.nodes[&quot;#loginButton&quot;].disabled, false);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 77 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 78 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 79 | <code>test(&quot;student login opens the personal dashboard&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 80 | <code>  const p = page(async () =&gt; ({</code> | Local state, DOM reference বা callback/result assign করে। |
| 81 | <code>    ok: true,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 82 | <code>    json: async () =&gt; ({ username: &quot;studentqa&quot;, user_type: &quot;STUDENT&quot; }),</code> | Local state, DOM reference বা callback/result assign করে। |
| 83 | <code>  }));</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 84 | <code>  await p.submit();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 85 | <code>  assert.deepEqual(p.redirects, [&quot;/student&quot;]);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 86 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 87 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 88 | <code>test(&quot;wrong password and network errors show useful messages&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 89 | <code>  const p = page(async () =&gt; ({</code> | Local state, DOM reference বা callback/result assign করে। |
| 90 | <code>    ok: false,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 91 | <code>    json: async () =&gt; ({ detail: &quot;Incorrect username or password&quot; }),</code> | Local state, DOM reference বা callback/result assign করে। |
| 92 | <code>  }));</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 93 | <code>  await p.submit();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 94 | <code>  assert.equal(p.nodes[&quot;#loginError&quot;].textContent, &quot;Incorrect username or password&quot;);</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 95 | <code>  const offline = page(async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 96 | <code>    throw new TypeError(&quot;Failed to fetch&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 97 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 98 | <code>  await offline.submit();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 99 | <code>  assert.match(offline.nodes[&quot;#loginError&quot;].textContent, /Cannot reach the server/);</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 100 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 101 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 102 | <code>test(&quot;repeated submission sends only one pending request&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 103 | <code>  let resolve,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 104 | <code>    calls = 0;</code> | Local state, DOM reference বা callback/result assign করে। |
| 105 | <code>  const p = page(() =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 106 | <code>    calls++;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 107 | <code>    return new Promise((done) =&gt; {</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 108 | <code>      resolve = done;</code> | Local state, DOM reference বা callback/result assign করে। |
| 109 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 110 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 111 | <code>  const pending = p.submit();</code> | Local state, DOM reference বা callback/result assign করে। |
| 112 | <code>  await p.submit();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 113 | <code>  assert.equal(calls, 1);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 114 | <code>  resolve({ ok: true, json: async () =&gt; ({ username: &quot;admin&quot;, user_type: &quot;ADMIN&quot; }) });</code> | Local state, DOM reference বা callback/result assign করে। |
| 115 | <code>  await pending;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 116 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
