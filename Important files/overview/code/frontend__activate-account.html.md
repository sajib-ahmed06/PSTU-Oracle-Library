# frontend/activate-account.html

এই page-এর semantic HTML structure: header placeholder, content sections, forms/dialogs এবং stylesheet/script links। Matching controller JavaScript interactions চালায়।

Source: [মূল file](../../frontend/activate-account.html)। Snapshot 2026-10-04; 72 lines; SHA-256 `8efa89ea60c41d294926ab64448dfc955740726158d5321518dc14dbae8ce619`।

## Function / object / element inventory

- DOM IDs: `activationForm`, `activationMessage`, `activationButton`
- Form keys: `memberId`, `phone`, `password`, `confirmPassword`
- Loaded/linked resources: `/static/login.css?v=activate-4`, `/login`, `/static/activate-account.js?v=1`

## সম্পূর্ণ original source

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>Activate account | PSTU Library</title>
    <link rel="stylesheet" href="/static/login.css?v=activate-4" />
  </head>
  <body>
    <main class="login-screen">
      <section class="login-brand">
        <div class="brand-badge">PSTU</div>
        <p>Patuakhali Science and Technology University</p>
        <h1>Central Library<br />Student Portal</h1>
        <span>Activate your library account</span>
      </section>
      <section class="login-panel">
        <form id="activationForm">
          <div class="form-heading">
            <span>Student access</span>
            <h2>Activate account</h2>
            <p>Use your library Member ID and registered phone number to set your password.</p>
          </div>
          <label
            >Member ID<input
              name="memberId"
              maxlength="25"
              placeholder="Example: PSTU-0001"
              autocomplete="username"
              required
              autofocus
          /></label>
          <label
            >Registered phone number<input
              name="phone"
              type="tel"
              inputmode="numeric"
              pattern="[0-9]{11}"
              minlength="11"
              maxlength="11"
              placeholder="11-digit registered phone number"
              autocomplete="tel"
              required
          /></label>
          <label
            >Set password<input
              name="password"
              type="password"
              minlength="4"
              maxlength="128"
              autocomplete="new-password"
              required
          /></label>
          <label
            >Confirm password<input
              name="confirmPassword"
              type="password"
              minlength="4"
              maxlength="128"
              autocomplete="new-password"
              required
          /></label>
          <p id="activationMessage" class="login-error" role="status" aria-live="polite"></p>
          <button id="activationButton" class="login-button">Activate account</button>
          <p class="account-link">Already activated? <a href="/login">Sign in</a></p>
        </form>
      </section>
    </main>
    <footer>Developed and Copyright &copy; 2026 by <strong>SAJIB AHMED</strong></footer>
    <script src="/static/activate-account.js?v=1"></script>
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
| 6 | <code>    &lt;title&gt;Activate account &#124; PSTU Library&lt;/title&gt;</code> | title: HTML structure/content |
| 7 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/login.css?v=activate-4&quot; /&gt;</code> | link: stylesheet/resource load |
| 8 | <code>  &lt;/head&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 9 | <code>  &lt;body&gt;</code> | body: HTML structure/content |
| 10 | <code>    &lt;main class=&quot;login-screen&quot;&gt;</code> | main: primary page content |
| 11 | <code>      &lt;section class=&quot;login-brand&quot;&gt;</code> | section: related UI content grouping |
| 12 | <code>        &lt;div class=&quot;brand-badge&quot;&gt;PSTU&lt;/div&gt;</code> | div: layout/dynamic content container |
| 13 | <code>        &lt;p&gt;Patuakhali Science and Technology University&lt;/p&gt;</code> | p: description/help text |
| 14 | <code>        &lt;h1&gt;Central Library&lt;br /&gt;Student Portal&lt;/h1&gt;</code> | h1: page heading; br: HTML structure/content |
| 15 | <code>        &lt;span&gt;Activate your library account&lt;/span&gt;</code> | span: HTML structure/content |
| 16 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 17 | <code>      &lt;section class=&quot;login-panel&quot;&gt;</code> | section: related UI content grouping |
| 18 | <code>        &lt;form id=&quot;activationForm&quot;&gt;</code> | form: submit-able input grouping |
| 19 | <code>          &lt;div class=&quot;form-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 20 | <code>            &lt;span&gt;Student access&lt;/span&gt;</code> | span: HTML structure/content |
| 21 | <code>            &lt;h2&gt;Activate account&lt;/h2&gt;</code> | h2: section/dialog heading |
| 22 | <code>            &lt;p&gt;Use your library Member ID and registered phone number to set your password.&lt;/p&gt;</code> | p: description/help text |
| 23 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 24 | <code>          &lt;label</code> | label: field-এর readable label |
| 25 | <code>            &gt;Member ID&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 26 | <code>              name=&quot;memberId&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 27 | <code>              maxlength=&quot;25&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 28 | <code>              placeholder=&quot;Example: PSTU-0001&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 29 | <code>              autocomplete=&quot;username&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 30 | <code>              required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 31 | <code>              autofocus</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 32 | <code>          /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 33 | <code>          &lt;label</code> | label: field-এর readable label |
| 34 | <code>            &gt;Registered phone number&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 35 | <code>              name=&quot;phone&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 36 | <code>              type=&quot;tel&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 37 | <code>              inputmode=&quot;numeric&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 38 | <code>              pattern=&quot;[0-9]{11}&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 39 | <code>              minlength=&quot;11&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 40 | <code>              maxlength=&quot;11&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 41 | <code>              placeholder=&quot;11-digit registered phone number&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 42 | <code>              autocomplete=&quot;tel&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 43 | <code>              required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 44 | <code>          /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 45 | <code>          &lt;label</code> | label: field-এর readable label |
| 46 | <code>            &gt;Set password&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 47 | <code>              name=&quot;password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 48 | <code>              type=&quot;password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 49 | <code>              minlength=&quot;4&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 50 | <code>              maxlength=&quot;128&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 51 | <code>              autocomplete=&quot;new-password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 52 | <code>              required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 53 | <code>          /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 54 | <code>          &lt;label</code> | label: field-এর readable label |
| 55 | <code>            &gt;Confirm password&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 56 | <code>              name=&quot;confirmPassword&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 57 | <code>              type=&quot;password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 58 | <code>              minlength=&quot;4&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 59 | <code>              maxlength=&quot;128&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 60 | <code>              autocomplete=&quot;new-password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 61 | <code>              required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 62 | <code>          /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 63 | <code>          &lt;p id=&quot;activationMessage&quot; class=&quot;login-error&quot; role=&quot;status&quot; aria-live=&quot;polite&quot;&gt;&lt;/p&gt;</code> | p: description/help text |
| 64 | <code>          &lt;button id=&quot;activationButton&quot; class=&quot;login-button&quot;&gt;Activate account&lt;/button&gt;</code> | button: action/submit/cancel control |
| 65 | <code>          &lt;p class=&quot;account-link&quot;&gt;Already activated? &lt;a href=&quot;/login&quot;&gt;Sign in&lt;/a&gt;&lt;/p&gt;</code> | p: description/help text; a: HTML structure/content |
| 66 | <code>        &lt;/form&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 67 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 68 | <code>    &lt;/main&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 69 | <code>    &lt;footer&gt;Developed and Copyright &amp;copy; 2026 by &lt;strong&gt;SAJIB AHMED&lt;/strong&gt;&lt;/footer&gt;</code> | footer: developer credit/footer; strong: HTML structure/content |
| 70 | <code>    &lt;script src=&quot;/static/activate-account.js?v=1&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 71 | <code>  &lt;/body&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 72 | <code>&lt;/html&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
