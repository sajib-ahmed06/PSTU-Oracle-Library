# frontend/notifications.js

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../frontend/notifications.js)। Snapshot 2026-10-04; 238 lines; SHA-256 `d09df265bcea3cd19dae8532bcad66c31a99fcb249ad76de4acacb034f4d05bc`।

## Function / object / element inventory

### `daysUntilDue(value, now = Date.now()` — L8

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

### `buildItems(data, session, now = Date.now()` — L17

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

### `create({ $, escapeHtml, toast })` — L104

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

### `saveRead()` — L118

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

### `renderCount()` — L128

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

### `render()` — L137

এই page-এর current state ও search/filter থেকে tables/metrics/options তৈরি করে, DOM update করে এবং generated action buttons-এর events bind করে। পাশের পূর্ণ code-এ page-specific fields দেখা যাবে।

### `update(data, connected = true)` — L163

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

### `setSession(account)` — L182

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

### `close()` — L198

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

## সম্পূর্ণ original source

```javascript
"use strict";

// Alerts describe current library work; reading one never resolves its underlying record.
window.LibraryNotifications = (() => {
  const money = (value) => `Tk ${Number(value).toLocaleString("en-BD")}`;
  const cents = (value) => Math.round(Number(value || 0) * 100);

  function daysUntilDue(value, now = Date.now()) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(value || "")) return null;
    const due = Date.parse(`${value}T00:00:00Z`);
    if (!Number.isFinite(due) || new Date(due).toISOString().slice(0, 10) !== value) return null;
    // Compare calendar dates in Dhaka, regardless of the browser's timezone.
    const today = Math.floor((now + 6 * 60 * 60 * 1000) / 86400000);
    return Math.floor(due / 86400000) - today;
  }

  function buildItems(data, session, now = Date.now()) {
    const personal = session.user_type === "STUDENT";
    const own = (record) => !personal || Number(record.student_id) === Number(session.student_id);
    const destination = (section) => (personal ? `/student#${section}` : `/${section}`);
    const items = [];

    for (const reservation of data.reservations || []) {
      const expiry = Date.parse(`${reservation.expires_at?.replace(" ", "T")}+06:00`);
      if (!own(reservation) || reservation.status !== "ACTIVE" || expiry <= now) continue;
      items.push({
        key: `reservation:${reservation.reservation_id}`,
        type: "reservation",
        priority: 3,
        deadline: reservation.expires_at,
        title: personal ? "Your reserved book is ready" : "Reservation awaiting pickup",
        detail: `${personal ? "" : `${reservation.student} · `}${reservation.title} · Copy #${reservation.copy_no}`,
        note: `Collect before ${reservation.expires_at}`,
        href: destination("reservations"),
        order: Number(reservation.reservation_id),
      });
    }

    const recordedIssues = new Set((data.fines || []).map((fine) => Number(fine.issue_id)));
    for (const fine of data.fines || []) {
      const balance = fine.balance ?? Number(fine.amount) - Number(fine.paid_amount || 0);
      if (!own(fine) || fine.payment_status === "PAID" || cents(balance) <= 0) continue;
      items.push({
        key: `fine:${fine.fine_id}:${cents(balance)}`,
        type: "fine",
        priority: 1,
        urgency: cents(balance),
        title: personal ? "You have an unpaid fine" : "Outstanding member fine",
        detail: `${personal ? "" : `${fine.student} · `}${fine.title}`,
        note: `${money(balance)} outstanding · Full payment required`,
        href: destination("fines"),
        order: Number(fine.fine_id),
      });
    }

    for (const issue of data.issues || []) {
      const remaining = daysUntilDue(issue.due_date, now);
      if (
        own(issue) &&
        issue.status === "ISSUED" &&
        remaining !== null &&
        remaining >= 0 &&
        remaining <= 3
      ) {
        items.push({
          key: `due:${issue.issue_id}:${issue.due_date}:${remaining}`,
          type: "due",
          priority: 2,
          deadline: issue.due_date,
          title:
            remaining === 0
              ? "Book return is due today"
              : `Book return is due in ${remaining} day${remaining === 1 ? "" : "s"}`,
          detail: `${personal ? "" : `${issue.student} · `}${issue.title} · ${issue.copy_no ? `Copy #${issue.copy_no}` : "Legacy copy"}`,
          note: `Issued ${issue.issue_date || "—"} · Return by ${issue.due_date} · Avoid Tk 10/day overdue fine`,
          href: personal ? "/student#loans" : "/circulation",
          order: Number(issue.issue_id),
        });
      }
      if (!own(issue) || issue.status !== "ISSUED" || recordedIssues.has(Number(issue.issue_id)))
        continue;
      if (cents(issue.current_fine) <= 0) continue;
      items.push({
        key: `overdue:${issue.issue_id}:${cents(issue.current_fine)}`,
        type: "fine",
        priority: 0,
        urgency: cents(issue.current_fine),
        title: personal ? "Your borrowed book is overdue" : "Overdue book accruing a fine",
        detail: `${personal ? "" : `${issue.student} · `}${issue.title}`,
        note: `${money(issue.current_fine)} estimated today · ${Number(issue.overdue_days) || Math.max(0, -(remaining || 0))} overdue day(s) · Tk 10/day until return · Return due ${issue.due_date}. Return the book and pay the final fine in full.`,
        href: destination("fines"),
        order: Number(issue.issue_id),
      });
    }
    return items.sort(
      (first, second) =>
        first.priority - second.priority ||
        String(first.deadline || "").localeCompare(String(second.deadline || "")) ||
        Number(second.urgency || 0) - Number(first.urgency || 0) ||
        second.order - first.order,
    );
  }

  function create({ $, escapeHtml, toast }) {
    const root = $("#notificationCenter");
    const bell = $("#notificationButton");
    const panel = $("#notificationPanel");
    const list = $("#notificationList");
    let session = null;
    let latestData = null;
    let items = [];
    let read = new Set();
    let previousKeys = null;
    let online = true;
    let filter = "all";
    let storageKey = "";

    function saveRead() {
      // Persist identifiers only, separately for each signed-in account.
      read = new Set(items.filter((item) => read.has(item.key)).map((item) => item.key));
      try {
        window.localStorage.setItem(storageKey, JSON.stringify([...read]));
      } catch {
        // Private browsing still supports read state for this page session.
      }
    }

    function renderCount() {
      const unread = items.filter((item) => !read.has(item.key)).length;
      $("#notificationBadge").textContent = unread > 99 ? "99+" : String(unread);
      $("#notificationBadge").hidden = unread === 0;
      bell.setAttribute("aria-label", `Notifications, ${unread} unread`);
      $("#notificationSummary").textContent = `${unread} unread · ${items.length} active alerts`;
      $("#notificationReadAll").disabled = unread === 0;
    }

    function render() {
      renderCount();
      $("#notificationFreshness").textContent = online
        ? "Updates automatically every 30–60 seconds"
        : "Connection lost · Showing the last loaded alerts";
      const visible = items.filter((item) => filter === "all" || item.type === filter);
      list.innerHTML = visible.length
        ? visible
            .map(
              (item) =>
                `<a class="notification-item ${read.has(item.key) ? "is-read" : "is-unread"}" href="${item.href}" data-alert-key="${escapeHtml(item.key)}"><span class="notification-symbol ${item.type}" aria-hidden="true">${item.type === "fine" ? "৳" : item.type === "due" ? "D" : "R"}</span><span class="notification-copy"><strong>${escapeHtml(item.title)}</strong><span>${escapeHtml(item.detail)}</span><small>${escapeHtml(item.note)}</small></span><span class="notification-unread-dot" aria-hidden="true"></span></a>`,
            )
            .join("")
        : '<div class="notification-empty"><strong>You’re all caught up</strong><span>No active alerts in this section.</span></div>';
      list.querySelectorAll("[data-alert-key]").forEach((link) => {
        link.onclick = () => {
          read.add(link.dataset.alertKey);
          saveRead();
          link.classList.remove("is-unread");
          link.classList.add("is-read");
          renderCount();
          close();
        };
      });
    }

    function update(data, connected = true) {
      online = connected;
      if (connected) latestData = data;
      if (!session) return;
      if (connected) {
        items = buildItems(latestData || {}, session);
        const newItems = items.filter(
          (item) => previousKeys && !previousKeys.has(item.key) && !read.has(item.key),
        );
        previousKeys = new Set(items.map((item) => item.key));
        saveRead();
        if (newItems.length)
          toast(
            `${newItems.length} new library alert${newItems.length === 1 ? "" : "s"}. Open the notification bell for details.`,
          );
      }
      render();
    }

    function setSession(account) {
      session = account;
      storageKey = `pstu-alerts:${account.user_type}:${account.user_id ?? account.username}`;
      try {
        const stored = JSON.parse(window.localStorage.getItem(storageKey) || "[]");
        read = new Set(
          Array.isArray(stored) ? stored.filter((key) => typeof key === "string") : [],
        );
      } catch {
        read = new Set();
      }
      previousKeys = null;
      if (latestData) update(latestData, online);
      else render();
    }

    function close() {
      panel.hidden = true;
      bell.setAttribute("aria-expanded", "false");
    }
    bell.onclick = () => {
      panel.hidden = !panel.hidden;
      bell.setAttribute("aria-expanded", String(!panel.hidden));
      if (!panel.hidden) $("#notificationClose").focus();
    };
    $("#notificationClose").onclick = () => {
      close();
      bell.focus();
    };
    $("#notificationReadAll").onclick = () => {
      items.forEach((item) => read.add(item.key));
      saveRead();
      render();
    };
    root.querySelectorAll("[data-alert-filter]").forEach((button) => {
      button.onclick = () => {
        filter = button.dataset.alertFilter;
        root.querySelectorAll("[data-alert-filter]").forEach((tab) => {
          tab.setAttribute("aria-pressed", String(tab === button));
        });
        render();
      };
    });
    document.addEventListener("click", (event) => {
      if (!root.contains(event.target)) close();
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && !panel.hidden) {
        close();
        bell.focus();
      }
    });
    return { update, setSession };
  }

  return { buildItems, create, daysUntilDue };
})();
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;use strict&quot;;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>// Alerts describe current library work; reading one never resolves its underlying record.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 4 | <code>window.LibraryNotifications = (() =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 5 | <code>  const money = (value) =&gt; `Tk ${Number(value).toLocaleString(&quot;en-BD&quot;)}`;</code> | Local state, DOM reference বা callback/result assign করে। |
| 6 | <code>  const cents = (value) =&gt; Math.round(Number(value &#124;&#124; 0) * 100);</code> | Local state, DOM reference বা callback/result assign করে। |
| 7 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 8 | <code>  function daysUntilDue(value, now = Date.now()) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 9 | <code>    if (!/^\d{4}-\d{2}-\d{2}$/.test(value &#124;&#124; &quot;&quot;)) return null;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 10 | <code>    const due = Date.parse(`${value}T00:00:00Z`);</code> | Local state, DOM reference বা callback/result assign করে। |
| 11 | <code>    if (!Number.isFinite(due) &#124;&#124; new Date(due).toISOString().slice(0, 10) !== value) return null;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 12 | <code>    // Compare calendar dates in Dhaka, regardless of the browser&#x27;s timezone.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 13 | <code>    const today = Math.floor((now + 6 * 60 * 60 * 1000) / 86400000);</code> | Local state, DOM reference বা callback/result assign করে। |
| 14 | <code>    return Math.floor(due / 86400000) - today;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 15 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 16 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 17 | <code>  function buildItems(data, session, now = Date.now()) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 18 | <code>    const personal = session.user_type === &quot;STUDENT&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 19 | <code>    const own = (record) =&gt; !personal &#124;&#124; Number(record.student_id) === Number(session.student_id);</code> | Local state, DOM reference বা callback/result assign করে। |
| 20 | <code>    const destination = (section) =&gt; (personal ? `/student#${section}` : `/${section}`);</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 21 | <code>    const items = [];</code> | Local state, DOM reference বা callback/result assign করে। |
| 22 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 23 | <code>    for (const reservation of data.reservations &#124;&#124; []) {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 24 | <code>      const expiry = Date.parse(`${reservation.expires_at?.replace(&quot; &quot;, &quot;T&quot;)}+06:00`);</code> | Local state, DOM reference বা callback/result assign করে। |
| 25 | <code>      if (!own(reservation) &#124;&#124; reservation.status !== &quot;ACTIVE&quot; &#124;&#124; expiry &lt;= now) continue;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 26 | <code>      items.push({</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 27 | <code>        key: `reservation:${reservation.reservation_id}`,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 28 | <code>        type: &quot;reservation&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 29 | <code>        priority: 3,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 30 | <code>        deadline: reservation.expires_at,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 31 | <code>        title: personal ? &quot;Your reserved book is ready&quot; : &quot;Reservation awaiting pickup&quot;,</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 32 | <code>        detail: `${personal ? &quot;&quot; : `${reservation.student} · `}${reservation.title} · Copy #${reservation.copy_no}`,</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 33 | <code>        note: `Collect before ${reservation.expires_at}`,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 34 | <code>        href: destination(&quot;reservations&quot;),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 35 | <code>        order: Number(reservation.reservation_id),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 36 | <code>      });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 37 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 38 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 39 | <code>    const recordedIssues = new Set((data.fines &#124;&#124; []).map((fine) =&gt; Number(fine.issue_id)));</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 40 | <code>    for (const fine of data.fines &#124;&#124; []) {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 41 | <code>      const balance = fine.balance ?? Number(fine.amount) - Number(fine.paid_amount &#124;&#124; 0);</code> | Local state, DOM reference বা callback/result assign করে। |
| 42 | <code>      if (!own(fine) &#124;&#124; fine.payment_status === &quot;PAID&quot; &#124;&#124; cents(balance) &lt;= 0) continue;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 43 | <code>      items.push({</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 44 | <code>        key: `fine:${fine.fine_id}:${cents(balance)}`,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 45 | <code>        type: &quot;fine&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 46 | <code>        priority: 1,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 47 | <code>        urgency: cents(balance),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 48 | <code>        title: personal ? &quot;You have an unpaid fine&quot; : &quot;Outstanding member fine&quot;,</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 49 | <code>        detail: `${personal ? &quot;&quot; : `${fine.student} · `}${fine.title}`,</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 50 | <code>        note: `${money(balance)} outstanding · Full payment required`,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 51 | <code>        href: destination(&quot;fines&quot;),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 52 | <code>        order: Number(fine.fine_id),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 53 | <code>      });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 54 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 55 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 56 | <code>    for (const issue of data.issues &#124;&#124; []) {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 57 | <code>      const remaining = daysUntilDue(issue.due_date, now);</code> | Local state, DOM reference বা callback/result assign করে। |
| 58 | <code>      if (</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 59 | <code>        own(issue) &amp;&amp;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 60 | <code>        issue.status === &quot;ISSUED&quot; &amp;&amp;</code> | Local state, DOM reference বা callback/result assign করে। |
| 61 | <code>        remaining !== null &amp;&amp;</code> | Local state, DOM reference বা callback/result assign করে। |
| 62 | <code>        remaining &gt;= 0 &amp;&amp;</code> | Local state, DOM reference বা callback/result assign করে। |
| 63 | <code>        remaining &lt;= 3</code> | Local state, DOM reference বা callback/result assign করে। |
| 64 | <code>      ) {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 65 | <code>        items.push({</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 66 | <code>          key: `due:${issue.issue_id}:${issue.due_date}:${remaining}`,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 67 | <code>          type: &quot;due&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 68 | <code>          priority: 2,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 69 | <code>          deadline: issue.due_date,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 70 | <code>          title:</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 71 | <code>            remaining === 0</code> | Local state, DOM reference বা callback/result assign করে। |
| 72 | <code>              ? &quot;Book return is due today&quot;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 73 | <code>              : `Book return is due in ${remaining} day${remaining === 1 ? &quot;&quot; : &quot;s&quot;}`,</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 74 | <code>          detail: `${personal ? &quot;&quot; : `${issue.student} · `}${issue.title} · ${issue.copy_no ? `Copy #${issue.copy_no}` : &quot;Legacy copy&quot;}`,</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 75 | <code>          note: `Issued ${issue.issue_date &#124;&#124; &quot;—&quot;} · Return by ${issue.due_date} · Avoid Tk 10/day overdue fine`,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 76 | <code>          href: personal ? &quot;/student#loans&quot; : &quot;/circulation&quot;,</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 77 | <code>          order: Number(issue.issue_id),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 78 | <code>        });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 79 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 80 | <code>      if (!own(issue) &#124;&#124; issue.status !== &quot;ISSUED&quot; &#124;&#124; recordedIssues.has(Number(issue.issue_id)))</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 81 | <code>        continue;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 82 | <code>      if (cents(issue.current_fine) &lt;= 0) continue;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 83 | <code>      items.push({</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 84 | <code>        key: `overdue:${issue.issue_id}:${cents(issue.current_fine)}`,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 85 | <code>        type: &quot;fine&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 86 | <code>        priority: 0,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 87 | <code>        urgency: cents(issue.current_fine),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 88 | <code>        title: personal ? &quot;Your borrowed book is overdue&quot; : &quot;Overdue book accruing a fine&quot;,</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 89 | <code>        detail: `${personal ? &quot;&quot; : `${issue.student} · `}${issue.title}`,</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 90 | <code>        note: `${money(issue.current_fine)} estimated today · ${Number(issue.overdue_days) &#124;&#124; Math.max(0, -(remaining &#124;&#124; 0))} overdue day(s) · Tk 10/day until return · Return due ${issue.due_date}. Return the book and pay the final fine in full.`,</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 91 | <code>        href: destination(&quot;fines&quot;),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 92 | <code>        order: Number(issue.issue_id),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 93 | <code>      });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 94 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 95 | <code>    return items.sort(</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 96 | <code>      (first, second) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 97 | <code>        first.priority - second.priority &#124;&#124;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 98 | <code>        String(first.deadline &#124;&#124; &quot;&quot;).localeCompare(String(second.deadline &#124;&#124; &quot;&quot;)) &#124;&#124;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 99 | <code>        Number(second.urgency &#124;&#124; 0) - Number(first.urgency &#124;&#124; 0) &#124;&#124;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 100 | <code>        second.order - first.order,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 101 | <code>    );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 102 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 103 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 104 | <code>  function create({ $, escapeHtml, toast }) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 105 | <code>    const root = $(&quot;#notificationCenter&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 106 | <code>    const bell = $(&quot;#notificationButton&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 107 | <code>    const panel = $(&quot;#notificationPanel&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 108 | <code>    const list = $(&quot;#notificationList&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 109 | <code>    let session = null;</code> | Local state, DOM reference বা callback/result assign করে। |
| 110 | <code>    let latestData = null;</code> | Local state, DOM reference বা callback/result assign করে। |
| 111 | <code>    let items = [];</code> | Local state, DOM reference বা callback/result assign করে। |
| 112 | <code>    let read = new Set();</code> | Local state, DOM reference বা callback/result assign করে। |
| 113 | <code>    let previousKeys = null;</code> | Local state, DOM reference বা callback/result assign করে। |
| 114 | <code>    let online = true;</code> | Local state, DOM reference বা callback/result assign করে। |
| 115 | <code>    let filter = &quot;all&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 116 | <code>    let storageKey = &quot;&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 117 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 118 | <code>    function saveRead() {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 119 | <code>      // Persist identifiers only, separately for each signed-in account.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 120 | <code>      read = new Set(items.filter((item) =&gt; read.has(item.key)).map((item) =&gt; item.key));</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 121 | <code>      try {</code> | Async failure handling ও UI cleanup/restore block। |
| 122 | <code>        window.localStorage.setItem(storageKey, JSON.stringify([...read]));</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 123 | <code>      } catch {</code> | Async failure handling ও UI cleanup/restore block। |
| 124 | <code>        // Private browsing still supports read state for this page session.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 125 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 126 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 127 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 128 | <code>    function renderCount() {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 129 | <code>      const unread = items.filter((item) =&gt; !read.has(item.key)).length;</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 130 | <code>      $(&quot;#notificationBadge&quot;).textContent = unread &gt; 99 ? &quot;99+&quot; : String(unread);</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 131 | <code>      $(&quot;#notificationBadge&quot;).hidden = unread === 0;</code> | Local state, DOM reference বা callback/result assign করে। |
| 132 | <code>      bell.setAttribute(&quot;aria-label&quot;, `Notifications, ${unread} unread`);</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 133 | <code>      $(&quot;#notificationSummary&quot;).textContent = `${unread} unread · ${items.length} active alerts`;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 134 | <code>      $(&quot;#notificationReadAll&quot;).disabled = unread === 0;</code> | Local state, DOM reference বা callback/result assign করে। |
| 135 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 136 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 137 | <code>    function render() {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 138 | <code>      renderCount();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 139 | <code>      $(&quot;#notificationFreshness&quot;).textContent = online</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 140 | <code>        ? &quot;Updates automatically every 30–60 seconds&quot;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 141 | <code>        : &quot;Connection lost · Showing the last loaded alerts&quot;;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 142 | <code>      const visible = items.filter((item) =&gt; filter === &quot;all&quot; &#124;&#124; item.type === filter);</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 143 | <code>      list.innerHTML = visible.length</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 144 | <code>        ? visible</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 145 | <code>            .map(</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 146 | <code>              (item) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 147 | <code>                `&lt;a class=&quot;notification-item ${read.has(item.key) ? &quot;is-read&quot; : &quot;is-unread&quot;}&quot; href=&quot;${item.href}&quot; data-alert-key=&quot;${escapeHtml(item.key)}&quot;&gt;&lt;span class=&quot;notification-symbol ${item.type}&quot; aria-hidden=&quot;true&quot;&gt;${item.type === &quot;fine&quot; ? &quot;৳&quot; : item.type === &quot;due&quot; ? &quot;D&quot; : &quot;R&quot;}&lt;/span&gt;&lt;span class=&quot;notification-copy&quot;&gt;&lt;strong&gt;${escapeHtml(item.title)}&lt;/strong&gt;&lt;span&gt;${escapeHtml(item.detail)}&lt;/span&gt;&lt;small&gt;${escapeHtml(item.note)}&lt;/small&gt;&lt;/span&gt;&lt;span class=&quot;notification-unread-dot&quot; aria-hidden=&quot;true&quot;&gt;&lt;/span&gt;&lt;/a&gt;`,</code> | User/database values escaped display markup-এ রূপান্তর করে। |
| 148 | <code>            )</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 149 | <code>            .join(&quot;&quot;)</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 150 | <code>        : &#x27;&lt;div class=&quot;notification-empty&quot;&gt;&lt;strong&gt;You’re all caught up&lt;/strong&gt;&lt;span&gt;No active alerts in this section.&lt;/span&gt;&lt;/div&gt;&#x27;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 151 | <code>      list.querySelectorAll(&quot;[data-alert-key]&quot;).forEach((link) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 152 | <code>        link.onclick = () =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 153 | <code>          read.add(link.dataset.alertKey);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 154 | <code>          saveRead();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 155 | <code>          link.classList.remove(&quot;is-unread&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 156 | <code>          link.classList.add(&quot;is-read&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 157 | <code>          renderCount();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 158 | <code>          close();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 159 | <code>        };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 160 | <code>      });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 161 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 162 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 163 | <code>    function update(data, connected = true) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 164 | <code>      online = connected;</code> | Local state, DOM reference বা callback/result assign করে। |
| 165 | <code>      if (connected) latestData = data;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 166 | <code>      if (!session) return;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 167 | <code>      if (connected) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 168 | <code>        items = buildItems(latestData &#124;&#124; {}, session);</code> | Local state, DOM reference বা callback/result assign করে। |
| 169 | <code>        const newItems = items.filter(</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 170 | <code>          (item) =&gt; previousKeys &amp;&amp; !previousKeys.has(item.key) &amp;&amp; !read.has(item.key),</code> | Local state, DOM reference বা callback/result assign করে। |
| 171 | <code>        );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 172 | <code>        previousKeys = new Set(items.map((item) =&gt; item.key));</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 173 | <code>        saveRead();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 174 | <code>        if (newItems.length)</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 175 | <code>          toast(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 176 | <code>            `${newItems.length} new library alert${newItems.length === 1 ? &quot;&quot; : &quot;s&quot;}. Open the notification bell for details.`,</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 177 | <code>          );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 178 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 179 | <code>      render();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 180 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 181 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 182 | <code>    function setSession(account) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 183 | <code>      session = account;</code> | Local state, DOM reference বা callback/result assign করে। |
| 184 | <code>      storageKey = `pstu-alerts:${account.user_type}:${account.user_id ?? account.username}`;</code> | Local state, DOM reference বা callback/result assign করে। |
| 185 | <code>      try {</code> | Async failure handling ও UI cleanup/restore block। |
| 186 | <code>        const stored = JSON.parse(window.localStorage.getItem(storageKey) &#124;&#124; &quot;[]&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 187 | <code>        read = new Set(</code> | Local state, DOM reference বা callback/result assign করে। |
| 188 | <code>          Array.isArray(stored) ? stored.filter((key) =&gt; typeof key === &quot;string&quot;) : [],</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 189 | <code>        );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 190 | <code>      } catch {</code> | Async failure handling ও UI cleanup/restore block। |
| 191 | <code>        read = new Set();</code> | Local state, DOM reference বা callback/result assign করে। |
| 192 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 193 | <code>      previousKeys = null;</code> | Local state, DOM reference বা callback/result assign করে। |
| 194 | <code>      if (latestData) update(latestData, online);</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 195 | <code>      else render();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 196 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 197 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 198 | <code>    function close() {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 199 | <code>      panel.hidden = true;</code> | Local state, DOM reference বা callback/result assign করে। |
| 200 | <code>      bell.setAttribute(&quot;aria-expanded&quot;, &quot;false&quot;);</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 201 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 202 | <code>    bell.onclick = () =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 203 | <code>      panel.hidden = !panel.hidden;</code> | Local state, DOM reference বা callback/result assign করে। |
| 204 | <code>      bell.setAttribute(&quot;aria-expanded&quot;, String(!panel.hidden));</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 205 | <code>      if (!panel.hidden) $(&quot;#notificationClose&quot;).focus();</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 206 | <code>    };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 207 | <code>    $(&quot;#notificationClose&quot;).onclick = () =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 208 | <code>      close();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 209 | <code>      bell.focus();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 210 | <code>    };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 211 | <code>    $(&quot;#notificationReadAll&quot;).onclick = () =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 212 | <code>      items.forEach((item) =&gt; read.add(item.key));</code> | Local state, DOM reference বা callback/result assign করে। |
| 213 | <code>      saveRead();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 214 | <code>      render();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 215 | <code>    };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 216 | <code>    root.querySelectorAll(&quot;[data-alert-filter]&quot;).forEach((button) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 217 | <code>      button.onclick = () =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 218 | <code>        filter = button.dataset.alertFilter;</code> | Local state, DOM reference বা callback/result assign করে। |
| 219 | <code>        root.querySelectorAll(&quot;[data-alert-filter]&quot;).forEach((tab) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 220 | <code>          tab.setAttribute(&quot;aria-pressed&quot;, String(tab === button));</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 221 | <code>        });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 222 | <code>        render();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 223 | <code>      };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 224 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 225 | <code>    document.addEventListener(&quot;click&quot;, (event) =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 226 | <code>      if (!root.contains(event.target)) close();</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 227 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 228 | <code>    document.addEventListener(&quot;keydown&quot;, (event) =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 229 | <code>      if (event.key === &quot;Escape&quot; &amp;&amp; !panel.hidden) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 230 | <code>        close();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 231 | <code>        bell.focus();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 232 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 233 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 234 | <code>    return { update, setSession };</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 235 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 236 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 237 | <code>  return { buildItems, create, daysUntilDue };</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 238 | <code>})();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
