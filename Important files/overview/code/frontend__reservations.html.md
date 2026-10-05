# frontend/reservations.html

এই page-এর semantic HTML structure: header placeholder, content sections, forms/dialogs এবং stylesheet/script links। Matching controller JavaScript interactions চালায়।

Source: [মূল file](../../frontend/reservations.html)। Snapshot 2026-10-04; 44 lines; SHA-256 `86cd13531a0b0f40b2e25875a55b6a50bb1b38a4ca71b8836c35e2d3d76cd08a`।

## Function / object / element inventory

- DOM IDs: `appHeader`, `refreshButton`, `reserveForm`, `reserveMember`, `reserveBook`, `reservationCount`, `reservationTable`, `toast`
- Form keys: `studentId`, `bookId`
- Loaded/linked resources: `/static/styles.css?v=members-audit-1`, `/static/polish.css?v=1`, `/static/notifications.css?v=due-2`, `/static/notifications.js?v=reminders-4`, `/static/shared.js?v=priority-3`, `/static/reservation-desk.js?v=modules-1`, `/static/reservations.js?v=priority-3`

## সম্পূর্ণ original source

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>Reservations | PSTU Library</title>
    <link rel="stylesheet" href="/static/styles.css?v=members-audit-1" />
    <link rel="stylesheet" href="/static/polish.css?v=1" />
    <link rel="stylesheet" href="/static/notifications.css?v=due-2" />
  </head>
  <body data-page="reservations">
    <div id="appHeader"></div>
    <main class="workspace">
      <section class="page-heading">
        <div>
          <p class="eyebrow">Library desk</p>
          <h1>Reservations</h1>
          <p class="heading-copy">
            Hold a copy for 3 days, issue it on collection, or cancel the hold.
          </p>
        </div>
        <button id="refreshButton" class="button secondary">Refresh</button>
      </section>
      <section class="surface form-surface">
        <h2>Reserve for a member</h2>
        <form id="reserveForm" class="account-form horizontal-form">
          <label>Member<select name="studentId" id="reserveMember" required></select></label
          ><label>Book<select name="bookId" id="reserveBook" required></select></label
          ><button class="button primary">Reserve for 3 days</button>
        </form>
      </section>
      <section class="toolbar">
        <strong>Reservations and history</strong
        ><span id="reservationCount" class="record-count"></span>
      </section>
      <section class="surface"><div id="reservationTable" class="table-wrap"></div></section>
    </main>
    <div id="toast" role="status" aria-live="polite"></div>
    <script src="/static/notifications.js?v=reminders-4"></script>
    <script src="/static/shared.js?v=priority-3"></script>
    <script src="/static/reservation-desk.js?v=modules-1"></script>
    <script src="/static/reservations.js?v=priority-3"></script>
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
| 5 | <code>    &lt;meta name=&quot;viewport&quot; content=&quot;width=device-width,initial-scale=1&quot; /&gt;</code> | meta: encoding/viewport metadata |
| 6 | <code>    &lt;title&gt;Reservations &#124; PSTU Library&lt;/title&gt;</code> | title: HTML structure/content |
| 7 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/styles.css?v=members-audit-1&quot; /&gt;</code> | link: stylesheet/resource load |
| 8 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/polish.css?v=1&quot; /&gt;</code> | link: stylesheet/resource load |
| 9 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/notifications.css?v=due-2&quot; /&gt;</code> | link: stylesheet/resource load |
| 10 | <code>  &lt;/head&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 11 | <code>  &lt;body data-page=&quot;reservations&quot;&gt;</code> | body: HTML structure/content |
| 12 | <code>    &lt;div id=&quot;appHeader&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 13 | <code>    &lt;main class=&quot;workspace&quot;&gt;</code> | main: primary page content |
| 14 | <code>      &lt;section class=&quot;page-heading&quot;&gt;</code> | section: related UI content grouping |
| 15 | <code>        &lt;div&gt;</code> | div: layout/dynamic content container |
| 16 | <code>          &lt;p class=&quot;eyebrow&quot;&gt;Library desk&lt;/p&gt;</code> | p: description/help text |
| 17 | <code>          &lt;h1&gt;Reservations&lt;/h1&gt;</code> | h1: page heading |
| 18 | <code>          &lt;p class=&quot;heading-copy&quot;&gt;</code> | p: description/help text |
| 19 | <code>            Hold a copy for 3 days, issue it on collection, or cancel the hold.</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 20 | <code>          &lt;/p&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 21 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 22 | <code>        &lt;button id=&quot;refreshButton&quot; class=&quot;button secondary&quot;&gt;Refresh&lt;/button&gt;</code> | button: action/submit/cancel control |
| 23 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 24 | <code>      &lt;section class=&quot;surface form-surface&quot;&gt;</code> | section: related UI content grouping |
| 25 | <code>        &lt;h2&gt;Reserve for a member&lt;/h2&gt;</code> | h2: section/dialog heading |
| 26 | <code>        &lt;form id=&quot;reserveForm&quot; class=&quot;account-form horizontal-form&quot;&gt;</code> | form: submit-able input grouping |
| 27 | <code>          &lt;label&gt;Member&lt;select name=&quot;studentId&quot; id=&quot;reserveMember&quot; required&gt;&lt;/select&gt;&lt;/label</code> | label: field-এর readable label; select: option থেকে value নির্বাচন |
| 28 | <code>          &gt;&lt;label&gt;Book&lt;select name=&quot;bookId&quot; id=&quot;reserveBook&quot; required&gt;&lt;/select&gt;&lt;/label</code> | label: field-এর readable label; select: option থেকে value নির্বাচন |
| 29 | <code>          &gt;&lt;button class=&quot;button primary&quot;&gt;Reserve for 3 days&lt;/button&gt;</code> | button: action/submit/cancel control |
| 30 | <code>        &lt;/form&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 31 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 32 | <code>      &lt;section class=&quot;toolbar&quot;&gt;</code> | section: related UI content grouping |
| 33 | <code>        &lt;strong&gt;Reservations and history&lt;/strong</code> | strong: HTML structure/content |
| 34 | <code>        &gt;&lt;span id=&quot;reservationCount&quot; class=&quot;record-count&quot;&gt;&lt;/span&gt;</code> | span: HTML structure/content |
| 35 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 36 | <code>      &lt;section class=&quot;surface&quot;&gt;&lt;div id=&quot;reservationTable&quot; class=&quot;table-wrap&quot;&gt;&lt;/div&gt;&lt;/section&gt;</code> | section: related UI content grouping; div: layout/dynamic content container |
| 37 | <code>    &lt;/main&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 38 | <code>    &lt;div id=&quot;toast&quot; role=&quot;status&quot; aria-live=&quot;polite&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 39 | <code>    &lt;script src=&quot;/static/notifications.js?v=reminders-4&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 40 | <code>    &lt;script src=&quot;/static/shared.js?v=priority-3&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 41 | <code>    &lt;script src=&quot;/static/reservation-desk.js?v=modules-1&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 42 | <code>    &lt;script src=&quot;/static/reservations.js?v=priority-3&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 43 | <code>  &lt;/body&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 44 | <code>&lt;/html&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
