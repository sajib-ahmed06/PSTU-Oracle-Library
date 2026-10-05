# frontend/accounts.js

Administrator-এর librarian create/toggle/delete এবং নিজের credentials change forms চালায়।

Source: [মূল file](../../frontend/accounts.js)। Snapshot 2026-10-04; 96 lines; SHA-256 `557460c0eef5eab86881debfc3a117794c2f81e4ec72691ef5c72d4aba99ad5b`।

## Function / object / element inventory

### `renderAccounts()` — L4

Admin account list fetch করে role/status/action rows render এবং toggle/delete button handlers বসায়।

### `submitForm(form, path, successMessage)` — L30

Accounts page form-এর submit button disable করে POST, successful form reset ও toast করে; finally button restore।

### `toggleAccount(id, action)` — L49

Confirmation নিয়ে librarian account toggle API call এবং account list refresh করে।

### `deleteAccount(id)` — L60

Permanent delete confirmation নিয়ে librarian deletion API call এবং list refresh করে।

## সম্পূর্ণ original source

```javascript
(() => {
  const { $, state, api, escapeHtml, table, toast, loadData } = LibraryApp;

  async function renderAccounts() {
    try {
      const accounts = await api("/accounts");
      $("#accountCount").textContent = `${accounts.length} accounts`;
      $("#accountTable").innerHTML = table(
        ["Account ID", "Username", "Role", "Status", "Actions"],
        accounts.map((account) => {
          const isAdmin = account.user_type === "ADMIN";
          const toggleLabel = account.account_status === "ACTIVE" ? "Disable" : "Enable";
          const actions = isAdmin
            ? '<span class="complete-text">Current administrator</span>'
            : `<div class="row-actions"><button class="button small ${toggleLabel === "Disable" ? "danger-quiet" : "primary"}" data-account-toggle="${account.user_id}">${toggleLabel}</button><button class="button small danger" data-account-delete="${account.user_id}">Delete</button></div>`;
          return `<tr><td><span class="member-id">ACC-${String(account.user_id).padStart(4, "0")}</span></td><td><b>${escapeHtml(account.username)}</b></td><td><span class="pill ${account.user_type.toLowerCase()}">${account.user_type}</span></td><td><span class="pill ${account.account_status.toLowerCase()}">${account.account_status}</span></td><td>${actions}</td></tr>`;
        }),
      );
      document.querySelectorAll("[data-account-toggle]").forEach((button) => {
        button.onclick = () => toggleAccount(button.dataset.accountToggle, button.textContent);
      });
      document.querySelectorAll("[data-account-delete]").forEach((button) => {
        button.onclick = () => deleteAccount(button.dataset.accountDelete);
      });
    } catch (error) {
      toast(error.message, true);
    }
  }

  async function submitForm(form, path, successMessage) {
    const button = $("button", form);
    button.disabled = true;
    try {
      const response = await api(path, {
        method: "POST",
        body: new URLSearchParams(new FormData(form)),
      });
      toast(successMessage || response.message);
      form.reset();
      return true;
    } catch (error) {
      toast(error.message, true);
      return false;
    } finally {
      button.disabled = false;
    }
  }

  async function toggleAccount(id, action) {
    if (!confirm(`${action} this librarian account?`)) return;
    try {
      const result = await api(`/accounts/${id}/toggle`, { method: "POST" });
      toast(result.message);
      await renderAccounts();
    } catch (error) {
      toast(error.message, true);
    }
  }

  async function deleteAccount(id) {
    if (!confirm("Permanently delete this librarian account?")) return;
    try {
      const result = await api(`/accounts/${id}`, { method: "DELETE" });
      toast(result.message);
      await renderAccounts();
    } catch (error) {
      toast(error.message, true);
    }
  }

  $("#librarianForm").onsubmit = async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    if (form.elements.password.value !== form.elements.confirmPassword.value) {
      toast("Passwords do not match", true);
      return;
    }
    if (await submitForm(form, "/accounts/librarians", "Librarian account created"))
      await renderAccounts();
  };

  $("#credentialsForm").onsubmit = async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    if (form.elements.newPassword.value !== form.elements.confirmPassword.value) {
      toast("New passwords do not match", true);
      return;
    }
    if (await submitForm(form, "/auth/change-credentials", "Administrator credentials updated")) {
      const session = await api("/auth/session");
      $("#sessionUser").textContent = `${session.username} - ${session.user_type}`;
    }
  };

  loadData(renderAccounts);
})();
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>(() =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 2 | <code>  const { $, state, api, escapeHtml, table, toast, loadData } = LibraryApp;</code> | Local state, DOM reference বা callback/result assign করে। |
| 3 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 4 | <code>  async function renderAccounts() {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 5 | <code>    try {</code> | Async failure handling ও UI cleanup/restore block। |
| 6 | <code>      const accounts = await api(&quot;/accounts&quot;);</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 7 | <code>      $(&quot;#accountCount&quot;).textContent = `${accounts.length} accounts`;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 8 | <code>      $(&quot;#accountTable&quot;).innerHTML = table(</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 9 | <code>        [&quot;Account ID&quot;, &quot;Username&quot;, &quot;Role&quot;, &quot;Status&quot;, &quot;Actions&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 10 | <code>        accounts.map((account) =&gt; {</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 11 | <code>          const isAdmin = account.user_type === &quot;ADMIN&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 12 | <code>          const toggleLabel = account.account_status === &quot;ACTIVE&quot; ? &quot;Disable&quot; : &quot;Enable&quot;;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 13 | <code>          const actions = isAdmin</code> | Local state, DOM reference বা callback/result assign করে। |
| 14 | <code>            ? &#x27;&lt;span class=&quot;complete-text&quot;&gt;Current administrator&lt;/span&gt;&#x27;</code> | Local state, DOM reference বা callback/result assign করে। |
| 15 | <code>            : `&lt;div class=&quot;row-actions&quot;&gt;&lt;button class=&quot;button small ${toggleLabel === &quot;Disable&quot; ? &quot;danger-quiet&quot; : &quot;primary&quot;}&quot; data-account-toggle=&quot;${account.user_id}&quot;&gt;${toggleLabel}&lt;/button&gt;&lt;button class=&quot;button small danger&quot; data-account-delete=&quot;${account.user_id}&quot;&gt;Delete&lt;/button&gt;&lt;/div&gt;`;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 16 | <code>          return `&lt;tr&gt;&lt;td&gt;&lt;span class=&quot;member-id&quot;&gt;ACC-${String(account.user_id).padStart(4, &quot;0&quot;)}&lt;/span&gt;&lt;/td&gt;&lt;td&gt;&lt;b&gt;${escapeHtml(account.username)}&lt;/b&gt;&lt;/td&gt;&lt;td&gt;&lt;span class=&quot;pill ${account.user_type.toLowerCase()}&quot;&gt;${account.user_type}&lt;/span&gt;&lt;/td&gt;&lt;td&gt;&lt;span class=&quot;pill ${account.account_status.toLowerCase()}&quot;&gt;${account.account_status}&lt;/span&gt;&lt;/td&gt;&lt;td&gt;${actions}&lt;/td&gt;&lt;/tr&gt;`;</code> | User/database values escaped display markup-এ রূপান্তর করে। |
| 17 | <code>        }),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 18 | <code>      );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 19 | <code>      document.querySelectorAll(&quot;[data-account-toggle]&quot;).forEach((button) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 20 | <code>        button.onclick = () =&gt; toggleAccount(button.dataset.accountToggle, button.textContent);</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 21 | <code>      });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 22 | <code>      document.querySelectorAll(&quot;[data-account-delete]&quot;).forEach((button) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 23 | <code>        button.onclick = () =&gt; deleteAccount(button.dataset.accountDelete);</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 24 | <code>      });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 25 | <code>    } catch (error) {</code> | Async failure handling ও UI cleanup/restore block। |
| 26 | <code>      toast(error.message, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 27 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 28 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 29 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 30 | <code>  async function submitForm(form, path, successMessage) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 31 | <code>    const button = $(&quot;button&quot;, form);</code> | Local state, DOM reference বা callback/result assign করে। |
| 32 | <code>    button.disabled = true;</code> | Local state, DOM reference বা callback/result assign করে। |
| 33 | <code>    try {</code> | Async failure handling ও UI cleanup/restore block। |
| 34 | <code>      const response = await api(path, {</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 35 | <code>        method: &quot;POST&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 36 | <code>        body: new URLSearchParams(new FormData(form)),</code> | Form fields বা filters URL-encoded request body/query parameters-এ রূপান্তর করে। |
| 37 | <code>      });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 38 | <code>      toast(successMessage &#124;&#124; response.message);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 39 | <code>      form.reset();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 40 | <code>      return true;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 41 | <code>    } catch (error) {</code> | Async failure handling ও UI cleanup/restore block। |
| 42 | <code>      toast(error.message, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 43 | <code>      return false;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 44 | <code>    } finally {</code> | Async failure handling ও UI cleanup/restore block। |
| 45 | <code>      button.disabled = false;</code> | Local state, DOM reference বা callback/result assign করে। |
| 46 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 47 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 48 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 49 | <code>  async function toggleAccount(id, action) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 50 | <code>    if (!confirm(`${action} this librarian account?`)) return;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 51 | <code>    try {</code> | Async failure handling ও UI cleanup/restore block। |
| 52 | <code>      const result = await api(`/accounts/${id}/toggle`, { method: &quot;POST&quot; });</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 53 | <code>      toast(result.message);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 54 | <code>      await renderAccounts();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 55 | <code>    } catch (error) {</code> | Async failure handling ও UI cleanup/restore block। |
| 56 | <code>      toast(error.message, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 57 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 58 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 59 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 60 | <code>  async function deleteAccount(id) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 61 | <code>    if (!confirm(&quot;Permanently delete this librarian account?&quot;)) return;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 62 | <code>    try {</code> | Async failure handling ও UI cleanup/restore block। |
| 63 | <code>      const result = await api(`/accounts/${id}`, { method: &quot;DELETE&quot; });</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 64 | <code>      toast(result.message);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 65 | <code>      await renderAccounts();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 66 | <code>    } catch (error) {</code> | Async failure handling ও UI cleanup/restore block। |
| 67 | <code>      toast(error.message, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 68 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 69 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 70 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 71 | <code>  $(&quot;#librarianForm&quot;).onsubmit = async (event) =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 72 | <code>    event.preventDefault();</code> | Default form navigation বন্ধ করে controlled API submission চালাতে দেয়। |
| 73 | <code>    const form = event.currentTarget;</code> | Local state, DOM reference বা callback/result assign করে। |
| 74 | <code>    if (form.elements.password.value !== form.elements.confirmPassword.value) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 75 | <code>      toast(&quot;Passwords do not match&quot;, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 76 | <code>      return;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 77 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 78 | <code>    if (await submitForm(form, &quot;/accounts/librarians&quot;, &quot;Librarian account created&quot;))</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 79 | <code>      await renderAccounts();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 80 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 81 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 82 | <code>  $(&quot;#credentialsForm&quot;).onsubmit = async (event) =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 83 | <code>    event.preventDefault();</code> | Default form navigation বন্ধ করে controlled API submission চালাতে দেয়। |
| 84 | <code>    const form = event.currentTarget;</code> | Local state, DOM reference বা callback/result assign করে। |
| 85 | <code>    if (form.elements.newPassword.value !== form.elements.confirmPassword.value) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 86 | <code>      toast(&quot;New passwords do not match&quot;, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 87 | <code>      return;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 88 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 89 | <code>    if (await submitForm(form, &quot;/auth/change-credentials&quot;, &quot;Administrator credentials updated&quot;)) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 90 | <code>      const session = await api(&quot;/auth/session&quot;);</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 91 | <code>      $(&quot;#sessionUser&quot;).textContent = `${session.username} - ${session.user_type}`;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 92 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 93 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 94 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 95 | <code>  loadData(renderAccounts);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 96 | <code>})();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
