# frontend/circulation.js

Eligible member search, available book selection, issuing, return এবং loan status filter পরিচালনা করে।

Source: [মূল file](../../frontend/circulation.js)। Snapshot 2026-10-04; 181 lines; SHA-256 `120b033d3594c2ffe735deec9c2fd1cf7107ed32b291f69af49e2e9ec34cd80b`।

## Function / object / element inventory

### `eligibleStudents()` — L21

ACTIVE members-এর মধ্যে active loan বা unpaid fine নেই এমন members নির্বাচন করে। Database procedure আবার একই rules enforce করে।

### `renderMembers(query = "")` — L36

Eligible members-এর name/internal ID/roll/reg search করে select options render করে; no match হলে empty option।

### `updateAllowance()` — L57

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

### `renderCopies(suffix = "")` — L67

Local function; enclosing page state ও নিচের code অনুযায়ী কাজ করে।

### `render()` — L94

এই page-এর current state ও search/filter থেকে tables/metrics/options তৈরি করে, DOM update করে এবং generated action buttons-এর events bind করে। পাশের পূর্ণ code-এ page-specific fields দেখা যাবে।

### `returnBook(id)` — L120

Confirmation-এর পরে return API call ও refreshed data render করে।

## সম্পূর্ণ original source

```javascript
(() => {
  const {
    $,
    $$,
    state,
    escapeHtml,
    memberId,
    toast,
    api,
    loadData,
    sortIssues,
    issueRows,
    dateFromToday,
    postForm,
    openRequestedModal,
  } = LibraryApp;

  const heldCount = (id) =>
    (state.reservations || []).filter((r) => r.student_id == id && r.status === "ACTIVE").length;

  function eligibleStudents() {
    return state.students.filter(
      (student) =>
        (student.membership_status || "ACTIVE") === "ACTIVE" &&
        state.issues.filter(
          (issue) => issue.student_id == student.student_id && issue.status === "ISSUED",
        ).length +
          heldCount(student.student_id) <
          3 &&
        !state.fines.some(
          (fine) => fine.student_id == student.student_id && fine.payment_status === "UNPAID",
        ),
    );
  }

  function renderMembers(query = "") {
    const eligible = eligibleStudents();
    const search = query.trim().toLowerCase();
    const matches = eligible.filter((student) =>
      `${memberId(student.student_id)} ${student.roll_no || ""} ${student.registration_no || ""} ${student.name} ${student.department}`
        .toLowerCase()
        .includes(search),
    );
    $("#studentOptions").innerHTML = matches.length
      ? matches
          .map(
            (student) =>
              `<option value="${student.student_id}">${memberId(student.student_id)} / Roll: ${escapeHtml(student.roll_no || "Not assigned")} / Reg: ${escapeHtml(student.registration_no || "Not assigned")} - ${escapeHtml(student.name)} (${escapeHtml(student.department)})</option>`,
          )
          .join("")
      : '<option value="">No matching eligible member</option>';
    $("#eligibilityNote").textContent =
      `${matches.length} of ${eligible.length} eligible members shown`;
    updateAllowance();
  }

  function updateAllowance() {
    const id = $("#studentOptions").value;
    const count = state.issues.filter(
      (issue) => issue.student_id == id && issue.status === "ISSUED",
    ).length;
    $("#loanAllowance").textContent =
      `${count} copies currently borrowed. You can issue up to ${3 - count - heldCount(id)} more, with ${heldCount(id)} active reservations. Use Reservations to issue a held copy.`;
  }

  const copyRequests = {};
  async function renderCopies(suffix = "") {
    const book = $(`#bookOptions${suffix}`);
    const copy = $(`#copyOptions${suffix}`);
    const version = (copyRequests[suffix] = (copyRequests[suffix] || 0) + 1);
    copy.innerHTML = '<option value="">Loading copies...</option>';
    copy.disabled = true;
    if (!book.value) {
      copy.innerHTML = '<option value="">Select a book first</option>';
      return;
    }
    try {
      const copies = await api(`/books/${book.value}/copies`);
      if (version !== copyRequests[suffix]) return;
      copy.innerHTML =
        copies
          .filter((item) => item.status === "AVAILABLE")
          .map((item) => `<option value="${item.copy_id}">Copy #${item.copy_no}</option>`)
          .join("") || '<option value="">No available copies</option>';
      copy.disabled = false;
    } catch (error) {
      if (version === copyRequests[suffix]) {
        copy.innerHTML = '<option value="">Unable to load copies</option>';
        toast(error.message, true);
      }
    }
  }

  function render() {
    const filter = $("#issueFilter").value;
    const issues = sortIssues(
      filter === "ALL" ? state.issues : state.issues.filter((issue) => issue.status === filter),
    );
    $("#issueCount").textContent = `${issues.length} ${issues.length === 1 ? "record" : "records"}`;
    $("#issueTable").innerHTML = issueRows(issues, true);
    $("#bookOptions").innerHTML = state.books
      .filter((book) => book.available_quantity > 0)
      .map(
        (book) =>
          `<option value="${book.book_id}">${escapeHtml(book.title)} (${book.available_quantity} available)</option>`,
      )
      .join("");
    for (const suffix of ["2", "3"]) {
      $(`#bookOptions${suffix}`).innerHTML =
        '<option value="">No additional book</option>' + $("#bookOptions").innerHTML;
      renderCopies(suffix);
    }
    renderCopies();
    renderMembers($("#issueMemberSearch").value);
    $$("[data-return]").forEach((button) => {
      button.onclick = () => returnBook(button.dataset.return);
    });
  }

  async function returnBook(id) {
    if (!confirm("Confirm this book return?")) return;
    if (!state.online) {
      toast("Connect to the database before making changes", true);
      return;
    }
    try {
      await api(`/issues/${id}/return`, { method: "POST" });
      toast("Book returned");
      await loadData(render);
    } catch (error) {
      toast(error.message, true);
    }
  }

  const form = $("#issueModal form");
  form.onsubmit = async (event) => {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(form));
    if (!state.online) {
      toast("Connect to the database before making changes", true);
      return;
    }
    const copies = [];
    for (const suffix of ["", "2", "3"]) {
      if (data[`bookId${suffix}`]) {
        if (!data[`copyId${suffix}`]) {
          toast("Select an available copy for each book", true);
          return;
        }
        copies.push(data[`copyId${suffix}`]);
      }
    }
    const active = state.issues.filter(
      (issue) => issue.student_id == data.studentId && issue.status === "ISSUED",
    ).length;
    if (active + heldCount(data.studentId) + copies.length > 3) {
      toast(`This member can borrow ${3 - active - heldCount(data.studentId)} more copies`, true);
      return;
    }
    if (new Set(copies).size !== copies.length) {
      toast("Select different copies for each loan", true);
      return;
    }
    if (await postForm(form, "/issues")) await loadData(render);
  };
  $("#issueFilter").onchange = render;
  $("#issueMemberSearch").oninput = (event) => renderMembers(event.target.value);
  $("#studentOptions").onchange = updateAllowance;
  for (const suffix of ["", "2", "3"])
    $(`#bookOptions${suffix}`).onchange = () => renderCopies(suffix);
  form.addEventListener("reset", () =>
    window.setTimeout(() => {
      for (const suffix of ["", "2", "3"]) renderCopies(suffix);
      updateAllowance();
    }, 0),
  );
  loadData(() => {
    render();
    openRequestedModal("issueModal");
  });
})();
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>(() =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 2 | <code>  const {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 3 | <code>    $,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 4 | <code>    $$,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 5 | <code>    state,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 6 | <code>    escapeHtml,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 7 | <code>    memberId,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 8 | <code>    toast,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 9 | <code>    api,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 10 | <code>    loadData,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 11 | <code>    sortIssues,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 12 | <code>    issueRows,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 13 | <code>    dateFromToday,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 14 | <code>    postForm,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 15 | <code>    openRequestedModal,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 16 | <code>  } = LibraryApp;</code> | Local state, DOM reference বা callback/result assign করে। |
| 17 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 18 | <code>  const heldCount = (id) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 19 | <code>    (state.reservations &#124;&#124; []).filter((r) =&gt; r.student_id == id &amp;&amp; r.status === &quot;ACTIVE&quot;).length;</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 20 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 21 | <code>  function eligibleStudents() {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 22 | <code>    return state.students.filter(</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 23 | <code>      (student) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 24 | <code>        (student.membership_status &#124;&#124; &quot;ACTIVE&quot;) === &quot;ACTIVE&quot; &amp;&amp;</code> | Local state, DOM reference বা callback/result assign করে। |
| 25 | <code>        state.issues.filter(</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 26 | <code>          (issue) =&gt; issue.student_id == student.student_id &amp;&amp; issue.status === &quot;ISSUED&quot;,</code> | Local state, DOM reference বা callback/result assign করে। |
| 27 | <code>        ).length +</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 28 | <code>          heldCount(student.student_id) &lt;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 29 | <code>          3 &amp;&amp;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 30 | <code>        !state.fines.some(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 31 | <code>          (fine) =&gt; fine.student_id == student.student_id &amp;&amp; fine.payment_status === &quot;UNPAID&quot;,</code> | Local state, DOM reference বা callback/result assign করে। |
| 32 | <code>        ),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 33 | <code>    );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 34 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 35 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 36 | <code>  function renderMembers(query = &quot;&quot;) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 37 | <code>    const eligible = eligibleStudents();</code> | Local state, DOM reference বা callback/result assign করে। |
| 38 | <code>    const search = query.trim().toLowerCase();</code> | Local state, DOM reference বা callback/result assign করে। |
| 39 | <code>    const matches = eligible.filter((student) =&gt;</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 40 | <code>      `${memberId(student.student_id)} ${student.roll_no &#124;&#124; &quot;&quot;} ${student.registration_no &#124;&#124; &quot;&quot;} ${student.name} ${student.department}`</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 41 | <code>        .toLowerCase()</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 42 | <code>        .includes(search),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 43 | <code>    );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 44 | <code>    $(&quot;#studentOptions&quot;).innerHTML = matches.length</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 45 | <code>      ? matches</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 46 | <code>          .map(</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 47 | <code>            (student) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 48 | <code>              `&lt;option value=&quot;${student.student_id}&quot;&gt;${memberId(student.student_id)} / Roll: ${escapeHtml(student.roll_no &#124;&#124; &quot;Not assigned&quot;)} / Reg: ${escapeHtml(student.registration_no &#124;&#124; &quot;Not assigned&quot;)} - ${escapeHtml(student.name)} (${escapeHtml(student.department)})&lt;/option&gt;`,</code> | User/database values escaped display markup-এ রূপান্তর করে। |
| 49 | <code>          )</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 50 | <code>          .join(&quot;&quot;)</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 51 | <code>      : &#x27;&lt;option value=&quot;&quot;&gt;No matching eligible member&lt;/option&gt;&#x27;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 52 | <code>    $(&quot;#eligibilityNote&quot;).textContent =</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 53 | <code>      `${matches.length} of ${eligible.length} eligible members shown`;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 54 | <code>    updateAllowance();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 55 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 56 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 57 | <code>  function updateAllowance() {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 58 | <code>    const id = $(&quot;#studentOptions&quot;).value;</code> | Local state, DOM reference বা callback/result assign করে। |
| 59 | <code>    const count = state.issues.filter(</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 60 | <code>      (issue) =&gt; issue.student_id == id &amp;&amp; issue.status === &quot;ISSUED&quot;,</code> | Local state, DOM reference বা callback/result assign করে। |
| 61 | <code>    ).length;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 62 | <code>    $(&quot;#loanAllowance&quot;).textContent =</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 63 | <code>      `${count} copies currently borrowed. You can issue up to ${3 - count - heldCount(id)} more, with ${heldCount(id)} active reservations. Use Reservations to issue a held copy.`;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 64 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 65 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 66 | <code>  const copyRequests = {};</code> | Local state, DOM reference বা callback/result assign করে। |
| 67 | <code>  async function renderCopies(suffix = &quot;&quot;) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 68 | <code>    const book = $(`#bookOptions${suffix}`);</code> | Local state, DOM reference বা callback/result assign করে। |
| 69 | <code>    const copy = $(`#copyOptions${suffix}`);</code> | Local state, DOM reference বা callback/result assign করে। |
| 70 | <code>    const version = (copyRequests[suffix] = (copyRequests[suffix] &#124;&#124; 0) + 1);</code> | Local state, DOM reference বা callback/result assign করে। |
| 71 | <code>    copy.innerHTML = &#x27;&lt;option value=&quot;&quot;&gt;Loading copies...&lt;/option&gt;&#x27;;</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 72 | <code>    copy.disabled = true;</code> | Local state, DOM reference বা callback/result assign করে। |
| 73 | <code>    if (!book.value) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 74 | <code>      copy.innerHTML = &#x27;&lt;option value=&quot;&quot;&gt;Select a book first&lt;/option&gt;&#x27;;</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 75 | <code>      return;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 76 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 77 | <code>    try {</code> | Async failure handling ও UI cleanup/restore block। |
| 78 | <code>      const copies = await api(`/books/${book.value}/copies`);</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 79 | <code>      if (version !== copyRequests[suffix]) return;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 80 | <code>      copy.innerHTML =</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 81 | <code>        copies</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 82 | <code>          .filter((item) =&gt; item.status === &quot;AVAILABLE&quot;)</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 83 | <code>          .map((item) =&gt; `&lt;option value=&quot;${item.copy_id}&quot;&gt;Copy #${item.copy_no}&lt;/option&gt;`)</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 84 | <code>          .join(&quot;&quot;) &#124;&#124; &#x27;&lt;option value=&quot;&quot;&gt;No available copies&lt;/option&gt;&#x27;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 85 | <code>      copy.disabled = false;</code> | Local state, DOM reference বা callback/result assign করে। |
| 86 | <code>    } catch (error) {</code> | Async failure handling ও UI cleanup/restore block। |
| 87 | <code>      if (version === copyRequests[suffix]) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 88 | <code>        copy.innerHTML = &#x27;&lt;option value=&quot;&quot;&gt;Unable to load copies&lt;/option&gt;&#x27;;</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 89 | <code>        toast(error.message, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 90 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 91 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 92 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 93 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 94 | <code>  function render() {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 95 | <code>    const filter = $(&quot;#issueFilter&quot;).value;</code> | Local state, DOM reference বা callback/result assign করে। |
| 96 | <code>    const issues = sortIssues(</code> | Local state, DOM reference বা callback/result assign করে। |
| 97 | <code>      filter === &quot;ALL&quot; ? state.issues : state.issues.filter((issue) =&gt; issue.status === filter),</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 98 | <code>    );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 99 | <code>    $(&quot;#issueCount&quot;).textContent = `${issues.length} ${issues.length === 1 ? &quot;record&quot; : &quot;records&quot;}`;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 100 | <code>    $(&quot;#issueTable&quot;).innerHTML = issueRows(issues, true);</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 101 | <code>    $(&quot;#bookOptions&quot;).innerHTML = state.books</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 102 | <code>      .filter((book) =&gt; book.available_quantity &gt; 0)</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 103 | <code>      .map(</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 104 | <code>        (book) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 105 | <code>          `&lt;option value=&quot;${book.book_id}&quot;&gt;${escapeHtml(book.title)} (${book.available_quantity} available)&lt;/option&gt;`,</code> | User/database values escaped display markup-এ রূপান্তর করে। |
| 106 | <code>      )</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 107 | <code>      .join(&quot;&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 108 | <code>    for (const suffix of [&quot;2&quot;, &quot;3&quot;]) {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 109 | <code>      $(`#bookOptions${suffix}`).innerHTML =</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 110 | <code>        &#x27;&lt;option value=&quot;&quot;&gt;No additional book&lt;/option&gt;&#x27; + $(&quot;#bookOptions&quot;).innerHTML;</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 111 | <code>      renderCopies(suffix);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 112 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 113 | <code>    renderCopies();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 114 | <code>    renderMembers($(&quot;#issueMemberSearch&quot;).value);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 115 | <code>    $$(&quot;[data-return]&quot;).forEach((button) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 116 | <code>      button.onclick = () =&gt; returnBook(button.dataset.return);</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 117 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 118 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 119 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 120 | <code>  async function returnBook(id) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 121 | <code>    if (!confirm(&quot;Confirm this book return?&quot;)) return;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 122 | <code>    if (!state.online) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 123 | <code>      toast(&quot;Connect to the database before making changes&quot;, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 124 | <code>      return;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 125 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 126 | <code>    try {</code> | Async failure handling ও UI cleanup/restore block। |
| 127 | <code>      await api(`/issues/${id}/return`, { method: &quot;POST&quot; });</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 128 | <code>      toast(&quot;Book returned&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 129 | <code>      await loadData(render);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 130 | <code>    } catch (error) {</code> | Async failure handling ও UI cleanup/restore block। |
| 131 | <code>      toast(error.message, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 132 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 133 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 134 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 135 | <code>  const form = $(&quot;#issueModal form&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 136 | <code>  form.onsubmit = async (event) =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 137 | <code>    event.preventDefault();</code> | Default form navigation বন্ধ করে controlled API submission চালাতে দেয়। |
| 138 | <code>    const data = Object.fromEntries(new FormData(form));</code> | Form fields বা filters URL-encoded request body/query parameters-এ রূপান্তর করে। |
| 139 | <code>    if (!state.online) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 140 | <code>      toast(&quot;Connect to the database before making changes&quot;, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 141 | <code>      return;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 142 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 143 | <code>    const copies = [];</code> | Local state, DOM reference বা callback/result assign করে। |
| 144 | <code>    for (const suffix of [&quot;&quot;, &quot;2&quot;, &quot;3&quot;]) {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 145 | <code>      if (data[`bookId${suffix}`]) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 146 | <code>        if (!data[`copyId${suffix}`]) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 147 | <code>          toast(&quot;Select an available copy for each book&quot;, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 148 | <code>          return;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 149 | <code>        }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 150 | <code>        copies.push(data[`copyId${suffix}`]);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 151 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 152 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 153 | <code>    const active = state.issues.filter(</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 154 | <code>      (issue) =&gt; issue.student_id == data.studentId &amp;&amp; issue.status === &quot;ISSUED&quot;,</code> | Local state, DOM reference বা callback/result assign করে। |
| 155 | <code>    ).length;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 156 | <code>    if (active + heldCount(data.studentId) + copies.length &gt; 3) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 157 | <code>      toast(`This member can borrow ${3 - active - heldCount(data.studentId)} more copies`, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 158 | <code>      return;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 159 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 160 | <code>    if (new Set(copies).size !== copies.length) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 161 | <code>      toast(&quot;Select different copies for each loan&quot;, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 162 | <code>      return;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 163 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 164 | <code>    if (await postForm(form, &quot;/issues&quot;)) await loadData(render);</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 165 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 166 | <code>  $(&quot;#issueFilter&quot;).onchange = render;</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 167 | <code>  $(&quot;#issueMemberSearch&quot;).oninput = (event) =&gt; renderMembers(event.target.value);</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 168 | <code>  $(&quot;#studentOptions&quot;).onchange = updateAllowance;</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 169 | <code>  for (const suffix of [&quot;&quot;, &quot;2&quot;, &quot;3&quot;])</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 170 | <code>    $(`#bookOptions${suffix}`).onchange = () =&gt; renderCopies(suffix);</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 171 | <code>  form.addEventListener(&quot;reset&quot;, () =&gt;</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 172 | <code>    window.setTimeout(() =&gt; {</code> | Timeout/reconnection/search debounce timer শুরু বা বন্ধ করে। |
| 173 | <code>      for (const suffix of [&quot;&quot;, &quot;2&quot;, &quot;3&quot;]) renderCopies(suffix);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 174 | <code>      updateAllowance();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 175 | <code>    }, 0),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 176 | <code>  );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 177 | <code>  loadData(() =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 178 | <code>    render();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 179 | <code>    openRequestedModal(&quot;issueModal&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 180 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 181 | <code>})();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
