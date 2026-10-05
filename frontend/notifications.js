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
