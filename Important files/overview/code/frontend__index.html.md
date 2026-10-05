# frontend/index.html

এই page-এর semantic HTML structure: header placeholder, content sections, forms/dialogs এবং stylesheet/script links। Matching controller JavaScript interactions চালায়।

Source: [মূল file](../../frontend/index.html)। Snapshot 2026-10-04; 136 lines; SHA-256 `edf4fcc0fae1009cf7ed31f44c69debc54fdc053cb7c05aa35adc280806f6baf`।

## Function / object / element inventory

- DOM IDs: `appHeader`, `today`, `refreshButton`, `stats`, `deskPriorities`, `dueSoonDetails`, `dueSoonCount`, `dueSoonTable`, `fineAttentionTotal`, `fineAttentionTable`, `recentTable`, `inventorySnapshot`, `toast`
- Form keys: 
- Loaded/linked resources: `/static/styles.css?v=members-audit-1`, `/static/polish.css?v=1`, `/static/notifications.css?v=due-2`, `/static/admin.css?v=details-2`, `/circulation?new=1`, `/circulation?new=1`, `/books?new=1`, `/students?new=1`, `/reservations`, `/circulation`, `/fines`, `/circulation`, `/static/notifications.js?v=reminders-4`, `/static/shared.js?v=priority-3`, `/static/dashboard.js?v=priority-3`

## সম্পূর্ণ original source

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Dashboard | PSTU Library</title>
    <link rel="stylesheet" href="/static/styles.css?v=members-audit-1" />
    <link rel="stylesheet" href="/static/polish.css?v=1" />
    <link rel="stylesheet" href="/static/notifications.css?v=due-2" />
    <link rel="stylesheet" href="/static/admin.css?v=details-2" />
  </head>
  <body data-page="overview">
    <div id="appHeader"></div>
    <main class="workspace">
      <section class="admin-heading">
        <div>
          <p class="eyebrow">LIBRARY OPERATIONS</p>
          <h1>Management overview</h1>
          <p>Everything you need to keep the library moving.</p>
        </div>
        <div class="admin-heading-tools">
          <span id="today" class="current-date"></span
          ><button id="refreshButton" class="button secondary">Refresh data</button>
        </div>
      </section>
      <section class="admin-welcome">
        <div>
          <span class="cover-label">THE LIBRARY, IN FOCUS</span>
          <h2>A well-run library.<br />A better reading experience.</h2>
          <p>Manage your collection, support members, and stay ahead of upcoming returns.</p>
          <a class="button light" href="/circulation?new=1">Issue a book &rarr;</a>
        </div>
        <span class="admin-cover-note">PSTU Central Library</span>
      </section>
      <nav class="admin-shortcuts" aria-label="Quick library actions">
        <a href="/circulation?new=1"
          ><span class="shortcut-mark">01</span
          ><span><strong>Issue &amp; return</strong><small>Manage borrowing</small></span
          ><b>&nearr;</b></a
        ><a href="/books?new=1"
          ><span class="shortcut-mark">02</span
          ><span><strong>Manage collection</strong><small>Add books or stock</small></span
          ><b>&nearr;</b></a
        ><a href="/students?new=1"
          ><span class="shortcut-mark">03</span
          ><span><strong>Member services</strong><small>Register or update members</small></span
          ><b>&nearr;</b></a
        ><a href="/reservations"
          ><span class="shortcut-mark">04</span
          ><span><strong>Reservations</strong><small>Prepare reserved pickups</small></span
          ><b>&nearr;</b></a
        >
      </nav>
      <div class="dashboard-section-heading">
        <div>
          <span class="section-label">AT A GLANCE</span>
          <h2>Library performance</h2>
        </div>
        <span>Current collection and circulation</span>
      </div>
      <section class="metric-grid" id="stats" aria-label="Library summary"></section>
      <section class="desk-priorities">
        <div class="dashboard-section-heading">
          <div>
            <span class="section-label">DESK PRIORITIES</span>
            <h2>What needs attention</h2>
          </div>
          <span>Keep today's work in view</span>
        </div>
        <div id="deskPriorities" class="priority-grid"></div>
      </section>
      <section
        class="dashboard-grid attention-details"
        aria-label="Return reminders and fine details"
      >
        <article class="surface" id="dueSoonDetails">
          <div class="surface-heading">
            <div>
              <span class="section-label">3-DAY REMINDERS</span>
              <h2>Upcoming return dates</h2>
              <p id="dueSoonCount"></p>
            </div>
            <a class="text-link" href="/circulation">View all loans</a>
          </div>
          <div id="dueSoonTable" class="table-wrap"></div>
        </article>
        <article class="surface">
          <div class="surface-heading">
            <div>
              <span class="section-label">FINES &amp; OVERDUE</span>
              <h2>Members with outstanding fines</h2>
              <p id="fineAttentionTotal"></p>
            </div>
            <a class="text-link" href="/fines">View fines</a>
          </div>
          <div id="fineAttentionTable" class="table-wrap"></div>
          <p class="fine-estimate-note">
            Overdue amounts are estimates for today. The final fine is recorded when the book is
            returned.
          </p>
        </article>
      </section>
      <div class="dashboard-section-heading">
        <div>
          <span class="section-label">CIRCULATION &amp; COLLECTION</span>
          <h2>Daily activity</h2>
        </div>
      </div>
      <section class="dashboard-grid">
        <article class="surface activity-surface">
          <div class="surface-heading">
            <div>
              <span class="section-label">PRIORITY ACTIONS</span>
              <h2>Circulation action queue</h2>
            </div>
            <a class="text-link" href="/circulation">View register</a>
          </div>
          <div class="table-wrap" id="recentTable"></div>
        </article>
        <aside class="surface health-surface">
          <div class="surface-heading">
            <div>
              <span class="section-label">Collection health</span>
              <h2>Inventory status</h2>
            </div>
          </div>
          <div id="inventorySnapshot"></div>
        </aside>
      </section>
    </main>
    <div id="toast" role="status" aria-live="polite"></div>
    <script src="/static/notifications.js?v=reminders-4"></script>
    <script src="/static/shared.js?v=priority-3"></script>
    <script src="/static/dashboard.js?v=priority-3"></script>
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
| 6 | <code>    &lt;title&gt;Dashboard &#124; PSTU Library&lt;/title&gt;</code> | title: HTML structure/content |
| 7 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/styles.css?v=members-audit-1&quot; /&gt;</code> | link: stylesheet/resource load |
| 8 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/polish.css?v=1&quot; /&gt;</code> | link: stylesheet/resource load |
| 9 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/notifications.css?v=due-2&quot; /&gt;</code> | link: stylesheet/resource load |
| 10 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/admin.css?v=details-2&quot; /&gt;</code> | link: stylesheet/resource load |
| 11 | <code>  &lt;/head&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 12 | <code>  &lt;body data-page=&quot;overview&quot;&gt;</code> | body: HTML structure/content |
| 13 | <code>    &lt;div id=&quot;appHeader&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 14 | <code>    &lt;main class=&quot;workspace&quot;&gt;</code> | main: primary page content |
| 15 | <code>      &lt;section class=&quot;admin-heading&quot;&gt;</code> | section: related UI content grouping |
| 16 | <code>        &lt;div&gt;</code> | div: layout/dynamic content container |
| 17 | <code>          &lt;p class=&quot;eyebrow&quot;&gt;LIBRARY OPERATIONS&lt;/p&gt;</code> | p: description/help text |
| 18 | <code>          &lt;h1&gt;Management overview&lt;/h1&gt;</code> | h1: page heading |
| 19 | <code>          &lt;p&gt;Everything you need to keep the library moving.&lt;/p&gt;</code> | p: description/help text |
| 20 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 21 | <code>        &lt;div class=&quot;admin-heading-tools&quot;&gt;</code> | div: layout/dynamic content container |
| 22 | <code>          &lt;span id=&quot;today&quot; class=&quot;current-date&quot;&gt;&lt;/span</code> | span: HTML structure/content |
| 23 | <code>          &gt;&lt;button id=&quot;refreshButton&quot; class=&quot;button secondary&quot;&gt;Refresh data&lt;/button&gt;</code> | button: action/submit/cancel control |
| 24 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 25 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 26 | <code>      &lt;section class=&quot;admin-welcome&quot;&gt;</code> | section: related UI content grouping |
| 27 | <code>        &lt;div&gt;</code> | div: layout/dynamic content container |
| 28 | <code>          &lt;span class=&quot;cover-label&quot;&gt;THE LIBRARY, IN FOCUS&lt;/span&gt;</code> | span: HTML structure/content |
| 29 | <code>          &lt;h2&gt;A well-run library.&lt;br /&gt;A better reading experience.&lt;/h2&gt;</code> | h2: section/dialog heading; br: HTML structure/content |
| 30 | <code>          &lt;p&gt;Manage your collection, support members, and stay ahead of upcoming returns.&lt;/p&gt;</code> | p: description/help text |
| 31 | <code>          &lt;a class=&quot;button light&quot; href=&quot;/circulation?new=1&quot;&gt;Issue a book &amp;rarr;&lt;/a&gt;</code> | a: HTML structure/content |
| 32 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 33 | <code>        &lt;span class=&quot;admin-cover-note&quot;&gt;PSTU Central Library&lt;/span&gt;</code> | span: HTML structure/content |
| 34 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 35 | <code>      &lt;nav class=&quot;admin-shortcuts&quot; aria-label=&quot;Quick library actions&quot;&gt;</code> | nav: HTML structure/content |
| 36 | <code>        &lt;a href=&quot;/circulation?new=1&quot;</code> | a: HTML structure/content |
| 37 | <code>          &gt;&lt;span class=&quot;shortcut-mark&quot;&gt;01&lt;/span</code> | span: HTML structure/content |
| 38 | <code>          &gt;&lt;span&gt;&lt;strong&gt;Issue &amp;amp; return&lt;/strong&gt;&lt;small&gt;Manage borrowing&lt;/small&gt;&lt;/span</code> | span: HTML structure/content; strong: HTML structure/content; small: HTML structure/content |
| 39 | <code>          &gt;&lt;b&gt;&amp;nearr;&lt;/b&gt;&lt;/a</code> | b: HTML structure/content |
| 40 | <code>        &gt;&lt;a href=&quot;/books?new=1&quot;</code> | a: HTML structure/content |
| 41 | <code>          &gt;&lt;span class=&quot;shortcut-mark&quot;&gt;02&lt;/span</code> | span: HTML structure/content |
| 42 | <code>          &gt;&lt;span&gt;&lt;strong&gt;Manage collection&lt;/strong&gt;&lt;small&gt;Add books or stock&lt;/small&gt;&lt;/span</code> | span: HTML structure/content; strong: HTML structure/content; small: HTML structure/content |
| 43 | <code>          &gt;&lt;b&gt;&amp;nearr;&lt;/b&gt;&lt;/a</code> | b: HTML structure/content |
| 44 | <code>        &gt;&lt;a href=&quot;/students?new=1&quot;</code> | a: HTML structure/content |
| 45 | <code>          &gt;&lt;span class=&quot;shortcut-mark&quot;&gt;03&lt;/span</code> | span: HTML structure/content |
| 46 | <code>          &gt;&lt;span&gt;&lt;strong&gt;Member services&lt;/strong&gt;&lt;small&gt;Register or update members&lt;/small&gt;&lt;/span</code> | span: HTML structure/content; strong: HTML structure/content; small: HTML structure/content |
| 47 | <code>          &gt;&lt;b&gt;&amp;nearr;&lt;/b&gt;&lt;/a</code> | b: HTML structure/content |
| 48 | <code>        &gt;&lt;a href=&quot;/reservations&quot;</code> | a: HTML structure/content |
| 49 | <code>          &gt;&lt;span class=&quot;shortcut-mark&quot;&gt;04&lt;/span</code> | span: HTML structure/content |
| 50 | <code>          &gt;&lt;span&gt;&lt;strong&gt;Reservations&lt;/strong&gt;&lt;small&gt;Prepare reserved pickups&lt;/small&gt;&lt;/span</code> | span: HTML structure/content; strong: HTML structure/content; small: HTML structure/content |
| 51 | <code>          &gt;&lt;b&gt;&amp;nearr;&lt;/b&gt;&lt;/a</code> | b: HTML structure/content |
| 52 | <code>        &gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 53 | <code>      &lt;/nav&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 54 | <code>      &lt;div class=&quot;dashboard-section-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 55 | <code>        &lt;div&gt;</code> | div: layout/dynamic content container |
| 56 | <code>          &lt;span class=&quot;section-label&quot;&gt;AT A GLANCE&lt;/span&gt;</code> | span: HTML structure/content |
| 57 | <code>          &lt;h2&gt;Library performance&lt;/h2&gt;</code> | h2: section/dialog heading |
| 58 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 59 | <code>        &lt;span&gt;Current collection and circulation&lt;/span&gt;</code> | span: HTML structure/content |
| 60 | <code>      &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 61 | <code>      &lt;section class=&quot;metric-grid&quot; id=&quot;stats&quot; aria-label=&quot;Library summary&quot;&gt;&lt;/section&gt;</code> | section: related UI content grouping |
| 62 | <code>      &lt;section class=&quot;desk-priorities&quot;&gt;</code> | section: related UI content grouping |
| 63 | <code>        &lt;div class=&quot;dashboard-section-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 64 | <code>          &lt;div&gt;</code> | div: layout/dynamic content container |
| 65 | <code>            &lt;span class=&quot;section-label&quot;&gt;DESK PRIORITIES&lt;/span&gt;</code> | span: HTML structure/content |
| 66 | <code>            &lt;h2&gt;What needs attention&lt;/h2&gt;</code> | h2: section/dialog heading |
| 67 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 68 | <code>          &lt;span&gt;Keep today&#x27;s work in view&lt;/span&gt;</code> | span: HTML structure/content |
| 69 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 70 | <code>        &lt;div id=&quot;deskPriorities&quot; class=&quot;priority-grid&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 71 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 72 | <code>      &lt;section</code> | section: related UI content grouping |
| 73 | <code>        class=&quot;dashboard-grid attention-details&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 74 | <code>        aria-label=&quot;Return reminders and fine details&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 75 | <code>      &gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 76 | <code>        &lt;article class=&quot;surface&quot; id=&quot;dueSoonDetails&quot;&gt;</code> | article: HTML structure/content |
| 77 | <code>          &lt;div class=&quot;surface-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 78 | <code>            &lt;div&gt;</code> | div: layout/dynamic content container |
| 79 | <code>              &lt;span class=&quot;section-label&quot;&gt;3-DAY REMINDERS&lt;/span&gt;</code> | span: HTML structure/content |
| 80 | <code>              &lt;h2&gt;Upcoming return dates&lt;/h2&gt;</code> | h2: section/dialog heading |
| 81 | <code>              &lt;p id=&quot;dueSoonCount&quot;&gt;&lt;/p&gt;</code> | p: description/help text |
| 82 | <code>            &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 83 | <code>            &lt;a class=&quot;text-link&quot; href=&quot;/circulation&quot;&gt;View all loans&lt;/a&gt;</code> | a: HTML structure/content |
| 84 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 85 | <code>          &lt;div id=&quot;dueSoonTable&quot; class=&quot;table-wrap&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 86 | <code>        &lt;/article&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 87 | <code>        &lt;article class=&quot;surface&quot;&gt;</code> | article: HTML structure/content |
| 88 | <code>          &lt;div class=&quot;surface-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 89 | <code>            &lt;div&gt;</code> | div: layout/dynamic content container |
| 90 | <code>              &lt;span class=&quot;section-label&quot;&gt;FINES &amp;amp; OVERDUE&lt;/span&gt;</code> | span: HTML structure/content |
| 91 | <code>              &lt;h2&gt;Members with outstanding fines&lt;/h2&gt;</code> | h2: section/dialog heading |
| 92 | <code>              &lt;p id=&quot;fineAttentionTotal&quot;&gt;&lt;/p&gt;</code> | p: description/help text |
| 93 | <code>            &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 94 | <code>            &lt;a class=&quot;text-link&quot; href=&quot;/fines&quot;&gt;View fines&lt;/a&gt;</code> | a: HTML structure/content |
| 95 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 96 | <code>          &lt;div id=&quot;fineAttentionTable&quot; class=&quot;table-wrap&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 97 | <code>          &lt;p class=&quot;fine-estimate-note&quot;&gt;</code> | p: description/help text |
| 98 | <code>            Overdue amounts are estimates for today. The final fine is recorded when the book is</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 99 | <code>            returned.</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 100 | <code>          &lt;/p&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 101 | <code>        &lt;/article&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 102 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 103 | <code>      &lt;div class=&quot;dashboard-section-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 104 | <code>        &lt;div&gt;</code> | div: layout/dynamic content container |
| 105 | <code>          &lt;span class=&quot;section-label&quot;&gt;CIRCULATION &amp;amp; COLLECTION&lt;/span&gt;</code> | span: HTML structure/content |
| 106 | <code>          &lt;h2&gt;Daily activity&lt;/h2&gt;</code> | h2: section/dialog heading |
| 107 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 108 | <code>      &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 109 | <code>      &lt;section class=&quot;dashboard-grid&quot;&gt;</code> | section: related UI content grouping |
| 110 | <code>        &lt;article class=&quot;surface activity-surface&quot;&gt;</code> | article: HTML structure/content |
| 111 | <code>          &lt;div class=&quot;surface-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 112 | <code>            &lt;div&gt;</code> | div: layout/dynamic content container |
| 113 | <code>              &lt;span class=&quot;section-label&quot;&gt;PRIORITY ACTIONS&lt;/span&gt;</code> | span: HTML structure/content |
| 114 | <code>              &lt;h2&gt;Circulation action queue&lt;/h2&gt;</code> | h2: section/dialog heading |
| 115 | <code>            &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 116 | <code>            &lt;a class=&quot;text-link&quot; href=&quot;/circulation&quot;&gt;View register&lt;/a&gt;</code> | a: HTML structure/content |
| 117 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 118 | <code>          &lt;div class=&quot;table-wrap&quot; id=&quot;recentTable&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 119 | <code>        &lt;/article&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 120 | <code>        &lt;aside class=&quot;surface health-surface&quot;&gt;</code> | aside: HTML structure/content |
| 121 | <code>          &lt;div class=&quot;surface-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 122 | <code>            &lt;div&gt;</code> | div: layout/dynamic content container |
| 123 | <code>              &lt;span class=&quot;section-label&quot;&gt;Collection health&lt;/span&gt;</code> | span: HTML structure/content |
| 124 | <code>              &lt;h2&gt;Inventory status&lt;/h2&gt;</code> | h2: section/dialog heading |
| 125 | <code>            &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 126 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 127 | <code>          &lt;div id=&quot;inventorySnapshot&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 128 | <code>        &lt;/aside&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 129 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 130 | <code>    &lt;/main&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 131 | <code>    &lt;div id=&quot;toast&quot; role=&quot;status&quot; aria-live=&quot;polite&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 132 | <code>    &lt;script src=&quot;/static/notifications.js?v=reminders-4&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 133 | <code>    &lt;script src=&quot;/static/shared.js?v=priority-3&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 134 | <code>    &lt;script src=&quot;/static/dashboard.js?v=priority-3&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 135 | <code>  &lt;/body&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 136 | <code>&lt;/html&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
