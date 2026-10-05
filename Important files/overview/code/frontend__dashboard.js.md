# frontend/dashboard.js

Books, copies, loans, members ও fines-এর overview metrics এবং recent loans render করে।

Source: [মূল file](../../frontend/dashboard.js)। Snapshot 2026-10-04; 211 lines; SHA-256 `2b757af04fad162d976de00f140a44f62d5092342a9b75a7a7950685e27d812d`।

## Function / object / element inventory

### `render()` — L5

এই page-এর current state ও search/filter থেকে tables/metrics/options তৈরি করে, DOM update করে এবং generated action buttons-এর events bind করে। পাশের পূর্ণ code-এ page-specific fields দেখা যাবে।

## সম্পূর্ণ original source

```javascript
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
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>(() =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 2 | <code>  const { $, state, loadData, sortIssues, issueRows, escapeHtml: e, table, memberId } = LibraryApp;</code> | Local state, DOM reference বা callback/result assign করে। |
| 3 | <code>  const money = (value) =&gt; `Tk ${Number(value).toLocaleString(&quot;en-BD&quot;)}`;</code> | Local state, DOM reference বা callback/result assign করে। |
| 4 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 5 | <code>  function render() {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 6 | <code>    const totalCopies = state.books.reduce((sum, book) =&gt; sum + Number(book.quantity), 0);</code> | Local state, DOM reference বা callback/result assign করে। |
| 7 | <code>    const available = state.books.reduce((sum, book) =&gt; sum + Number(book.available_quantity), 0);</code> | Local state, DOM reference বা callback/result assign করে। |
| 8 | <code>    const activeLoans = state.issues.filter((issue) =&gt; issue.status === &quot;ISSUED&quot;).length;</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 9 | <code>    const loans = state.issues.filter((issue) =&gt; issue.status === &quot;ISSUED&quot;);</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 10 | <code>    const dueSoon = loans</code> | Local state, DOM reference বা callback/result assign করে। |
| 11 | <code>      .filter((issue) =&gt; {</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 12 | <code>        const days = window.LibraryNotifications.daysUntilDue(issue.due_date);</code> | Local state, DOM reference বা callback/result assign করে। |
| 13 | <code>        return days !== null &amp;&amp; days &gt;= 0 &amp;&amp; days &lt;= 3;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 14 | <code>      })</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 15 | <code>      .sort((a, b) =&gt; a.due_date.localeCompare(b.due_date));</code> | Local state, DOM reference বা callback/result assign করে। |
| 16 | <code>    const overdueLoans = loans.filter((issue) =&gt; Number(issue.overdue_days) &gt; 0);</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 17 | <code>    const reserved = (state.reservations &#124;&#124; []).filter((item) =&gt; item.status === &quot;ACTIVE&quot;).length;</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 18 | <code>    const activeMembers = state.students.filter(</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 19 | <code>      (student) =&gt; (student.membership_status &#124;&#124; &quot;ACTIVE&quot;) === &quot;ACTIVE&quot;,</code> | Local state, DOM reference বা callback/result assign করে। |
| 20 | <code>    ).length;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 21 | <code>    const unpaid = state.fines.filter(</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 22 | <code>      (fine) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 23 | <code>        fine.payment_status === &quot;UNPAID&quot; &amp;&amp;</code> | Local state, DOM reference বা callback/result assign করে। |
| 24 | <code>        Number(fine.balance ?? Number(fine.amount) - Number(fine.paid_amount &#124;&#124; 0)) &gt; 0,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 25 | <code>    );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 26 | <code>    const unpaidAmount =</code> | Local state, DOM reference বা callback/result assign করে। |
| 27 | <code>      unpaid.reduce(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 28 | <code>        (sum, fine) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 29 | <code>          sum +</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 30 | <code>          Math.round(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 31 | <code>            Number(fine.balance ?? Number(fine.amount) - Number(fine.paid_amount &#124;&#124; 0)) * 100,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 32 | <code>          ),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 33 | <code>        0,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 34 | <code>      ) / 100;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 35 | <code>    const recordedIssues = new Set(state.fines.map((fine) =&gt; Number(fine.issue_id)));</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 36 | <code>    const estimatedLoans = overdueLoans.filter(</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 37 | <code>      (issue) =&gt; !recordedIssues.has(Number(issue.issue_id)),</code> | Local state, DOM reference বা callback/result assign করে। |
| 38 | <code>    );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 39 | <code>    const overdueEstimate =</code> | Local state, DOM reference বা callback/result assign করে। |
| 40 | <code>      estimatedLoans.reduce(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 41 | <code>        (sum, issue) =&gt; sum + Math.round(Number(issue.current_fine &#124;&#124; 0) * 100),</code> | Local state, DOM reference বা callback/result assign করে। |
| 42 | <code>        0,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 43 | <code>      ) / 100;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 44 | <code>    const affectedMembers = new Set(unpaid.map((fine) =&gt; fine.student_id)).size;</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 45 | <code>    const details = [</code> | Local state, DOM reference বা callback/result assign করে। |
| 46 | <code>      [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 47 | <code>        `${state.meta.authors?.length &#124;&#124; 0} authors`,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 48 | <code>        `${state.books.filter((book) =&gt; Number(book.available_quantity) === 0).length} titles out of stock`,</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 49 | <code>        &quot;/books&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 50 | <code>      ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 51 | <code>      [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 52 | <code>        `${activeLoans} on loan · ${reserved} held`,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 53 | <code>        `${totalCopies ? Math.round((available / totalCopies) * 100) : 0}% ready to issue`,</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 54 | <code>        &quot;/books&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 55 | <code>      ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 56 | <code>      [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 57 | <code>        `${dueSoon.length} due within 3 days`,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 58 | <code>        `${overdueLoans.length} overdue · ${new Set(loans.map((issue) =&gt; issue.student_id)).size} borrowers`,</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 59 | <code>        &quot;/circulation&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 60 | <code>      ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 61 | <code>      [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 62 | <code>        `${(state.reservations &#124;&#124; []).filter((item) =&gt; item.status === &quot;COLLECTED&quot;).length} collected`,</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 63 | <code>        `${(state.reservations &#124;&#124; []).filter((item) =&gt; item.status === &quot;EXPIRED&quot;).length} expired · ${(state.reservations &#124;&#124; []).filter((item) =&gt; item.status === &quot;CANCELLED&quot;).length} cancelled`,</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 64 | <code>        &quot;/reservations&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 65 | <code>      ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 66 | <code>      [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 67 | <code>        `${state.students.length - activeMembers} disabled memberships`,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 68 | <code>        `${new Set(loans.map((issue) =&gt; issue.student_id)).size} currently borrowing`,</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 69 | <code>        &quot;/students&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 70 | <code>      ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 71 | <code>      [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 72 | <code>        `${money(overdueEstimate)} overdue estimate`,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 73 | <code>        `${money(unpaidAmount + overdueEstimate)} combined outstanding`,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 74 | <code>        &quot;/fines&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 75 | <code>      ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 76 | <code>    ];</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 77 | <code>    const metrics = [</code> | Local state, DOM reference বা callback/result assign করে। |
| 78 | <code>      [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 79 | <code>        &quot;BK&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 80 | <code>        &quot;Book titles&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 81 | <code>        state.books.length,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 82 | <code>        `${state.meta.categories?.length &#124;&#124; 0} categories`,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 83 | <code>        &quot;green&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 84 | <code>      ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 85 | <code>      [&quot;AV&quot;, &quot;Available copies&quot;, available, `${totalCopies} total copies`, &quot;blue&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 86 | <code>      [&quot;LN&quot;, &quot;Active loans&quot;, activeLoans, &quot;Awaiting return&quot;, &quot;gold&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 87 | <code>      [&quot;RS&quot;, &quot;Reserved copies&quot;, reserved, &quot;Collect within 3 days&quot;, &quot;blue&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 88 | <code>      [&quot;MB&quot;, &quot;Active members&quot;, activeMembers, `${state.students.length} registered`, &quot;slate&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 89 | <code>      [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 90 | <code>        &quot;TK&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 91 | <code>        &quot;Unpaid fines&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 92 | <code>        money(unpaidAmount),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 93 | <code>        `${unpaid.length} fine records · ${affectedMembers} members`,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 94 | <code>        &quot;red&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 95 | <code>      ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 96 | <code>    ];</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 97 | <code>    $(&quot;#stats&quot;).innerHTML = metrics</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 98 | <code>      .map(</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 99 | <code>        ([mark, label, value, note, tone], index) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 100 | <code>          `&lt;article class=&quot;metric ${tone}&quot;&gt;&lt;div class=&quot;metric-top&quot;&gt;&lt;span class=&quot;metric-mark&quot;&gt;${mark}&lt;/span&gt;&lt;span&gt;${label}&lt;/span&gt;&lt;/div&gt;&lt;strong&gt;${value}&lt;/strong&gt;&lt;small&gt;${note}&lt;/small&gt;&lt;div class=&quot;metric-details&quot;&gt;&lt;span&gt;${details[index][0]}&lt;/span&gt;&lt;span&gt;${details[index][1]}&lt;/span&gt;&lt;/div&gt;&lt;a class=&quot;metric-details-link&quot; href=&quot;${details[index][2]}&quot;&gt;View details &amp;rarr;&lt;/a&gt;&lt;/article&gt;`,</code> | Local state, DOM reference বা callback/result assign করে। |
| 101 | <code>      )</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 102 | <code>      .join(&quot;&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 103 | <code>    $(&quot;#recentTable&quot;).innerHTML = issueRows(sortIssues(state.issues).slice(0, 6));</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 104 | <code>    $(&quot;#dueSoonTable&quot;).innerHTML = table(</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 105 | <code>      [&quot;Member / book&quot;, &quot;Copy&quot;, &quot;Issued&quot;, &quot;Return by&quot;, &quot;Reminder&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 106 | <code>      dueSoon.map((issue) =&gt; {</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 107 | <code>        const days = window.LibraryNotifications.daysUntilDue(issue.due_date);</code> | Local state, DOM reference বা callback/result assign করে। |
| 108 | <code>        return `&lt;tr&gt;&lt;td&gt;&lt;b&gt;${e(issue.student)}&lt;/b&gt;&lt;small&gt;${memberId(issue.student_id)} · ${e(issue.title)}&lt;/small&gt;&lt;/td&gt;&lt;td&gt;${issue.copy_no ? `#${issue.copy_no}` : &quot;Legacy&quot;}&lt;/td&gt;&lt;td&gt;${e(issue.issue_date &#124;&#124; &quot;—&quot;)}&lt;/td&gt;&lt;td&gt;${e(issue.due_date)}&lt;/td&gt;&lt;td&gt;&lt;span class=&quot;pill ${days === 0 ? &quot;overdue&quot; : &quot;active&quot;}&quot;&gt;${days === 0 ? &quot;Due today&quot; : `${days} days left`}&lt;/span&gt;&lt;/td&gt;&lt;/tr&gt;`;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 109 | <code>      }),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 110 | <code>    );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 111 | <code>    const fineRows = [</code> | Local state, DOM reference বা callback/result assign করে। |
| 112 | <code>      ...unpaid.map((fine) =&gt; ({</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 113 | <code>        ...fine,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 114 | <code>        total: Number(fine.balance ?? Number(fine.amount) - Number(fine.paid_amount &#124;&#124; 0)),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 115 | <code>        label: &quot;Unpaid fine&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 116 | <code>      })),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 117 | <code>      ...estimatedLoans.map((issue) =&gt; ({</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 118 | <code>        ...issue,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 119 | <code>        total: Number(issue.current_fine &#124;&#124; 0),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 120 | <code>        label: &quot;Overdue estimate&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 121 | <code>      })),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 122 | <code>    ].sort(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 123 | <code>      (a, b) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 124 | <code>        Number(b.label === &quot;Overdue estimate&quot;) - Number(a.label === &quot;Overdue estimate&quot;) &#124;&#124;</code> | Local state, DOM reference বা callback/result assign করে। |
| 125 | <code>        b.total - a.total,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 126 | <code>    );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 127 | <code>    $(&quot;#fineAttentionTable&quot;).innerHTML = table(</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 128 | <code>      [&quot;Member / book&quot;, &quot;Fine&quot;, &quot;Received&quot;, &quot;Outstanding&quot;, &quot;Type&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 129 | <code>      fineRows.map(</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 130 | <code>        (item) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 131 | <code>          `&lt;tr&gt;&lt;td&gt;&lt;b&gt;${e(item.student)}&lt;/b&gt;&lt;small&gt;${memberId(item.student_id)} · ${e(item.title)}&lt;/small&gt;&lt;/td&gt;&lt;td&gt;${money(item.amount ?? item.total)}&lt;/td&gt;&lt;td&gt;${money(item.paid_amount &#124;&#124; 0)}&lt;/td&gt;&lt;td&gt;&lt;b&gt;${money(item.total)}&lt;/b&gt;&lt;/td&gt;&lt;td&gt;${item.label}&lt;/td&gt;&lt;/tr&gt;`,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 132 | <code>      ),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 133 | <code>    );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 134 | <code>    $(&quot;#dueSoonCount&quot;).textContent = `${dueSoon.length} upcoming returns`;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 135 | <code>    if (!dueSoon.length)</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 136 | <code>      $(&quot;#dueSoonTable&quot;).innerHTML =</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 137 | <code>        &#x27;&lt;div class=&quot;empty-state&quot;&gt;&lt;strong&gt;No returns due within 3 days&lt;/strong&gt;&lt;span&gt;Upcoming return reminders will appear here automatically.&lt;/span&gt;&lt;/div&gt;&#x27;;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 138 | <code>    if (!fineRows.length)</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 139 | <code>      $(&quot;#fineAttentionTable&quot;).innerHTML =</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 140 | <code>        &#x27;&lt;div class=&quot;empty-state&quot;&gt;&lt;strong&gt;No outstanding fines&lt;/strong&gt;&lt;span&gt;There are no unpaid fines or overdue estimates to follow up.&lt;/span&gt;&lt;/div&gt;&#x27;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 141 | <code>    $(&quot;#fineAttentionTotal&quot;).textContent =</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 142 | <code>      `${money(unpaidAmount + overdueEstimate)} recorded + estimated`;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 143 | <code>    const overdue = state.issues.filter(</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 144 | <code>      (issue) =&gt; issue.status === &quot;ISSUED&quot; &amp;&amp; Number(issue.overdue_days) &gt; 0,</code> | Local state, DOM reference বা callback/result assign করে। |
| 145 | <code>    ).length;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 146 | <code>    $(&quot;#deskPriorities&quot;).innerHTML = [</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 147 | <code>      [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 148 | <code>        &quot;Due within 3 days&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 149 | <code>        dueSoon.length,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 150 | <code>        dueSoon.length ? &quot;Follow up before overdue fines start&quot; : &quot;No upcoming due dates&quot;,</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 151 | <code>        &quot;#dueSoonDetails&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 152 | <code>        &quot;&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 153 | <code>      ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 154 | <code>      [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 155 | <code>        &quot;Overdue returns&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 156 | <code>        overdue,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 157 | <code>        overdue ? &quot;Follow up with borrowing members&quot; : &quot;No overdue returns&quot;,</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 158 | <code>        &quot;/circulation&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 159 | <code>        &quot;urgent&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 160 | <code>      ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 161 | <code>      [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 162 | <code>        &quot;Reserved pickups&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 163 | <code>        reserved,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 164 | <code>        reserved ? &quot;Issue copies before holds expire&quot; : &quot;No copies awaiting collection&quot;,</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 165 | <code>        &quot;/reservations&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 166 | <code>        &quot;&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 167 | <code>      ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 168 | <code>      [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 169 | <code>        &quot;Outstanding fines&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 170 | <code>        unpaid.length,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 171 | <code>        unpaid.length</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 172 | <code>          ? `${unpaid.length} records awaiting full payment`</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 173 | <code>          : &quot;No recorded unpaid fines&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 174 | <code>        &quot;/fines&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 175 | <code>        &quot;urgent&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 176 | <code>      ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 177 | <code>    ]</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 178 | <code>      .sort((a, b) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 179 | <code>        const rank = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 180 | <code>          &quot;Overdue returns&quot;: 0,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 181 | <code>          &quot;Outstanding fines&quot;: 1,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 182 | <code>          &quot;Due within 3 days&quot;: 2,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 183 | <code>          &quot;Reserved pickups&quot;: 3,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 184 | <code>        };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 185 | <code>        return (a[1] ? rank[a[0]] : 10 + rank[a[0]]) - (b[1] ? rank[b[0]] : 10 + rank[b[0]]);</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 186 | <code>      })</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 187 | <code>      .map(</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 188 | <code>        ([label, count, note, path, tone]) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 189 | <code>          `&lt;a class=&quot;priority-card ${count ? tone : &quot;clear&quot;}&quot; href=&quot;${path}&quot;&gt;&lt;span&gt;&lt;strong&gt;${label}&lt;/strong&gt;&lt;small&gt;${note}&lt;/small&gt;&lt;/span&gt;&lt;b class=&quot;priority-count&quot;&gt;${count}&lt;/b&gt;&lt;/a&gt;`,</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 190 | <code>      )</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 191 | <code>      .join(&quot;&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 192 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 193 | <code>    const items = [</code> | Local state, DOM reference বা callback/result assign করে। |
| 194 | <code>      [&quot;Available&quot;, available, totalCopies],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 195 | <code>      [&quot;On loan&quot;, activeLoans, totalCopies],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 196 | <code>      [&quot;Reserved&quot;, reserved, totalCopies],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 197 | <code>      [&quot;Members&quot;, state.students.length, Math.max(state.students.length, 10)],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 198 | <code>    ];</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 199 | <code>    $(&quot;#inventorySnapshot&quot;).innerHTML =</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 200 | <code>      `&lt;div class=&quot;health-list&quot;&gt;${items.map(([label, value, maximum]) =&gt; `&lt;div class=&quot;health-row&quot;&gt;&lt;div&gt;&lt;span&gt;${label}&lt;/span&gt;&lt;b&gt;${value}&lt;/b&gt;&lt;/div&gt;&lt;progress max=&quot;${maximum &#124;&#124; 1}&quot; value=&quot;${value}&quot;&gt;&lt;/progress&gt;&lt;/div&gt;`).join(&quot;&quot;)}&lt;/div&gt;&lt;div class=&quot;health-note&quot;&gt;&lt;b&gt;${totalCopies ? Math.round((available / totalCopies) * 100) : 0}%&lt;/b&gt;&lt;span&gt;of the collection is ready to issue&lt;/span&gt;&lt;/div&gt;`;</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 201 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 202 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 203 | <code>  $(&quot;#today&quot;).textContent = new Date().toLocaleDateString(&quot;en-GB&quot;, {</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 204 | <code>    timeZone: &quot;Asia/Dhaka&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 205 | <code>    day: &quot;2-digit&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 206 | <code>    month: &quot;short&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 207 | <code>    year: &quot;numeric&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 208 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 209 | <code>  $(&quot;#refreshButton&quot;).onclick = () =&gt; loadData(render);</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 210 | <code>  loadData(render);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 211 | <code>})();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
