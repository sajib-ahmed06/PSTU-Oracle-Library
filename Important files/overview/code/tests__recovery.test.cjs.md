# tests/recovery.test.cjs

Regression/behavior test file; test functions-এর নাম, assertions ও fixtures নিচের পূর্ণ source ও inventory-তে দেওয়া আছে।

Source: [মূল file](../../tests/recovery.test.cjs)। Snapshot 2026-10-04; 95 lines; SHA-256 `5dc59aafe4a95536f8cea6b9cb3ba718b14a7c6af4e3d975a2abac84a5d9e517`।

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
    rollNo: "007",
    registrationNo: "REG-007",
    email: "member@example.com",
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
    "#recoveryForm": form,
    "#recoveryButton": { disabled: false },
    "#recoveryMessage": { textContent: "" },
  };
  const redirects = [];
  vm.runInNewContext(fs.readFileSync("frontend/forgot-password.js", "utf8"), {
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

test("recovery sends member and phone and returns to login with Member ID", async () => {
  const p = page(async (path, options) => {
    assert.equal(path, "/api/auth/reset-password");
    assert.equal(options.body.get("memberId"), "PSTU-0007");
    assert.equal(options.body.get("phone"), "01700000007");
    assert.equal(options.body.get("rollNo"), "007");
    assert.equal(options.body.get("registrationNo"), "REG-007");
    assert.equal(options.body.get("email"), "member@example.com");
    return {
      ok: true,
      json: async () => ({ member_id: "PSTU-0007", message: "Password changed" }),
    };
  });
  await p.submit();
  assert.deepEqual(p.redirects, ["/login?memberId=PSTU-0007&recovered=1"]);
  assert.equal(p.nodes["#recoveryForm"].resetCalled, true);
});

test("password mismatch never sends an recovery request", async () => {
  let calls = 0;
  const p = page(async () => {
    calls++;
  });
  p.nodes["#recoveryForm"].elements.confirmPassword.value = "different";
  await p.submit();
  assert.equal(calls, 0);
  assert.match(p.nodes["#recoveryMessage"].textContent, /Passwords do not match/);
});

test("repeated clicks submit once and recovery errors keep the form available", async () => {
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
  finish({ ok: false, json: async () => ({ detail: "Member details do not match" }) });
  await first;
  assert.equal(p.nodes["#recoveryButton"].disabled, false);
  assert.match(p.nodes["#recoveryMessage"].textContent, /do not match/);
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
| 12 | <code>    rollNo: &quot;007&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 13 | <code>    registrationNo: &quot;REG-007&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 14 | <code>    email: &quot;member@example.com&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 15 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 16 | <code>  const form = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 17 | <code>    elements: {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 18 | <code>      password: { value: fields.password },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 19 | <code>      confirmPassword: { value: fields.confirmPassword },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 20 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 21 | <code>    setAttribute() {},</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 22 | <code>    reset() {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 23 | <code>      this.resetCalled = true;</code> | Local state, DOM reference বা callback/result assign করে। |
| 24 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 25 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 26 | <code>  const nodes = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 27 | <code>    &quot;#recoveryForm&quot;: form,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 28 | <code>    &quot;#recoveryButton&quot;: { disabled: false },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 29 | <code>    &quot;#recoveryMessage&quot;: { textContent: &quot;&quot; },</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 30 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 31 | <code>  const redirects = [];</code> | Local state, DOM reference বা callback/result assign করে। |
| 32 | <code>  vm.runInNewContext(fs.readFileSync(&quot;frontend/forgot-password.js&quot;, &quot;utf8&quot;), {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 33 | <code>    document: { querySelector: (s) =&gt; nodes[s] },</code> | Local state, DOM reference বা callback/result assign করে। |
| 34 | <code>    fetch,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 35 | <code>    FormData: class {</code> | Form fields বা filters URL-encoded request body/query parameters-এ রূপান্তর করে। |
| 36 | <code>      constructor() {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 37 | <code>        return Object.entries(fields);</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 38 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 39 | <code>    },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 40 | <code>    URLSearchParams,</code> | Form fields বা filters URL-encoded request body/query parameters-এ রূপান্তর করে। |
| 41 | <code>    AbortSignal,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 42 | <code>    TypeError,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 43 | <code>    encodeURIComponent,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 44 | <code>    window: { location: { replace: (path) =&gt; redirects.push(path) } },</code> | Local state, DOM reference বা callback/result assign করে। |
| 45 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 46 | <code>  return { nodes, redirects, submit: () =&gt; form.onsubmit({ preventDefault() {} }) };</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 47 | <code>}</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 48 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 49 | <code>test(&quot;recovery sends member and phone and returns to login with Member ID&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 50 | <code>  const p = page(async (path, options) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 51 | <code>    assert.equal(path, &quot;/api/auth/reset-password&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 52 | <code>    assert.equal(options.body.get(&quot;memberId&quot;), &quot;PSTU-0007&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 53 | <code>    assert.equal(options.body.get(&quot;phone&quot;), &quot;01700000007&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 54 | <code>    assert.equal(options.body.get(&quot;rollNo&quot;), &quot;007&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 55 | <code>    assert.equal(options.body.get(&quot;registrationNo&quot;), &quot;REG-007&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 56 | <code>    assert.equal(options.body.get(&quot;email&quot;), &quot;member@example.com&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 57 | <code>    return {</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 58 | <code>      ok: true,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 59 | <code>      json: async () =&gt; ({ member_id: &quot;PSTU-0007&quot;, message: &quot;Password changed&quot; }),</code> | Local state, DOM reference বা callback/result assign করে। |
| 60 | <code>    };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 61 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 62 | <code>  await p.submit();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 63 | <code>  assert.deepEqual(p.redirects, [&quot;/login?memberId=PSTU-0007&amp;recovered=1&quot;]);</code> | Local state, DOM reference বা callback/result assign করে। |
| 64 | <code>  assert.equal(p.nodes[&quot;#recoveryForm&quot;].resetCalled, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 65 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 66 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 67 | <code>test(&quot;password mismatch never sends an recovery request&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 68 | <code>  let calls = 0;</code> | Local state, DOM reference বা callback/result assign করে। |
| 69 | <code>  const p = page(async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 70 | <code>    calls++;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 71 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 72 | <code>  p.nodes[&quot;#recoveryForm&quot;].elements.confirmPassword.value = &quot;different&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 73 | <code>  await p.submit();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 74 | <code>  assert.equal(calls, 0);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 75 | <code>  assert.match(p.nodes[&quot;#recoveryMessage&quot;].textContent, /Passwords do not match/);</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 76 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 77 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 78 | <code>test(&quot;repeated clicks submit once and recovery errors keep the form available&quot;, async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 79 | <code>  let finish,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 80 | <code>    calls = 0;</code> | Local state, DOM reference বা callback/result assign করে। |
| 81 | <code>  const p = page(() =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 82 | <code>    calls++;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 83 | <code>    return new Promise((resolve) =&gt; {</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 84 | <code>      finish = resolve;</code> | Local state, DOM reference বা callback/result assign করে। |
| 85 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 86 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 87 | <code>  const first = p.submit();</code> | Local state, DOM reference বা callback/result assign করে। |
| 88 | <code>  await p.submit();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 89 | <code>  assert.equal(calls, 1);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 90 | <code>  finish({ ok: false, json: async () =&gt; ({ detail: &quot;Member details do not match&quot; }) });</code> | Local state, DOM reference বা callback/result assign করে। |
| 91 | <code>  await first;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 92 | <code>  assert.equal(p.nodes[&quot;#recoveryButton&quot;].disabled, false);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 93 | <code>  assert.match(p.nodes[&quot;#recoveryMessage&quot;].textContent, /do not match/);</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 94 | <code>  assert.equal(p.redirects.length, 0);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 95 | <code>});</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
