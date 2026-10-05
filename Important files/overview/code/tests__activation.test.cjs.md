# tests/activation.test.cjs

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/activation.test.cjs)। Snapshot 2026-10-04; 89 lines; SHA-256 `76db5e8c381baee9b75e0a6bad6e6e0766f279efb19151434f520d63bed1d2b3`।

## Function / object / element inventory

### `page(fetch)` — L6

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

## সম্পূর্ণ original source

```javascript
const assert = require("node:assert/strict");
const { test } = require("node:test");
const fs = require("node:fs");
const vm = require("node:vm");

function page(fetch) {
  const fields = {
    memberId: "PSTU-0007",
    phone: "01700000007",
    password: "Secret1234",
    confirmPassword: "Secret1234",
  };
  const form = {
    elements: {
      password: { value: fields.password },
      confirmPassword: { value: fields.confirmPassword },
    },
    setAttribute() {},
    reset() {
      this.resetCalled = true;
    },
  };
  const nodes = {
    "#activationForm": form,
    "#activationButton": { disabled: false },
    "#activationMessage": { textContent: "" },
  };
  const redirects = [];
  vm.runInNewContext(fs.readFileSync("frontend/activate-account.js", "utf8"), {
    document: { querySelector: (s) => nodes[s] },
    fetch,
    FormData: class {
      constructor() {
        return Object.entries(fields);
      }
    },
    URLSearchParams,
    AbortSignal,
    TypeError,
    encodeURIComponent,
    window: { location: { replace: (path) => redirects.push(path) } },
  });
  return { nodes, redirects, submit: () => form.onsubmit({ preventDefault() {} }) };
}

test("activation sends member and phone and returns to login with Member ID", async () => {
  const p = page(async (path, options) => {
    assert.equal(path, "/api/auth/activate");
    assert.equal(options.body.get("memberId"), "PSTU-0007");
    assert.equal(options.body.get("phone"), "01700000007");
    return {
      ok: true,
      json: async () => ({ member_id: "PSTU-0007", message: "Account activated" }),
    };
  });
  await p.submit();
  assert.deepEqual(p.redirects, ["/login?memberId=PSTU-0007&activated=1"]);
  assert.equal(p.nodes["#activationForm"].resetCalled, true);
});

test("password mismatch never sends an activation request", async () => {
  let calls = 0;
  const p = page(async () => {
    calls++;
  });
  p.nodes["#activationForm"].elements.confirmPassword.value = "different";
  await p.submit();
  assert.equal(calls, 0);
  assert.match(p.nodes["#activationMessage"].textContent, /Passwords do not match/);
});

test("repeated clicks submit once and activation errors keep the form available", async () => {
  let finish,
    calls = 0;
  const p = page(() => {
    calls++;
    return new Promise((resolve) => {
      finish = resolve;
    });
  });
  const first = p.submit();
  await p.submit();
  assert.equal(calls, 1);
  finish({ ok: false, json: async () => ({ detail: "Account already activated" }) });
  await first;
  assert.equal(p.nodes["#activationButton"].disabled, false);
  assert.match(p.nodes["#activationMessage"].textContent, /already activated/);
  assert.equal(p.redirects.length, 0);
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
| 6 | <code>function page(fetch) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 7 | <code>  const fields = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 8 | <code>    memberId: &quot;PSTU-0007&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 9 | <code>    phone: &quot;01700000007&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 10 | <code>    password: &quot;Secret1234&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 11 | <code>    confirmPassword: &quot;Secret1234&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 12 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 13 | <code>  const form = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 14 | <code>    elements: {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 15 | <code>      password: { value: fields.password },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 16 | <code>      confirmPassword: { value: fields.confirmPassword },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 17 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 18 | <code>    setAttribute() {},</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 19 | <code>    reset() {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 20 | <code>      this.resetCalled = true;</code> | Local state, DOM reference বা callback/result assign করে। |
| 21 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 22 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 23 | <code>  const nodes = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 24 | <code>    &quot;#activationForm&quot;: form,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 25 | <code>    &quot;#activationButton&quot;: { disabled: false },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 26 | <code>    &quot;#activationMessage&quot;: { textContent: &quot;&quot; },</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 27 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 28 | <code>  const redirects = [];</code> | Local state, DOM reference বা callback/result assign করে। |
| 29 | <code>  vm.runInNewContext(fs.readFileSync(&quot;frontend/activate-account.js&quot;, &quot;utf8&quot;), {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 30 | <code>    document: { querySelector: (s) =&gt; nodes[s] },</code> | Local state, DOM reference বা callback/result assign করে। |
| 31 | <code>    fetch,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 32 | <code>    FormData: class {</code> | Form fields বা filters URL-encoded request body/query parameters-এ রূপান্তর করে। |
| 33 | <code>      constructor() {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 34 | <code>        return Object.entries(fields);</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 35 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 36 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 37 | <code>    URLSearchParams,</code> | Form fields বা filters URL-encoded request body/query parameters-এ রূপান্তর করে। |
| 38 | <code>    AbortSignal,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 39 | <code>    TypeError,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 40 | <code>    encodeURIComponent,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 41 | <code>    window: { location: { replace: (path) =&gt; redirects.push(path) } },</code> | Local state, DOM reference বা callback/result assign করে। |
| 42 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 43 | <code>  return { nodes, redirects, submit: () =&gt; form.onsubmit({ preventDefault() {} }) };</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 44 | <code>}</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 45 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 46 | <code>test(&quot;activation sends member and phone and returns to login with Member ID&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 47 | <code>  const p = page(async (path, options) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 48 | <code>    assert.equal(path, &quot;/api/auth/activate&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 49 | <code>    assert.equal(options.body.get(&quot;memberId&quot;), &quot;PSTU-0007&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 50 | <code>    assert.equal(options.body.get(&quot;phone&quot;), &quot;01700000007&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 51 | <code>    return {</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 52 | <code>      ok: true,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 53 | <code>      json: async () =&gt; ({ member_id: &quot;PSTU-0007&quot;, message: &quot;Account activated&quot; }),</code> | Local state, DOM reference বা callback/result assign করে। |
| 54 | <code>    };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 55 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 56 | <code>  await p.submit();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 57 | <code>  assert.deepEqual(p.redirects, [&quot;/login?memberId=PSTU-0007&amp;activated=1&quot;]);</code> | Local state, DOM reference বা callback/result assign করে। |
| 58 | <code>  assert.equal(p.nodes[&quot;#activationForm&quot;].resetCalled, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 59 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 60 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 61 | <code>test(&quot;password mismatch never sends an activation request&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 62 | <code>  let calls = 0;</code> | Local state, DOM reference বা callback/result assign করে। |
| 63 | <code>  const p = page(async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 64 | <code>    calls++;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 65 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 66 | <code>  p.nodes[&quot;#activationForm&quot;].elements.confirmPassword.value = &quot;different&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 67 | <code>  await p.submit();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 68 | <code>  assert.equal(calls, 0);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 69 | <code>  assert.match(p.nodes[&quot;#activationMessage&quot;].textContent, /Passwords do not match/);</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 70 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 71 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 72 | <code>test(&quot;repeated clicks submit once and activation errors keep the form available&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 73 | <code>  let finish,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 74 | <code>    calls = 0;</code> | Local state, DOM reference বা callback/result assign করে। |
| 75 | <code>  const p = page(() =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 76 | <code>    calls++;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 77 | <code>    return new Promise((resolve) =&gt; {</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 78 | <code>      finish = resolve;</code> | Local state, DOM reference বা callback/result assign করে। |
| 79 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 80 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 81 | <code>  const first = p.submit();</code> | Local state, DOM reference বা callback/result assign করে। |
| 82 | <code>  await p.submit();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 83 | <code>  assert.equal(calls, 1);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 84 | <code>  finish({ ok: false, json: async () =&gt; ({ detail: &quot;Account already activated&quot; }) });</code> | Local state, DOM reference বা callback/result assign করে। |
| 85 | <code>  await first;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 86 | <code>  assert.equal(p.nodes[&quot;#activationButton&quot;].disabled, false);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 87 | <code>  assert.match(p.nodes[&quot;#activationMessage&quot;].textContent, /already activated/);</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 88 | <code>  assert.equal(p.redirects.length, 0);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 89 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
