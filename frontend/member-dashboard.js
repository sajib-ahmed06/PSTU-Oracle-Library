"use strict";

// Personal collection, loans, fines, and account controls.
window.MemberDashboard = {
  create(context) {
    const {
      $,
      $$,
      state,
      api,
      escapeHtml: e,
      table,
      toast,
      memberId,
      money,
      getData,
      action,
      reservationTable,
    } = context;
    function catalogue() {
      const data = getData();
      if (!data) return;
      const query = $("#bookSearch").value.toLowerCase().trim();
      const active = data.reservations.filter((r) => r.status === "ACTIVE");
      const capacity = data.issues.filter((i) => i.status === "ISSUED").length + active.length < 3;
      const debt = data.fines.some((f) => Number(f.balance) > 0);
      const availableOnly = $("#availabilityFilter")?.value === "available";
      const books = data.books.filter(
        (b) =>
          `${b.title} ${b.author_name} ${b.category_name}`.toLowerCase().includes(query) &&
          (!availableOnly || Number(b.available_quantity) > 0),
      );
      const countLabel = $("#catalogueCount");
      if (countLabel)
        countLabel.textContent = `${books.length} of ${data.books.length} titles · Reserve an available copy for 3 days`;
      $("#catalogueTable").innerHTML = books.length
        ? books
            .map((b) => {
              const held = active.some((r) => r.book_id === b.book_id);
              const enabled =
                state.online && capacity && !debt && !held && Number(b.available_quantity) > 0;
              const label = held
                ? "Already reserved"
                : Number(b.available_quantity) <= 0
                  ? "Out of stock"
                  : debt
                    ? "Clear fines first"
                    : !capacity
                      ? "3-copy limit reached"
                      : "Reserve for 3 days";
              return `<article class="book-card"><div class="book-card-top"><span class="book-spine" aria-hidden="true">${e(String(b.title || "B").slice(0, 1))}</span><div><h3>${e(b.title)}</h3><p>${e(b.author_name)}</p></div></div><span class="book-card-category">${e(b.category_name)}</span><div class="book-card-stock"><span>${b.quantity} total copies</span><b>${b.available_quantity} available</b></div><button class="button small primary" data-reserve="${b.book_id}" ${enabled ? "" : "disabled"}>${label}</button></article>`;
            })
            .join("")
        : '<div class="empty-state"><strong>No matching books</strong><span>Try another title, author or category.</span></div>';
      $$("[data-reserve]").forEach((button) => {
        button.onclick = () =>
          action(
            button,
            "/reservations",
            { bookId: button.dataset.reserve },
            "Reserve this copy for 3 days?",
          );
      });
    }

    function renderStudent() {
      const data = getData();
      if (!data) return;
      $("#memberName").textContent = `Welcome, ${data.member.name}`;
      $("#memberIdentity").textContent =
        `${memberId(data.member.student_id)} · Roll: ${data.member.roll_no || "Not assigned"} · Registration: ${data.member.registration_no || "Not assigned"}`;
      const loans = data.issues.filter((i) => i.status === "ISSUED");
      const active = data.reservations.filter((r) => r.status === "ACTIVE");
      const outstanding =
        data.fines.reduce((sum, f) => sum + Number(f.balance || 0), 0) +
        loans
          .filter((i) => !data.fines.some((f) => f.issue_id === i.issue_id))
          .reduce((sum, i) => sum + Number(i.current_fine || 0), 0);
      $("#studentStats").innerHTML = [
        ["Books on loan", loans.length, "Your current reading"],
        ["Active reservations", active.length, "Held for 3 days"],
        [
          "Outstanding + overdue estimate",
          money(outstanding),
          "Updates daily · Tk 10/day until return",
        ],
        ["Titles to explore", data.books.length, "Browse the full collection"],
      ]
        .map(
          ([label, value, note]) =>
            `<article class="member-stat"><span>${label}</span><strong>${value}</strong><small>${note}</small></article>`,
        )
        .join("");
      // The panel mirrors the bell, using only the member-scoped dashboard response.
      if ($("#memberAlerts") && window.LibraryNotifications) {
        const alerts = window.LibraryNotifications.buildItems(data, {
          user_type: "STUDENT",
          student_id: data.member.student_id,
        });
        const reminders = alerts.filter((item) => item.type === "due" || item.type === "fine");
        $("#memberAlerts").innerHTML = reminders.length
          ? reminders
              .map(
                (item) =>
                  `<a class="member-reminder ${item.type}" href="${item.href}"><span class="visit-mark">${item.type === "due" ? "DUE" : "FINE"}</span><div><strong>${e(item.title)}</strong><span>${e(item.detail)}</span><small>${e(item.note)}</small></div><b aria-hidden="true">&rarr;</b></a>`,
              )
              .join("")
          : '<div class="member-reminder clear"><span class="visit-mark">OK</span><div><strong>No upcoming return reminders or unpaid fines</strong><small>Reminders appear 3 days before your return date.</small></div></div>';
      }
      const nextLoan = [...loans]
        .filter((i) => i.due_date)
        .sort((a, b) => a.due_date.localeCompare(b.due_date))[0];
      const nextHold = [...active]
        .filter((r) => r.expires_at)
        .sort((a, b) => a.expires_at.localeCompare(b.expires_at))[0];
      const nextSteps = [];
      if (nextLoan)
        nextSteps.push(
          `<div class="next-visit-item"><span class="visit-mark">RET</span><div><strong>${e(nextLoan.title)}</strong><small>${Number(nextLoan.overdue_days) > 0 ? "Overdue · due" : "Return by"} ${e(nextLoan.due_date)}</small></div><a href="#loans">View loan &rarr;</a></div>`,
        );
      if (nextHold)
        nextSteps.push(
          `<div class="next-visit-item"><span class="visit-mark">HOLD</span><div><strong>${e(nextHold.title)}</strong><small>Collect before ${e(nextHold.expires_at)}</small></div><a href="#reservations">View hold &rarr;</a></div>`,
        );
      $("#memberNextStep").innerHTML = nextSteps.length
        ? nextSteps.join("")
        : '<p class="section-description">No upcoming returns or pickups. Find something new in the catalogue and reserve your next read.</p><div class="next-visit-item"><span class="visit-mark">READ</span><div><strong>Your next chapter is waiting.</strong><small>Explore books by title, author or category.</small></div><a href="#catalogue">Discover &rarr;</a></div>';
      reservationTable(data.reservations);
      const loanSelection = $("#loanFilter")?.value || "all";
      const visibleLoans = (
        context.sortIssues ? context.sortIssues(data.issues) : data.issues
      ).filter(
        (i) => !["ISSUED", "RETURNED"].includes(loanSelection) || i.status === loanSelection,
      );
      $("#loanTable").innerHTML = table(
        ["Book", "Copy", "Issued", "Due date", "Return date", "Status", "Overdue fine estimate"],
        visibleLoans.map(
          (i) =>
            `<tr><td><b>${e(i.title)}</b></td><td>${i.copy_no ? `Copy #${i.copy_no}` : "Legacy copy"}</td><td>${e(i.issue_date)}</td><td>${e(i.due_date)}</td><td>${e(i.return_date || "Awaiting return")}</td><td><span class="pill ${i.status === "ISSUED" && Number(i.overdue_days) > 0 ? "overdue" : String(i.status).toLowerCase()}">${i.status === "ISSUED" && Number(i.overdue_days) > 0 ? "OVERDUE" : e(i.status)}</span></td><td>${money(i.current_fine)}</td></tr>`,
        ),
      );
      $("#studentFineTable").innerHTML = table(
        ["Book", "Fine", "Received", "Outstanding", "Status"],
        [...data.fines]
          .sort(
            (a, b) =>
              Number(Number(b.balance) > 0) - Number(Number(a.balance) > 0) ||
              Number(b.balance || 0) - Number(a.balance || 0),
          )
          .map(
            (f) =>
              `<tr><td>${e(f.title)}</td><td>${money(f.amount)}</td><td>${money(f.paid_amount)}</td><td>${money(f.balance)}</td><td>${e(f.payment_status)}</td></tr>`,
          ),
      );
      if (!visibleLoans.length)
        $("#loanTable").innerHTML =
          '<div class="empty-state"><strong>No books in this view.</strong><span>Your borrowed books and return dates will appear here.</span></div>';
      if (!data.fines.length)
        $("#studentFineTable").innerHTML =
          '<div class="empty-state"><strong>No recorded fines.</strong><span>Return your books by their due dates to keep it that way.</span></div>';
      catalogue();
    }

    function bind() {
      $("#bookSearch").oninput = catalogue;
      if ($("#availabilityFilter")) $("#availabilityFilter").onchange = catalogue;
      if ($("#loanFilter")) $("#loanFilter").onchange = renderStudent;
      $("#studentPasswordForm").onsubmit = async (event) => {
        event.preventDefault();
        const form = event.currentTarget;
        if (await action($("button", form), "/student/password", new FormData(form)))
          window.location.replace("/login");
      };
    }
    return { render: renderStudent, bind };
  },
};
