# frontend/accounts.html

এই page-এর semantic HTML structure: header placeholder, content sections, forms/dialogs এবং stylesheet/script links। Matching controller JavaScript interactions চালায়।

Source: [মূল file](../../frontend/accounts.html)। Snapshot 2026-10-04; 122 lines; SHA-256 `79caa915bc7d1184091c337b86346e706d3421fb6ee30f2fa8122f2a839e361d`।

## Function / object / element inventory

- DOM IDs: `appHeader`, `accountCount`, `accountTable`, `librarianForm`, `credentialsForm`, `toast`
- Form keys: `username`, `password`, `confirmPassword`, `currentPassword`, `newUsername`, `newPassword`, `confirmPassword`
- Loaded/linked resources: `/static/styles.css?v=members-audit-1`, `/static/polish.css?v=1`, `/static/notifications.css?v=due-2`, `/static/notifications.js?v=reminders-4`, `/static/shared.js?v=priority-3`, `/static/accounts.js`

## সম্পূর্ণ original source

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Accounts | PSTU Library</title>
    <link rel="stylesheet" href="/static/styles.css?v=members-audit-1" />
    <link rel="stylesheet" href="/static/polish.css?v=1" />
    <link rel="stylesheet" href="/static/notifications.css?v=due-2" />
  </head>
  <body data-page="accounts">
    <div id="appHeader"></div>
    <main class="workspace">
      <section class="page-heading">
        <div>
          <p class="eyebrow">Administration</p>
          <h1>Account management</h1>
          <p class="heading-copy">
            Create librarian access and maintain administrator credentials.
          </p>
        </div>
      </section>

      <section class="account-grid">
        <article class="surface account-list-panel">
          <div class="surface-heading">
            <div>
              <span class="section-label">Authorized users</span>
              <h2>Management accounts</h2>
            </div>
            <span class="record-count" id="accountCount"></span>
          </div>
          <div class="table-wrap" id="accountTable"></div>
        </article>

        <article class="surface form-surface">
          <div class="surface-heading">
            <div>
              <span class="section-label">New access</span>
              <h2>Create librarian</h2>
            </div>
          </div>
          <form id="librarianForm" class="account-form">
            <label
              >Username<input
                name="username"
                minlength="3"
                maxlength="30"
                pattern="[A-Za-z][A-Za-z0-9_]{2,29}"
                placeholder="Example: librarian01"
                required
            /></label>
            <label
              >Password<input
                name="password"
                type="password"
                minlength="4"
                autocomplete="new-password"
                required
            /></label>
            <label
              >Confirm password<input
                name="confirmPassword"
                type="password"
                minlength="4"
                autocomplete="new-password"
                required
            /></label>
            <button class="button primary">Create librarian account</button>
          </form>
        </article>
      </section>

      <section class="surface credentials-surface">
        <div class="surface-heading">
          <div>
            <span class="section-label">Administrator security</span>
            <h2>Change my username and password</h2>
          </div>
        </div>
        <form id="credentialsForm" class="account-form horizontal-form">
          <label
            >Current password<input
              name="currentPassword"
              type="password"
              autocomplete="current-password"
              required
          /></label>
          <label
            >New username<input
              name="newUsername"
              minlength="3"
              maxlength="30"
              pattern="[A-Za-z][A-Za-z0-9_]{2,29}"
              required
          /></label>
          <label
            >New password<input
              name="newPassword"
              type="password"
              minlength="4"
              autocomplete="new-password"
              required
          /></label>
          <label
            >Confirm new password<input
              name="confirmPassword"
              type="password"
              minlength="4"
              autocomplete="new-password"
              required
          /></label>
          <button class="button primary">Update credentials</button>
        </form>
      </section>
    </main>
    <div id="toast" role="status" aria-live="polite"></div>
    <script src="/static/notifications.js?v=reminders-4"></script>
    <script src="/static/shared.js?v=priority-3"></script>
    <script src="/static/accounts.js"></script>
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
| 6 | <code>    &lt;title&gt;Accounts &#124; PSTU Library&lt;/title&gt;</code> | title: HTML structure/content |
| 7 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/styles.css?v=members-audit-1&quot; /&gt;</code> | link: stylesheet/resource load |
| 8 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/polish.css?v=1&quot; /&gt;</code> | link: stylesheet/resource load |
| 9 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/notifications.css?v=due-2&quot; /&gt;</code> | link: stylesheet/resource load |
| 10 | <code>  &lt;/head&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 11 | <code>  &lt;body data-page=&quot;accounts&quot;&gt;</code> | body: HTML structure/content |
| 12 | <code>    &lt;div id=&quot;appHeader&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 13 | <code>    &lt;main class=&quot;workspace&quot;&gt;</code> | main: primary page content |
| 14 | <code>      &lt;section class=&quot;page-heading&quot;&gt;</code> | section: related UI content grouping |
| 15 | <code>        &lt;div&gt;</code> | div: layout/dynamic content container |
| 16 | <code>          &lt;p class=&quot;eyebrow&quot;&gt;Administration&lt;/p&gt;</code> | p: description/help text |
| 17 | <code>          &lt;h1&gt;Account management&lt;/h1&gt;</code> | h1: page heading |
| 18 | <code>          &lt;p class=&quot;heading-copy&quot;&gt;</code> | p: description/help text |
| 19 | <code>            Create librarian access and maintain administrator credentials.</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 20 | <code>          &lt;/p&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 21 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 22 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 23 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 24 | <code>      &lt;section class=&quot;account-grid&quot;&gt;</code> | section: related UI content grouping |
| 25 | <code>        &lt;article class=&quot;surface account-list-panel&quot;&gt;</code> | article: HTML structure/content |
| 26 | <code>          &lt;div class=&quot;surface-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 27 | <code>            &lt;div&gt;</code> | div: layout/dynamic content container |
| 28 | <code>              &lt;span class=&quot;section-label&quot;&gt;Authorized users&lt;/span&gt;</code> | span: HTML structure/content |
| 29 | <code>              &lt;h2&gt;Management accounts&lt;/h2&gt;</code> | h2: section/dialog heading |
| 30 | <code>            &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 31 | <code>            &lt;span class=&quot;record-count&quot; id=&quot;accountCount&quot;&gt;&lt;/span&gt;</code> | span: HTML structure/content |
| 32 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 33 | <code>          &lt;div class=&quot;table-wrap&quot; id=&quot;accountTable&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 34 | <code>        &lt;/article&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 35 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 36 | <code>        &lt;article class=&quot;surface form-surface&quot;&gt;</code> | article: HTML structure/content |
| 37 | <code>          &lt;div class=&quot;surface-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 38 | <code>            &lt;div&gt;</code> | div: layout/dynamic content container |
| 39 | <code>              &lt;span class=&quot;section-label&quot;&gt;New access&lt;/span&gt;</code> | span: HTML structure/content |
| 40 | <code>              &lt;h2&gt;Create librarian&lt;/h2&gt;</code> | h2: section/dialog heading |
| 41 | <code>            &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 42 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 43 | <code>          &lt;form id=&quot;librarianForm&quot; class=&quot;account-form&quot;&gt;</code> | form: submit-able input grouping |
| 44 | <code>            &lt;label</code> | label: field-এর readable label |
| 45 | <code>              &gt;Username&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 46 | <code>                name=&quot;username&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 47 | <code>                minlength=&quot;3&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 48 | <code>                maxlength=&quot;30&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 49 | <code>                pattern=&quot;[A-Za-z][A-Za-z0-9_]{2,29}&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 50 | <code>                placeholder=&quot;Example: librarian01&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 51 | <code>                required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 52 | <code>            /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 53 | <code>            &lt;label</code> | label: field-এর readable label |
| 54 | <code>              &gt;Password&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 55 | <code>                name=&quot;password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 56 | <code>                type=&quot;password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 57 | <code>                minlength=&quot;4&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 58 | <code>                autocomplete=&quot;new-password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 59 | <code>                required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 60 | <code>            /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 61 | <code>            &lt;label</code> | label: field-এর readable label |
| 62 | <code>              &gt;Confirm password&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 63 | <code>                name=&quot;confirmPassword&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 64 | <code>                type=&quot;password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 65 | <code>                minlength=&quot;4&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 66 | <code>                autocomplete=&quot;new-password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 67 | <code>                required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 68 | <code>            /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 69 | <code>            &lt;button class=&quot;button primary&quot;&gt;Create librarian account&lt;/button&gt;</code> | button: action/submit/cancel control |
| 70 | <code>          &lt;/form&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 71 | <code>        &lt;/article&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 72 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 73 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 74 | <code>      &lt;section class=&quot;surface credentials-surface&quot;&gt;</code> | section: related UI content grouping |
| 75 | <code>        &lt;div class=&quot;surface-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 76 | <code>          &lt;div&gt;</code> | div: layout/dynamic content container |
| 77 | <code>            &lt;span class=&quot;section-label&quot;&gt;Administrator security&lt;/span&gt;</code> | span: HTML structure/content |
| 78 | <code>            &lt;h2&gt;Change my username and password&lt;/h2&gt;</code> | h2: section/dialog heading |
| 79 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 80 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 81 | <code>        &lt;form id=&quot;credentialsForm&quot; class=&quot;account-form horizontal-form&quot;&gt;</code> | form: submit-able input grouping |
| 82 | <code>          &lt;label</code> | label: field-এর readable label |
| 83 | <code>            &gt;Current password&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 84 | <code>              name=&quot;currentPassword&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 85 | <code>              type=&quot;password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 86 | <code>              autocomplete=&quot;current-password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 87 | <code>              required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 88 | <code>          /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 89 | <code>          &lt;label</code> | label: field-এর readable label |
| 90 | <code>            &gt;New username&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 91 | <code>              name=&quot;newUsername&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 92 | <code>              minlength=&quot;3&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 93 | <code>              maxlength=&quot;30&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 94 | <code>              pattern=&quot;[A-Za-z][A-Za-z0-9_]{2,29}&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 95 | <code>              required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 96 | <code>          /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 97 | <code>          &lt;label</code> | label: field-এর readable label |
| 98 | <code>            &gt;New password&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 99 | <code>              name=&quot;newPassword&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 100 | <code>              type=&quot;password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 101 | <code>              minlength=&quot;4&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 102 | <code>              autocomplete=&quot;new-password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 103 | <code>              required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 104 | <code>          /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 105 | <code>          &lt;label</code> | label: field-এর readable label |
| 106 | <code>            &gt;Confirm new password&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 107 | <code>              name=&quot;confirmPassword&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 108 | <code>              type=&quot;password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 109 | <code>              minlength=&quot;4&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 110 | <code>              autocomplete=&quot;new-password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 111 | <code>              required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 112 | <code>          /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 113 | <code>          &lt;button class=&quot;button primary&quot;&gt;Update credentials&lt;/button&gt;</code> | button: action/submit/cancel control |
| 114 | <code>        &lt;/form&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 115 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 116 | <code>    &lt;/main&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 117 | <code>    &lt;div id=&quot;toast&quot; role=&quot;status&quot; aria-live=&quot;polite&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 118 | <code>    &lt;script src=&quot;/static/notifications.js?v=reminders-4&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 119 | <code>    &lt;script src=&quot;/static/shared.js?v=priority-3&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 120 | <code>    &lt;script src=&quot;/static/accounts.js&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 121 | <code>  &lt;/body&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 122 | <code>&lt;/html&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
