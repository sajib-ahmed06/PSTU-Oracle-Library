(() => {
  const { $, $$, api, escapeHtml, table, toast, loadData, openModal } = LibraryApp;
  const entities = {
    STUDENT: "Member",
    BOOK: "Book",
    AUTHOR: "Author",
    CATEGORY: "Category",
    ISSUE_BOOK: "Loan",
    RETURN_BOOK: "Return",
    FINE: "Fine",
    LOGIN_USER: "Account",
    ADMIN: "Admin profile",
  };
  const actions = {
    INSERT: "Created",
    UPDATE: "Updated",
    DELETE: "Deleted",
    SNAPSHOT: "Initial snapshot",
  };
  let page = 1;
  let records = [];
  let requestNumber = 0;
  let searchTimer;
  const formatTime = (value) =>
    new Date(value).toLocaleString("en-GB", { timeZone: "Asia/Dhaka", hour12: true });
  const label = (key) =>
    ({ roll_no: "ID / Roll", registration_no: "Registration No." })[key] ||
    key.replaceAll("_", " ");

  async function loadAudit() {
    const currentRequest = ++requestNumber;
    $("#auditTable").setAttribute("aria-busy", "true");
    $("#auditPrevious").disabled = true;
    $("#auditNext").disabled = true;
    const query = new URLSearchParams({
      page,
      q: $("#auditSearch").value.trim(),
      entity: $("#auditEntity").value,
      action: $("#auditAction").value,
    });
    try {
      const result = await api(`/audit?${query}`);
      if (currentRequest !== requestNumber) return;
      records = result.items;
      const pages = Math.max(1, Math.ceil(result.total / result.page_size));
      $("#auditCount").textContent =
        `${result.total} events | Page ${page} of ${pages} | Asia/Dhaka`;
      $("#auditTable").innerHTML = records.length
        ? table(
            ["Time", "Changed by", "Action", "Record type", "Record", "Details"],
            records.map((record) => {
              const details = record.after || record.before || {};
              const name =
                details.name ||
                details.title ||
                details.username ||
                details.author_name ||
                details.category_name ||
                `#${record.record_id}`;
              return `<tr><td>${escapeHtml(formatTime(record.occurred_at))}</td><td>${escapeHtml(record.actor)}</td><td>${escapeHtml(actions[record.action] || record.action)}</td><td>${escapeHtml(entities[record.entity] || record.entity)}</td><td><b>${escapeHtml(name)}</b><small class="audit-record-id">Record #${record.record_id}</small></td><td><button class="button small secondary" data-audit="${record.audit_id}">View details</button></td></tr>`;
            }),
          )
        : '<div class="empty-state"><strong>No audit events found</strong><span>Try another search or filter.</span></div>';
      $$("[data-audit]").forEach((button) => {
        button.onclick = () => showDetails(button.dataset.audit);
      });
      $("#auditPrevious").disabled = page <= 1;
      $("#auditNext").disabled = page >= pages;
    } catch (error) {
      if (currentRequest === requestNumber) toast(error.message, true);
    } finally {
      if (currentRequest === requestNumber) $("#auditTable").setAttribute("aria-busy", "false");
    }
  }

  function showDetails(id) {
    const record = records.find((item) => item.audit_id == id);
    if (!record) return;
    $("#auditDetailTitle").textContent =
      `${entities[record.entity]} #${record.record_id} | ${actions[record.action]}`;
    $("#auditDetailMeta").textContent =
      `${record.actor} | ${formatTime(record.occurred_at)} (Asia/Dhaka)`;
    const keys = [
      ...new Set([...Object.keys(record.before || {}), ...Object.keys(record.after || {})]),
    ];
    $("#auditValues").innerHTML = table(
      ["Field", "Before", "After"],
      keys.map((key) => {
        const before = record.before?.[key],
          after = record.after?.[key];
        const changed = record.before && record.after && before !== after;
        return `<tr class="${changed ? "audit-changed" : ""}"><td>${escapeHtml(label(key))}${changed ? ' <span class="pill">Changed</span>' : ""}</td><td>${escapeHtml(before ?? "-")}</td><td>${escapeHtml(after ?? "-")}</td></tr>`;
      }),
    );
    openModal("auditDetail");
  }

  $("#auditSearch").oninput = () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      page = 1;
      loadAudit();
    }, 300);
  };
  ["#auditEntity", "#auditAction"].forEach((selector) => {
    $(selector).onchange = () => {
      page = 1;
      loadAudit();
    };
  });
  $("#auditPrevious").onclick = () => {
    if (page > 1) {
      page--;
      loadAudit();
    }
  };
  $("#auditNext").onclick = () => {
    page++;
    loadAudit();
  };
  $("#refreshAudit").onclick = () => loadData(loadAudit);
  loadData(loadAudit);
})();
