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
