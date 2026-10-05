# frontend/fines.html

এই page-এর semantic HTML structure: header placeholder, content sections, forms/dialogs এবং stylesheet/script links। Matching controller JavaScript interactions চালায়।

Source: [মূল file](../../frontend/fines.html)। Snapshot 2026-10-04; 94 lines; SHA-256 `dbfc21c499b20ba8e9937c34785736a348d7483a481865d01f09f0591ac2cc68`।

## Function / object / element inventory

- DOM IDs: `appHeader`, `refreshButton`, `fineSummary`, `fineCollection`, `overdueTotal`, `overdueTable`, `fineTotal`, `fineTable`, `paymentModal`, `paymentBalance`, `paymentHistoryModal`, `paymentHistory`, `toast`
- Form keys: `fineId`, `note`
- Loaded/linked resources: `/static/styles.css?v=members-audit-1`, `/static/polish.css?v=1`, `/static/notifications.css?v=due-2`, `/static/notifications.js?v=reminders-4`, `/static/shared.js?v=priority-3`, `/static/fines.js?v=collection-1`

## সম্পূর্ণ original source

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Fines | PSTU Library</title>
    <link rel="stylesheet" href="/static/styles.css?v=members-audit-1" />
    <link rel="stylesheet" href="/static/polish.css?v=1" />
    <link rel="stylesheet" href="/static/notifications.css?v=due-2" />
  </head>
  <body data-page="fines">
    <div id="appHeader"></div>
    <main class="workspace">
      <section class="page-heading">
        <div>
          <p class="eyebrow">Accounts</p>
          <h1>Fine register</h1>
          <p class="heading-copy">
            Review overdue books, return them, and track all outstanding fines.
          </p>
        </div>
        <button id="refreshButton" class="button secondary">Refresh data</button>
      </section>
      <section class="metric-grid compact" id="fineSummary"></section>
      <section class="toolbar">
        <div>
          <strong>Fine collection</strong>
          <p class="form-note">
            Total includes all recorded payments. Today and this month use dated receipts in
            Asia/Dhaka.
          </p>
        </div>
      </section>
      <section
        class="metric-grid compact"
        id="fineCollection"
        aria-label="Fine collection totals"
        aria-live="polite"
      ></section>
      <section class="toolbar">
        <div>
          <strong>Overdue books awaiting return</strong>
          <p class="form-note">
            Fine grows by Tk 10 per overdue day. Returning the book records the final fine below.
          </p>
        </div>
        <span class="record-count" id="overdueTotal"></span>
      </section>
      <section class="surface"><div class="table-wrap" id="overdueTable"></div></section>
      <section class="toolbar">
        <strong>Returns and payment history</strong
        ><span class="record-count" id="fineTotal"></span>
      </section>
      <section class="surface"><div class="table-wrap" id="fineTable"></div></section>
    </main>
    <div class="modal" id="paymentModal" aria-hidden="true">
      <form>
        <div class="modal-heading">
          <div>
            <span class="section-label">Fine payment</span>
            <h2>Pay full fine</h2>
          </div>
          <button type="button" class="icon-button cancel" aria-label="Close">&times;</button>
        </div>
        <p id="paymentBalance" class="form-note"></p>
        <input type="hidden" name="fineId" />
        <label
          >Note / reason (optional)<input
            name="note"
            maxlength="300"
            placeholder="Payment reference"
        /></label>
        <p class="form-note">The full outstanding balance will be paid in one payment.</p>
        <div class="form-actions">
          <button type="button" class="button secondary cancel">Cancel</button
          ><button class="button primary">Pay full fine</button>
        </div>
      </form>
    </div>
    <div class="modal" id="paymentHistoryModal" aria-hidden="true">
      <form>
        <div class="modal-heading">
          <h2>Payment receipts</h2>
          <button type="button" class="icon-button cancel" aria-label="Close">&times;</button>
        </div>
        <div id="paymentHistory"></div>
      </form>
    </div>
    <div id="toast" role="status" aria-live="polite"></div>
    <script src="/static/notifications.js?v=reminders-4"></script>
    <script src="/static/shared.js?v=priority-3"></script>
    <script src="/static/fines.js?v=collection-1"></script>
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
| 6 | <code>    &lt;title&gt;Fines &#124; PSTU Library&lt;/title&gt;</code> | title: HTML structure/content |
| 7 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/styles.css?v=members-audit-1&quot; /&gt;</code> | link: stylesheet/resource load |
| 8 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/polish.css?v=1&quot; /&gt;</code> | link: stylesheet/resource load |
| 9 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/notifications.css?v=due-2&quot; /&gt;</code> | link: stylesheet/resource load |
| 10 | <code>  &lt;/head&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 11 | <code>  &lt;body data-page=&quot;fines&quot;&gt;</code> | body: HTML structure/content |
| 12 | <code>    &lt;div id=&quot;appHeader&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 13 | <code>    &lt;main class=&quot;workspace&quot;&gt;</code> | main: primary page content |
| 14 | <code>      &lt;section class=&quot;page-heading&quot;&gt;</code> | section: related UI content grouping |
| 15 | <code>        &lt;div&gt;</code> | div: layout/dynamic content container |
| 16 | <code>          &lt;p class=&quot;eyebrow&quot;&gt;Accounts&lt;/p&gt;</code> | p: description/help text |
| 17 | <code>          &lt;h1&gt;Fine register&lt;/h1&gt;</code> | h1: page heading |
| 18 | <code>          &lt;p class=&quot;heading-copy&quot;&gt;</code> | p: description/help text |
| 19 | <code>            Review overdue books, return them, and track all outstanding fines.</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 20 | <code>          &lt;/p&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 21 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 22 | <code>        &lt;button id=&quot;refreshButton&quot; class=&quot;button secondary&quot;&gt;Refresh data&lt;/button&gt;</code> | button: action/submit/cancel control |
| 23 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 24 | <code>      &lt;section class=&quot;metric-grid compact&quot; id=&quot;fineSummary&quot;&gt;&lt;/section&gt;</code> | section: related UI content grouping |
| 25 | <code>      &lt;section class=&quot;toolbar&quot;&gt;</code> | section: related UI content grouping |
| 26 | <code>        &lt;div&gt;</code> | div: layout/dynamic content container |
| 27 | <code>          &lt;strong&gt;Fine collection&lt;/strong&gt;</code> | strong: HTML structure/content |
| 28 | <code>          &lt;p class=&quot;form-note&quot;&gt;</code> | p: description/help text |
| 29 | <code>            Total includes all recorded payments. Today and this month use dated receipts in</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 30 | <code>            Asia/Dhaka.</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 31 | <code>          &lt;/p&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 32 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 33 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 34 | <code>      &lt;section</code> | section: related UI content grouping |
| 35 | <code>        class=&quot;metric-grid compact&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 36 | <code>        id=&quot;fineCollection&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 37 | <code>        aria-label=&quot;Fine collection totals&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 38 | <code>        aria-live=&quot;polite&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 39 | <code>      &gt;&lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 40 | <code>      &lt;section class=&quot;toolbar&quot;&gt;</code> | section: related UI content grouping |
| 41 | <code>        &lt;div&gt;</code> | div: layout/dynamic content container |
| 42 | <code>          &lt;strong&gt;Overdue books awaiting return&lt;/strong&gt;</code> | strong: HTML structure/content |
| 43 | <code>          &lt;p class=&quot;form-note&quot;&gt;</code> | p: description/help text |
| 44 | <code>            Fine grows by Tk 10 per overdue day. Returning the book records the final fine below.</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 45 | <code>          &lt;/p&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 46 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 47 | <code>        &lt;span class=&quot;record-count&quot; id=&quot;overdueTotal&quot;&gt;&lt;/span&gt;</code> | span: HTML structure/content |
| 48 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 49 | <code>      &lt;section class=&quot;surface&quot;&gt;&lt;div class=&quot;table-wrap&quot; id=&quot;overdueTable&quot;&gt;&lt;/div&gt;&lt;/section&gt;</code> | section: related UI content grouping; div: layout/dynamic content container |
| 50 | <code>      &lt;section class=&quot;toolbar&quot;&gt;</code> | section: related UI content grouping |
| 51 | <code>        &lt;strong&gt;Returns and payment history&lt;/strong</code> | strong: HTML structure/content |
| 52 | <code>        &gt;&lt;span class=&quot;record-count&quot; id=&quot;fineTotal&quot;&gt;&lt;/span&gt;</code> | span: HTML structure/content |
| 53 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 54 | <code>      &lt;section class=&quot;surface&quot;&gt;&lt;div class=&quot;table-wrap&quot; id=&quot;fineTable&quot;&gt;&lt;/div&gt;&lt;/section&gt;</code> | section: related UI content grouping; div: layout/dynamic content container |
| 55 | <code>    &lt;/main&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 56 | <code>    &lt;div class=&quot;modal&quot; id=&quot;paymentModal&quot; aria-hidden=&quot;true&quot;&gt;</code> | div: layout/dynamic content container |
| 57 | <code>      &lt;form&gt;</code> | form: submit-able input grouping |
| 58 | <code>        &lt;div class=&quot;modal-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 59 | <code>          &lt;div&gt;</code> | div: layout/dynamic content container |
| 60 | <code>            &lt;span class=&quot;section-label&quot;&gt;Fine payment&lt;/span&gt;</code> | span: HTML structure/content |
| 61 | <code>            &lt;h2&gt;Pay full fine&lt;/h2&gt;</code> | h2: section/dialog heading |
| 62 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 63 | <code>          &lt;button type=&quot;button&quot; class=&quot;icon-button cancel&quot; aria-label=&quot;Close&quot;&gt;&amp;times;&lt;/button&gt;</code> | button: action/submit/cancel control |
| 64 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 65 | <code>        &lt;p id=&quot;paymentBalance&quot; class=&quot;form-note&quot;&gt;&lt;/p&gt;</code> | p: description/help text |
| 66 | <code>        &lt;input type=&quot;hidden&quot; name=&quot;fineId&quot; /&gt;</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 67 | <code>        &lt;label</code> | label: field-এর readable label |
| 68 | <code>          &gt;Note / reason (optional)&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 69 | <code>            name=&quot;note&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 70 | <code>            maxlength=&quot;300&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 71 | <code>            placeholder=&quot;Payment reference&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 72 | <code>        /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 73 | <code>        &lt;p class=&quot;form-note&quot;&gt;The full outstanding balance will be paid in one payment.&lt;/p&gt;</code> | p: description/help text |
| 74 | <code>        &lt;div class=&quot;form-actions&quot;&gt;</code> | div: layout/dynamic content container |
| 75 | <code>          &lt;button type=&quot;button&quot; class=&quot;button secondary cancel&quot;&gt;Cancel&lt;/button</code> | button: action/submit/cancel control |
| 76 | <code>          &gt;&lt;button class=&quot;button primary&quot;&gt;Pay full fine&lt;/button&gt;</code> | button: action/submit/cancel control |
| 77 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 78 | <code>      &lt;/form&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 79 | <code>    &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 80 | <code>    &lt;div class=&quot;modal&quot; id=&quot;paymentHistoryModal&quot; aria-hidden=&quot;true&quot;&gt;</code> | div: layout/dynamic content container |
| 81 | <code>      &lt;form&gt;</code> | form: submit-able input grouping |
| 82 | <code>        &lt;div class=&quot;modal-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 83 | <code>          &lt;h2&gt;Payment receipts&lt;/h2&gt;</code> | h2: section/dialog heading |
| 84 | <code>          &lt;button type=&quot;button&quot; class=&quot;icon-button cancel&quot; aria-label=&quot;Close&quot;&gt;&amp;times;&lt;/button&gt;</code> | button: action/submit/cancel control |
| 85 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 86 | <code>        &lt;div id=&quot;paymentHistory&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 87 | <code>      &lt;/form&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 88 | <code>    &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 89 | <code>    &lt;div id=&quot;toast&quot; role=&quot;status&quot; aria-live=&quot;polite&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 90 | <code>    &lt;script src=&quot;/static/notifications.js?v=reminders-4&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 91 | <code>    &lt;script src=&quot;/static/shared.js?v=priority-3&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 92 | <code>    &lt;script src=&quot;/static/fines.js?v=collection-1&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 93 | <code>  &lt;/body&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 94 | <code>&lt;/html&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
