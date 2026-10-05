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
