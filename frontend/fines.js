(() => {
  const { $, $$, state, escapeHtml, memberId, table, toast, api, loadData, openModal, closeModal } =
    LibraryApp;
  const money = (value) => `Tk ${Number(value).toLocaleString("en-BD")}`;
  const cents = (value) => Math.round(Number(value || 0) * 100);
  const balance = (fine) =>
    fine.balance ??
    (fine.payment_status === "PAID" ? 0 : Number(fine.amount) - Number(fine.paid_amount || 0));
  const copyLabel = (issue) => (issue?.copy_no ? `Copy #${issue.copy_no}` : "Legacy copy");

  function memberCell(id, name) {
    const member = state.students.find((student) => student.student_id === id);
    return `<td><span class="member-id">${memberId(id)}</span></td><td><b>${escapeHtml(name)}</b><small class="audit-record-id">Roll: ${escapeHtml(member?.roll_no || "Not assigned")} / Reg: ${escapeHtml(member?.registration_no || "Not assigned")}</small></td>`;
  }

  async function render() {
    const overdue = state.issues
      .filter((issue) => issue.status === "ISSUED" && Number(issue.overdue_days) > 0)
      .sort(
        (a, b) =>
          Number(b.overdue_days) - Number(a.overdue_days) ||
          Number(b.current_fine || 0) - Number(a.current_fine || 0),
      );
    const unpaid = state.fines.filter((fine) => fine.payment_status === "UNPAID");
    const unpaidAmount = unpaid.reduce((sum, fine) => sum + cents(balance(fine)), 0) / 100;
    // Fines normally exist only after return; never count a recorded issue twice.
    const recordedIssues = new Set(state.fines.map((fine) => fine.issue_id));
    const overdueAmount = overdue.reduce(
      (sum, issue) => sum + (recordedIssues.has(issue.issue_id) ? 0 : Number(issue.current_fine)),
      0,
    );
    const metrics = [
      [
        "Total outstanding",
        unpaidAmount + overdueAmount,
        "Unpaid fines + overdue estimates",
        "red",
      ],
      ["Overdue fine estimate", overdueAmount, `${overdue.length} books awaiting return`, "gold"],
      ["Recorded unpaid fines", unpaidAmount, `${unpaid.length} unpaid records`, "green"],
    ];
    $("#fineSummary").innerHTML = metrics
      .map(
        ([label, amount, note, tone]) =>
          `<article class="metric ${tone}"><span>${label}</span><strong>${money(amount)}</strong><small>${note}</small></article>`,
      )
      .join("");
    $("#overdueTotal").textContent = `${overdue.length} overdue books / ${money(overdueAmount)}`;
    $("#overdueTable").innerHTML = overdue.length
      ? table(
          ["Member ID", "Student", "Book", "Due date", "Overdue days", "Fine today", "Return"],
          overdue.map(
            (issue) =>
              `<tr>${memberCell(issue.student_id, issue.student)}<td><b>${escapeHtml(issue.title)}</b><small class="audit-record-id">${copyLabel(issue)}</small></td><td>${escapeHtml(issue.due_date)}</td><td><span class="pill overdue">${issue.overdue_days} days</span></td><td><b>${money(issue.current_fine)}</b></td><td><button class="button small primary" data-fine-return="${issue.issue_id}">Return book</button></td></tr>`,
          ),
        )
      : '<div class="empty-state"><strong>No overdue books</strong><span>All current loans are within their due dates.</span></div>';
    const paidCount = state.fines.filter((fine) => fine.payment_status === "PAID").length;
    $("#fineTotal").textContent = `${state.fines.length} fine records / ${paidCount} paid`;
    $("#fineTable").innerHTML = table(
      [
        "Member ID",
        "Student",
        "Book / copy",
        "Return date",
        "Fine",
        "Received",
        "Remaining",
        "Payment",
        "Action",
      ],
      [...state.fines]
        .sort(
          (a, b) =>
            Number(balance(b) > 0) - Number(balance(a) > 0) ||
            Number(balance(b)) - Number(balance(a)) ||
            Number(b.fine_id) - Number(a.fine_id),
        )
        .map((fine) => {
          const issue = state.issues.find((item) => item.issue_id === fine.issue_id);
          const paid = fine.paid_amount ?? (fine.payment_status === "PAID" ? fine.amount : 0);
          const status = balance(fine) > 0 && Number(paid) > 0 ? "PARTIAL" : fine.payment_status;
          return `<tr>${memberCell(fine.student_id, fine.student)}<td><b>${escapeHtml(fine.title)}</b><small class="audit-record-id">${copyLabel(issue)}</small></td><td>${escapeHtml(issue?.return_date || "Not returned")}</td><td><b>${money(fine.amount)}</b></td><td>${money(paid)}</td><td><b>${money(balance(fine))}</b></td><td><span class="pill ${status === "PARTIAL" ? "unpaid" : status.toLowerCase()}">${status}</span></td><td>${balance(fine) > 0 ? `<button class="button small primary" data-pay="${fine.fine_id}">Pay full fine</button>` : '<span class="complete-text">Completed</span>'} <button class="button small secondary" data-history="${fine.fine_id}">Receipts</button></td></tr>`;
        }),
    );
    $$("[data-pay]").forEach((button) => {
      button.onclick = () => {
        const fine = state.fines.find((item) => item.fine_id == button.dataset.pay);
        const form = $("#paymentModal form");
        form.elements.fineId.value = fine.fine_id;
        $("#paymentBalance").textContent =
          `${fine.student} / ${fine.title} / ${money(balance(fine))} remaining`;
        openModal("paymentModal");
      };
    });
    $$("[data-history]").forEach((button) => {
      button.onclick = async () => {
        $("#paymentHistory").textContent = "Loading receipts...";
        openModal("paymentHistoryModal");
        try {
          const payments = await api(`/fines/${button.dataset.history}/payments`);
          $("#paymentHistory").innerHTML = payments.length
            ? table(
                ["Receipt", "Date", "Amount", "Received by", "Note"],
                payments.map(
                  (item) =>
                    `<tr><td>${item.payment_id}</td><td>${escapeHtml(item.paid_at)}</td><td>${money(item.amount)}</td><td>${escapeHtml(item.actor)}</td><td>${escapeHtml(item.note || "—")}</td></tr>`,
                ),
              )
            : "<p>There are no receipts for this fine. Payments made before this feature are included in the received total.</p>";
        } catch (error) {
          $("#paymentHistory").textContent = error.message;
        }
      };
    });
    $$("[data-fine-return]").forEach((button) => {
      button.onclick = () =>
        performAction(
          button,
          `/issues/${button.dataset.fineReturn}/return`,
          "Return this overdue book and record its final fine?",
          "Book returned. Final fine is shown below",
        );
    });
    await renderCollection();
  }

  const paymentForm = $("#paymentModal form");
  if (paymentForm?.elements) {
    paymentForm.onsubmit = async (event) => {
      event.preventDefault();
      if (!state.online) {
        toast("Connect to the database before making changes", true);
        return;
      }
      const button = $("button:not([type='button'])", paymentForm);
      if (button.disabled) return;
      button.disabled = true;
      try {
        await api(`/fines/${paymentForm.elements.fineId.value}/pay`, {
          method: "POST",
          body: new URLSearchParams({ note: paymentForm.elements.note.value }),
        });
        closeModal($("#paymentModal"));
        toast("Fine paid in full");
        await loadData(render);
      } catch (error) {
        toast(error.message, true);
      } finally {
        button.disabled = false;
      }
    };
  }

  async function performAction(button, path, confirmation, message) {
    if (button.disabled || !confirm(confirmation)) return;
    if (!state.online) {
      toast("Connect to the database before making changes", true);
      return;
    }
    button.disabled = true;
    try {
      await api(path, { method: "POST" });
      toast(message);
      await loadData(render);
    } catch (error) {
      toast(error.message, true);
    } finally {
      button.disabled = false;
    }
  }

  async function renderCollection() {
    const container = $("#fineCollection");
    container.innerHTML = '<div class="form-note">Loading fine collection…</div>';
    try {
      const collection = await api("/fines/collection-summary");
      const metrics = [
        [
          "Total fine collection",
          collection.total,
          "All recorded payments, including legacy balances",
          "green",
        ],
        [
          "Today’s fine collection",
          collection.today,
          `Receipts on ${collection.date} · Asia/Dhaka`,
          "blue",
        ],
        [
          "Monthly fine collection",
          collection.month,
          `Current month: ${collection.month_start.slice(0, 7)}`,
          "gold",
        ],
      ];
      container.innerHTML = metrics
        .map(
          ([label, value, note, tone]) =>
            `<article class="metric ${tone}"><span>${label}</span><strong>${money(value)}</strong><small>${note}</small></article>`,
        )
        .join("");
    } catch (error) {
      container.innerHTML =
        '<div class="empty-state"><strong>Collection totals unavailable</strong><span>Refresh after the database connection is restored.</span></div>';
    }
  }

  $("#refreshButton").onclick = () => loadData(render);
  // Oracle recalculates today's estimate; keep an open page current as days change.
  window.setInterval(() => {
    if (!document.hidden) loadData(render);
  }, 60000);
  loadData(render);
})();
