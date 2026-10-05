# frontend/audit.js

Admin audit search, filters, pagination এবং before/after details modal render করে।

Source: [মূল file](../../frontend/audit.js)। Snapshot 2026-10-04; 123 lines; SHA-256 `c03e0ca58b4b59d54a9ea90d9decb8400a6968dd44c9457aeae140051fdd1375`।

## Function / object / element inventory

### `loadAudit()` — L30

Filters/page থেকে query বানায়, request counter দিয়ে stale responses ignore করে, table ও pagination render করে; row detail buttons bind করে।

### `showDetails(id)` — L76

Selected audit event-এর before/after keys union করে comparison table বানায়; changed fields highlight করে modal খোলে।

## সম্পূর্ণ original source

```javascript
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
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>(() =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 2 | <code>  const { $, $$, api, escapeHtml, table, toast, loadData, openModal } = LibraryApp;</code> | Local state, DOM reference বা callback/result assign করে। |
| 3 | <code>  const entities = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 4 | <code>    STUDENT: &quot;Member&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 5 | <code>    BOOK: &quot;Book&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 6 | <code>    AUTHOR: &quot;Author&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 7 | <code>    CATEGORY: &quot;Category&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 8 | <code>    ISSUE_BOOK: &quot;Loan&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 9 | <code>    RETURN_BOOK: &quot;Return&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 10 | <code>    FINE: &quot;Fine&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 11 | <code>    LOGIN_USER: &quot;Account&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 12 | <code>    ADMIN: &quot;Admin profile&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 13 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 14 | <code>  const actions = {</code> | Local state, DOM reference বা callback/result assign করে। |
| 15 | <code>    INSERT: &quot;Created&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 16 | <code>    UPDATE: &quot;Updated&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 17 | <code>    DELETE: &quot;Deleted&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 18 | <code>    SNAPSHOT: &quot;Initial snapshot&quot;,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 19 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 20 | <code>  let page = 1;</code> | Local state, DOM reference বা callback/result assign করে। |
| 21 | <code>  let records = [];</code> | Local state, DOM reference বা callback/result assign করে। |
| 22 | <code>  let requestNumber = 0;</code> | Local state, DOM reference বা callback/result assign করে। |
| 23 | <code>  let searchTimer;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 24 | <code>  const formatTime = (value) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 25 | <code>    new Date(value).toLocaleString(&quot;en-GB&quot;, { timeZone: &quot;Asia/Dhaka&quot;, hour12: true });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 26 | <code>  const label = (key) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 27 | <code>    ({ roll_no: &quot;ID / Roll&quot;, registration_no: &quot;Registration No.&quot; })[key] &#124;&#124;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 28 | <code>    key.replaceAll(&quot;_&quot;, &quot; &quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 29 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 30 | <code>  async function loadAudit() {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 31 | <code>    const currentRequest = ++requestNumber;</code> | Local state, DOM reference বা callback/result assign করে। |
| 32 | <code>    $(&quot;#auditTable&quot;).setAttribute(&quot;aria-busy&quot;, &quot;true&quot;);</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 33 | <code>    $(&quot;#auditPrevious&quot;).disabled = true;</code> | Local state, DOM reference বা callback/result assign করে। |
| 34 | <code>    $(&quot;#auditNext&quot;).disabled = true;</code> | Local state, DOM reference বা callback/result assign করে। |
| 35 | <code>    const query = new URLSearchParams({</code> | Form fields বা filters URL-encoded request body/query parameters-এ রূপান্তর করে। |
| 36 | <code>      page,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 37 | <code>      q: $(&quot;#auditSearch&quot;).value.trim(),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 38 | <code>      entity: $(&quot;#auditEntity&quot;).value,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 39 | <code>      action: $(&quot;#auditAction&quot;).value,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 40 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 41 | <code>    try {</code> | Async failure handling ও UI cleanup/restore block। |
| 42 | <code>      const result = await api(`/audit?${query}`);</code> | HTTP/API request করে; response asynchronousভাবে process হয়। |
| 43 | <code>      if (currentRequest !== requestNumber) return;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 44 | <code>      records = result.items;</code> | Local state, DOM reference বা callback/result assign করে। |
| 45 | <code>      const pages = Math.max(1, Math.ceil(result.total / result.page_size));</code> | Local state, DOM reference বা callback/result assign করে। |
| 46 | <code>      $(&quot;#auditCount&quot;).textContent =</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 47 | <code>        `${result.total} events &#124; Page ${page} of ${pages} &#124; Asia/Dhaka`;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 48 | <code>      $(&quot;#auditTable&quot;).innerHTML = records.length</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 49 | <code>        ? table(</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 50 | <code>            [&quot;Time&quot;, &quot;Changed by&quot;, &quot;Action&quot;, &quot;Record type&quot;, &quot;Record&quot;, &quot;Details&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 51 | <code>            records.map((record) =&gt; {</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 52 | <code>              const details = record.after &#124;&#124; record.before &#124;&#124; {};</code> | Local state, DOM reference বা callback/result assign করে। |
| 53 | <code>              const name =</code> | Local state, DOM reference বা callback/result assign করে। |
| 54 | <code>                details.name &#124;&#124;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 55 | <code>                details.title &#124;&#124;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 56 | <code>                details.username &#124;&#124;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 57 | <code>                details.author_name &#124;&#124;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 58 | <code>                details.category_name &#124;&#124;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 59 | <code>                `#${record.record_id}`;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 60 | <code>              return `&lt;tr&gt;&lt;td&gt;${escapeHtml(formatTime(record.occurred_at))}&lt;/td&gt;&lt;td&gt;${escapeHtml(record.actor)}&lt;/td&gt;&lt;td&gt;${escapeHtml(actions[record.action] &#124;&#124; record.action)}&lt;/td&gt;&lt;td&gt;${escapeHtml(entities[record.entity] &#124;&#124; record.entity)}&lt;/td&gt;&lt;td&gt;&lt;b&gt;${escapeHtml(name)}&lt;/b&gt;&lt;small class=&quot;audit-record-id&quot;&gt;Record #${record.record_id}&lt;/small&gt;&lt;/td&gt;&lt;td&gt;&lt;button class=&quot;button small secondary&quot; data-audit=&quot;${record.audit_id}&quot;&gt;View details&lt;/button&gt;&lt;/td&gt;&lt;/tr&gt;`;</code> | User/database values escaped display markup-এ রূপান্তর করে। |
| 61 | <code>            }),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 62 | <code>          )</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 63 | <code>        : &#x27;&lt;div class=&quot;empty-state&quot;&gt;&lt;strong&gt;No audit events found&lt;/strong&gt;&lt;span&gt;Try another search or filter.&lt;/span&gt;&lt;/div&gt;&#x27;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 64 | <code>      $$(&quot;[data-audit]&quot;).forEach((button) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 65 | <code>        button.onclick = () =&gt; showDetails(button.dataset.audit);</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 66 | <code>      });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 67 | <code>      $(&quot;#auditPrevious&quot;).disabled = page &lt;= 1;</code> | Local state, DOM reference বা callback/result assign করে। |
| 68 | <code>      $(&quot;#auditNext&quot;).disabled = page &gt;= pages;</code> | Local state, DOM reference বা callback/result assign করে। |
| 69 | <code>    } catch (error) {</code> | Async failure handling ও UI cleanup/restore block। |
| 70 | <code>      if (currentRequest === requestNumber) toast(error.message, true);</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 71 | <code>    } finally {</code> | Async failure handling ও UI cleanup/restore block। |
| 72 | <code>      if (currentRequest === requestNumber) $(&quot;#auditTable&quot;).setAttribute(&quot;aria-busy&quot;, &quot;false&quot;);</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 73 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 74 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 75 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 76 | <code>  function showDetails(id) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 77 | <code>    const record = records.find((item) =&gt; item.audit_id == id);</code> | Local state, DOM reference বা callback/result assign করে। |
| 78 | <code>    if (!record) return;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 79 | <code>    $(&quot;#auditDetailTitle&quot;).textContent =</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 80 | <code>      `${entities[record.entity]} #${record.record_id} &#124; ${actions[record.action]}`;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 81 | <code>    $(&quot;#auditDetailMeta&quot;).textContent =</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 82 | <code>      `${record.actor} &#124; ${formatTime(record.occurred_at)} (Asia/Dhaka)`;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 83 | <code>    const keys = [</code> | Local state, DOM reference বা callback/result assign করে। |
| 84 | <code>      ...new Set([...Object.keys(record.before &#124;&#124; {}), ...Object.keys(record.after &#124;&#124; {})]),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 85 | <code>    ];</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 86 | <code>    $(&quot;#auditValues&quot;).innerHTML = table(</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 87 | <code>      [&quot;Field&quot;, &quot;Before&quot;, &quot;After&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 88 | <code>      keys.map((key) =&gt; {</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 89 | <code>        const before = record.before?.[key],</code> | Local state, DOM reference বা callback/result assign করে। |
| 90 | <code>          after = record.after?.[key];</code> | Local state, DOM reference বা callback/result assign করে। |
| 91 | <code>        const changed = record.before &amp;&amp; record.after &amp;&amp; before !== after;</code> | Local state, DOM reference বা callback/result assign করে। |
| 92 | <code>        return `&lt;tr class=&quot;${changed ? &quot;audit-changed&quot; : &quot;&quot;}&quot;&gt;&lt;td&gt;${escapeHtml(label(key))}${changed ? &#x27; &lt;span class=&quot;pill&quot;&gt;Changed&lt;/span&gt;&#x27; : &quot;&quot;}&lt;/td&gt;&lt;td&gt;${escapeHtml(before ?? &quot;-&quot;)}&lt;/td&gt;&lt;td&gt;${escapeHtml(after ?? &quot;-&quot;)}&lt;/td&gt;&lt;/tr&gt;`;</code> | User/database values escaped display markup-এ রূপান্তর করে। |
| 93 | <code>      }),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 94 | <code>    );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 95 | <code>    openModal(&quot;auditDetail&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 96 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 97 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 98 | <code>  $(&quot;#auditSearch&quot;).oninput = () =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 99 | <code>    clearTimeout(searchTimer);</code> | Timeout/reconnection/search debounce timer শুরু বা বন্ধ করে। |
| 100 | <code>    searchTimer = setTimeout(() =&gt; {</code> | Timeout/reconnection/search debounce timer শুরু বা বন্ধ করে। |
| 101 | <code>      page = 1;</code> | Local state, DOM reference বা callback/result assign করে। |
| 102 | <code>      loadAudit();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 103 | <code>    }, 300);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 104 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 105 | <code>  [&quot;#auditEntity&quot;, &quot;#auditAction&quot;].forEach((selector) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 106 | <code>    $(selector).onchange = () =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 107 | <code>      page = 1;</code> | Local state, DOM reference বা callback/result assign করে। |
| 108 | <code>      loadAudit();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 109 | <code>    };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 110 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 111 | <code>  $(&quot;#auditPrevious&quot;).onclick = () =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 112 | <code>    if (page &gt; 1) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 113 | <code>      page--;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 114 | <code>      loadAudit();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 115 | <code>    }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 116 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 117 | <code>  $(&quot;#auditNext&quot;).onclick = () =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 118 | <code>    page++;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 119 | <code>    loadAudit();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 120 | <code>  };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 121 | <code>  $(&quot;#refreshAudit&quot;).onclick = () =&gt; loadData(loadAudit);</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 122 | <code>  loadData(loadAudit);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 123 | <code>})();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
