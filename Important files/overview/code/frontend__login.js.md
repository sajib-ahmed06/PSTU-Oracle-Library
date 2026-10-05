# frontend/login.js

Password show/hide, single pending login request, username trim, timeout, response validation এবং successful redirect পরিচালনা করে।

Source: [মূল file](../../frontend/login.js)। Snapshot 2026-10-04; 81 lines; SHA-256 `4640f41b3c23a5e2a128924151624f56492c8d603f7f5da12563a878171e740c`।

## Function / object / element inventory

Login controller named functions-এর বদলে onclick/onsubmit callbacks ব্যবহার করে। submitting guard, AbortController, JSON/role response check, error message ও finally cleanup প্রতিটি branch নিচে আছে।

## সম্পূর্ণ original source

```javascript
(() => {
  const form = document.querySelector("#loginForm");
  const password = document.querySelector("#password");
  const togglePassword = document.querySelector("#togglePassword");
  const loginButton = document.querySelector("#loginButton");
  const loginError = document.querySelector("#loginError");
  let submitting = false;
  const query = new URLSearchParams(window.location.search || "");
  const activatedMember = query.get("memberId");
  if (activatedMember && /^PSTU-[0-9]{1,20}$/i.test(activatedMember)) {
    form.elements.username.value = activatedMember;
    if (query.get("activated") === "1") {
      loginError.textContent = "Account activated. Sign in with your Member ID and password";
      password.focus?.();
    }
    if (query.get("recovered") === "1") {
      loginError.textContent = "Password changed. Sign in with your Member ID and new password";
      password.focus?.();
    }
  }

  togglePassword.onclick = () => {
    const showing = password.type === "text";
    password.type = showing ? "password" : "text";
    togglePassword.textContent = showing ? "Show" : "Hide";
    togglePassword.setAttribute("aria-label", showing ? "Show password" : "Hide password");
    togglePassword.setAttribute("aria-pressed", String(!showing));
  };

  form.onsubmit = async (event) => {
    event.preventDefault();
    if (submitting) return;
    const body = new URLSearchParams(new FormData(form));
    body.set("username", String(body.get("username") || "").trim());
    if (!body.get("username")) {
      loginError.textContent = "Enter your Member ID or staff username";
      form.elements.username.focus();
      return;
    }
    submitting = true;
    loginError.textContent = "";
    loginButton.disabled = true;
    loginButton.textContent = "Signing in...";
    form.setAttribute("aria-busy", "true");
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 30000);

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        signal: controller.signal,
        body,
      });
      let data;
      try {
        data = await response.json();
      } catch (error) {
        if (controller.signal.aborted) throw error;
        throw new Error("The server returned an unexpected response. Please try again");
      }
      if (!response.ok)
        throw new Error(typeof data?.detail === "string" ? data.detail : "Sign in failed");
      if (!data?.username || !["ADMIN", "LIBRARIAN", "STUDENT"].includes(data.user_type)) {
        throw new Error("The server returned an unexpected response. Please try again");
      }
      window.location.replace(data.user_type === "STUDENT" ? "/student" : "/");
    } catch (error) {
      loginError.textContent = controller.signal.aborted
        ? "Sign in timed out. Please try again"
        : error instanceof TypeError
          ? "Cannot reach the server. Check your connection and try again"
          : error.message;
    } finally {
      clearTimeout(timer);
      submitting = false;
      loginButton.disabled = false;
      loginButton.textContent = "Sign in";
      form.setAttribute("aria-busy", "false");
    }
  };
})();
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>(() =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 2 | <code>  const form = document.querySelector(&quot;#loginForm&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 3 | <code>  const password = document.querySelector(&quot;#password&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 4 | <code>  const togglePassword = document.querySelector(&quot;#togglePassword&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 5 | <code>  const loginButton = document.querySelector(&quot;#loginButton&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 6 | <code>  const loginError = document.querySelector(&quot;#loginError&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 7 | <code>  let submitting = false;</code> | Local state, DOM reference বা callback/result assign করে। |
| 8 | <code>  const query = new URLSearchParams(window.location.search &#124;&#124; &quot;&quot;);</code> | Form fields বা filters URL-encoded request body/query parameters-এ রূপান্তর করে। |
| 9 | <code>  const activatedMember = query.get(&quot;memberId&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 10 | <code>  if (activatedMember &amp;&amp; /^PSTU-[0-9]{1,20}$/i.test(activatedMember)) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 11 | <code>    form.elements.username.value = activatedMember;</code> | Local state, DOM reference বা callback/result assign করে। |
| 12 | <code>    if (query.get(&quot;activated&quot;) === &quot;1&quot;) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 13 | <code>      loginError.textContent = &quot;Account activated. Sign in with your Member ID and password&quot;;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 14 | <code>      password.focus?.();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 15 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 16 | <code>    if (query.get(&quot;recovered&quot;) === &quot;1&quot;) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 17 | <code>      loginError.textContent = &quot;Password changed. Sign in with your Member ID and new password&quot;;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 18 | <code>      password.focus?.();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 19 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 20 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 21 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 22 | <code>  togglePassword.onclick = () =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 23 | <code>    const showing = password.type === &quot;text&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 24 | <code>    password.type = showing ? &quot;password&quot; : &quot;text&quot;;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 25 | <code>    togglePassword.textContent = showing ? &quot;Show&quot; : &quot;Hide&quot;;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 26 | <code>    togglePassword.setAttribute(&quot;aria-label&quot;, showing ? &quot;Show password&quot; : &quot;Hide password&quot;);</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 27 | <code>    togglePassword.setAttribute(&quot;aria-pressed&quot;, String(!showing));</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 28 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 29 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 30 | <code>  form.onsubmit = async (event) =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 31 | <code>    event.preventDefault();</code> | Default form navigation বন্ধ করে controlled API submission চালাতে দেয়। |
| 32 | <code>    if (submitting) return;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 33 | <code>    const body = new URLSearchParams(new FormData(form));</code> | Form fields বা filters URL-encoded request body/query parameters-এ রূপান্তর করে। |
| 34 | <code>    body.set(&quot;username&quot;, String(body.get(&quot;username&quot;) &#124;&#124; &quot;&quot;).trim());</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 35 | <code>    if (!body.get(&quot;username&quot;)) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 36 | <code>      loginError.textContent = &quot;Enter your Member ID or staff username&quot;;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 37 | <code>      form.elements.username.focus();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 38 | <code>      return;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 39 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 40 | <code>    submitting = true;</code> | Local state, DOM reference বা callback/result assign করে। |
| 41 | <code>    loginError.textContent = &quot;&quot;;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 42 | <code>    loginButton.disabled = true;</code> | Local state, DOM reference বা callback/result assign করে। |
| 43 | <code>    loginButton.textContent = &quot;Signing in...&quot;;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 44 | <code>    form.setAttribute(&quot;aria-busy&quot;, &quot;true&quot;);</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 45 | <code>    const controller = new AbortController();</code> | Local state, DOM reference বা callback/result assign করে। |
| 46 | <code>    const timer = setTimeout(() =&gt; controller.abort(), 30000);</code> | Timeout/reconnection/search debounce timer শুরু বা বন্ধ করে। |
| 47 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 48 | <code>    try {</code> | Async failure handling ও UI cleanup/restore block। |
| 49 | <code>      const response = await fetch(&quot;/api/auth/login&quot;, {</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 50 | <code>        method: &quot;POST&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 51 | <code>        signal: controller.signal,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 52 | <code>        body,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 53 | <code>      });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 54 | <code>      let data;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 55 | <code>      try {</code> | Async failure handling ও UI cleanup/restore block। |
| 56 | <code>        data = await response.json();</code> | Local state, DOM reference বা callback/result assign করে। |
| 57 | <code>      } catch (error) {</code> | Async failure handling ও UI cleanup/restore block। |
| 58 | <code>        if (controller.signal.aborted) throw error;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 59 | <code>        throw new Error(&quot;The server returned an unexpected response. Please try again&quot;);</code> | Async failure handling ও UI cleanup/restore block। |
| 60 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 61 | <code>      if (!response.ok)</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 62 | <code>        throw new Error(typeof data?.detail === &quot;string&quot; ? data.detail : &quot;Sign in failed&quot;);</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 63 | <code>      if (!data?.username &#124;&#124; ![&quot;ADMIN&quot;, &quot;LIBRARIAN&quot;, &quot;STUDENT&quot;].includes(data.user_type)) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 64 | <code>        throw new Error(&quot;The server returned an unexpected response. Please try again&quot;);</code> | Async failure handling ও UI cleanup/restore block। |
| 65 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 66 | <code>      window.location.replace(data.user_type === &quot;STUDENT&quot; ? &quot;/student&quot; : &quot;/&quot;);</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 67 | <code>    } catch (error) {</code> | Async failure handling ও UI cleanup/restore block। |
| 68 | <code>      loginError.textContent = controller.signal.aborted</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 69 | <code>        ? &quot;Sign in timed out. Please try again&quot;</code> | Async failure handling ও UI cleanup/restore block। |
| 70 | <code>        : error instanceof TypeError</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 71 | <code>          ? &quot;Cannot reach the server. Check your connection and try again&quot;</code> | Async failure handling ও UI cleanup/restore block। |
| 72 | <code>          : error.message;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 73 | <code>    } finally {</code> | Async failure handling ও UI cleanup/restore block। |
| 74 | <code>      clearTimeout(timer);</code> | Timeout/reconnection/search debounce timer শুরু বা বন্ধ করে। |
| 75 | <code>      submitting = false;</code> | Local state, DOM reference বা callback/result assign করে। |
| 76 | <code>      loginButton.disabled = false;</code> | Local state, DOM reference বা callback/result assign করে। |
| 77 | <code>      loginButton.textContent = &quot;Sign in&quot;;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 78 | <code>      form.setAttribute(&quot;aria-busy&quot;, &quot;false&quot;);</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 79 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 80 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 81 | <code>})();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
