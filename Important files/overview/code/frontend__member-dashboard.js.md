# frontend/member-dashboard.js

Render personal borrowing, reservations, catalogue, fines and security controls.

Source: [মূল file](../../frontend/member-dashboard.js)। Snapshot 2026-10-04; 177 lines; SHA-256 `393c33a672577cd08f382ed9a937f1f0b68f44b1c63c655d61f8c6cc26d426d3`।

## Function / object / element inventory

### `catalogue()` — L20

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

### `renderStudent()` — L66

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

### `bind()` — L164

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

## সম্পূর্ণ original source

```javascript
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
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&quot;use strict&quot;;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 2 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 3 | <code>// Personal collection, loans, fines, and account controls.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 4 | <code>window.MemberDashboard = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 5 | <code>  create(context) {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 6 | <code>    const {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 7 | <code>      $,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 8 | <code>      $$,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 9 | <code>      state,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 10 | <code>      api,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 11 | <code>      escapeHtml: e,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 12 | <code>      table,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 13 | <code>      toast,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 14 | <code>      memberId,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 15 | <code>      money,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 16 | <code>      getData,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 17 | <code>      action,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 18 | <code>      reservationTable,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 19 | <code>    } = context;</code> | Local state, DOM reference বা callback/result assign করে। |
| 20 | <code>    function catalogue() {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 21 | <code>      const data = getData();</code> | Local state, DOM reference বা callback/result assign করে। |
| 22 | <code>      if (!data) return;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 23 | <code>      const query = $(&quot;#bookSearch&quot;).value.toLowerCase().trim();</code> | Local state, DOM reference বা callback/result assign করে। |
| 24 | <code>      const active = data.reservations.filter((r) =&gt; r.status === &quot;ACTIVE&quot;);</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 25 | <code>      const capacity = data.issues.filter((i) =&gt; i.status === &quot;ISSUED&quot;).length + active.length &lt; 3;</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 26 | <code>      const debt = data.fines.some((f) =&gt; Number(f.balance) &gt; 0);</code> | Local state, DOM reference বা callback/result assign করে। |
| 27 | <code>      const availableOnly = $(&quot;#availabilityFilter&quot;)?.value === &quot;available&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 28 | <code>      const books = data.books.filter(</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 29 | <code>        (b) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 30 | <code>          `${b.title} ${b.author_name} ${b.category_name}`.toLowerCase().includes(query) &amp;&amp;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 31 | <code>          (!availableOnly &#124;&#124; Number(b.available_quantity) &gt; 0),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 32 | <code>      );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 33 | <code>      const countLabel = $(&quot;#catalogueCount&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 34 | <code>      if (countLabel)</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 35 | <code>        countLabel.textContent = `${books.length} of ${data.books.length} titles · Reserve an available copy for 3 days`;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 36 | <code>      $(&quot;#catalogueTable&quot;).innerHTML = books.length</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 37 | <code>        ? books</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 38 | <code>            .map((b) =&gt; {</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 39 | <code>              const held = active.some((r) =&gt; r.book_id === b.book_id);</code> | Local state, DOM reference বা callback/result assign করে। |
| 40 | <code>              const enabled =</code> | Local state, DOM reference বা callback/result assign করে। |
| 41 | <code>                state.online &amp;&amp; capacity &amp;&amp; !debt &amp;&amp; !held &amp;&amp; Number(b.available_quantity) &gt; 0;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 42 | <code>              const label = held</code> | Local state, DOM reference বা callback/result assign করে। |
| 43 | <code>                ? &quot;Already reserved&quot;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 44 | <code>                : Number(b.available_quantity) &lt;= 0</code> | Local state, DOM reference বা callback/result assign করে। |
| 45 | <code>                  ? &quot;Out of stock&quot;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 46 | <code>                  : debt</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 47 | <code>                    ? &quot;Clear fines first&quot;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 48 | <code>                    : !capacity</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 49 | <code>                      ? &quot;3-copy limit reached&quot;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 50 | <code>                      : &quot;Reserve for 3 days&quot;;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 51 | <code>              return `&lt;article class=&quot;book-card&quot;&gt;&lt;div class=&quot;book-card-top&quot;&gt;&lt;span class=&quot;book-spine&quot; aria-hidden=&quot;true&quot;&gt;${e(String(b.title &#124;&#124; &quot;B&quot;).slice(0, 1))}&lt;/span&gt;&lt;div&gt;&lt;h3&gt;${e(b.title)}&lt;/h3&gt;&lt;p&gt;${e(b.author_name)}&lt;/p&gt;&lt;/div&gt;&lt;/div&gt;&lt;span class=&quot;book-card-category&quot;&gt;${e(b.category_name)}&lt;/span&gt;&lt;div class=&quot;book-card-stock&quot;&gt;&lt;span&gt;${b.quantity} total copies&lt;/span&gt;&lt;b&gt;${b.available_quantity} available&lt;/b&gt;&lt;/div&gt;&lt;button class=&quot;button small primary&quot; data-reserve=&quot;${b.book_id}&quot; ${enabled ? &quot;&quot; : &quot;disabled&quot;}&gt;${label}&lt;/button&gt;&lt;/article&gt;`;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 52 | <code>            })</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 53 | <code>            .join(&quot;&quot;)</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 54 | <code>        : &#x27;&lt;div class=&quot;empty-state&quot;&gt;&lt;strong&gt;No matching books&lt;/strong&gt;&lt;span&gt;Try another title, author or category.&lt;/span&gt;&lt;/div&gt;&#x27;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 55 | <code>      $$(&quot;[data-reserve]&quot;).forEach((button) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 56 | <code>        button.onclick = () =&gt;</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 57 | <code>          action(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 58 | <code>            button,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 59 | <code>            &quot;/reservations&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 60 | <code>            { bookId: button.dataset.reserve },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 61 | <code>            &quot;Reserve this copy for 3 days?&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 62 | <code>          );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 63 | <code>      });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 64 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 65 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 66 | <code>    function renderStudent() {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 67 | <code>      const data = getData();</code> | Local state, DOM reference বা callback/result assign করে। |
| 68 | <code>      if (!data) return;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 69 | <code>      $(&quot;#memberName&quot;).textContent = `Welcome, ${data.member.name}`;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 70 | <code>      $(&quot;#memberIdentity&quot;).textContent =</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 71 | <code>        `${memberId(data.member.student_id)} · Roll: ${data.member.roll_no &#124;&#124; &quot;Not assigned&quot;} · Registration: ${data.member.registration_no &#124;&#124; &quot;Not assigned&quot;}`;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 72 | <code>      const loans = data.issues.filter((i) =&gt; i.status === &quot;ISSUED&quot;);</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 73 | <code>      const active = data.reservations.filter((r) =&gt; r.status === &quot;ACTIVE&quot;);</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 74 | <code>      const outstanding =</code> | Local state, DOM reference বা callback/result assign করে। |
| 75 | <code>        data.fines.reduce((sum, f) =&gt; sum + Number(f.balance &#124;&#124; 0), 0) +</code> | Local state, DOM reference বা callback/result assign করে। |
| 76 | <code>        loans</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 77 | <code>          .filter((i) =&gt; !data.fines.some((f) =&gt; f.issue_id === i.issue_id))</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 78 | <code>          .reduce((sum, i) =&gt; sum + Number(i.current_fine &#124;&#124; 0), 0);</code> | Local state, DOM reference বা callback/result assign করে। |
| 79 | <code>      $(&quot;#studentStats&quot;).innerHTML = [</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 80 | <code>        [&quot;Books on loan&quot;, loans.length, &quot;Your current reading&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 81 | <code>        [&quot;Active reservations&quot;, active.length, &quot;Held for 3 days&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 82 | <code>        [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 83 | <code>          &quot;Outstanding + overdue estimate&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 84 | <code>          money(outstanding),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 85 | <code>          &quot;Updates daily · Tk 10/day until return&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 86 | <code>        ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 87 | <code>        [&quot;Titles to explore&quot;, data.books.length, &quot;Browse the full collection&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 88 | <code>      ]</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 89 | <code>        .map(</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 90 | <code>          ([label, value, note]) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 91 | <code>            `&lt;article class=&quot;member-stat&quot;&gt;&lt;span&gt;${label}&lt;/span&gt;&lt;strong&gt;${value}&lt;/strong&gt;&lt;small&gt;${note}&lt;/small&gt;&lt;/article&gt;`,</code> | Local state, DOM reference বা callback/result assign করে। |
| 92 | <code>        )</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 93 | <code>        .join(&quot;&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 94 | <code>      // The panel mirrors the bell, using only the member-scoped dashboard response.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 95 | <code>      if ($(&quot;#memberAlerts&quot;) &amp;&amp; window.LibraryNotifications) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 96 | <code>        const alerts = window.LibraryNotifications.buildItems(data, {</code> | Local state, DOM reference বা callback/result assign করে। |
| 97 | <code>          user_type: &quot;STUDENT&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 98 | <code>          student_id: data.member.student_id,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 99 | <code>        });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 100 | <code>        const reminders = alerts.filter((item) =&gt; item.type === &quot;due&quot; &#124;&#124; item.type === &quot;fine&quot;);</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 101 | <code>        $(&quot;#memberAlerts&quot;).innerHTML = reminders.length</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 102 | <code>          ? reminders</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 103 | <code>              .map(</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 104 | <code>                (item) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 105 | <code>                  `&lt;a class=&quot;member-reminder ${item.type}&quot; href=&quot;${item.href}&quot;&gt;&lt;span class=&quot;visit-mark&quot;&gt;${item.type === &quot;due&quot; ? &quot;DUE&quot; : &quot;FINE&quot;}&lt;/span&gt;&lt;div&gt;&lt;strong&gt;${e(item.title)}&lt;/strong&gt;&lt;span&gt;${e(item.detail)}&lt;/span&gt;&lt;small&gt;${e(item.note)}&lt;/small&gt;&lt;/div&gt;&lt;b aria-hidden=&quot;true&quot;&gt;&amp;rarr;&lt;/b&gt;&lt;/a&gt;`,</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 106 | <code>              )</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 107 | <code>              .join(&quot;&quot;)</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 108 | <code>          : &#x27;&lt;div class=&quot;member-reminder clear&quot;&gt;&lt;span class=&quot;visit-mark&quot;&gt;OK&lt;/span&gt;&lt;div&gt;&lt;strong&gt;No upcoming return reminders or unpaid fines&lt;/strong&gt;&lt;small&gt;Reminders appear 3 days before your return date.&lt;/small&gt;&lt;/div&gt;&lt;/div&gt;&#x27;;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 109 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 110 | <code>      const nextLoan = [...loans]</code> | Local state, DOM reference বা callback/result assign করে। |
| 111 | <code>        .filter((i) =&gt; i.due_date)</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 112 | <code>        .sort((a, b) =&gt; a.due_date.localeCompare(b.due_date))[0];</code> | Local state, DOM reference বা callback/result assign করে। |
| 113 | <code>      const nextHold = [...active]</code> | Local state, DOM reference বা callback/result assign করে। |
| 114 | <code>        .filter((r) =&gt; r.expires_at)</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 115 | <code>        .sort((a, b) =&gt; a.expires_at.localeCompare(b.expires_at))[0];</code> | Local state, DOM reference বা callback/result assign করে। |
| 116 | <code>      const nextSteps = [];</code> | Local state, DOM reference বা callback/result assign করে। |
| 117 | <code>      if (nextLoan)</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 118 | <code>        nextSteps.push(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 119 | <code>          `&lt;div class=&quot;next-visit-item&quot;&gt;&lt;span class=&quot;visit-mark&quot;&gt;RET&lt;/span&gt;&lt;div&gt;&lt;strong&gt;${e(nextLoan.title)}&lt;/strong&gt;&lt;small&gt;${Number(nextLoan.overdue_days) &gt; 0 ? &quot;Overdue · due&quot; : &quot;Return by&quot;} ${e(nextLoan.due_date)}&lt;/small&gt;&lt;/div&gt;&lt;a href=&quot;#loans&quot;&gt;View loan &amp;rarr;&lt;/a&gt;&lt;/div&gt;`,</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 120 | <code>        );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 121 | <code>      if (nextHold)</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 122 | <code>        nextSteps.push(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 123 | <code>          `&lt;div class=&quot;next-visit-item&quot;&gt;&lt;span class=&quot;visit-mark&quot;&gt;HOLD&lt;/span&gt;&lt;div&gt;&lt;strong&gt;${e(nextHold.title)}&lt;/strong&gt;&lt;small&gt;Collect before ${e(nextHold.expires_at)}&lt;/small&gt;&lt;/div&gt;&lt;a href=&quot;#reservations&quot;&gt;View hold &amp;rarr;&lt;/a&gt;&lt;/div&gt;`,</code> | Local state, DOM reference বা callback/result assign করে। |
| 124 | <code>        );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 125 | <code>      $(&quot;#memberNextStep&quot;).innerHTML = nextSteps.length</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 126 | <code>        ? nextSteps.join(&quot;&quot;)</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 127 | <code>        : &#x27;&lt;p class=&quot;section-description&quot;&gt;No upcoming returns or pickups. Find something new in the catalogue and reserve your next read.&lt;/p&gt;&lt;div class=&quot;next-visit-item&quot;&gt;&lt;span class=&quot;visit-mark&quot;&gt;READ&lt;/span&gt;&lt;div&gt;&lt;strong&gt;Your next chapter is waiting.&lt;/strong&gt;&lt;small&gt;Explore books by title, author or category.&lt;/small&gt;&lt;/div&gt;&lt;a href=&quot;#catalogue&quot;&gt;Discover &amp;rarr;&lt;/a&gt;&lt;/div&gt;&#x27;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 128 | <code>      reservationTable(data.reservations);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 129 | <code>      const loanSelection = $(&quot;#loanFilter&quot;)?.value &#124;&#124; &quot;all&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 130 | <code>      const visibleLoans = (</code> | Local state, DOM reference বা callback/result assign করে। |
| 131 | <code>        context.sortIssues ? context.sortIssues(data.issues) : data.issues</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 132 | <code>      ).filter(</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 133 | <code>        (i) =&gt; ![&quot;ISSUED&quot;, &quot;RETURNED&quot;].includes(loanSelection) &#124;&#124; i.status === loanSelection,</code> | Local state, DOM reference বা callback/result assign করে। |
| 134 | <code>      );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 135 | <code>      $(&quot;#loanTable&quot;).innerHTML = table(</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 136 | <code>        [&quot;Book&quot;, &quot;Copy&quot;, &quot;Issued&quot;, &quot;Due date&quot;, &quot;Return date&quot;, &quot;Status&quot;, &quot;Overdue fine estimate&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 137 | <code>        visibleLoans.map(</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 138 | <code>          (i) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 139 | <code>            `&lt;tr&gt;&lt;td&gt;&lt;b&gt;${e(i.title)}&lt;/b&gt;&lt;/td&gt;&lt;td&gt;${i.copy_no ? `Copy #${i.copy_no}` : &quot;Legacy copy&quot;}&lt;/td&gt;&lt;td&gt;${e(i.issue_date)}&lt;/td&gt;&lt;td&gt;${e(i.due_date)}&lt;/td&gt;&lt;td&gt;${e(i.return_date &#124;&#124; &quot;Awaiting return&quot;)}&lt;/td&gt;&lt;td&gt;&lt;span class=&quot;pill ${i.status === &quot;ISSUED&quot; &amp;&amp; Number(i.overdue_days) &gt; 0 ? &quot;overdue&quot; : String(i.status).toLowerCase()}&quot;&gt;${i.status === &quot;ISSUED&quot; &amp;&amp; Number(i.overdue_days) &gt; 0 ? &quot;OVERDUE&quot; : e(i.status)}&lt;/span&gt;&lt;/td&gt;&lt;td&gt;${money(i.current_fine)}&lt;/td&gt;&lt;/tr&gt;`,</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 140 | <code>        ),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 141 | <code>      );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 142 | <code>      $(&quot;#studentFineTable&quot;).innerHTML = table(</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 143 | <code>        [&quot;Book&quot;, &quot;Fine&quot;, &quot;Received&quot;, &quot;Outstanding&quot;, &quot;Status&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 144 | <code>        [...data.fines]</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 145 | <code>          .sort(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 146 | <code>            (a, b) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 147 | <code>              Number(Number(b.balance) &gt; 0) - Number(Number(a.balance) &gt; 0) &#124;&#124;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 148 | <code>              Number(b.balance &#124;&#124; 0) - Number(a.balance &#124;&#124; 0),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 149 | <code>          )</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 150 | <code>          .map(</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 151 | <code>            (f) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 152 | <code>              `&lt;tr&gt;&lt;td&gt;${e(f.title)}&lt;/td&gt;&lt;td&gt;${money(f.amount)}&lt;/td&gt;&lt;td&gt;${money(f.paid_amount)}&lt;/td&gt;&lt;td&gt;${money(f.balance)}&lt;/td&gt;&lt;td&gt;${e(f.payment_status)}&lt;/td&gt;&lt;/tr&gt;`,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 153 | <code>          ),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 154 | <code>      );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 155 | <code>      if (!visibleLoans.length)</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 156 | <code>        $(&quot;#loanTable&quot;).innerHTML =</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 157 | <code>          &#x27;&lt;div class=&quot;empty-state&quot;&gt;&lt;strong&gt;No books in this view.&lt;/strong&gt;&lt;span&gt;Your borrowed books and return dates will appear here.&lt;/span&gt;&lt;/div&gt;&#x27;;</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 158 | <code>      if (!data.fines.length)</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 159 | <code>        $(&quot;#studentFineTable&quot;).innerHTML =</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 160 | <code>          &#x27;&lt;div class=&quot;empty-state&quot;&gt;&lt;strong&gt;No recorded fines.&lt;/strong&gt;&lt;span&gt;Return your books by their due dates to keep it that way.&lt;/span&gt;&lt;/div&gt;&#x27;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 161 | <code>      catalogue();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 162 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 163 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 164 | <code>    function bind() {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 165 | <code>      $(&quot;#bookSearch&quot;).oninput = catalogue;</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 166 | <code>      if ($(&quot;#availabilityFilter&quot;)) $(&quot;#availabilityFilter&quot;).onchange = catalogue;</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 167 | <code>      if ($(&quot;#loanFilter&quot;)) $(&quot;#loanFilter&quot;).onchange = renderStudent;</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 168 | <code>      $(&quot;#studentPasswordForm&quot;).onsubmit = async (event) =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 169 | <code>        event.preventDefault();</code> | Default form navigation বন্ধ করে controlled API submission চালাতে দেয়। |
| 170 | <code>        const form = event.currentTarget;</code> | Local state, DOM reference বা callback/result assign করে। |
| 171 | <code>        if (await action($(&quot;button&quot;, form), &quot;/student/password&quot;, new FormData(form)))</code> | Form fields বা filters URL-encoded request body/query parameters-এ রূপান্তর করে। |
| 172 | <code>          window.location.replace(&quot;/login&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 173 | <code>      };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 174 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 175 | <code>    return { render: renderStudent, bind };</code> | Current callback/function result ফেরায় অথবা branch early-exit করে। |
| 176 | <code>  },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 177 | <code>};</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
