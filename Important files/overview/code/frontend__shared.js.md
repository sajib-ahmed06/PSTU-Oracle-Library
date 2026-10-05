# frontend/shared.js

সব management page-এর shared API client, state, header, navigation, live data loader, reconnection monitor, escaping, modal ও form submission helpers।

Source: [মূল file](../../frontend/shared.js)। Snapshot 2026-10-04; 405 lines; SHA-256 `d619d07ada6c58b6f0e5e2c74e0021dc787dfc38dce7a4154aa537379d1b3158`।

## Function / object / element inventory

### `api(path, options = {})` — L29

Relative /api URL-এ no-store fetch, 60-second timeout এবং temporary GET 503/504/network failure-এ একবার retry। POST/DELETE replay হয় না। 401 login redirect, অন্য failed status Error।

### `escapeHtml(value)` — L65

& < > quote/apostrophe-কে HTML entities বানায় যাতে user-controlled values template HTML হিসেবে execute না হয়।

### `memberId(id)` — L79

Internal numeric ID-কে display-only PSTU-0001 format-এ বানায়; academic roll/reg-এর সঙ্গে এক নয়।

### `table(headers, rows)` — L83

Headers ও row HTML দিয়ে table বানায়; rows খালি হলে empty-state message দেয়। Calling code-কে values escape করতে হয়।

### `toast(message, error = false)` — L89

Toast textContent/class বদলায় এবং পুরোনো timer clear করে প্রায় 2.8 seconds পরে message লুকায়।

### `renderHeader()` — L100

Navigation, connection indicator, session user ও logout button বসায়; Accounts/Audit links শুধু ADMIN-এর জন্য visible হয়।

### `setConnection(online)` — L173

Connection dot/label update করে; offline অবস্থায় Database unavailable দেখায়।

### `loadData(render)` — L179

Coalesce overlapping requests and GET /api/snapshot instead of five separate read endpoints; update live state and connection status together.

### `startConnectionMonitor()` — L222

5-second interval-এ health পরীক্ষা; hidden/pending check/data load skip। Reconnect-এ state reload; browser online ও visibilitychange recovery handlers-ও থাকে।

### `sortIssues(items)` — L259

Issue date descending ও তারপর numeric issue ID descending-এ copied list sort করে।

### `issueRows(items, actions = false)` — L284

Loan table HTML render করে; active loan-এর due date পেরোলে OVERDUE label; actions enabled হলে Return button।

### `openModal(id)` — L299

Dialog open করে aria attributes বসায়, return-focus element ধরে এবং প্রথম input/select/button-এ focus দেয়।

### `closeModal(modal)` — L310

Dialog hide করে form reset ও opener focus restore করে।

### `bindModals()` — L317

Open/close/backdrop/Escape handlers এবং Tab/Shift+Tab focus containment বসায়।

### `postForm(form, path)` — L349

Offline হলে save আটকায়; submit button disable করে URLSearchParams(FormData) POST; success-এ modal close ও toast; শেষে button restore। Login-এর মতো আলাদা submitting flag এখানে নেই।

### `openRequestedModal(id)` — L369

URL-এর new=1 থাকলে requested dialog খুলে query parameter সরায়; reconnection-এ dialog পুনরায় খোলা বন্ধ হয়।

## সম্পূর্ণ original source

```javascript
const LibraryApp = (() => {
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const day = 24 * 60 * 60 * 1000;
  const dateFromToday = (offset) =>
    new Intl.DateTimeFormat("en-CA", {
      timeZone: "Asia/Dhaka",
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    }).format(new Date(Date.now() + offset * day));

  const state = {
    books: [],
    students: [],
    issues: [],
    fines: [],
    meta: { authors: [], categories: [] },
    online: false,
  };
  let activeRender = null;
  let connectionTimer = null;
  let checkingConnection = false;
  let loadingData = null;
  let snapshotSupported = true;
  let notifications = null;
  let lastDataRefresh = 0;

  async function api(path, options = {}) {
    const readOnly = !options.method || options.method.toUpperCase() === "GET";
    for (let attempt = 0; attempt < (readOnly ? 2 : 1); attempt++) {
      try {
        const response = await fetch(`/api${path}`, {
          ...options,
          cache: "no-store",
          signal: options.signal || AbortSignal.timeout(60000),
        });
        if (response.status === 401) {
          window.location.replace("/login");
          throw new Error("Your session has expired. Please sign in again");
        }
        if (readOnly && attempt === 0 && [503, 504].includes(response.status)) {
          await new Promise((resolve) => setTimeout(resolve, 400));
          continue;
        }
        const data = await response.json();
        if (!response.ok) {
          const error = new Error(
            typeof data.detail === "string" ? data.detail : data.error || "Request failed",
          );
          error.status = response.status;
          throw error;
        }
        return data;
      } catch (error) {
        if (readOnly && attempt === 0 && error instanceof TypeError && !options.signal?.aborted) {
          await new Promise((resolve) => setTimeout(resolve, 400));
          continue;
        }
        throw error;
      }
    }
  }

  function escapeHtml(value) {
    return String(value ?? "").replace(
      /[&<>"']/g,
      (character) =>
        ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        })[character],
    );
  }

  function memberId(id) {
    return `PSTU-${String(id).padStart(4, "0")}`;
  }

  function table(headers, rows) {
    if (!rows.length)
      return '<div class="empty-state"><strong>No records found</strong><span>Try another search or add a new record.</span></div>';
    return `<table><thead><tr>${headers.map((header) => `<th>${header}</th>`).join("")}</tr></thead><tbody>${rows.join("")}</tbody></table>`;
  }

  function toast(message, error = false) {
    const element = $("#toast");
    if (!element) return;
    element.textContent = message;
    element.className = error ? "show error" : "show";
    clearTimeout(element.timer);
    element.timer = setTimeout(() => {
      element.className = "";
    }, 2800);
  }

  function renderHeader() {
    const activePage = document.body.dataset.page;
    const pages = [
      ["overview", "/", "Dashboard"],
      ["books", "/books", "Books"],
      ["students", "/students", "Members"],
      ["circulation", "/circulation", "Issue & Return"],
      ["fines", "/fines", "Fines"],
      ["accounts", "/accounts", "Accounts"],
      ["audit", "/audit", "Audit"],
      ["reservations", "/reservations", "Reservations"],
    ];
    $("#appHeader").innerHTML = `
      <header class="app-header">
        <div class="brand-block"><span class="brand-mark">PSTU</span><div><strong>Central Library</strong><small>Management System</small></div></div>
        <div class="university-name">Patuakhali Science and Technology University</div>
        <div class="header-tools">
          <div class="connection"><i id="dbDot"></i><span id="dbText">Connecting...</span></div>
          <div id="notificationCenter" class="notification-center">
            <button id="notificationButton" class="notification-button" type="button" aria-label="Notifications" aria-expanded="false" aria-controls="notificationPanel">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9M10 21h4" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <span id="notificationBadge" class="notification-badge" hidden aria-live="polite"></span>
            </button>
            <section id="notificationPanel" class="notification-panel" aria-label="Library notifications" hidden>
              <div class="notification-heading"><div><h2>Notifications</h2><p id="notificationSummary">Loading library alerts…</p></div><button id="notificationClose" class="notification-close" type="button" aria-label="Close notifications">&times;</button></div>
              <div class="notification-controls"><button type="button" data-alert-filter="all" aria-pressed="true">All</button><button type="button" data-alert-filter="reservation" aria-pressed="false">Reservations</button><button type="button" data-alert-filter="due" aria-pressed="false">Due dates</button><button type="button" data-alert-filter="fine" aria-pressed="false">Fines</button><button id="notificationReadAll" type="button">Mark all read</button></div>
              <div id="notificationList" class="notification-list"></div><p id="notificationFreshness" class="notification-freshness"></p>
            </section>
          </div>
          <div class="user-menu"><span id="sessionUser">Account</span><button id="logoutButton" type="button">Sign out</button></div>
        </div>
      </header>
      <nav class="main-nav" aria-label="Main navigation">
        <div class="nav-inner">${pages.map(([key, href, label]) => `<a href="${href}" class="${activePage === key ? "active" : ""} ${["accounts", "audit"].includes(key) ? "admin-only" : ""}">${label}</a>`).join("")}</div>
      </nav>`;

    if (!$(".app-footer")) {
      document.body.insertAdjacentHTML(
        "beforeend",
        `<footer class="app-footer">
          <span class="footer-line"></span>
          <div class="footer-credit">
            <span>Developed and Copyright &copy; ${new Date().getFullYear()} by</span>
            <strong>SAJIB AHMED</strong>
          </div>
          <span class="footer-line"></span>
        </footer>`,
      );
    }

    notifications = window.LibraryNotifications?.create({ $, escapeHtml, toast });
    api("/auth/session")
      .then((session) => {
        $("#sessionUser").textContent = `${session.username} - ${session.user_type}`;
        notifications?.setSession(session);
        if (session.user_type === "STUDENT") {
          $(".nav-inner").innerHTML = '<a href="/student" class="active">My dashboard</a>';
        }
        if (session.user_type === "ADMIN")
          $$(".admin-only").forEach((link) => link.classList.add("visible"));
      })
      .catch((error) => toast(error.message, true));

    $("#logoutButton").onclick = async () => {
      $("#logoutButton").disabled = true;
      try {
        await api("/auth/logout", { method: "POST" });
      } finally {
        window.location.replace("/login");
      }
    };
  }

  function setConnection(online) {
    $("#dbDot")?.classList.toggle("online", online);
    const label = $("#dbText");
    if (label) label.textContent = online ? "Oracle XE connected" : "Database unavailable";
  }

  async function loadData(render) {
    activeRender = render;
    if (loadingData) return loadingData;
    loadingData = (async () => {
      try {
        // One database connection supplies the complete page dataset.
        let snapshot;
        if (snapshotSupported) {
          try {
            snapshot = await api("/snapshot");
          } catch (error) {
            if (error.status !== 404) throw error;
            // A server started before this update still exposes the individual routes.
            snapshotSupported = false;
          }
        }
        if (!snapshotSupported) {
          snapshot = {};
          for (const resource of ["books", "students", "issues", "fines", "meta"]) {
            snapshot[resource] = await api(`/${resource}`);
          }
        }
        Object.assign(state, snapshot, { online: true });
        lastDataRefresh = Date.now();
        notifications?.update(state, true);
        setConnection(true);
      } catch (error) {
        state.online = false;
        notifications?.update(state, false);
        setConnection(false);
        toast(`${error.message}. Retrying the connection automatically.`, true);
      }
      await activeRender();
      startConnectionMonitor();
      return state.online;
    })();
    try {
      return await loadingData;
    } finally {
      loadingData = null;
    }
  }

  function startConnectionMonitor() {
    if (connectionTimer) return;

    connectionTimer = window.setInterval(async () => {
      if (checkingConnection || loadingData || document.hidden) return;
      checkingConnection = true;
      const wasOnline = state.online;

      try {
        if (wasOnline && activeRender && Date.now() - lastDataRefresh >= 30000) {
          await loadData(activeRender);
          return;
        }
        await api("/health");
        if (!wasOnline && activeRender) {
          const reconnected = await loadData(activeRender);
          if (reconnected) toast("Oracle XE reconnected. Live data restored.");
        }
      } catch (error) {
        if (wasOnline) {
          state.online = false;
          notifications?.update(state, false);
          setConnection(false);
          toast("Oracle connection lost. Retrying automatically.", true);
        }
      } finally {
        checkingConnection = false;
      }
    }, 5000);
    window.addEventListener("online", () => {
      if (activeRender) loadData(activeRender);
    });
    document.addEventListener("visibilitychange", () => {
      if (!document.hidden && !state.online && activeRender) loadData(activeRender);
    });
  }

  function sortIssues(items) {
    const today = dateFromToday(0);
    const soon = dateFromToday(3);
    const priority = (issue) => {
      if (issue.status !== "ISSUED") return 3;
      if (Number(issue.overdue_days) > 0 || (issue.due_date && issue.due_date < today)) return 0;
      if (issue.due_date && issue.due_date <= soon) return 1;
      return 2;
    };
    return [...items].sort((first, second) => {
      const urgency = priority(first) - priority(second);
      if (urgency) return urgency;
      if (first.status === "ISSUED") {
        const deadline = String(first.due_date || "9999-12-31").localeCompare(
          String(second.due_date || "9999-12-31"),
        );
        if (deadline) return deadline;
        const overdue = Number(second.overdue_days || 0) - Number(first.overdue_days || 0);
        if (overdue) return overdue;
      }
      const order = String(second.issue_date || "").localeCompare(String(first.issue_date || ""));
      return order || Number(second.issue_id) - Number(first.issue_id);
    });
  }

  function issueRows(items, actions = false) {
    return table(
      ["Member", "Book", "Issue date", "Due date", "Status", ...(actions ? ["Action"] : [])],
      items.map((issue) => {
        const overdue = issue.status === "ISSUED" && issue.due_date < dateFromToday(0);
        const status = overdue ? "OVERDUE" : issue.status;
        const action =
          actions && issue.status === "ISSUED"
            ? `<button class="button small primary" data-return="${issue.issue_id}">Return</button>`
            : "";
        return `<tr><td>${escapeHtml(issue.student)}</td><td><b>${escapeHtml(issue.title)}</b><small class="audit-record-id">${issue.copy_no ? `Copy #${issue.copy_no}` : "Legacy copy"}</small></td><td>${escapeHtml(issue.issue_date)}</td><td>${escapeHtml(issue.due_date || "-")}</td><td><span class="pill ${status.toLowerCase()}">${status}</span></td>${actions ? `<td>${action}</td>` : ""}</tr>`;
      }),
    );
  }

  function openModal(id) {
    const modal = $(`#${id}`);
    if (!modal) return;
    modal.returnFocus = document.activeElement;
    modal.setAttribute("role", "dialog");
    modal.setAttribute("aria-modal", "true");
    modal.classList.add("open");
    modal.setAttribute("aria-hidden", "false");
    $("input:not([type='hidden']), select, button", modal)?.focus();
  }

  function closeModal(modal) {
    modal.classList.remove("open");
    modal.setAttribute("aria-hidden", "true");
    $("form", modal)?.reset();
    modal.returnFocus?.focus();
  }

  function bindModals() {
    $$("[data-open]").forEach((button) => {
      button.onclick = () => openModal(button.dataset.open);
    });
    $$(".modal .cancel").forEach((button) => {
      button.onclick = () => closeModal(button.closest(".modal"));
    });
    $$(".modal").forEach((modal) => {
      modal.onclick = (event) => {
        if (event.target === modal) closeModal(modal);
      };
    });
    document.addEventListener("keydown", (event) => {
      const modal = $(".modal.open");
      if (!modal) return;
      if (event.key === "Escape") closeModal(modal);
      if (event.key !== "Tab") return;
      const controls = $$("input:not([type='hidden']), select, button, a[href]", modal).filter(
        (element) => !element.disabled,
      );
      const first = controls[0],
        last = controls.at(-1);
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last?.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first?.focus();
      }
    });
  }

  async function postForm(form, path) {
    if (!state.online) {
      toast("Connect to the database before saving changes", true);
      return false;
    }
    const button = $("button:not([type='button'])", form);
    try {
      button.disabled = true;
      await api(path, { method: "POST", body: new URLSearchParams(new FormData(form)) });
      closeModal(form.closest(".modal"));
      toast("Saved successfully");
      return true;
    } catch (error) {
      toast(error.message, true);
      return false;
    } finally {
      button.disabled = false;
    }
  }

  function openRequestedModal(id) {
    const query = new URLSearchParams(location.search);
    if (query.get("new") !== "1") return;
    openModal(id);
    query.delete("new");
    history.replaceState(
      null,
      "",
      `${location.pathname}${query.size ? `?${query}` : ""}${location.hash}`,
    );
  }

  $("#toast")?.setAttribute("role", "status");
  $("#toast")?.setAttribute("aria-live", "polite");
  renderHeader();
  bindModals();

  return {
    $,
    $$,
    state,
    api,
    escapeHtml,
    memberId,
    table,
    toast,
    loadData,
    sortIssues,
    issueRows,
    dateFromToday,
    openModal,
    closeModal,
    postForm,
    openRequestedModal,
    updateNotifications: (data, online) => notifications?.update(data, online),
  };
})();
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>const LibraryApp = (() =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 2 | <code>  const $ = (selector, root = document) =&gt; root.querySelector(selector);</code> | Local state, DOM reference বা callback/result assign করে। |
| 3 | <code>  const $$ = (selector, root = document) =&gt; [...root.querySelectorAll(selector)];</code> | Local state, DOM reference বা callback/result assign করে। |
| 4 | <code>  const day = 24 * 60 * 60 * 1000;</code> | Local state, DOM reference বা callback/result assign করে। |
| 5 | <code>  const dateFromToday = (offset) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 6 | <code>    new Intl.DateTimeFormat(&quot;en-CA&quot;, {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 7 | <code>      timeZone: &quot;Asia/Dhaka&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 8 | <code>      year: &quot;numeric&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 9 | <code>      month: &quot;2-digit&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 10 | <code>      day: &quot;2-digit&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 11 | <code>    }).format(new Date(Date.now() + offset * day));</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 12 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 13 | <code>  const state = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 14 | <code>    books: [],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 15 | <code>    students: [],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 16 | <code>    issues: [],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 17 | <code>    fines: [],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 18 | <code>    meta: { authors: [], categories: [] },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 19 | <code>    online: false,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 20 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 21 | <code>  let activeRender = null;</code> | Local state, DOM reference বা callback/result assign করে। |
| 22 | <code>  let connectionTimer = null;</code> | Local state, DOM reference বা callback/result assign করে। |
| 23 | <code>  let checkingConnection = false;</code> | Local state, DOM reference বা callback/result assign করে। |
| 24 | <code>  let loadingData = null;</code> | Local state, DOM reference বা callback/result assign করে। |
| 25 | <code>  let snapshotSupported = true;</code> | Local state, DOM reference বা callback/result assign করে। |
| 26 | <code>  let notifications = null;</code> | Local state, DOM reference বা callback/result assign করে। |
| 27 | <code>  let lastDataRefresh = 0;</code> | Local state, DOM reference বা callback/result assign করে। |
| 28 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 29 | <code>  async function api(path, options = {}) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 30 | <code>    const readOnly = !options.method &#124;&#124; options.method.toUpperCase() === &quot;GET&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 31 | <code>    for (let attempt = 0; attempt &lt; (readOnly ? 2 : 1); attempt++) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 32 | <code>      try {</code> | Async failure handling ও UI cleanup/restore block। |
| 33 | <code>        const response = await fetch(`/api${path}`, {</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 34 | <code>          ...options,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 35 | <code>          cache: &quot;no-store&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 36 | <code>          signal: options.signal &#124;&#124; AbortSignal.timeout(60000),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 37 | <code>        });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 38 | <code>        if (response.status === 401) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 39 | <code>          window.location.replace(&quot;/login&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 40 | <code>          throw new Error(&quot;Your session has expired. Please sign in again&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 41 | <code>        }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 42 | <code>        if (readOnly &amp;&amp; attempt === 0 &amp;&amp; [503, 504].includes(response.status)) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 43 | <code>          await new Promise((resolve) =&gt; setTimeout(resolve, 400));</code> | Timeout/reconnection/search debounce timer শুরু বা বন্ধ করে। |
| 44 | <code>          continue;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 45 | <code>        }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 46 | <code>        const data = await response.json();</code> | Local state, DOM reference বা callback/result assign করে। |
| 47 | <code>        if (!response.ok) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 48 | <code>          const error = new Error(</code> | Local state, DOM reference বা callback/result assign করে। |
| 49 | <code>            typeof data.detail === &quot;string&quot; ? data.detail : data.error &#124;&#124; &quot;Request failed&quot;,</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 50 | <code>          );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 51 | <code>          error.status = response.status;</code> | Local state, DOM reference বা callback/result assign করে। |
| 52 | <code>          throw error;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 53 | <code>        }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 54 | <code>        return data;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 55 | <code>      } catch (error) {</code> | Async failure handling ও UI cleanup/restore block। |
| 56 | <code>        if (readOnly &amp;&amp; attempt === 0 &amp;&amp; error instanceof TypeError &amp;&amp; !options.signal?.aborted) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 57 | <code>          await new Promise((resolve) =&gt; setTimeout(resolve, 400));</code> | Timeout/reconnection/search debounce timer শুরু বা বন্ধ করে। |
| 58 | <code>          continue;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 59 | <code>        }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 60 | <code>        throw error;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 61 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 62 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 63 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 64 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 65 | <code>  function escapeHtml(value) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 66 | <code>    return String(value ?? &quot;&quot;).replace(</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 67 | <code>      /[&amp;&lt;&gt;&quot;&#x27;]/g,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 68 | <code>      (character) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 69 | <code>        ({</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 70 | <code>          &quot;&amp;&quot;: &quot;&amp;amp;&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 71 | <code>          &quot;&lt;&quot;: &quot;&amp;lt;&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 72 | <code>          &quot;&gt;&quot;: &quot;&amp;gt;&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 73 | <code>          &#x27;&quot;&#x27;: &quot;&amp;quot;&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 74 | <code>          &quot;&#x27;&quot;: &quot;&amp;#39;&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 75 | <code>        })[character],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 76 | <code>    );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 77 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 78 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 79 | <code>  function memberId(id) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 80 | <code>    return `PSTU-${String(id).padStart(4, &quot;0&quot;)}`;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 81 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 82 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 83 | <code>  function table(headers, rows) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 84 | <code>    if (!rows.length)</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 85 | <code>      return &#x27;&lt;div class=&quot;empty-state&quot;&gt;&lt;strong&gt;No records found&lt;/strong&gt;&lt;span&gt;Try another search or add a new record.&lt;/span&gt;&lt;/div&gt;&#x27;;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 86 | <code>    return `&lt;table&gt;&lt;thead&gt;&lt;tr&gt;${headers.map((header) =&gt; `&lt;th&gt;${header}&lt;/th&gt;`).join(&quot;&quot;)}&lt;/tr&gt;&lt;/thead&gt;&lt;tbody&gt;${rows.join(&quot;&quot;)}&lt;/tbody&gt;&lt;/table&gt;`;</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 87 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 88 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 89 | <code>  function toast(message, error = false) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 90 | <code>    const element = $(&quot;#toast&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 91 | <code>    if (!element) return;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 92 | <code>    element.textContent = message;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 93 | <code>    element.className = error ? &quot;show error&quot; : &quot;show&quot;;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 94 | <code>    clearTimeout(element.timer);</code> | Timeout/reconnection/search debounce timer শুরু বা বন্ধ করে। |
| 95 | <code>    element.timer = setTimeout(() =&gt; {</code> | Timeout/reconnection/search debounce timer শুরু বা বন্ধ করে। |
| 96 | <code>      element.className = &quot;&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 97 | <code>    }, 2800);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 98 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 99 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 100 | <code>  function renderHeader() {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 101 | <code>    const activePage = document.body.dataset.page;</code> | Local state, DOM reference বা callback/result assign করে। |
| 102 | <code>    const pages = [</code> | Local state, DOM reference বা callback/result assign করে। |
| 103 | <code>      [&quot;overview&quot;, &quot;/&quot;, &quot;Dashboard&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 104 | <code>      [&quot;books&quot;, &quot;/books&quot;, &quot;Books&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 105 | <code>      [&quot;students&quot;, &quot;/students&quot;, &quot;Members&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 106 | <code>      [&quot;circulation&quot;, &quot;/circulation&quot;, &quot;Issue &amp; Return&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 107 | <code>      [&quot;fines&quot;, &quot;/fines&quot;, &quot;Fines&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 108 | <code>      [&quot;accounts&quot;, &quot;/accounts&quot;, &quot;Accounts&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 109 | <code>      [&quot;audit&quot;, &quot;/audit&quot;, &quot;Audit&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 110 | <code>      [&quot;reservations&quot;, &quot;/reservations&quot;, &quot;Reservations&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 111 | <code>    ];</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 112 | <code>    $(&quot;#appHeader&quot;).innerHTML = `</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 113 | <code>      &lt;header class=&quot;app-header&quot;&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 114 | <code>        &lt;div class=&quot;brand-block&quot;&gt;&lt;span class=&quot;brand-mark&quot;&gt;PSTU&lt;/span&gt;&lt;div&gt;&lt;strong&gt;Central Library&lt;/strong&gt;&lt;small&gt;Management System&lt;/small&gt;&lt;/div&gt;&lt;/div&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 115 | <code>        &lt;div class=&quot;university-name&quot;&gt;Patuakhali Science and Technology University&lt;/div&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 116 | <code>        &lt;div class=&quot;header-tools&quot;&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 117 | <code>          &lt;div class=&quot;connection&quot;&gt;&lt;i id=&quot;dbDot&quot;&gt;&lt;/i&gt;&lt;span id=&quot;dbText&quot;&gt;Connecting...&lt;/span&gt;&lt;/div&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 118 | <code>          &lt;div id=&quot;notificationCenter&quot; class=&quot;notification-center&quot;&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 119 | <code>            &lt;button id=&quot;notificationButton&quot; class=&quot;notification-button&quot; type=&quot;button&quot; aria-label=&quot;Notifications&quot; aria-expanded=&quot;false&quot; aria-controls=&quot;notificationPanel&quot;&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 120 | <code>              &lt;svg viewBox=&quot;0 0 24 24&quot; fill=&quot;none&quot; stroke=&quot;currentColor&quot; stroke-width=&quot;1.8&quot; aria-hidden=&quot;true&quot;&gt;&lt;path d=&quot;M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9M10 21h4&quot; stroke-linecap=&quot;round&quot; stroke-linejoin=&quot;round&quot;/&gt;&lt;/svg&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 121 | <code>              &lt;span id=&quot;notificationBadge&quot; class=&quot;notification-badge&quot; hidden aria-live=&quot;polite&quot;&gt;&lt;/span&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 122 | <code>            &lt;/button&gt;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 123 | <code>            &lt;section id=&quot;notificationPanel&quot; class=&quot;notification-panel&quot; aria-label=&quot;Library notifications&quot; hidden&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 124 | <code>              &lt;div class=&quot;notification-heading&quot;&gt;&lt;div&gt;&lt;h2&gt;Notifications&lt;/h2&gt;&lt;p id=&quot;notificationSummary&quot;&gt;Loading library alerts…&lt;/p&gt;&lt;/div&gt;&lt;button id=&quot;notificationClose&quot; class=&quot;notification-close&quot; type=&quot;button&quot; aria-label=&quot;Close notifications&quot;&gt;&amp;times;&lt;/button&gt;&lt;/div&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 125 | <code>              &lt;div class=&quot;notification-controls&quot;&gt;&lt;button type=&quot;button&quot; data-alert-filter=&quot;all&quot; aria-pressed=&quot;true&quot;&gt;All&lt;/button&gt;&lt;button type=&quot;button&quot; data-alert-filter=&quot;reservation&quot; aria-pressed=&quot;false&quot;&gt;Reservations&lt;/button&gt;&lt;button type=&quot;button&quot; data-alert-filter=&quot;due&quot; aria-pressed=&quot;false&quot;&gt;Due dates&lt;/button&gt;&lt;button type=&quot;button&quot; data-alert-filter=&quot;fine&quot; aria-pressed=&quot;false&quot;&gt;Fines&lt;/button&gt;&lt;button id=&quot;notificationReadAll&quot; type=&quot;button&quot;&gt;Mark all read&lt;/button&gt;&lt;/div&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 126 | <code>              &lt;div id=&quot;notificationList&quot; class=&quot;notification-list&quot;&gt;&lt;/div&gt;&lt;p id=&quot;notificationFreshness&quot; class=&quot;notification-freshness&quot;&gt;&lt;/p&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 127 | <code>            &lt;/section&gt;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 128 | <code>          &lt;/div&gt;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 129 | <code>          &lt;div class=&quot;user-menu&quot;&gt;&lt;span id=&quot;sessionUser&quot;&gt;Account&lt;/span&gt;&lt;button id=&quot;logoutButton&quot; type=&quot;button&quot;&gt;Sign out&lt;/button&gt;&lt;/div&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 130 | <code>        &lt;/div&gt;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 131 | <code>      &lt;/header&gt;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 132 | <code>      &lt;nav class=&quot;main-nav&quot; aria-label=&quot;Main navigation&quot;&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 133 | <code>        &lt;div class=&quot;nav-inner&quot;&gt;${pages.map(([key, href, label]) =&gt; `&lt;a href=&quot;${href}&quot; class=&quot;${activePage === key ? &quot;active&quot; : &quot;&quot;} ${[&quot;accounts&quot;, &quot;audit&quot;].includes(key) ? &quot;admin-only&quot; : &quot;&quot;}&quot;&gt;${label}&lt;/a&gt;`).join(&quot;&quot;)}&lt;/div&gt;</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 134 | <code>      &lt;/nav&gt;`;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 135 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 136 | <code>    if (!$(&quot;.app-footer&quot;)) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 137 | <code>      document.body.insertAdjacentHTML(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 138 | <code>        &quot;beforeend&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 139 | <code>        `&lt;footer class=&quot;app-footer&quot;&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 140 | <code>          &lt;span class=&quot;footer-line&quot;&gt;&lt;/span&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 141 | <code>          &lt;div class=&quot;footer-credit&quot;&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 142 | <code>            &lt;span&gt;Developed and Copyright &amp;copy; ${new Date().getFullYear()} by&lt;/span&gt;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 143 | <code>            &lt;strong&gt;SAJIB AHMED&lt;/strong&gt;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 144 | <code>          &lt;/div&gt;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 145 | <code>          &lt;span class=&quot;footer-line&quot;&gt;&lt;/span&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 146 | <code>        &lt;/footer&gt;`,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 147 | <code>      );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 148 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 149 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 150 | <code>    notifications = window.LibraryNotifications?.create({ $, escapeHtml, toast });</code> | Local state, DOM reference বা callback/result assign করে। |
| 151 | <code>    api(&quot;/auth/session&quot;)</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 152 | <code>      .then((session) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 153 | <code>        $(&quot;#sessionUser&quot;).textContent = `${session.username} - ${session.user_type}`;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 154 | <code>        notifications?.setSession(session);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 155 | <code>        if (session.user_type === &quot;STUDENT&quot;) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 156 | <code>          $(&quot;.nav-inner&quot;).innerHTML = &#x27;&lt;a href=&quot;/student&quot; class=&quot;active&quot;&gt;My dashboard&lt;/a&gt;&#x27;;</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 157 | <code>        }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 158 | <code>        if (session.user_type === &quot;ADMIN&quot;)</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 159 | <code>          $$(&quot;.admin-only&quot;).forEach((link) =&gt; link.classList.add(&quot;visible&quot;));</code> | Local state, DOM reference বা callback/result assign করে। |
| 160 | <code>      })</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 161 | <code>      .catch((error) =&gt; toast(error.message, true));</code> | Async failure handling ও UI cleanup/restore block। |
| 162 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 163 | <code>    $(&quot;#logoutButton&quot;).onclick = async () =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 164 | <code>      $(&quot;#logoutButton&quot;).disabled = true;</code> | Local state, DOM reference বা callback/result assign করে। |
| 165 | <code>      try {</code> | Async failure handling ও UI cleanup/restore block। |
| 166 | <code>        await api(&quot;/auth/logout&quot;, { method: &quot;POST&quot; });</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 167 | <code>      } finally {</code> | Async failure handling ও UI cleanup/restore block। |
| 168 | <code>        window.location.replace(&quot;/login&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 169 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 170 | <code>    };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 171 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 172 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 173 | <code>  function setConnection(online) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 174 | <code>    $(&quot;#dbDot&quot;)?.classList.toggle(&quot;online&quot;, online);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 175 | <code>    const label = $(&quot;#dbText&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 176 | <code>    if (label) label.textContent = online ? &quot;Oracle XE connected&quot; : &quot;Database unavailable&quot;;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 177 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 178 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 179 | <code>  async function loadData(render) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 180 | <code>    activeRender = render;</code> | Local state, DOM reference বা callback/result assign করে। |
| 181 | <code>    if (loadingData) return loadingData;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 182 | <code>    loadingData = (async () =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 183 | <code>      try {</code> | Async failure handling ও UI cleanup/restore block। |
| 184 | <code>        // One database connection supplies the complete page dataset.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 185 | <code>        let snapshot;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 186 | <code>        if (snapshotSupported) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 187 | <code>          try {</code> | Async failure handling ও UI cleanup/restore block। |
| 188 | <code>            snapshot = await api(&quot;/snapshot&quot;);</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 189 | <code>          } catch (error) {</code> | Async failure handling ও UI cleanup/restore block। |
| 190 | <code>            if (error.status !== 404) throw error;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 191 | <code>            // A server started before this update still exposes the individual routes.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 192 | <code>            snapshotSupported = false;</code> | Local state, DOM reference বা callback/result assign করে। |
| 193 | <code>          }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 194 | <code>        }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 195 | <code>        if (!snapshotSupported) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 196 | <code>          snapshot = {};</code> | Local state, DOM reference বা callback/result assign করে। |
| 197 | <code>          for (const resource of [&quot;books&quot;, &quot;students&quot;, &quot;issues&quot;, &quot;fines&quot;, &quot;meta&quot;]) {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 198 | <code>            snapshot[resource] = await api(`/${resource}`);</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 199 | <code>          }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 200 | <code>        }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 201 | <code>        Object.assign(state, snapshot, { online: true });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 202 | <code>        lastDataRefresh = Date.now();</code> | Local state, DOM reference বা callback/result assign করে। |
| 203 | <code>        notifications?.update(state, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 204 | <code>        setConnection(true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 205 | <code>      } catch (error) {</code> | Async failure handling ও UI cleanup/restore block। |
| 206 | <code>        state.online = false;</code> | Local state, DOM reference বা callback/result assign করে। |
| 207 | <code>        notifications?.update(state, false);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 208 | <code>        setConnection(false);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 209 | <code>        toast(`${error.message}. Retrying the connection automatically.`, true);</code> | Async failure handling ও UI cleanup/restore block। |
| 210 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 211 | <code>      await activeRender();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 212 | <code>      startConnectionMonitor();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 213 | <code>      return state.online;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 214 | <code>    })();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 215 | <code>    try {</code> | Async failure handling ও UI cleanup/restore block। |
| 216 | <code>      return await loadingData;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 217 | <code>    } finally {</code> | Async failure handling ও UI cleanup/restore block। |
| 218 | <code>      loadingData = null;</code> | Local state, DOM reference বা callback/result assign করে। |
| 219 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 220 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 221 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 222 | <code>  function startConnectionMonitor() {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 223 | <code>    if (connectionTimer) return;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 224 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 225 | <code>    connectionTimer = window.setInterval(async () =&gt; {</code> | Timeout/reconnection/search debounce timer শুরু বা বন্ধ করে। |
| 226 | <code>      if (checkingConnection &#124;&#124; loadingData &#124;&#124; document.hidden) return;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 227 | <code>      checkingConnection = true;</code> | Local state, DOM reference বা callback/result assign করে। |
| 228 | <code>      const wasOnline = state.online;</code> | Local state, DOM reference বা callback/result assign করে। |
| 229 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 230 | <code>      try {</code> | Async failure handling ও UI cleanup/restore block। |
| 231 | <code>        if (wasOnline &amp;&amp; activeRender &amp;&amp; Date.now() - lastDataRefresh &gt;= 30000) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 232 | <code>          await loadData(activeRender);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 233 | <code>          return;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 234 | <code>        }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 235 | <code>        await api(&quot;/health&quot;);</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 236 | <code>        if (!wasOnline &amp;&amp; activeRender) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 237 | <code>          const reconnected = await loadData(activeRender);</code> | Local state, DOM reference বা callback/result assign করে। |
| 238 | <code>          if (reconnected) toast(&quot;Oracle XE reconnected. Live data restored.&quot;);</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 239 | <code>        }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 240 | <code>      } catch (error) {</code> | Async failure handling ও UI cleanup/restore block। |
| 241 | <code>        if (wasOnline) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 242 | <code>          state.online = false;</code> | Local state, DOM reference বা callback/result assign করে। |
| 243 | <code>          notifications?.update(state, false);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 244 | <code>          setConnection(false);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 245 | <code>          toast(&quot;Oracle connection lost. Retrying automatically.&quot;, true);</code> | Async failure handling ও UI cleanup/restore block। |
| 246 | <code>        }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 247 | <code>      } finally {</code> | Async failure handling ও UI cleanup/restore block। |
| 248 | <code>        checkingConnection = false;</code> | Local state, DOM reference বা callback/result assign করে। |
| 249 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 250 | <code>    }, 5000);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 251 | <code>    window.addEventListener(&quot;online&quot;, () =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 252 | <code>      if (activeRender) loadData(activeRender);</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 253 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 254 | <code>    document.addEventListener(&quot;visibilitychange&quot;, () =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 255 | <code>      if (!document.hidden &amp;&amp; !state.online &amp;&amp; activeRender) loadData(activeRender);</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 256 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 257 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 258 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 259 | <code>  function sortIssues(items) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 260 | <code>    const today = dateFromToday(0);</code> | Local state, DOM reference বা callback/result assign করে। |
| 261 | <code>    const soon = dateFromToday(3);</code> | Local state, DOM reference বা callback/result assign করে। |
| 262 | <code>    const priority = (issue) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 263 | <code>      if (issue.status !== &quot;ISSUED&quot;) return 3;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 264 | <code>      if (Number(issue.overdue_days) &gt; 0 &#124;&#124; (issue.due_date &amp;&amp; issue.due_date &lt; today)) return 0;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 265 | <code>      if (issue.due_date &amp;&amp; issue.due_date &lt;= soon) return 1;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 266 | <code>      return 2;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 267 | <code>    };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 268 | <code>    return [...items].sort((first, second) =&gt; {</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 269 | <code>      const urgency = priority(first) - priority(second);</code> | Local state, DOM reference বা callback/result assign করে। |
| 270 | <code>      if (urgency) return urgency;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 271 | <code>      if (first.status === &quot;ISSUED&quot;) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 272 | <code>        const deadline = String(first.due_date &#124;&#124; &quot;9999-12-31&quot;).localeCompare(</code> | Local state, DOM reference বা callback/result assign করে। |
| 273 | <code>          String(second.due_date &#124;&#124; &quot;9999-12-31&quot;),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 274 | <code>        );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 275 | <code>        if (deadline) return deadline;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 276 | <code>        const overdue = Number(second.overdue_days &#124;&#124; 0) - Number(first.overdue_days &#124;&#124; 0);</code> | Local state, DOM reference বা callback/result assign করে। |
| 277 | <code>        if (overdue) return overdue;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 278 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 279 | <code>      const order = String(second.issue_date &#124;&#124; &quot;&quot;).localeCompare(String(first.issue_date &#124;&#124; &quot;&quot;));</code> | Local state, DOM reference বা callback/result assign করে। |
| 280 | <code>      return order &#124;&#124; Number(second.issue_id) - Number(first.issue_id);</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 281 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 282 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 283 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 284 | <code>  function issueRows(items, actions = false) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 285 | <code>    return table(</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 286 | <code>      [&quot;Member&quot;, &quot;Book&quot;, &quot;Issue date&quot;, &quot;Due date&quot;, &quot;Status&quot;, ...(actions ? [&quot;Action&quot;] : [])],</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 287 | <code>      items.map((issue) =&gt; {</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 288 | <code>        const overdue = issue.status === &quot;ISSUED&quot; &amp;&amp; issue.due_date &lt; dateFromToday(0);</code> | Local state, DOM reference বা callback/result assign করে। |
| 289 | <code>        const status = overdue ? &quot;OVERDUE&quot; : issue.status;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 290 | <code>        const action =</code> | Local state, DOM reference বা callback/result assign করে। |
| 291 | <code>          actions &amp;&amp; issue.status === &quot;ISSUED&quot;</code> | Local state, DOM reference বা callback/result assign করে। |
| 292 | <code>            ? `&lt;button class=&quot;button small primary&quot; data-return=&quot;${issue.issue_id}&quot;&gt;Return&lt;/button&gt;`</code> | Local state, DOM reference বা callback/result assign করে। |
| 293 | <code>            : &quot;&quot;;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 294 | <code>        return `&lt;tr&gt;&lt;td&gt;${escapeHtml(issue.student)}&lt;/td&gt;&lt;td&gt;&lt;b&gt;${escapeHtml(issue.title)}&lt;/b&gt;&lt;small class=&quot;audit-record-id&quot;&gt;${issue.copy_no ? `Copy #${issue.copy_no}` : &quot;Legacy copy&quot;}&lt;/small&gt;&lt;/td&gt;&lt;td&gt;${escapeHtml(issue.issue_date)}&lt;/td&gt;&lt;td&gt;${escapeHtml(issue.due_date &#124;&#124; &quot;-&quot;)}&lt;/td&gt;&lt;td&gt;&lt;span class=&quot;pill ${status.toLowerCase()}&quot;&gt;${status}&lt;/span&gt;&lt;/td&gt;${actions ? `&lt;td&gt;${action}&lt;/td&gt;` : &quot;&quot;}&lt;/tr&gt;`;</code> | User/database values escaped display markup-এ রূপান্তর করে। |
| 295 | <code>      }),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 296 | <code>    );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 297 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 298 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 299 | <code>  function openModal(id) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 300 | <code>    const modal = $(`#${id}`);</code> | Local state, DOM reference বা callback/result assign করে। |
| 301 | <code>    if (!modal) return;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 302 | <code>    modal.returnFocus = document.activeElement;</code> | Local state, DOM reference বা callback/result assign করে। |
| 303 | <code>    modal.setAttribute(&quot;role&quot;, &quot;dialog&quot;);</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 304 | <code>    modal.setAttribute(&quot;aria-modal&quot;, &quot;true&quot;);</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 305 | <code>    modal.classList.add(&quot;open&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 306 | <code>    modal.setAttribute(&quot;aria-hidden&quot;, &quot;false&quot;);</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 307 | <code>    $(&quot;input:not([type=&#x27;hidden&#x27;]), select, button&quot;, modal)?.focus();</code> | Local state, DOM reference বা callback/result assign করে। |
| 308 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 309 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 310 | <code>  function closeModal(modal) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 311 | <code>    modal.classList.remove(&quot;open&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 312 | <code>    modal.setAttribute(&quot;aria-hidden&quot;, &quot;true&quot;);</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 313 | <code>    $(&quot;form&quot;, modal)?.reset();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 314 | <code>    modal.returnFocus?.focus();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 315 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 316 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 317 | <code>  function bindModals() {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 318 | <code>    $$(&quot;[data-open]&quot;).forEach((button) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 319 | <code>      button.onclick = () =&gt; openModal(button.dataset.open);</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 320 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 321 | <code>    $$(&quot;.modal .cancel&quot;).forEach((button) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 322 | <code>      button.onclick = () =&gt; closeModal(button.closest(&quot;.modal&quot;));</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 323 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 324 | <code>    $$(&quot;.modal&quot;).forEach((modal) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 325 | <code>      modal.onclick = (event) =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 326 | <code>        if (event.target === modal) closeModal(modal);</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 327 | <code>      };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 328 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 329 | <code>    document.addEventListener(&quot;keydown&quot;, (event) =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 330 | <code>      const modal = $(&quot;.modal.open&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 331 | <code>      if (!modal) return;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 332 | <code>      if (event.key === &quot;Escape&quot;) closeModal(modal);</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 333 | <code>      if (event.key !== &quot;Tab&quot;) return;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 334 | <code>      const controls = $$(&quot;input:not([type=&#x27;hidden&#x27;]), select, button, a[href]&quot;, modal).filter(</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 335 | <code>        (element) =&gt; !element.disabled,</code> | Local state, DOM reference বা callback/result assign করে। |
| 336 | <code>      );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 337 | <code>      const first = controls[0],</code> | Local state, DOM reference বা callback/result assign করে। |
| 338 | <code>        last = controls.at(-1);</code> | Local state, DOM reference বা callback/result assign করে। |
| 339 | <code>      if (event.shiftKey &amp;&amp; document.activeElement === first) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 340 | <code>        event.preventDefault();</code> | Default form navigation বন্ধ করে controlled API submission চালাতে দেয়। |
| 341 | <code>        last?.focus();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 342 | <code>      } else if (!event.shiftKey &amp;&amp; document.activeElement === last) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 343 | <code>        event.preventDefault();</code> | Default form navigation বন্ধ করে controlled API submission চালাতে দেয়। |
| 344 | <code>        first?.focus();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 345 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 346 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 347 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 348 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 349 | <code>  async function postForm(form, path) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 350 | <code>    if (!state.online) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 351 | <code>      toast(&quot;Connect to the database before saving changes&quot;, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 352 | <code>      return false;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 353 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 354 | <code>    const button = $(&quot;button:not([type=&#x27;button&#x27;])&quot;, form);</code> | Local state, DOM reference বা callback/result assign করে। |
| 355 | <code>    try {</code> | Async failure handling ও UI cleanup/restore block। |
| 356 | <code>      button.disabled = true;</code> | Local state, DOM reference বা callback/result assign করে। |
| 357 | <code>      await api(path, { method: &quot;POST&quot;, body: new URLSearchParams(new FormData(form)) });</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 358 | <code>      closeModal(form.closest(&quot;.modal&quot;));</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 359 | <code>      toast(&quot;Saved successfully&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 360 | <code>      return true;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 361 | <code>    } catch (error) {</code> | Async failure handling ও UI cleanup/restore block। |
| 362 | <code>      toast(error.message, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 363 | <code>      return false;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 364 | <code>    } finally {</code> | Async failure handling ও UI cleanup/restore block। |
| 365 | <code>      button.disabled = false;</code> | Local state, DOM reference বা callback/result assign করে। |
| 366 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 367 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 368 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 369 | <code>  function openRequestedModal(id) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 370 | <code>    const query = new URLSearchParams(location.search);</code> | Form fields বা filters URL-encoded request body/query parameters-এ রূপান্তর করে। |
| 371 | <code>    if (query.get(&quot;new&quot;) !== &quot;1&quot;) return;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 372 | <code>    openModal(id);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 373 | <code>    query.delete(&quot;new&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 374 | <code>    history.replaceState(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 375 | <code>      null,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 376 | <code>      &quot;&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 377 | <code>      `${location.pathname}${query.size ? `?${query}` : &quot;&quot;}${location.hash}`,</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 378 | <code>    );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 379 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 380 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 381 | <code>  $(&quot;#toast&quot;)?.setAttribute(&quot;role&quot;, &quot;status&quot;);</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 382 | <code>  $(&quot;#toast&quot;)?.setAttribute(&quot;aria-live&quot;, &quot;polite&quot;);</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 383 | <code>  renderHeader();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 384 | <code>  bindModals();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 385 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 386 | <code>  return {</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 387 | <code>    $,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 388 | <code>    $$,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 389 | <code>    state,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 390 | <code>    api,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 391 | <code>    escapeHtml,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 392 | <code>    memberId,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 393 | <code>    table,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 394 | <code>    toast,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 395 | <code>    loadData,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 396 | <code>    sortIssues,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 397 | <code>    issueRows,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 398 | <code>    dateFromToday,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 399 | <code>    openModal,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 400 | <code>    closeModal,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 401 | <code>    postForm,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 402 | <code>    openRequestedModal,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 403 | <code>    updateNotifications: (data, online) =&gt; notifications?.update(data, online),</code> | Local state, DOM reference বা callback/result assign করে। |
| 404 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 405 | <code>})();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
