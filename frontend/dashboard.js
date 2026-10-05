(() => {
  const { $, state, loadData, sortIssues, issueRows, escapeHtml: e, table, memberId } = LibraryApp;
  const money = (value) => `Tk ${Number(value).toLocaleString("en-BD")}`;

  function render() {
    const totalCopies = state.books.reduce((sum, book) => sum + Number(book.quantity), 0);
    const available = state.books.reduce((sum, book) => sum + Number(book.available_quantity), 0);
    const activeLoans = state.issues.filter((issue) => issue.status === "ISSUED").length;
    const loans = state.issues.filter((issue) => issue.status === "ISSUED");
    const dueSoon = loans
      .filter((issue) => {
        const days = window.LibraryNotifications.daysUntilDue(issue.due_date);
        return days !== null && days >= 0 && days <= 3;
      })
      .sort((a, b) => a.due_date.localeCompare(b.due_date));
    const overdueLoans = loans.filter((issue) => Number(issue.overdue_days) > 0);
    const reserved = (state.reservations || []).filter((item) => item.status === "ACTIVE").length;
    const activeMembers = state.students.filter(
      (student) => (student.membership_status || "ACTIVE") === "ACTIVE",
    ).length;
    const unpaid = state.fines.filter(
      (fine) =>
        fine.payment_status === "UNPAID" &&
        Number(fine.balance ?? Number(fine.amount) - Number(fine.paid_amount || 0)) > 0,
    );
    const unpaidAmount =
      unpaid.reduce(
        (sum, fine) =>
          sum +
          Math.round(
            Number(fine.balance ?? Number(fine.amount) - Number(fine.paid_amount || 0)) * 100,
          ),
        0,
      ) / 100;
    const recordedIssues = new Set(state.fines.map((fine) => Number(fine.issue_id)));
    const estimatedLoans = overdueLoans.filter(
      (issue) => !recordedIssues.has(Number(issue.issue_id)),
    );
    const overdueEstimate =
      estimatedLoans.reduce(
        (sum, issue) => sum + Math.round(Number(issue.current_fine || 0) * 100),
        0,
      ) / 100;
    const affectedMembers = new Set(unpaid.map((fine) => fine.student_id)).size;
    const details = [
      [
        `${state.meta.authors?.length || 0} authors`,
        `${state.books.filter((book) => Number(book.available_quantity) === 0).length} titles out of stock`,
        "/books",
      ],
      [
        `${activeLoans} on loan · ${reserved} held`,
        `${totalCopies ? Math.round((available / totalCopies) * 100) : 0}% ready to issue`,
        "/books",
      ],
      [
        `${dueSoon.length} due within 3 days`,
        `${overdueLoans.length} overdue · ${new Set(loans.map((issue) => issue.student_id)).size} borrowers`,
        "/circulation",
      ],
      [
        `${(state.reservations || []).filter((item) => item.status === "COLLECTED").length} collected`,
        `${(state.reservations || []).filter((item) => item.status === "EXPIRED").length} expired · ${(state.reservations || []).filter((item) => item.status === "CANCELLED").length} cancelled`,
        "/reservations",
      ],
      [
        `${state.students.length - activeMembers} disabled memberships`,
        `${new Set(loans.map((issue) => issue.student_id)).size} currently borrowing`,
        "/students",
      ],
      [
        `${money(overdueEstimate)} overdue estimate`,
        `${money(unpaidAmount + overdueEstimate)} combined outstanding`,
        "/fines",
      ],
    ];
    const metrics = [
      [
        "BK",
        "Book titles",
        state.books.length,
        `${state.meta.categories?.length || 0} categories`,
        "green",
      ],
      ["AV", "Available copies", available, `${totalCopies} total copies`, "blue"],
      ["LN", "Active loans", activeLoans, "Awaiting return", "gold"],
      ["RS", "Reserved copies", reserved, "Collect within 3 days", "blue"],
      ["MB", "Active members", activeMembers, `${state.students.length} registered`, "slate"],
      [
        "TK",
        "Unpaid fines",
        money(unpaidAmount),
        `${unpaid.length} fine records · ${affectedMembers} members`,
        "red",
      ],
    ];
    $("#stats").innerHTML = metrics
      .map(
        ([mark, label, value, note, tone], index) =>
          `<article class="metric ${tone}"><div class="metric-top"><span class="metric-mark">${mark}</span><span>${label}</span></div><strong>${value}</strong><small>${note}</small><div class="metric-details"><span>${details[index][0]}</span><span>${details[index][1]}</span></div><a class="metric-details-link" href="${details[index][2]}">View details &rarr;</a></article>`,
      )
      .join("");
    $("#recentTable").innerHTML = issueRows(sortIssues(state.issues).slice(0, 6));
    $("#dueSoonTable").innerHTML = table(
      ["Member / book", "Copy", "Issued", "Return by", "Reminder"],
      dueSoon.map((issue) => {
        const days = window.LibraryNotifications.daysUntilDue(issue.due_date);
        return `<tr><td><b>${e(issue.student)}</b><small>${memberId(issue.student_id)} · ${e(issue.title)}</small></td><td>${issue.copy_no ? `#${issue.copy_no}` : "Legacy"}</td><td>${e(issue.issue_date || "—")}</td><td>${e(issue.due_date)}</td><td><span class="pill ${days === 0 ? "overdue" : "active"}">${days === 0 ? "Due today" : `${days} days left`}</span></td></tr>`;
      }),
    );
    const fineRows = [
      ...unpaid.map((fine) => ({
        ...fine,
        total: Number(fine.balance ?? Number(fine.amount) - Number(fine.paid_amount || 0)),
        label: "Unpaid fine",
      })),
      ...estimatedLoans.map((issue) => ({
        ...issue,
        total: Number(issue.current_fine || 0),
        label: "Overdue estimate",
      })),
    ].sort(
      (a, b) =>
        Number(b.label === "Overdue estimate") - Number(a.label === "Overdue estimate") ||
        b.total - a.total,
    );
    $("#fineAttentionTable").innerHTML = table(
      ["Member / book", "Fine", "Received", "Outstanding", "Type"],
      fineRows.map(
        (item) =>
          `<tr><td><b>${e(item.student)}</b><small>${memberId(item.student_id)} · ${e(item.title)}</small></td><td>${money(item.amount ?? item.total)}</td><td>${money(item.paid_amount || 0)}</td><td><b>${money(item.total)}</b></td><td>${item.label}</td></tr>`,
      ),
    );
    $("#dueSoonCount").textContent = `${dueSoon.length} upcoming returns`;
    if (!dueSoon.length)
      $("#dueSoonTable").innerHTML =
        '<div class="empty-state"><strong>No returns due within 3 days</strong><span>Upcoming return reminders will appear here automatically.</span></div>';
    if (!fineRows.length)
      $("#fineAttentionTable").innerHTML =
        '<div class="empty-state"><strong>No outstanding fines</strong><span>There are no unpaid fines or overdue estimates to follow up.</span></div>';
    $("#fineAttentionTotal").textContent =
      `${money(unpaidAmount + overdueEstimate)} recorded + estimated`;
    const overdue = state.issues.filter(
      (issue) => issue.status === "ISSUED" && Number(issue.overdue_days) > 0,
    ).length;
    $("#deskPriorities").innerHTML = [
      [
        "Due within 3 days",
        dueSoon.length,
        dueSoon.length ? "Follow up before overdue fines start" : "No upcoming due dates",
        "#dueSoonDetails",
        "",
      ],
      [
        "Overdue returns",
        overdue,
        overdue ? "Follow up with borrowing members" : "No overdue returns",
        "/circulation",
        "urgent",
      ],
      [
        "Reserved pickups",
        reserved,
        reserved ? "Issue copies before holds expire" : "No copies awaiting collection",
        "/reservations",
        "",
      ],
      [
        "Outstanding fines",
        unpaid.length,
        unpaid.length
          ? `${unpaid.length} records awaiting full payment`
          : "No recorded unpaid fines",
        "/fines",
        "urgent",
      ],
    ]
      .sort((a, b) => {
        const rank = {
          "Overdue returns": 0,
          "Outstanding fines": 1,
          "Due within 3 days": 2,
          "Reserved pickups": 3,
        };
        return (a[1] ? rank[a[0]] : 10 + rank[a[0]]) - (b[1] ? rank[b[0]] : 10 + rank[b[0]]);
      })
      .map(
        ([label, count, note, path, tone]) =>
          `<a class="priority-card ${count ? tone : "clear"}" href="${path}"><span><strong>${label}</strong><small>${note}</small></span><b class="priority-count">${count}</b></a>`,
      )
      .join("");

    const items = [
      ["Available", available, totalCopies],
      ["On loan", activeLoans, totalCopies],
      ["Reserved", reserved, totalCopies],
      ["Members", state.students.length, Math.max(state.students.length, 10)],
    ];
    $("#inventorySnapshot").innerHTML =
      `<div class="health-list">${items.map(([label, value, maximum]) => `<div class="health-row"><div><span>${label}</span><b>${value}</b></div><progress max="${maximum || 1}" value="${value}"></progress></div>`).join("")}</div><div class="health-note"><b>${totalCopies ? Math.round((available / totalCopies) * 100) : 0}%</b><span>of the collection is ready to issue</span></div>`;
  }

  $("#today").textContent = new Date().toLocaleDateString("en-GB", {
    timeZone: "Asia/Dhaka",
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
  $("#refreshButton").onclick = () => loadData(render);
  loadData(render);
})();
