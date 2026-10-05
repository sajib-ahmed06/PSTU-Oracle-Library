# frontend/students.js

Member directory ও search; add, full Edit এবং membership enable/disable actions চালায়।

Source: [মূল file](../../frontend/students.js)। Snapshot 2026-10-04; 110 lines; SHA-256 `a698a137e809490f4b6e64c339e6761815e99222af4c4713a7183453e2e43b66`।

## Function / object / element inventory

### `render()` — L17

এই page-এর current state ও search/filter থেকে tables/metrics/options তৈরি করে, DOM update করে এবং generated action buttons-এর events bind করে। পাশের পূর্ণ code-এ page-specific fields দেখা যাবে।

### `toggleMembership(id)` — L72

User confirmation ও online check-এর পরে member toggle API call, toast ও fresh render।

## সম্পূর্ণ original source

```javascript
(() => {
  const {
    $,
    $$,
    state,
    escapeHtml,
    memberId,
    table,
    toast,
    api,
    loadData,
    postForm,
    openRequestedModal,
    openModal,
  } = LibraryApp;

  function render() {
    const query = $("#studentSearch").value.trim().toLowerCase();
    const students = state.students.filter((student) =>
      `${memberId(student.student_id)} ${student.roll_no || ""} ${student.registration_no || ""} ${student.academic_session || ""} ${student.name} ${student.department} ${student.phone} ${student.email}`
        .toLowerCase()
        .includes(query),
    );
    $("#studentCount").textContent =
      `${students.length} ${students.length === 1 ? "member" : "members"}`;
    $("#studentTable").innerHTML = table(
      [
        "Member ID",
        "ID / Roll",
        "Registration No.",
        "Student",
        "Session",
        "Department",
        "Phone",
        "Email",
        "Status",
        "Action",
      ],
      students.map((student) => {
        const status = student.membership_status || "ACTIVE";
        const action = status === "ACTIVE" ? "Disable" : "Enable";
        return `<tr><td><span class="member-id">${memberId(student.student_id)}</span></td><td>${escapeHtml(student.roll_no || "Not assigned")}</td><td>${escapeHtml(student.registration_no || "Not assigned")}</td><td><b>${escapeHtml(student.name)}</b></td><td>${escapeHtml(student.academic_session || "Not assigned")}</td><td>${escapeHtml(student.department)}</td><td>${escapeHtml(student.phone)}</td><td>${escapeHtml(student.email)}</td><td><span class="pill ${status.toLowerCase()}">${status}</span></td><td><div class="row-actions"><button class="button small secondary" data-identity="${student.student_id}">Edit</button><button class="button small ${action === "Disable" ? "danger-quiet" : "primary"}" data-toggle="${student.student_id}">${action}</button></div></td></tr>`;
      }),
    );
    $$("[data-identity]").forEach((button) => {
      button.onclick = () => {
        const member = state.students.find((item) => item.student_id == button.dataset.identity);
        const form = $("#identityModal form");
        form.elements.student_id.value = member.student_id;
        for (const field of [
          "academic_session",
          "name",
          "department",
          "phone",
          "email",
          "membership_status",
        ]) {
          form.elements[field].value =
            member[field] || (field === "membership_status" ? "ACTIVE" : "");
        }
        form.elements.roll_no.value = member.roll_no || "";
        form.elements.registration_no.value = member.registration_no || "";
        $("#identityMember").textContent = `${memberId(member.student_id)} - ${member.name}`;
        openModal("identityModal");
      };
    });
    $$("[data-toggle]").forEach((button) => {
      button.onclick = () => toggleMembership(button.dataset.toggle);
    });
  }

  async function toggleMembership(id) {
    const student = state.students.find((item) => item.student_id == id);
    const disabling = (student.membership_status || "ACTIVE") === "ACTIVE";
    if (!confirm(`${disabling ? "Disable" : "Enable"} ${student.name}'s membership?`)) return;
    if (!state.online) {
      toast("Connect to the database before making changes", true);
      return;
    }
    try {
      await api(`/students/${id}/toggle`, { method: "POST" });
      toast("Membership updated");
      await loadData(render);
    } catch (error) {
      toast(error.message, true);
    }
  }

  const form = $("#studentModal form");
  form.onsubmit = async (event) => {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(form));
    if (!state.online) {
      toast("Connect to the database before making changes", true);
      return;
    }
    if (await postForm(form, "/students")) await loadData(render);
  };
  $("#identityModal form").onsubmit = async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    if (await postForm(form, `/students/${form.elements.student_id.value}/edit`))
      await loadData(render);
  };
  $("#studentSearch").oninput = render;
  loadData(() => {
    render();
    openRequestedModal("studentModal");
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
| 8 | <code>    table,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 9 | <code>    toast,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 10 | <code>    api,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 11 | <code>    loadData,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 12 | <code>    postForm,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 13 | <code>    openRequestedModal,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 14 | <code>    openModal,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 15 | <code>  } = LibraryApp;</code> | Local state, DOM reference বা callback/result assign করে। |
| 16 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 17 | <code>  function render() {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 18 | <code>    const query = $(&quot;#studentSearch&quot;).value.trim().toLowerCase();</code> | Local state, DOM reference বা callback/result assign করে। |
| 19 | <code>    const students = state.students.filter((student) =&gt;</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 20 | <code>      `${memberId(student.student_id)} ${student.roll_no &#124;&#124; &quot;&quot;} ${student.registration_no &#124;&#124; &quot;&quot;} ${student.academic_session &#124;&#124; &quot;&quot;} ${student.name} ${student.department} ${student.phone} ${student.email}`</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 21 | <code>        .toLowerCase()</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 22 | <code>        .includes(query),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 23 | <code>    );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 24 | <code>    $(&quot;#studentCount&quot;).textContent =</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 25 | <code>      `${students.length} ${students.length === 1 ? &quot;member&quot; : &quot;members&quot;}`;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 26 | <code>    $(&quot;#studentTable&quot;).innerHTML = table(</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 27 | <code>      [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 28 | <code>        &quot;Member ID&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 29 | <code>        &quot;ID / Roll&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 30 | <code>        &quot;Registration No.&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 31 | <code>        &quot;Student&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 32 | <code>        &quot;Session&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 33 | <code>        &quot;Department&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 34 | <code>        &quot;Phone&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 35 | <code>        &quot;Email&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 36 | <code>        &quot;Status&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 37 | <code>        &quot;Action&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 38 | <code>      ],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 39 | <code>      students.map((student) =&gt; {</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 40 | <code>        const status = student.membership_status &#124;&#124; &quot;ACTIVE&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 41 | <code>        const action = status === &quot;ACTIVE&quot; ? &quot;Disable&quot; : &quot;Enable&quot;;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 42 | <code>        return `&lt;tr&gt;&lt;td&gt;&lt;span class=&quot;member-id&quot;&gt;${memberId(student.student_id)}&lt;/span&gt;&lt;/td&gt;&lt;td&gt;${escapeHtml(student.roll_no &#124;&#124; &quot;Not assigned&quot;)}&lt;/td&gt;&lt;td&gt;${escapeHtml(student.registration_no &#124;&#124; &quot;Not assigned&quot;)}&lt;/td&gt;&lt;td&gt;&lt;b&gt;${escapeHtml(student.name)}&lt;/b&gt;&lt;/td&gt;&lt;td&gt;${escapeHtml(student.academic_session &#124;&#124; &quot;Not assigned&quot;)}&lt;/td&gt;&lt;td&gt;${escapeHtml(student.department)}&lt;/td&gt;&lt;td&gt;${escapeHtml(student.phone)}&lt;/td&gt;&lt;td&gt;${escapeHtml(student.email)}&lt;/td&gt;&lt;td&gt;&lt;span class=&quot;pill ${status.toLowerCase()}&quot;&gt;${status}&lt;/span&gt;&lt;/td&gt;&lt;td&gt;&lt;div class=&quot;row-actions&quot;&gt;&lt;button class=&quot;button small secondary&quot; data-identity=&quot;${student.student_id}&quot;&gt;Edit&lt;/button&gt;&lt;button class=&quot;button small ${action === &quot;Disable&quot; ? &quot;danger-quiet&quot; : &quot;primary&quot;}&quot; data-toggle=&quot;${student.student_id}&quot;&gt;${action}&lt;/button&gt;&lt;/div&gt;&lt;/td&gt;&lt;/tr&gt;`;</code> | User/database values escaped display markup-এ রূপান্তর করে। |
| 43 | <code>      }),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 44 | <code>    );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 45 | <code>    $$(&quot;[data-identity]&quot;).forEach((button) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 46 | <code>      button.onclick = () =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 47 | <code>        const member = state.students.find((item) =&gt; item.student_id == button.dataset.identity);</code> | Local state, DOM reference বা callback/result assign করে। |
| 48 | <code>        const form = $(&quot;#identityModal form&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 49 | <code>        form.elements.student_id.value = member.student_id;</code> | Local state, DOM reference বা callback/result assign করে। |
| 50 | <code>        for (const field of [</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 51 | <code>          &quot;academic_session&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 52 | <code>          &quot;name&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 53 | <code>          &quot;department&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 54 | <code>          &quot;phone&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 55 | <code>          &quot;email&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 56 | <code>          &quot;membership_status&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 57 | <code>        ]) {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 58 | <code>          form.elements[field].value =</code> | Local state, DOM reference বা callback/result assign করে। |
| 59 | <code>            member[field] &#124;&#124; (field === &quot;membership_status&quot; ? &quot;ACTIVE&quot; : &quot;&quot;);</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 60 | <code>        }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 61 | <code>        form.elements.roll_no.value = member.roll_no &#124;&#124; &quot;&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 62 | <code>        form.elements.registration_no.value = member.registration_no &#124;&#124; &quot;&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 63 | <code>        $(&quot;#identityMember&quot;).textContent = `${memberId(member.student_id)} - ${member.name}`;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 64 | <code>        openModal(&quot;identityModal&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 65 | <code>      };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 66 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 67 | <code>    $$(&quot;[data-toggle]&quot;).forEach((button) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 68 | <code>      button.onclick = () =&gt; toggleMembership(button.dataset.toggle);</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 69 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 70 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 71 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 72 | <code>  async function toggleMembership(id) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 73 | <code>    const student = state.students.find((item) =&gt; item.student_id == id);</code> | Local state, DOM reference বা callback/result assign করে। |
| 74 | <code>    const disabling = (student.membership_status &#124;&#124; &quot;ACTIVE&quot;) === &quot;ACTIVE&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 75 | <code>    if (!confirm(`${disabling ? &quot;Disable&quot; : &quot;Enable&quot;} ${student.name}&#x27;s membership?`)) return;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 76 | <code>    if (!state.online) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 77 | <code>      toast(&quot;Connect to the database before making changes&quot;, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 78 | <code>      return;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 79 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 80 | <code>    try {</code> | Async failure handling ও UI cleanup/restore block। |
| 81 | <code>      await api(`/students/${id}/toggle`, { method: &quot;POST&quot; });</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 82 | <code>      toast(&quot;Membership updated&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 83 | <code>      await loadData(render);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 84 | <code>    } catch (error) {</code> | Async failure handling ও UI cleanup/restore block। |
| 85 | <code>      toast(error.message, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 86 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 87 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 88 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 89 | <code>  const form = $(&quot;#studentModal form&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 90 | <code>  form.onsubmit = async (event) =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 91 | <code>    event.preventDefault();</code> | Default form navigation বন্ধ করে controlled API submission চালাতে দেয়। |
| 92 | <code>    const data = Object.fromEntries(new FormData(form));</code> | Form fields বা filters URL-encoded request body/query parameters-এ রূপান্তর করে। |
| 93 | <code>    if (!state.online) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 94 | <code>      toast(&quot;Connect to the database before making changes&quot;, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 95 | <code>      return;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 96 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 97 | <code>    if (await postForm(form, &quot;/students&quot;)) await loadData(render);</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 98 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 99 | <code>  $(&quot;#identityModal form&quot;).onsubmit = async (event) =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 100 | <code>    event.preventDefault();</code> | Default form navigation বন্ধ করে controlled API submission চালাতে দেয়। |
| 101 | <code>    const form = event.currentTarget;</code> | Local state, DOM reference বা callback/result assign করে। |
| 102 | <code>    if (await postForm(form, `/students/${form.elements.student_id.value}/edit`))</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 103 | <code>      await loadData(render);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 104 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 105 | <code>  $(&quot;#studentSearch&quot;).oninput = render;</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 106 | <code>  loadData(() =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 107 | <code>    render();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 108 | <code>    openRequestedModal(&quot;studentModal&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 109 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 110 | <code>})();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
