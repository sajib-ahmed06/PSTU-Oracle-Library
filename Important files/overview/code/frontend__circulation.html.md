# frontend/circulation.html

এই page-এর semantic HTML structure: header placeholder, content sections, forms/dialogs এবং stylesheet/script links। Matching controller JavaScript interactions চালায়।

Source: [মূল file](../../frontend/circulation.html)। Snapshot 2026-10-04; 72 lines; SHA-256 `6aef52c55dcbb97c422b3d21c9eaa38366381382b655d25eb2f35e7597090f91`।

## Function / object / element inventory

- DOM IDs: `appHeader`, `issueFilter`, `issueCount`, `issueTable`, `issueModal`, `issueMemberSearch`, `studentOptions`, `eligibilityNote`, `loanAllowance`, `bookOptions`, `copyOptions`, `bookOptions2`, `copyOptions2`, `bookOptions3`, `copyOptions3`, `toast`
- Form keys: `studentId`, `bookId`, `copyId`, `bookId2`, `copyId2`, `bookId3`, `copyId3`
- Loaded/linked resources: `/static/styles.css?v=members-audit-1`, `/static/polish.css?v=1`, `/static/notifications.css?v=due-2`, `/static/notifications.js?v=reminders-4`, `/static/shared.js?v=priority-3`, `/static/circulation.js?v=copy-3`

## সম্পূর্ণ original source

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Circulation | PSTU Library</title>
    <link rel="stylesheet" href="/static/styles.css?v=members-audit-1" />
    <link rel="stylesheet" href="/static/polish.css?v=1" />
    <link rel="stylesheet" href="/static/notifications.css?v=due-2" />
  </head>
  <body data-page="circulation">
    <div id="appHeader"></div>
    <main class="workspace">
      <section class="page-heading">
        <div>
          <p class="eyebrow">Circulation</p>
          <h1>Issue and return</h1>
          <p class="heading-copy">Track every borrowing transaction in date order.</p>
        </div>
        <button class="button primary" data-open="issueModal">Issue book</button>
      </section>
      <section class="toolbar">
        <label class="filter-field"
          ><span>Show records</span
          ><select id="issueFilter">
            <option value="ALL">All transactions</option>
            <option value="ISSUED">Currently issued</option>
            <option value="RETURNED">Returned</option>
          </select></label
        ><span class="record-count" id="issueCount"></span>
      </section>
      <section class="surface"><div class="table-wrap" id="issueTable"></div></section>
    </main>
    <div class="modal" id="issueModal" aria-hidden="true">
      <form data-kind="issue">
        <div class="modal-heading">
          <div>
            <span class="section-label">New transaction</span>
            <h2>Issue book</h2>
          </div>
          <button type="button" class="icon-button cancel" aria-label="Close">&times;</button>
        </div>
        <label
          >Find member<input
            id="issueMemberSearch"
            type="search"
            placeholder="Search by ID, name or department"
            autocomplete="off" /></label
        ><label
          >Eligible member<select name="studentId" id="studentOptions" required></select
        ></label>
        <p class="form-note" id="eligibilityNote"></p>
        <p class="form-note" id="loanAllowance"></p>
        <p class="form-note">Books are due 15 days after the issue date.</p>
        <label>Book 1<select name="bookId" id="bookOptions" required></select></label
        ><label>Physical copy<select name="copyId" id="copyOptions" required></select></label>
        <label>Book 2 (optional)<select name="bookId2" id="bookOptions2"></select></label
        ><label>Physical copy<select name="copyId2" id="copyOptions2"></select></label>
        <label>Book 3 (optional)<select name="bookId3" id="bookOptions3"></select></label
        ><label>Physical copy<select name="copyId3" id="copyOptions3"></select></label>
        <div class="form-actions">
          <button type="button" class="button secondary cancel">Cancel</button
          ><button class="button primary">Issue selected copies</button>
        </div>
      </form>
    </div>
    <div id="toast" role="status" aria-live="polite"></div>
    <script src="/static/notifications.js?v=reminders-4"></script>
    <script src="/static/shared.js?v=priority-3"></script>
    <script src="/static/circulation.js?v=copy-3"></script>
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
| 6 | <code>    &lt;title&gt;Circulation &#124; PSTU Library&lt;/title&gt;</code> | title: HTML structure/content |
| 7 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/styles.css?v=members-audit-1&quot; /&gt;</code> | link: stylesheet/resource load |
| 8 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/polish.css?v=1&quot; /&gt;</code> | link: stylesheet/resource load |
| 9 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/notifications.css?v=due-2&quot; /&gt;</code> | link: stylesheet/resource load |
| 10 | <code>  &lt;/head&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 11 | <code>  &lt;body data-page=&quot;circulation&quot;&gt;</code> | body: HTML structure/content |
| 12 | <code>    &lt;div id=&quot;appHeader&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 13 | <code>    &lt;main class=&quot;workspace&quot;&gt;</code> | main: primary page content |
| 14 | <code>      &lt;section class=&quot;page-heading&quot;&gt;</code> | section: related UI content grouping |
| 15 | <code>        &lt;div&gt;</code> | div: layout/dynamic content container |
| 16 | <code>          &lt;p class=&quot;eyebrow&quot;&gt;Circulation&lt;/p&gt;</code> | p: description/help text |
| 17 | <code>          &lt;h1&gt;Issue and return&lt;/h1&gt;</code> | h1: page heading |
| 18 | <code>          &lt;p class=&quot;heading-copy&quot;&gt;Track every borrowing transaction in date order.&lt;/p&gt;</code> | p: description/help text |
| 19 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 20 | <code>        &lt;button class=&quot;button primary&quot; data-open=&quot;issueModal&quot;&gt;Issue book&lt;/button&gt;</code> | button: action/submit/cancel control |
| 21 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 22 | <code>      &lt;section class=&quot;toolbar&quot;&gt;</code> | section: related UI content grouping |
| 23 | <code>        &lt;label class=&quot;filter-field&quot;</code> | label: field-এর readable label |
| 24 | <code>          &gt;&lt;span&gt;Show records&lt;/span</code> | span: HTML structure/content |
| 25 | <code>          &gt;&lt;select id=&quot;issueFilter&quot;&gt;</code> | select: option থেকে value নির্বাচন |
| 26 | <code>            &lt;option value=&quot;ALL&quot;&gt;All transactions&lt;/option&gt;</code> | option: select-এর choice |
| 27 | <code>            &lt;option value=&quot;ISSUED&quot;&gt;Currently issued&lt;/option&gt;</code> | option: select-এর choice |
| 28 | <code>            &lt;option value=&quot;RETURNED&quot;&gt;Returned&lt;/option&gt;</code> | option: select-এর choice |
| 29 | <code>          &lt;/select&gt;&lt;/label</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 30 | <code>        &gt;&lt;span class=&quot;record-count&quot; id=&quot;issueCount&quot;&gt;&lt;/span&gt;</code> | span: HTML structure/content |
| 31 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 32 | <code>      &lt;section class=&quot;surface&quot;&gt;&lt;div class=&quot;table-wrap&quot; id=&quot;issueTable&quot;&gt;&lt;/div&gt;&lt;/section&gt;</code> | section: related UI content grouping; div: layout/dynamic content container |
| 33 | <code>    &lt;/main&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 34 | <code>    &lt;div class=&quot;modal&quot; id=&quot;issueModal&quot; aria-hidden=&quot;true&quot;&gt;</code> | div: layout/dynamic content container |
| 35 | <code>      &lt;form data-kind=&quot;issue&quot;&gt;</code> | form: submit-able input grouping |
| 36 | <code>        &lt;div class=&quot;modal-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 37 | <code>          &lt;div&gt;</code> | div: layout/dynamic content container |
| 38 | <code>            &lt;span class=&quot;section-label&quot;&gt;New transaction&lt;/span&gt;</code> | span: HTML structure/content |
| 39 | <code>            &lt;h2&gt;Issue book&lt;/h2&gt;</code> | h2: section/dialog heading |
| 40 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 41 | <code>          &lt;button type=&quot;button&quot; class=&quot;icon-button cancel&quot; aria-label=&quot;Close&quot;&gt;&amp;times;&lt;/button&gt;</code> | button: action/submit/cancel control |
| 42 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 43 | <code>        &lt;label</code> | label: field-এর readable label |
| 44 | <code>          &gt;Find member&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 45 | <code>            id=&quot;issueMemberSearch&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 46 | <code>            type=&quot;search&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 47 | <code>            placeholder=&quot;Search by ID, name or department&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 48 | <code>            autocomplete=&quot;off&quot; /&gt;&lt;/label</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 49 | <code>        &gt;&lt;label</code> | label: field-এর readable label |
| 50 | <code>          &gt;Eligible member&lt;select name=&quot;studentId&quot; id=&quot;studentOptions&quot; required&gt;&lt;/select</code> | select: option থেকে value নির্বাচন |
| 51 | <code>        &gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 52 | <code>        &lt;p class=&quot;form-note&quot; id=&quot;eligibilityNote&quot;&gt;&lt;/p&gt;</code> | p: description/help text |
| 53 | <code>        &lt;p class=&quot;form-note&quot; id=&quot;loanAllowance&quot;&gt;&lt;/p&gt;</code> | p: description/help text |
| 54 | <code>        &lt;p class=&quot;form-note&quot;&gt;Books are due 15 days after the issue date.&lt;/p&gt;</code> | p: description/help text |
| 55 | <code>        &lt;label&gt;Book 1&lt;select name=&quot;bookId&quot; id=&quot;bookOptions&quot; required&gt;&lt;/select&gt;&lt;/label</code> | label: field-এর readable label; select: option থেকে value নির্বাচন |
| 56 | <code>        &gt;&lt;label&gt;Physical copy&lt;select name=&quot;copyId&quot; id=&quot;copyOptions&quot; required&gt;&lt;/select&gt;&lt;/label&gt;</code> | label: field-এর readable label; select: option থেকে value নির্বাচন |
| 57 | <code>        &lt;label&gt;Book 2 (optional)&lt;select name=&quot;bookId2&quot; id=&quot;bookOptions2&quot;&gt;&lt;/select&gt;&lt;/label</code> | label: field-এর readable label; select: option থেকে value নির্বাচন |
| 58 | <code>        &gt;&lt;label&gt;Physical copy&lt;select name=&quot;copyId2&quot; id=&quot;copyOptions2&quot;&gt;&lt;/select&gt;&lt;/label&gt;</code> | label: field-এর readable label; select: option থেকে value নির্বাচন |
| 59 | <code>        &lt;label&gt;Book 3 (optional)&lt;select name=&quot;bookId3&quot; id=&quot;bookOptions3&quot;&gt;&lt;/select&gt;&lt;/label</code> | label: field-এর readable label; select: option থেকে value নির্বাচন |
| 60 | <code>        &gt;&lt;label&gt;Physical copy&lt;select name=&quot;copyId3&quot; id=&quot;copyOptions3&quot;&gt;&lt;/select&gt;&lt;/label&gt;</code> | label: field-এর readable label; select: option থেকে value নির্বাচন |
| 61 | <code>        &lt;div class=&quot;form-actions&quot;&gt;</code> | div: layout/dynamic content container |
| 62 | <code>          &lt;button type=&quot;button&quot; class=&quot;button secondary cancel&quot;&gt;Cancel&lt;/button</code> | button: action/submit/cancel control |
| 63 | <code>          &gt;&lt;button class=&quot;button primary&quot;&gt;Issue selected copies&lt;/button&gt;</code> | button: action/submit/cancel control |
| 64 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 65 | <code>      &lt;/form&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 66 | <code>    &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 67 | <code>    &lt;div id=&quot;toast&quot; role=&quot;status&quot; aria-live=&quot;polite&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 68 | <code>    &lt;script src=&quot;/static/notifications.js?v=reminders-4&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 69 | <code>    &lt;script src=&quot;/static/shared.js?v=priority-3&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 70 | <code>    &lt;script src=&quot;/static/circulation.js?v=copy-3&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 71 | <code>  &lt;/body&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 72 | <code>&lt;/html&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
