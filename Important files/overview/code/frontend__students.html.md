# frontend/students.html

এই page-এর semantic HTML structure: header placeholder, content sections, forms/dialogs এবং stylesheet/script links। Matching controller JavaScript interactions চালায়।

Source: [মূল file](../../frontend/students.html)। Snapshot 2026-10-04; 154 lines; SHA-256 `f54cb6b9ddbce94dbec972439ee7cecf6cbfce1dc3ce10be6c8d24c42bdec105`।

## Function / object / element inventory

- DOM IDs: `appHeader`, `studentSearch`, `studentCount`, `studentTable`, `studentModal`, `identityModal`, `identityMember`, `toast`
- Form keys: `roll_no`, `registration_no`, `academic_session`, `name`, `department`, `phone`, `email`, `student_id`, `roll_no`, `registration_no`, `academic_session`, `name`, `department`, `phone`, `email`, `membership_status`
- Loaded/linked resources: `/static/styles.css?v=members-audit-1`, `/static/polish.css?v=1`, `/static/notifications.css?v=due-2`, `/static/notifications.js?v=reminders-4`, `/static/shared.js?v=priority-3`, `/static/students.js?v=session-1`

## সম্পূর্ণ original source

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Members | PSTU Library</title>
    <link rel="stylesheet" href="/static/styles.css?v=members-audit-1" />
    <link rel="stylesheet" href="/static/polish.css?v=1" />
    <link rel="stylesheet" href="/static/notifications.css?v=due-2" />
  </head>
  <body data-page="students">
    <div id="appHeader"></div>
    <main class="workspace">
      <section class="page-heading">
        <div>
          <p class="eyebrow">Membership</p>
          <h1>Student directory</h1>
          <p class="heading-copy">Register members and control borrowing access.</p>
        </div>
        <button class="button primary" data-open="studentModal">Add member</button>
      </section>
      <section class="toolbar">
        <label class="search-field"
          ><span>Find member</span
          ><input
            id="studentSearch"
            type="search"
            placeholder="ID, roll, registration, name, phone or email" /></label
        ><span class="record-count" id="studentCount"></span>
      </section>
      <section class="surface"><div class="table-wrap" id="studentTable"></div></section>
    </main>
    <div class="modal" id="studentModal" aria-hidden="true">
      <form data-kind="student">
        <div class="modal-heading">
          <div>
            <span class="section-label">Membership</span>
            <h2>Add library member</h2>
          </div>
          <button type="button" class="icon-button cancel" aria-label="Close">&times;</button>
        </div>
        <p class="form-note">
          A library member ID is generated automatically. ID/Roll and Registration No. must each be
          unique.
        </p>
        <label
          >ID / Roll number<input
            name="roll_no"
            maxlength="40"
            pattern="[A-Za-z0-9][A-Za-z0-9.\/_\-]{0,39}"
            placeholder="e.g. 2201001"
            required
        /></label>
        <label
          >Registration No.<input
            name="registration_no"
            maxlength="40"
            pattern="[A-Za-z0-9][A-Za-z0-9.\/_\-]{0,39}"
            placeholder="e.g. 2022-00123"
            required
        /></label>
        <label
          >Academic session<input
            name="academic_session"
            maxlength="9"
            pattern="[0-9]{4}-([0-9]{2}|[0-9]{4})"
            title="Use 2023-24 or 2023-2024"
            placeholder="2023-24"
            required
        /></label>
        <label>Name<input name="name" required /></label
        ><label>Department<input name="department" required /></label
        ><label
          >Phone number<input
            name="phone"
            type="tel"
            inputmode="numeric"
            minlength="11"
            maxlength="11"
            pattern="[0-9]{11}"
            placeholder="01XXXXXXXXX"
            required /></label
        ><label>Email<input name="email" type="email" required /></label>
        <div class="form-actions">
          <button type="button" class="button secondary cancel">Cancel</button
          ><button class="button primary">Save member</button>
        </div>
      </form>
    </div>
    <div class="modal" id="identityModal" aria-hidden="true">
      <form>
        <div class="modal-heading">
          <div>
            <span class="section-label">Membership</span>
            <h2>Edit member</h2>
          </div>
          <button type="button" class="icon-button cancel" aria-label="Close">&times;</button>
        </div>
        <p class="form-note" id="identityMember"></p>
        <input name="student_id" type="hidden" />
        <label
          >ID / Roll number<input
            name="roll_no"
            maxlength="40"
            pattern="[A-Za-z0-9][A-Za-z0-9.\/_\-]{0,39}"
            required
        /></label>
        <label
          >Registration No.<input
            name="registration_no"
            maxlength="40"
            pattern="[A-Za-z0-9][A-Za-z0-9.\/_\-]{0,39}"
            required
        /></label>
        <label
          >Academic session<input
            name="academic_session"
            maxlength="9"
            pattern="[0-9]{4}-([0-9]{2}|[0-9]{4})"
            title="Use 2023-24 or 2023-2024"
            placeholder="2023-24"
            required
        /></label>
        <label>Name<input name="name" maxlength="100" required /></label>
        <label>Department<input name="department" maxlength="100" required /></label>
        <label
          >Phone number<input
            name="phone"
            type="tel"
            inputmode="numeric"
            minlength="11"
            maxlength="11"
            pattern="[0-9]{11}"
            required
        /></label>
        <label>Email<input name="email" type="email" maxlength="100" required /></label>
        <label
          >Membership status<select name="membership_status">
            <option value="ACTIVE">Active</option>
            <option value="DISABLED">Disabled</option>
          </select></label
        >
        <div class="form-actions">
          <button type="button" class="button secondary cancel">Cancel</button
          ><button class="button primary">Save changes</button>
        </div>
      </form>
    </div>
    <div id="toast" role="status" aria-live="polite"></div>
    <script src="/static/notifications.js?v=reminders-4"></script>
    <script src="/static/shared.js?v=priority-3"></script>
    <script src="/static/students.js?v=session-1"></script>
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
| 6 | <code>    &lt;title&gt;Members &#124; PSTU Library&lt;/title&gt;</code> | title: HTML structure/content |
| 7 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/styles.css?v=members-audit-1&quot; /&gt;</code> | link: stylesheet/resource load |
| 8 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/polish.css?v=1&quot; /&gt;</code> | link: stylesheet/resource load |
| 9 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/notifications.css?v=due-2&quot; /&gt;</code> | link: stylesheet/resource load |
| 10 | <code>  &lt;/head&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 11 | <code>  &lt;body data-page=&quot;students&quot;&gt;</code> | body: HTML structure/content |
| 12 | <code>    &lt;div id=&quot;appHeader&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 13 | <code>    &lt;main class=&quot;workspace&quot;&gt;</code> | main: primary page content |
| 14 | <code>      &lt;section class=&quot;page-heading&quot;&gt;</code> | section: related UI content grouping |
| 15 | <code>        &lt;div&gt;</code> | div: layout/dynamic content container |
| 16 | <code>          &lt;p class=&quot;eyebrow&quot;&gt;Membership&lt;/p&gt;</code> | p: description/help text |
| 17 | <code>          &lt;h1&gt;Student directory&lt;/h1&gt;</code> | h1: page heading |
| 18 | <code>          &lt;p class=&quot;heading-copy&quot;&gt;Register members and control borrowing access.&lt;/p&gt;</code> | p: description/help text |
| 19 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 20 | <code>        &lt;button class=&quot;button primary&quot; data-open=&quot;studentModal&quot;&gt;Add member&lt;/button&gt;</code> | button: action/submit/cancel control |
| 21 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 22 | <code>      &lt;section class=&quot;toolbar&quot;&gt;</code> | section: related UI content grouping |
| 23 | <code>        &lt;label class=&quot;search-field&quot;</code> | label: field-এর readable label |
| 24 | <code>          &gt;&lt;span&gt;Find member&lt;/span</code> | span: HTML structure/content |
| 25 | <code>          &gt;&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 26 | <code>            id=&quot;studentSearch&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 27 | <code>            type=&quot;search&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 28 | <code>            placeholder=&quot;ID, roll, registration, name, phone or email&quot; /&gt;&lt;/label</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 29 | <code>        &gt;&lt;span class=&quot;record-count&quot; id=&quot;studentCount&quot;&gt;&lt;/span&gt;</code> | span: HTML structure/content |
| 30 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 31 | <code>      &lt;section class=&quot;surface&quot;&gt;&lt;div class=&quot;table-wrap&quot; id=&quot;studentTable&quot;&gt;&lt;/div&gt;&lt;/section&gt;</code> | section: related UI content grouping; div: layout/dynamic content container |
| 32 | <code>    &lt;/main&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 33 | <code>    &lt;div class=&quot;modal&quot; id=&quot;studentModal&quot; aria-hidden=&quot;true&quot;&gt;</code> | div: layout/dynamic content container |
| 34 | <code>      &lt;form data-kind=&quot;student&quot;&gt;</code> | form: submit-able input grouping |
| 35 | <code>        &lt;div class=&quot;modal-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 36 | <code>          &lt;div&gt;</code> | div: layout/dynamic content container |
| 37 | <code>            &lt;span class=&quot;section-label&quot;&gt;Membership&lt;/span&gt;</code> | span: HTML structure/content |
| 38 | <code>            &lt;h2&gt;Add library member&lt;/h2&gt;</code> | h2: section/dialog heading |
| 39 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 40 | <code>          &lt;button type=&quot;button&quot; class=&quot;icon-button cancel&quot; aria-label=&quot;Close&quot;&gt;&amp;times;&lt;/button&gt;</code> | button: action/submit/cancel control |
| 41 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 42 | <code>        &lt;p class=&quot;form-note&quot;&gt;</code> | p: description/help text |
| 43 | <code>          A library member ID is generated automatically. ID/Roll and Registration No. must each be</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 44 | <code>          unique.</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 45 | <code>        &lt;/p&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 46 | <code>        &lt;label</code> | label: field-এর readable label |
| 47 | <code>          &gt;ID / Roll number&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 48 | <code>            name=&quot;roll_no&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 49 | <code>            maxlength=&quot;40&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 50 | <code>            pattern=&quot;[A-Za-z0-9][A-Za-z0-9.\/_\-]{0,39}&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 51 | <code>            placeholder=&quot;e.g. 2201001&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 52 | <code>            required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 53 | <code>        /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 54 | <code>        &lt;label</code> | label: field-এর readable label |
| 55 | <code>          &gt;Registration No.&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 56 | <code>            name=&quot;registration_no&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 57 | <code>            maxlength=&quot;40&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 58 | <code>            pattern=&quot;[A-Za-z0-9][A-Za-z0-9.\/_\-]{0,39}&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 59 | <code>            placeholder=&quot;e.g. 2022-00123&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 60 | <code>            required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 61 | <code>        /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 62 | <code>        &lt;label</code> | label: field-এর readable label |
| 63 | <code>          &gt;Academic session&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 64 | <code>            name=&quot;academic_session&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 65 | <code>            maxlength=&quot;9&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 66 | <code>            pattern=&quot;[0-9]{4}-([0-9]{2}&#124;[0-9]{4})&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 67 | <code>            title=&quot;Use 2023-24 or 2023-2024&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 68 | <code>            placeholder=&quot;2023-24&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 69 | <code>            required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 70 | <code>        /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 71 | <code>        &lt;label&gt;Name&lt;input name=&quot;name&quot; required /&gt;&lt;/label</code> | label: field-এর readable label; input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 72 | <code>        &gt;&lt;label&gt;Department&lt;input name=&quot;department&quot; required /&gt;&lt;/label</code> | label: field-এর readable label; input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 73 | <code>        &gt;&lt;label</code> | label: field-এর readable label |
| 74 | <code>          &gt;Phone number&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 75 | <code>            name=&quot;phone&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 76 | <code>            type=&quot;tel&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 77 | <code>            inputmode=&quot;numeric&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 78 | <code>            minlength=&quot;11&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 79 | <code>            maxlength=&quot;11&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 80 | <code>            pattern=&quot;[0-9]{11}&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 81 | <code>            placeholder=&quot;01XXXXXXXXX&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 82 | <code>            required /&gt;&lt;/label</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 83 | <code>        &gt;&lt;label&gt;Email&lt;input name=&quot;email&quot; type=&quot;email&quot; required /&gt;&lt;/label&gt;</code> | label: field-এর readable label; input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 84 | <code>        &lt;div class=&quot;form-actions&quot;&gt;</code> | div: layout/dynamic content container |
| 85 | <code>          &lt;button type=&quot;button&quot; class=&quot;button secondary cancel&quot;&gt;Cancel&lt;/button</code> | button: action/submit/cancel control |
| 86 | <code>          &gt;&lt;button class=&quot;button primary&quot;&gt;Save member&lt;/button&gt;</code> | button: action/submit/cancel control |
| 87 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 88 | <code>      &lt;/form&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 89 | <code>    &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 90 | <code>    &lt;div class=&quot;modal&quot; id=&quot;identityModal&quot; aria-hidden=&quot;true&quot;&gt;</code> | div: layout/dynamic content container |
| 91 | <code>      &lt;form&gt;</code> | form: submit-able input grouping |
| 92 | <code>        &lt;div class=&quot;modal-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 93 | <code>          &lt;div&gt;</code> | div: layout/dynamic content container |
| 94 | <code>            &lt;span class=&quot;section-label&quot;&gt;Membership&lt;/span&gt;</code> | span: HTML structure/content |
| 95 | <code>            &lt;h2&gt;Edit member&lt;/h2&gt;</code> | h2: section/dialog heading |
| 96 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 97 | <code>          &lt;button type=&quot;button&quot; class=&quot;icon-button cancel&quot; aria-label=&quot;Close&quot;&gt;&amp;times;&lt;/button&gt;</code> | button: action/submit/cancel control |
| 98 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 99 | <code>        &lt;p class=&quot;form-note&quot; id=&quot;identityMember&quot;&gt;&lt;/p&gt;</code> | p: description/help text |
| 100 | <code>        &lt;input name=&quot;student_id&quot; type=&quot;hidden&quot; /&gt;</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 101 | <code>        &lt;label</code> | label: field-এর readable label |
| 102 | <code>          &gt;ID / Roll number&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 103 | <code>            name=&quot;roll_no&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 104 | <code>            maxlength=&quot;40&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 105 | <code>            pattern=&quot;[A-Za-z0-9][A-Za-z0-9.\/_\-]{0,39}&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 106 | <code>            required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 107 | <code>        /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 108 | <code>        &lt;label</code> | label: field-এর readable label |
| 109 | <code>          &gt;Registration No.&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 110 | <code>            name=&quot;registration_no&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 111 | <code>            maxlength=&quot;40&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 112 | <code>            pattern=&quot;[A-Za-z0-9][A-Za-z0-9.\/_\-]{0,39}&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 113 | <code>            required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 114 | <code>        /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 115 | <code>        &lt;label</code> | label: field-এর readable label |
| 116 | <code>          &gt;Academic session&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 117 | <code>            name=&quot;academic_session&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 118 | <code>            maxlength=&quot;9&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 119 | <code>            pattern=&quot;[0-9]{4}-([0-9]{2}&#124;[0-9]{4})&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 120 | <code>            title=&quot;Use 2023-24 or 2023-2024&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 121 | <code>            placeholder=&quot;2023-24&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 122 | <code>            required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 123 | <code>        /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 124 | <code>        &lt;label&gt;Name&lt;input name=&quot;name&quot; maxlength=&quot;100&quot; required /&gt;&lt;/label&gt;</code> | label: field-এর readable label; input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 125 | <code>        &lt;label&gt;Department&lt;input name=&quot;department&quot; maxlength=&quot;100&quot; required /&gt;&lt;/label&gt;</code> | label: field-এর readable label; input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 126 | <code>        &lt;label</code> | label: field-এর readable label |
| 127 | <code>          &gt;Phone number&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 128 | <code>            name=&quot;phone&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 129 | <code>            type=&quot;tel&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 130 | <code>            inputmode=&quot;numeric&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 131 | <code>            minlength=&quot;11&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 132 | <code>            maxlength=&quot;11&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 133 | <code>            pattern=&quot;[0-9]{11}&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 134 | <code>            required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 135 | <code>        /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 136 | <code>        &lt;label&gt;Email&lt;input name=&quot;email&quot; type=&quot;email&quot; maxlength=&quot;100&quot; required /&gt;&lt;/label&gt;</code> | label: field-এর readable label; input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 137 | <code>        &lt;label</code> | label: field-এর readable label |
| 138 | <code>          &gt;Membership status&lt;select name=&quot;membership_status&quot;&gt;</code> | select: option থেকে value নির্বাচন |
| 139 | <code>            &lt;option value=&quot;ACTIVE&quot;&gt;Active&lt;/option&gt;</code> | option: select-এর choice |
| 140 | <code>            &lt;option value=&quot;DISABLED&quot;&gt;Disabled&lt;/option&gt;</code> | option: select-এর choice |
| 141 | <code>          &lt;/select&gt;&lt;/label</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 142 | <code>        &gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 143 | <code>        &lt;div class=&quot;form-actions&quot;&gt;</code> | div: layout/dynamic content container |
| 144 | <code>          &lt;button type=&quot;button&quot; class=&quot;button secondary cancel&quot;&gt;Cancel&lt;/button</code> | button: action/submit/cancel control |
| 145 | <code>          &gt;&lt;button class=&quot;button primary&quot;&gt;Save changes&lt;/button&gt;</code> | button: action/submit/cancel control |
| 146 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 147 | <code>      &lt;/form&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 148 | <code>    &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 149 | <code>    &lt;div id=&quot;toast&quot; role=&quot;status&quot; aria-live=&quot;polite&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 150 | <code>    &lt;script src=&quot;/static/notifications.js?v=reminders-4&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 151 | <code>    &lt;script src=&quot;/static/shared.js?v=priority-3&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 152 | <code>    &lt;script src=&quot;/static/students.js?v=session-1&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 153 | <code>  &lt;/body&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 154 | <code>&lt;/html&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
