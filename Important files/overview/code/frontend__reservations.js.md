# frontend/reservations.js

Coordinate page-specific views, refresh requests and reservation actions.

Source: [মূল file](../../frontend/reservations.js)। Snapshot 2026-10-04; 113 lines; SHA-256 `ad73a3cc426e35523ebfd280b953b0b952da52936cdc21b4e3dcb3c754c71e45`।

## Function / object / element inventory

### `reservationTable(items)` — L8

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

### `refresh()` — L64

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

### `action(button, path, body, confirmation)` — L90

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

## সম্পূর্ণ original source

```javascript
(() => {
  const { $, $$, state, api, escapeHtml: e, table, toast, memberId, loadData } = LibraryApp;
  const student = document.body.dataset.page === "student";
  const money = (value) => `Tk ${Number(value || 0).toLocaleString("en-BD")}`;
  let data = null;
  let pending = null;

  function reservationTable(items) {
    $("#reservationTable").innerHTML =
      student && !items.length
        ? '<div class="empty-state"><strong>Your next read is waiting.</strong><span>Browse the catalogue to reserve an available copy for 3 days.</span></div>'
        : table(
            student
              ? ["Book", "Copy", "Reserved", "Collect before", "Status", "Action"]
              : ["Member", "Book", "Copy", "Reserved", "Collect before", "Status", "Action"],
            items.map((r) => {
              const active = r.status === "ACTIVE";
              const actions = active
                ? `${student ? "" : `<button class="button small primary" data-collect="${r.reservation_id}">Issue reserved copy</button>`} <button class="button small secondary" data-cancel="${r.reservation_id}">Cancel</button>`
                : "—";
              return `<tr>${student ? "" : `<td><b>${e(r.student)}</b><small>${memberId(r.student_id)}</small></td>`}<td>${e(r.title)}</td><td>Copy #${r.copy_no}</td><td>${e(r.reserved_at)}</td><td>${e(r.expires_at)}</td><td><span class="pill ${active ? "active" : "returned"}">${e(r.status)}</span></td><td>${actions}</td></tr>`;
            }),
          );
    $$("[data-cancel]").forEach((button) => {
      button.onclick = () =>
        action(
          button,
          `/reservations/${button.dataset.cancel}/cancel`,
          {},
          "Cancel this reservation?",
        );
    });
    $$("[data-collect]").forEach((button) => {
      button.onclick = () =>
        action(
          button,
          `/reservations/${button.dataset.collect}/collect`,
          {},
          "Issue this copy to the member now?",
        );
    });
  }

  // Each page owns its rendering; transport and write protection stay here.
  const context = {
    sortIssues: LibraryApp.sortIssues,
    $,
    $$,
    state,
    api,
    escapeHtml: e,
    table,
    toast,
    memberId,
    money,
    getData: () => data,
    action,
    reservationTable,
  };
  const view = student
    ? window.MemberDashboard.create(context)
    : window.ReservationDesk.create(context);

  async function refresh() {
    if (pending) return pending;
    pending = (async () => {
      if (!student) return loadData(view.render);
      try {
        data = await api("/student/dashboard");
        state.online = true;
        LibraryApp.updateNotifications?.(data, true);
        $("#dbDot")?.classList.add("online");
        $("#dbText").textContent = "Oracle XE connected";
      } catch (error) {
        state.online = false;
        LibraryApp.updateNotifications?.(data, false);
        $("#dbDot")?.classList.remove("online");
        $("#dbText").textContent = "Database unavailable";
        toast(error.message, true);
      }
      view.render();
    })();
    try {
      await pending;
    } finally {
      pending = null;
    }
  }

  async function action(button, path, body, confirmation) {
    if (button.disabled || !state.online) return;
    if (confirmation && !confirm(confirmation)) return;
    button.disabled = true;
    try {
      const result = await api(path, { method: "POST", body: new URLSearchParams(body) });
      toast(result.message);
      await refresh();
      return true;
    } catch (error) {
      toast(error.message, true);
      return false;
    } finally {
      button.disabled = false;
    }
  }

  view.bind();
  $("#refreshButton").onclick = refresh;
  window.setInterval(() => {
    if (!document.hidden) refresh();
  }, 60000);
  refresh();
})();
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>(() =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 2 | <code>  const { $, $$, state, api, escapeHtml: e, table, toast, memberId, loadData } = LibraryApp;</code> | Local state, DOM reference বা callback/result assign করে। |
| 3 | <code>  const student = document.body.dataset.page === &quot;student&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 4 | <code>  const money = (value) =&gt; `Tk ${Number(value &#124;&#124; 0).toLocaleString(&quot;en-BD&quot;)}`;</code> | Local state, DOM reference বা callback/result assign করে। |
| 5 | <code>  let data = null;</code> | Local state, DOM reference বা callback/result assign করে। |
| 6 | <code>  let pending = null;</code> | Local state, DOM reference বা callback/result assign করে। |
| 7 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 8 | <code>  function reservationTable(items) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 9 | <code>    $(&quot;#reservationTable&quot;).innerHTML =</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 10 | <code>      student &amp;&amp; !items.length</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 11 | <code>        ? &#x27;&lt;div class=&quot;empty-state&quot;&gt;&lt;strong&gt;Your next read is waiting.&lt;/strong&gt;&lt;span&gt;Browse the catalogue to reserve an available copy for 3 days.&lt;/span&gt;&lt;/div&gt;&#x27;</code> | Local state, DOM reference বা callback/result assign করে। |
| 12 | <code>        : table(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 13 | <code>            student</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 14 | <code>              ? [&quot;Book&quot;, &quot;Copy&quot;, &quot;Reserved&quot;, &quot;Collect before&quot;, &quot;Status&quot;, &quot;Action&quot;]</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 15 | <code>              : [&quot;Member&quot;, &quot;Book&quot;, &quot;Copy&quot;, &quot;Reserved&quot;, &quot;Collect before&quot;, &quot;Status&quot;, &quot;Action&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 16 | <code>            items.map((r) =&gt; {</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 17 | <code>              const active = r.status === &quot;ACTIVE&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 18 | <code>              const actions = active</code> | Local state, DOM reference বা callback/result assign করে। |
| 19 | <code>                ? `${student ? &quot;&quot; : `&lt;button class=&quot;button small primary&quot; data-collect=&quot;${r.reservation_id}&quot;&gt;Issue reserved copy&lt;/button&gt;`} &lt;button class=&quot;button small secondary&quot; data-cancel=&quot;${r.reservation_id}&quot;&gt;Cancel&lt;/button&gt;`</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 20 | <code>                : &quot;—&quot;;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 21 | <code>              return `&lt;tr&gt;${student ? &quot;&quot; : `&lt;td&gt;&lt;b&gt;${e(r.student)}&lt;/b&gt;&lt;small&gt;${memberId(r.student_id)}&lt;/small&gt;&lt;/td&gt;`}&lt;td&gt;${e(r.title)}&lt;/td&gt;&lt;td&gt;Copy #${r.copy_no}&lt;/td&gt;&lt;td&gt;${e(r.reserved_at)}&lt;/td&gt;&lt;td&gt;${e(r.expires_at)}&lt;/td&gt;&lt;td&gt;&lt;span class=&quot;pill ${active ? &quot;active&quot; : &quot;returned&quot;}&quot;&gt;${e(r.status)}&lt;/span&gt;&lt;/td&gt;&lt;td&gt;${actions}&lt;/td&gt;&lt;/tr&gt;`;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 22 | <code>            }),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 23 | <code>          );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 24 | <code>    $$(&quot;[data-cancel]&quot;).forEach((button) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 25 | <code>      button.onclick = () =&gt;</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 26 | <code>        action(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 27 | <code>          button,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 28 | <code>          `/reservations/${button.dataset.cancel}/cancel`,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 29 | <code>          {},</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 30 | <code>          &quot;Cancel this reservation?&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 31 | <code>        );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 32 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 33 | <code>    $$(&quot;[data-collect]&quot;).forEach((button) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 34 | <code>      button.onclick = () =&gt;</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 35 | <code>        action(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 36 | <code>          button,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 37 | <code>          `/reservations/${button.dataset.collect}/collect`,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 38 | <code>          {},</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 39 | <code>          &quot;Issue this copy to the member now?&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 40 | <code>        );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 41 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 42 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 43 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 44 | <code>  // Each page owns its rendering; transport and write protection stay here.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 45 | <code>  const context = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 46 | <code>    sortIssues: LibraryApp.sortIssues,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 47 | <code>    $,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 48 | <code>    $$,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 49 | <code>    state,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 50 | <code>    api,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 51 | <code>    escapeHtml: e,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 52 | <code>    table,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 53 | <code>    toast,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 54 | <code>    memberId,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 55 | <code>    money,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 56 | <code>    getData: () =&gt; data,</code> | Local state, DOM reference বা callback/result assign করে। |
| 57 | <code>    action,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 58 | <code>    reservationTable,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 59 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 60 | <code>  const view = student</code> | Local state, DOM reference বা callback/result assign করে। |
| 61 | <code>    ? window.MemberDashboard.create(context)</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 62 | <code>    : window.ReservationDesk.create(context);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 63 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 64 | <code>  async function refresh() {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 65 | <code>    if (pending) return pending;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 66 | <code>    pending = (async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 67 | <code>      if (!student) return loadData(view.render);</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 68 | <code>      try {</code> | Async failure handling ও UI cleanup/restore block। |
| 69 | <code>        data = await api(&quot;/student/dashboard&quot;);</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 70 | <code>        state.online = true;</code> | Local state, DOM reference বা callback/result assign করে। |
| 71 | <code>        LibraryApp.updateNotifications?.(data, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 72 | <code>        $(&quot;#dbDot&quot;)?.classList.add(&quot;online&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 73 | <code>        $(&quot;#dbText&quot;).textContent = &quot;Oracle XE connected&quot;;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 74 | <code>      } catch (error) {</code> | Async failure handling ও UI cleanup/restore block। |
| 75 | <code>        state.online = false;</code> | Local state, DOM reference বা callback/result assign করে। |
| 76 | <code>        LibraryApp.updateNotifications?.(data, false);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 77 | <code>        $(&quot;#dbDot&quot;)?.classList.remove(&quot;online&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 78 | <code>        $(&quot;#dbText&quot;).textContent = &quot;Database unavailable&quot;;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 79 | <code>        toast(error.message, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 80 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 81 | <code>      view.render();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 82 | <code>    })();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 83 | <code>    try {</code> | Async failure handling ও UI cleanup/restore block। |
| 84 | <code>      await pending;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 85 | <code>    } finally {</code> | Async failure handling ও UI cleanup/restore block। |
| 86 | <code>      pending = null;</code> | Local state, DOM reference বা callback/result assign করে। |
| 87 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 88 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 89 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 90 | <code>  async function action(button, path, body, confirmation) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 91 | <code>    if (button.disabled &#124;&#124; !state.online) return;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 92 | <code>    if (confirmation &amp;&amp; !confirm(confirmation)) return;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 93 | <code>    button.disabled = true;</code> | Local state, DOM reference বা callback/result assign করে। |
| 94 | <code>    try {</code> | Async failure handling ও UI cleanup/restore block। |
| 95 | <code>      const result = await api(path, { method: &quot;POST&quot;, body: new URLSearchParams(body) });</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 96 | <code>      toast(result.message);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 97 | <code>      await refresh();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 98 | <code>      return true;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 99 | <code>    } catch (error) {</code> | Async failure handling ও UI cleanup/restore block। |
| 100 | <code>      toast(error.message, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 101 | <code>      return false;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 102 | <code>    } finally {</code> | Async failure handling ও UI cleanup/restore block। |
| 103 | <code>      button.disabled = false;</code> | Local state, DOM reference বা callback/result assign করে। |
| 104 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 105 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 106 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 107 | <code>  view.bind();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 108 | <code>  $(&quot;#refreshButton&quot;).onclick = refresh;</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 109 | <code>  window.setInterval(() =&gt; {</code> | Timeout/reconnection/search debounce timer শুরু বা বন্ধ করে। |
| 110 | <code>    if (!document.hidden) refresh();</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 111 | <code>  }, 60000);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 112 | <code>  refresh();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 113 | <code>})();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
