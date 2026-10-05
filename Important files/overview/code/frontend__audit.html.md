# frontend/audit.html

এই page-এর semantic HTML structure: header placeholder, content sections, forms/dialogs এবং stylesheet/script links। Matching controller JavaScript interactions চালায়।

Source: [মূল file](../../frontend/audit.html)। Snapshot 2026-10-04; 93 lines; SHA-256 `8779ab11c06d7ac3c2c68f29e36ffc2900aa78c8b481c1aeb1318d3de35305b4`।

## Function / object / element inventory

- DOM IDs: `appHeader`, `refreshAudit`, `auditSearch`, `auditEntity`, `auditAction`, `auditTable`, `auditCount`, `auditPrevious`, `auditNext`, `auditDetail`, `auditDetailTitle`, `auditDetailMeta`, `auditValues`, `toast`
- Form keys: 
- Loaded/linked resources: `/static/styles.css?v=members-audit-1`, `/static/polish.css?v=1`, `/static/notifications.css?v=due-2`, `/static/notifications.js?v=reminders-4`, `/static/shared.js?v=priority-3`, `/static/audit.js`

## সম্পূর্ণ original source

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Audit | PSTU Library</title>
    <link rel="stylesheet" href="/static/styles.css?v=members-audit-1" />
    <link rel="stylesheet" href="/static/polish.css?v=1" />
    <link rel="stylesheet" href="/static/notifications.css?v=due-2" />
  </head>
  <body data-page="audit">
    <div id="appHeader"></div>
    <main class="workspace">
      <section class="page-heading">
        <div>
          <p class="eyebrow">Administration</p>
          <h1>Audit history</h1>
          <p class="heading-copy">
            Review who changed each record, when it changed, and the values before and after.
          </p>
        </div>
        <button id="refreshAudit" class="button secondary">Refresh history</button>
      </section>
      <p class="form-note">
        Snapshots show records as they existed when tracking started. Later changes are recorded
        automatically. Passwords are excluded.
      </p>
      <section class="toolbar audit-filters">
        <label
          >Search<input
            id="auditSearch"
            type="search"
            maxlength="100"
            placeholder="Name, roll, registration, actor or record ID"
        /></label>
        <label
          >Record type<select id="auditEntity">
            <option value="">All records</option>
            <option value="STUDENT">Members</option>
            <option value="BOOK">Books</option>
            <option value="AUTHOR">Authors</option>
            <option value="CATEGORY">Categories</option>
            <option value="ISSUE_BOOK">Loans</option>
            <option value="RETURN_BOOK">Returns</option>
            <option value="FINE">Fines</option>
            <option value="BOOK_RESERVATION">Reservations</option>
            <option value="LOGIN_USER">Accounts</option>
            <option value="ADMIN">Admin profiles</option>
          </select></label
        >
        <label
          >Action<select id="auditAction">
            <option value="">All actions</option>
            <option value="INSERT">Created</option>
            <option value="UPDATE">Updated</option>
            <option value="DELETE">Deleted</option>
            <option value="SNAPSHOT">Initial snapshot</option>
          </select></label
        >
      </section>
      <section class="surface">
        <div class="table-wrap" id="auditTable" aria-live="polite"></div>
      </section>
      <div class="audit-pagination">
        <span id="auditCount" class="record-count"></span>
        <div class="row-actions">
          <button id="auditPrevious" class="button secondary" disabled>Previous</button
          ><button id="auditNext" class="button secondary" disabled>Next</button>
        </div>
      </div>
    </main>
    <div class="modal" id="auditDetail" aria-hidden="true">
      <form class="audit-detail-form">
        <div class="modal-heading">
          <div>
            <span class="section-label">Audit details</span>
            <h2 id="auditDetailTitle">Record change</h2>
          </div>
          <button type="button" class="icon-button cancel" aria-label="Close">&times;</button>
        </div>
        <p id="auditDetailMeta" class="form-note"></p>
        <div class="table-wrap" id="auditValues"></div>
        <div class="form-actions">
          <button type="button" class="button secondary cancel">Close</button>
        </div>
      </form>
    </div>
    <div id="toast" role="status" aria-live="polite"></div>
    <script src="/static/notifications.js?v=reminders-4"></script>
    <script src="/static/shared.js?v=priority-3"></script>
    <script src="/static/audit.js"></script>
  </body>
</html>
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&lt;!doctype html&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 2 | <code>&lt;html lang=&quot;en&quot;&gt;</code> | html: HTML structure/content |
| 3 | <code>  &lt;head&gt;</code> | head: HTML structure/content |
| 4 | <code>    &lt;meta charset=&quot;utf-8&quot; /&gt;</code> | meta: encoding/viewport metadata |
| 5 | <code>    &lt;meta name=&quot;viewport&quot; content=&quot;width=device-width, initial-scale=1&quot; /&gt;</code> | meta: encoding/viewport metadata |
| 6 | <code>    &lt;title&gt;Audit &#124; PSTU Library&lt;/title&gt;</code> | title: HTML structure/content |
| 7 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/styles.css?v=members-audit-1&quot; /&gt;</code> | link: stylesheet/resource load |
| 8 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/polish.css?v=1&quot; /&gt;</code> | link: stylesheet/resource load |
| 9 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/notifications.css?v=due-2&quot; /&gt;</code> | link: stylesheet/resource load |
| 10 | <code>  &lt;/head&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 11 | <code>  &lt;body data-page=&quot;audit&quot;&gt;</code> | body: HTML structure/content |
| 12 | <code>    &lt;div id=&quot;appHeader&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 13 | <code>    &lt;main class=&quot;workspace&quot;&gt;</code> | main: primary page content |
| 14 | <code>      &lt;section class=&quot;page-heading&quot;&gt;</code> | section: related UI content grouping |
| 15 | <code>        &lt;div&gt;</code> | div: layout/dynamic content container |
| 16 | <code>          &lt;p class=&quot;eyebrow&quot;&gt;Administration&lt;/p&gt;</code> | p: description/help text |
| 17 | <code>          &lt;h1&gt;Audit history&lt;/h1&gt;</code> | h1: page heading |
| 18 | <code>          &lt;p class=&quot;heading-copy&quot;&gt;</code> | p: description/help text |
| 19 | <code>            Review who changed each record, when it changed, and the values before and after.</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 20 | <code>          &lt;/p&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 21 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 22 | <code>        &lt;button id=&quot;refreshAudit&quot; class=&quot;button secondary&quot;&gt;Refresh history&lt;/button&gt;</code> | button: action/submit/cancel control |
| 23 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 24 | <code>      &lt;p class=&quot;form-note&quot;&gt;</code> | p: description/help text |
| 25 | <code>        Snapshots show records as they existed when tracking started. Later changes are recorded</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 26 | <code>        automatically. Passwords are excluded.</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 27 | <code>      &lt;/p&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 28 | <code>      &lt;section class=&quot;toolbar audit-filters&quot;&gt;</code> | section: related UI content grouping |
| 29 | <code>        &lt;label</code> | label: field-এর readable label |
| 30 | <code>          &gt;Search&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 31 | <code>            id=&quot;auditSearch&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 32 | <code>            type=&quot;search&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 33 | <code>            maxlength=&quot;100&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 34 | <code>            placeholder=&quot;Name, roll, registration, actor or record ID&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 35 | <code>        /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 36 | <code>        &lt;label</code> | label: field-এর readable label |
| 37 | <code>          &gt;Record type&lt;select id=&quot;auditEntity&quot;&gt;</code> | select: option থেকে value নির্বাচন |
| 38 | <code>            &lt;option value=&quot;&quot;&gt;All records&lt;/option&gt;</code> | option: select-এর choice |
| 39 | <code>            &lt;option value=&quot;STUDENT&quot;&gt;Members&lt;/option&gt;</code> | option: select-এর choice |
| 40 | <code>            &lt;option value=&quot;BOOK&quot;&gt;Books&lt;/option&gt;</code> | option: select-এর choice |
| 41 | <code>            &lt;option value=&quot;AUTHOR&quot;&gt;Authors&lt;/option&gt;</code> | option: select-এর choice |
| 42 | <code>            &lt;option value=&quot;CATEGORY&quot;&gt;Categories&lt;/option&gt;</code> | option: select-এর choice |
| 43 | <code>            &lt;option value=&quot;ISSUE_BOOK&quot;&gt;Loans&lt;/option&gt;</code> | option: select-এর choice |
| 44 | <code>            &lt;option value=&quot;RETURN_BOOK&quot;&gt;Returns&lt;/option&gt;</code> | option: select-এর choice |
| 45 | <code>            &lt;option value=&quot;FINE&quot;&gt;Fines&lt;/option&gt;</code> | option: select-এর choice |
| 46 | <code>            &lt;option value=&quot;BOOK_RESERVATION&quot;&gt;Reservations&lt;/option&gt;</code> | option: select-এর choice |
| 47 | <code>            &lt;option value=&quot;LOGIN_USER&quot;&gt;Accounts&lt;/option&gt;</code> | option: select-এর choice |
| 48 | <code>            &lt;option value=&quot;ADMIN&quot;&gt;Admin profiles&lt;/option&gt;</code> | option: select-এর choice |
| 49 | <code>          &lt;/select&gt;&lt;/label</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 50 | <code>        &gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 51 | <code>        &lt;label</code> | label: field-এর readable label |
| 52 | <code>          &gt;Action&lt;select id=&quot;auditAction&quot;&gt;</code> | select: option থেকে value নির্বাচন |
| 53 | <code>            &lt;option value=&quot;&quot;&gt;All actions&lt;/option&gt;</code> | option: select-এর choice |
| 54 | <code>            &lt;option value=&quot;INSERT&quot;&gt;Created&lt;/option&gt;</code> | option: select-এর choice |
| 55 | <code>            &lt;option value=&quot;UPDATE&quot;&gt;Updated&lt;/option&gt;</code> | option: select-এর choice |
| 56 | <code>            &lt;option value=&quot;DELETE&quot;&gt;Deleted&lt;/option&gt;</code> | option: select-এর choice |
| 57 | <code>            &lt;option value=&quot;SNAPSHOT&quot;&gt;Initial snapshot&lt;/option&gt;</code> | option: select-এর choice |
| 58 | <code>          &lt;/select&gt;&lt;/label</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 59 | <code>        &gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 60 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 61 | <code>      &lt;section class=&quot;surface&quot;&gt;</code> | section: related UI content grouping |
| 62 | <code>        &lt;div class=&quot;table-wrap&quot; id=&quot;auditTable&quot; aria-live=&quot;polite&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 63 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 64 | <code>      &lt;div class=&quot;audit-pagination&quot;&gt;</code> | div: layout/dynamic content container |
| 65 | <code>        &lt;span id=&quot;auditCount&quot; class=&quot;record-count&quot;&gt;&lt;/span&gt;</code> | span: HTML structure/content |
| 66 | <code>        &lt;div class=&quot;row-actions&quot;&gt;</code> | div: layout/dynamic content container |
| 67 | <code>          &lt;button id=&quot;auditPrevious&quot; class=&quot;button secondary&quot; disabled&gt;Previous&lt;/button</code> | button: action/submit/cancel control |
| 68 | <code>          &gt;&lt;button id=&quot;auditNext&quot; class=&quot;button secondary&quot; disabled&gt;Next&lt;/button&gt;</code> | button: action/submit/cancel control |
| 69 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 70 | <code>      &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 71 | <code>    &lt;/main&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 72 | <code>    &lt;div class=&quot;modal&quot; id=&quot;auditDetail&quot; aria-hidden=&quot;true&quot;&gt;</code> | div: layout/dynamic content container |
| 73 | <code>      &lt;form class=&quot;audit-detail-form&quot;&gt;</code> | form: submit-able input grouping |
| 74 | <code>        &lt;div class=&quot;modal-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 75 | <code>          &lt;div&gt;</code> | div: layout/dynamic content container |
| 76 | <code>            &lt;span class=&quot;section-label&quot;&gt;Audit details&lt;/span&gt;</code> | span: HTML structure/content |
| 77 | <code>            &lt;h2 id=&quot;auditDetailTitle&quot;&gt;Record change&lt;/h2&gt;</code> | h2: section/dialog heading |
| 78 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 79 | <code>          &lt;button type=&quot;button&quot; class=&quot;icon-button cancel&quot; aria-label=&quot;Close&quot;&gt;&amp;times;&lt;/button&gt;</code> | button: action/submit/cancel control |
| 80 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 81 | <code>        &lt;p id=&quot;auditDetailMeta&quot; class=&quot;form-note&quot;&gt;&lt;/p&gt;</code> | p: description/help text |
| 82 | <code>        &lt;div class=&quot;table-wrap&quot; id=&quot;auditValues&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 83 | <code>        &lt;div class=&quot;form-actions&quot;&gt;</code> | div: layout/dynamic content container |
| 84 | <code>          &lt;button type=&quot;button&quot; class=&quot;button secondary cancel&quot;&gt;Close&lt;/button&gt;</code> | button: action/submit/cancel control |
| 85 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 86 | <code>      &lt;/form&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 87 | <code>    &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 88 | <code>    &lt;div id=&quot;toast&quot; role=&quot;status&quot; aria-live=&quot;polite&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 89 | <code>    &lt;script src=&quot;/static/notifications.js?v=reminders-4&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 90 | <code>    &lt;script src=&quot;/static/shared.js?v=priority-3&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 91 | <code>    &lt;script src=&quot;/static/audit.js&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 92 | <code>  &lt;/body&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 93 | <code>&lt;/html&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
