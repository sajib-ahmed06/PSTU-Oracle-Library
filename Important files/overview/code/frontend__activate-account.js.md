# frontend/activate-account.js

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../frontend/activate-account.js)। Snapshot 2026-10-04; 40 lines; SHA-256 `7242da694ba170797298a28e86bd2ae128d16115a9c72cec2d2c3f0fc2313756`।

## Function / object / element inventory

## সম্পূর্ণ original source

```javascript
(() => {
  const form = document.querySelector("#activationForm");
  const button = document.querySelector("#activationButton");
  const message = document.querySelector("#activationMessage");
  form.onsubmit = async (event) => {
    event.preventDefault();
    if (button.disabled) return;
    if (form.elements.password.value !== form.elements.confirmPassword.value) {
      message.textContent = "Passwords do not match";
      return;
    }
    button.disabled = true;
    form.setAttribute("aria-busy", "true");
    message.textContent = "Activating...";
    try {
      const response = await fetch("/api/auth/activate", {
        method: "POST",
        body: new URLSearchParams(new FormData(form)),
        signal: AbortSignal.timeout(30000),
      });
      const data = await response.json();
      if (!response.ok)
        throw new Error(typeof data.detail === "string" ? data.detail : "Activation failed");
      if (!data.member_id) throw new Error("Unexpected server response. Please try signing in");
      form.reset();
      message.textContent = data.message;
      window.location.replace(`/login?memberId=${encodeURIComponent(data.member_id)}&activated=1`);
    } catch (error) {
      message.textContent =
        error instanceof TypeError
          ? "Cannot reach the server. Please try again"
          : ["TimeoutError", "AbortError"].includes(error.name)
            ? "Activation timed out. Try signing in before activating again"
            : error.message;
    } finally {
      button.disabled = false;
      form.setAttribute("aria-busy", "false");
    }
  };
})();
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>(() =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 2 | <code>  const form = document.querySelector(&quot;#activationForm&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 3 | <code>  const button = document.querySelector(&quot;#activationButton&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 4 | <code>  const message = document.querySelector(&quot;#activationMessage&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 5 | <code>  form.onsubmit = async (event) =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 6 | <code>    event.preventDefault();</code> | Default form navigation বন্ধ করে controlled API submission চালাতে দেয়। |
| 7 | <code>    if (button.disabled) return;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 8 | <code>    if (form.elements.password.value !== form.elements.confirmPassword.value) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 9 | <code>      message.textContent = &quot;Passwords do not match&quot;;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 10 | <code>      return;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 11 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 12 | <code>    button.disabled = true;</code> | Local state, DOM reference বা callback/result assign করে। |
| 13 | <code>    form.setAttribute(&quot;aria-busy&quot;, &quot;true&quot;);</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 14 | <code>    message.textContent = &quot;Activating...&quot;;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 15 | <code>    try {</code> | Async failure handling ও UI cleanup/restore block। |
| 16 | <code>      const response = await fetch(&quot;/api/auth/activate&quot;, {</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 17 | <code>        method: &quot;POST&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 18 | <code>        body: new URLSearchParams(new FormData(form)),</code> | Form fields বা filters URL-encoded request body/query parameters-এ রূপান্তর করে। |
| 19 | <code>        signal: AbortSignal.timeout(30000),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 20 | <code>      });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 21 | <code>      const data = await response.json();</code> | Local state, DOM reference বা callback/result assign করে। |
| 22 | <code>      if (!response.ok)</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 23 | <code>        throw new Error(typeof data.detail === &quot;string&quot; ? data.detail : &quot;Activation failed&quot;);</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 24 | <code>      if (!data.member_id) throw new Error(&quot;Unexpected server response. Please try signing in&quot;);</code> | Async failure handling ও UI cleanup/restore block। |
| 25 | <code>      form.reset();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 26 | <code>      message.textContent = data.message;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 27 | <code>      window.location.replace(`/login?memberId=${encodeURIComponent(data.member_id)}&amp;activated=1`);</code> | Local state, DOM reference বা callback/result assign করে। |
| 28 | <code>    } catch (error) {</code> | Async failure handling ও UI cleanup/restore block। |
| 29 | <code>      message.textContent =</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 30 | <code>        error instanceof TypeError</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 31 | <code>          ? &quot;Cannot reach the server. Please try again&quot;</code> | Async failure handling ও UI cleanup/restore block। |
| 32 | <code>          : [&quot;TimeoutError&quot;, &quot;AbortError&quot;].includes(error.name)</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 33 | <code>            ? &quot;Activation timed out. Try signing in before activating again&quot;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 34 | <code>            : error.message;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 35 | <code>    } finally {</code> | Async failure handling ও UI cleanup/restore block। |
| 36 | <code>      button.disabled = false;</code> | Local state, DOM reference বা callback/result assign করে। |
| 37 | <code>      form.setAttribute(&quot;aria-busy&quot;, &quot;false&quot;);</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 38 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 39 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 40 | <code>})();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
