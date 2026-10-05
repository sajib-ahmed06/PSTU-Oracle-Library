# frontend/fines.js

Overdue loans, Oracle-calculated daily fine estimates, Return book actions, return/payment history and combined outstanding totals; paid fines excluded and issues never counted twice.

Source: [মূল file](../../frontend/fines.js)। Snapshot 2026-10-04; 216 lines; SHA-256 `68652c2588013427d19c4c21d252ed6bd0864071b8cf8cb093919a35865bf399`।

## Function / object / element inventory

### `memberCell(id, name)` — L11

Render internal member ID, name, academic roll and registration for a fine/overdue row.

### `render()` — L16

এই page-এর current state ও search/filter থেকে tables/metrics/options তৈরি করে, DOM update করে এবং generated action buttons-এর events bind করে। পাশের পূর্ণ code-এ page-specific fields দেখা যাবে।

### `performAction(button, path, confirmation, message)` — L155

Confirm and execute one return/payment POST, disable its button while pending, reload live data and restore the button on completion.

### `renderCollection()` — L173

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

## সম্পূর্ণ original source

```javascript
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
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>(() =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 2 | <code>  const { $, $$, state, escapeHtml, memberId, table, toast, api, loadData, openModal, closeModal } =</code> | Local state, DOM reference বা callback/result assign করে। |
| 3 | <code>    LibraryApp;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 4 | <code>  const money = (value) =&gt; `Tk ${Number(value).toLocaleString(&quot;en-BD&quot;)}`;</code> | Local state, DOM reference বা callback/result assign করে। |
| 5 | <code>  const cents = (value) =&gt; Math.round(Number(value &#124;&#124; 0) * 100);</code> | Local state, DOM reference বা callback/result assign করে। |
| 6 | <code>  const balance = (fine) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 7 | <code>    fine.balance ??</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 8 | <code>    (fine.payment_status === &quot;PAID&quot; ? 0 : Number(fine.amount) - Number(fine.paid_amount &#124;&#124; 0));</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 9 | <code>  const copyLabel = (issue) =&gt; (issue?.copy_no ? `Copy #${issue.copy_no}` : &quot;Legacy copy&quot;);</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 10 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 11 | <code>  function memberCell(id, name) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 12 | <code>    const member = state.students.find((student) =&gt; student.student_id === id);</code> | Local state, DOM reference বা callback/result assign করে। |
| 13 | <code>    return `&lt;td&gt;&lt;span class=&quot;member-id&quot;&gt;${memberId(id)}&lt;/span&gt;&lt;/td&gt;&lt;td&gt;&lt;b&gt;${escapeHtml(name)}&lt;/b&gt;&lt;small class=&quot;audit-record-id&quot;&gt;Roll: ${escapeHtml(member?.roll_no &#124;&#124; &quot;Not assigned&quot;)} / Reg: ${escapeHtml(member?.registration_no &#124;&#124; &quot;Not assigned&quot;)}&lt;/small&gt;&lt;/td&gt;`;</code> | User/database values escaped display markup-এ রূপান্তর করে। |
| 14 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 15 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 16 | <code>  async function render() {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 17 | <code>    const overdue = state.issues</code> | Local state, DOM reference বা callback/result assign করে। |
| 18 | <code>      .filter((issue) =&gt; issue.status === &quot;ISSUED&quot; &amp;&amp; Number(issue.overdue_days) &gt; 0)</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 19 | <code>      .sort(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 20 | <code>        (a, b) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 21 | <code>          Number(b.overdue_days) - Number(a.overdue_days) &#124;&#124;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 22 | <code>          Number(b.current_fine &#124;&#124; 0) - Number(a.current_fine &#124;&#124; 0),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 23 | <code>      );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 24 | <code>    const unpaid = state.fines.filter((fine) =&gt; fine.payment_status === &quot;UNPAID&quot;);</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 25 | <code>    const unpaidAmount = unpaid.reduce((sum, fine) =&gt; sum + cents(balance(fine)), 0) / 100;</code> | Local state, DOM reference বা callback/result assign করে। |
| 26 | <code>    // Fines normally exist only after return; never count a recorded issue twice.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 27 | <code>    const recordedIssues = new Set(state.fines.map((fine) =&gt; fine.issue_id));</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 28 | <code>    const overdueAmount = overdue.reduce(</code> | Local state, DOM reference বা callback/result assign করে। |
| 29 | <code>      (sum, issue) =&gt; sum + (recordedIssues.has(issue.issue_id) ? 0 : Number(issue.current_fine)),</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 30 | <code>      0,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 31 | <code>    );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 32 | <code>    const metrics = [</code> | Local state, DOM reference বা callback/result assign করে। |
| 33 | <code>      [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 34 | <code>        &quot;Total outstanding&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 35 | <code>        unpaidAmount + overdueAmount,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 36 | <code>        &quot;Unpaid fines + overdue estimates&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 37 | <code>        &quot;red&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 38 | <code>      ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 39 | <code>      [&quot;Overdue fine estimate&quot;, overdueAmount, `${overdue.length} books awaiting return`, &quot;gold&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 40 | <code>      [&quot;Recorded unpaid fines&quot;, unpaidAmount, `${unpaid.length} unpaid records`, &quot;green&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 41 | <code>    ];</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 42 | <code>    $(&quot;#fineSummary&quot;).innerHTML = metrics</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 43 | <code>      .map(</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 44 | <code>        ([label, amount, note, tone]) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 45 | <code>          `&lt;article class=&quot;metric ${tone}&quot;&gt;&lt;span&gt;${label}&lt;/span&gt;&lt;strong&gt;${money(amount)}&lt;/strong&gt;&lt;small&gt;${note}&lt;/small&gt;&lt;/article&gt;`,</code> | Local state, DOM reference বা callback/result assign করে। |
| 46 | <code>      )</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 47 | <code>      .join(&quot;&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 48 | <code>    $(&quot;#overdueTotal&quot;).textContent = `${overdue.length} overdue books / ${money(overdueAmount)}`;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 49 | <code>    $(&quot;#overdueTable&quot;).innerHTML = overdue.length</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 50 | <code>      ? table(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 51 | <code>          [&quot;Member ID&quot;, &quot;Student&quot;, &quot;Book&quot;, &quot;Due date&quot;, &quot;Overdue days&quot;, &quot;Fine today&quot;, &quot;Return&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 52 | <code>          overdue.map(</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 53 | <code>            (issue) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 54 | <code>              `&lt;tr&gt;${memberCell(issue.student_id, issue.student)}&lt;td&gt;&lt;b&gt;${escapeHtml(issue.title)}&lt;/b&gt;&lt;small class=&quot;audit-record-id&quot;&gt;${copyLabel(issue)}&lt;/small&gt;&lt;/td&gt;&lt;td&gt;${escapeHtml(issue.due_date)}&lt;/td&gt;&lt;td&gt;&lt;span class=&quot;pill overdue&quot;&gt;${issue.overdue_days} days&lt;/span&gt;&lt;/td&gt;&lt;td&gt;&lt;b&gt;${money(issue.current_fine)}&lt;/b&gt;&lt;/td&gt;&lt;td&gt;&lt;button class=&quot;button small primary&quot; data-fine-return=&quot;${issue.issue_id}&quot;&gt;Return book&lt;/button&gt;&lt;/td&gt;&lt;/tr&gt;`,</code> | User/database values escaped display markup-এ রূপান্তর করে। |
| 55 | <code>          ),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 56 | <code>        )</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 57 | <code>      : &#x27;&lt;div class=&quot;empty-state&quot;&gt;&lt;strong&gt;No overdue books&lt;/strong&gt;&lt;span&gt;All current loans are within their due dates.&lt;/span&gt;&lt;/div&gt;&#x27;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 58 | <code>    const paidCount = state.fines.filter((fine) =&gt; fine.payment_status === &quot;PAID&quot;).length;</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 59 | <code>    $(&quot;#fineTotal&quot;).textContent = `${state.fines.length} fine records / ${paidCount} paid`;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 60 | <code>    $(&quot;#fineTable&quot;).innerHTML = table(</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 61 | <code>      [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 62 | <code>        &quot;Member ID&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 63 | <code>        &quot;Student&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 64 | <code>        &quot;Book / copy&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 65 | <code>        &quot;Return date&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 66 | <code>        &quot;Fine&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 67 | <code>        &quot;Received&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 68 | <code>        &quot;Remaining&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 69 | <code>        &quot;Payment&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 70 | <code>        &quot;Action&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 71 | <code>      ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 72 | <code>      [...state.fines]</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 73 | <code>        .sort(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 74 | <code>          (a, b) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 75 | <code>            Number(balance(b) &gt; 0) - Number(balance(a) &gt; 0) &#124;&#124;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 76 | <code>            Number(balance(b)) - Number(balance(a)) &#124;&#124;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 77 | <code>            Number(b.fine_id) - Number(a.fine_id),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 78 | <code>        )</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 79 | <code>        .map((fine) =&gt; {</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 80 | <code>          const issue = state.issues.find((item) =&gt; item.issue_id === fine.issue_id);</code> | Local state, DOM reference বা callback/result assign করে। |
| 81 | <code>          const paid = fine.paid_amount ?? (fine.payment_status === &quot;PAID&quot; ? fine.amount : 0);</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 82 | <code>          const status = balance(fine) &gt; 0 &amp;&amp; Number(paid) &gt; 0 ? &quot;PARTIAL&quot; : fine.payment_status;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 83 | <code>          return `&lt;tr&gt;${memberCell(fine.student_id, fine.student)}&lt;td&gt;&lt;b&gt;${escapeHtml(fine.title)}&lt;/b&gt;&lt;small class=&quot;audit-record-id&quot;&gt;${copyLabel(issue)}&lt;/small&gt;&lt;/td&gt;&lt;td&gt;${escapeHtml(issue?.return_date &#124;&#124; &quot;Not returned&quot;)}&lt;/td&gt;&lt;td&gt;&lt;b&gt;${money(fine.amount)}&lt;/b&gt;&lt;/td&gt;&lt;td&gt;${money(paid)}&lt;/td&gt;&lt;td&gt;&lt;b&gt;${money(balance(fine))}&lt;/b&gt;&lt;/td&gt;&lt;td&gt;&lt;span class=&quot;pill ${status === &quot;PARTIAL&quot; ? &quot;unpaid&quot; : status.toLowerCase()}&quot;&gt;${status}&lt;/span&gt;&lt;/td&gt;&lt;td&gt;${balance(fine) &gt; 0 ? `&lt;button class=&quot;button small primary&quot; data-pay=&quot;${fine.fine_id}&quot;&gt;Pay full fine&lt;/button&gt;` : &#x27;&lt;span class=&quot;complete-text&quot;&gt;Completed&lt;/span&gt;&#x27;} &lt;button class=&quot;button small secondary&quot; data-history=&quot;${fine.fine_id}&quot;&gt;Receipts&lt;/button&gt;&lt;/td&gt;&lt;/tr&gt;`;</code> | User/database values escaped display markup-এ রূপান্তর করে। |
| 84 | <code>        }),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 85 | <code>    );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 86 | <code>    $$(&quot;[data-pay]&quot;).forEach((button) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 87 | <code>      button.onclick = () =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 88 | <code>        const fine = state.fines.find((item) =&gt; item.fine_id == button.dataset.pay);</code> | Local state, DOM reference বা callback/result assign করে। |
| 89 | <code>        const form = $(&quot;#paymentModal form&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 90 | <code>        form.elements.fineId.value = fine.fine_id;</code> | Local state, DOM reference বা callback/result assign করে। |
| 91 | <code>        $(&quot;#paymentBalance&quot;).textContent =</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 92 | <code>          `${fine.student} / ${fine.title} / ${money(balance(fine))} remaining`;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 93 | <code>        openModal(&quot;paymentModal&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 94 | <code>      };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 95 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 96 | <code>    $$(&quot;[data-history]&quot;).forEach((button) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 97 | <code>      button.onclick = async () =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 98 | <code>        $(&quot;#paymentHistory&quot;).textContent = &quot;Loading receipts...&quot;;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 99 | <code>        openModal(&quot;paymentHistoryModal&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 100 | <code>        try {</code> | Async failure handling ও UI cleanup/restore block। |
| 101 | <code>          const payments = await api(`/fines/${button.dataset.history}/payments`);</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 102 | <code>          $(&quot;#paymentHistory&quot;).innerHTML = payments.length</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 103 | <code>            ? table(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 104 | <code>                [&quot;Receipt&quot;, &quot;Date&quot;, &quot;Amount&quot;, &quot;Received by&quot;, &quot;Note&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 105 | <code>                payments.map(</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 106 | <code>                  (item) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 107 | <code>                    `&lt;tr&gt;&lt;td&gt;${item.payment_id}&lt;/td&gt;&lt;td&gt;${escapeHtml(item.paid_at)}&lt;/td&gt;&lt;td&gt;${money(item.amount)}&lt;/td&gt;&lt;td&gt;${escapeHtml(item.actor)}&lt;/td&gt;&lt;td&gt;${escapeHtml(item.note &#124;&#124; &quot;—&quot;)}&lt;/td&gt;&lt;/tr&gt;`,</code> | User/database values escaped display markup-এ রূপান্তর করে। |
| 108 | <code>                ),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 109 | <code>              )</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 110 | <code>            : &quot;&lt;p&gt;There are no receipts for this fine. Payments made before this feature are included in the received total.&lt;/p&gt;&quot;;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 111 | <code>        } catch (error) {</code> | Async failure handling ও UI cleanup/restore block। |
| 112 | <code>          $(&quot;#paymentHistory&quot;).textContent = error.message;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 113 | <code>        }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 114 | <code>      };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 115 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 116 | <code>    $$(&quot;[data-fine-return]&quot;).forEach((button) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 117 | <code>      button.onclick = () =&gt;</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 118 | <code>        performAction(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 119 | <code>          button,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 120 | <code>          `/issues/${button.dataset.fineReturn}/return`,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 121 | <code>          &quot;Return this overdue book and record its final fine?&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 122 | <code>          &quot;Book returned. Final fine is shown below&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 123 | <code>        );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 124 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 125 | <code>    await renderCollection();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 126 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 127 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 128 | <code>  const paymentForm = $(&quot;#paymentModal form&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 129 | <code>  if (paymentForm?.elements) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 130 | <code>    paymentForm.onsubmit = async (event) =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 131 | <code>      event.preventDefault();</code> | Default form navigation বন্ধ করে controlled API submission চালাতে দেয়। |
| 132 | <code>      if (!state.online) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 133 | <code>        toast(&quot;Connect to the database before making changes&quot;, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 134 | <code>        return;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 135 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 136 | <code>      const button = $(&quot;button:not([type=&#x27;button&#x27;])&quot;, paymentForm);</code> | Local state, DOM reference বা callback/result assign করে। |
| 137 | <code>      if (button.disabled) return;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 138 | <code>      button.disabled = true;</code> | Local state, DOM reference বা callback/result assign করে। |
| 139 | <code>      try {</code> | Async failure handling ও UI cleanup/restore block। |
| 140 | <code>        await api(`/fines/${paymentForm.elements.fineId.value}/pay`, {</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 141 | <code>          method: &quot;POST&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 142 | <code>          body: new URLSearchParams({ note: paymentForm.elements.note.value }),</code> | Form fields বা filters URL-encoded request body/query parameters-এ রূপান্তর করে। |
| 143 | <code>        });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 144 | <code>        closeModal($(&quot;#paymentModal&quot;));</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 145 | <code>        toast(&quot;Fine paid in full&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 146 | <code>        await loadData(render);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 147 | <code>      } catch (error) {</code> | Async failure handling ও UI cleanup/restore block। |
| 148 | <code>        toast(error.message, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 149 | <code>      } finally {</code> | Async failure handling ও UI cleanup/restore block। |
| 150 | <code>        button.disabled = false;</code> | Local state, DOM reference বা callback/result assign করে। |
| 151 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 152 | <code>    };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 153 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 154 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 155 | <code>  async function performAction(button, path, confirmation, message) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 156 | <code>    if (button.disabled &#124;&#124; !confirm(confirmation)) return;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 157 | <code>    if (!state.online) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 158 | <code>      toast(&quot;Connect to the database before making changes&quot;, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 159 | <code>      return;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 160 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 161 | <code>    button.disabled = true;</code> | Local state, DOM reference বা callback/result assign করে। |
| 162 | <code>    try {</code> | Async failure handling ও UI cleanup/restore block। |
| 163 | <code>      await api(path, { method: &quot;POST&quot; });</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 164 | <code>      toast(message);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 165 | <code>      await loadData(render);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 166 | <code>    } catch (error) {</code> | Async failure handling ও UI cleanup/restore block। |
| 167 | <code>      toast(error.message, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 168 | <code>    } finally {</code> | Async failure handling ও UI cleanup/restore block। |
| 169 | <code>      button.disabled = false;</code> | Local state, DOM reference বা callback/result assign করে। |
| 170 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 171 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 172 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 173 | <code>  async function renderCollection() {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 174 | <code>    const container = $(&quot;#fineCollection&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 175 | <code>    container.innerHTML = &#x27;&lt;div class=&quot;form-note&quot;&gt;Loading fine collection…&lt;/div&gt;&#x27;;</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 176 | <code>    try {</code> | Async failure handling ও UI cleanup/restore block। |
| 177 | <code>      const collection = await api(&quot;/fines/collection-summary&quot;);</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 178 | <code>      const metrics = [</code> | Local state, DOM reference বা callback/result assign করে। |
| 179 | <code>        [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 180 | <code>          &quot;Total fine collection&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 181 | <code>          collection.total,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 182 | <code>          &quot;All recorded payments, including legacy balances&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 183 | <code>          &quot;green&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 184 | <code>        ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 185 | <code>        [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 186 | <code>          &quot;Today’s fine collection&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 187 | <code>          collection.today,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 188 | <code>          `Receipts on ${collection.date} · Asia/Dhaka`,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 189 | <code>          &quot;blue&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 190 | <code>        ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 191 | <code>        [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 192 | <code>          &quot;Monthly fine collection&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 193 | <code>          collection.month,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 194 | <code>          `Current month: ${collection.month_start.slice(0, 7)}`,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 195 | <code>          &quot;gold&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 196 | <code>        ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 197 | <code>      ];</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 198 | <code>      container.innerHTML = metrics</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 199 | <code>        .map(</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 200 | <code>          ([label, value, note, tone]) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 201 | <code>            `&lt;article class=&quot;metric ${tone}&quot;&gt;&lt;span&gt;${label}&lt;/span&gt;&lt;strong&gt;${money(value)}&lt;/strong&gt;&lt;small&gt;${note}&lt;/small&gt;&lt;/article&gt;`,</code> | Local state, DOM reference বা callback/result assign করে। |
| 202 | <code>        )</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 203 | <code>        .join(&quot;&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 204 | <code>    } catch (error) {</code> | Async failure handling ও UI cleanup/restore block। |
| 205 | <code>      container.innerHTML =</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 206 | <code>        &#x27;&lt;div class=&quot;empty-state&quot;&gt;&lt;strong&gt;Collection totals unavailable&lt;/strong&gt;&lt;span&gt;Refresh after the database connection is restored.&lt;/span&gt;&lt;/div&gt;&#x27;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 207 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 208 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 209 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 210 | <code>  $(&quot;#refreshButton&quot;).onclick = () =&gt; loadData(render);</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 211 | <code>  // Oracle recalculates today&#x27;s estimate; keep an open page current as days change.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 212 | <code>  window.setInterval(() =&gt; {</code> | Timeout/reconnection/search debounce timer শুরু বা বন্ধ করে। |
| 213 | <code>    if (!document.hidden) loadData(render);</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 214 | <code>  }, 60000);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 215 | <code>  loadData(render);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 216 | <code>})();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
