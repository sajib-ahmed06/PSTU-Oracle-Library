# frontend/forgot-password.html

এই page-এর semantic HTML structure: header placeholder, content sections, forms/dialogs এবং stylesheet/script links। Matching controller JavaScript interactions চালায়।

Source: [মূল file](../../frontend/forgot-password.html)। Snapshot 2026-10-04; 84 lines; SHA-256 `685c35823552f64b670396bf511891ed6d831b740a6cc03785ba66f1ad2d6dd2`।

## Function / object / element inventory

- DOM IDs: `recoveryForm`, `recoveryMessage`, `recoveryButton`
- Form keys: `memberId`, `rollNo`, `registrationNo`, `phone`, `email`, `password`, `confirmPassword`
- Loaded/linked resources: `/static/login.css?v=recovery-5`, `/login`, `/static/forgot-password.js?v=1`

## সম্পূর্ণ original source

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>Forgot password | PSTU Library</title>
    <link rel="stylesheet" href="/static/login.css?v=recovery-5" />
  </head>
  <body>
    <main class="login-screen">
      <section class="login-brand">
        <div class="brand-badge">PSTU</div>
        <p>Patuakhali Science and Technology University</p>
        <h1>Central Library<br />Student Portal</h1>
        <span>Member password recovery</span>
      </section>
      <section class="login-panel">
        <form id="recoveryForm">
          <div class="form-heading">
            <span>Members only</span>
            <h2>Forgot password?</h2>
            <p>
              All details must match your library membership record. Staff accounts cannot use this
              form.
            </p>
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
          <label>ID / Roll number<input name="rollNo" maxlength="40" required /></label>
          <label>Registration No.<input name="registrationNo" maxlength="40" required /></label>
          <label
            >Registered phone number<input
              name="phone"
              type="tel"
              inputmode="numeric"
              pattern="[0-9]{11}"
              minlength="11"
              maxlength="11"
              autocomplete="tel"
              required
          /></label>
          <label
            >Registered email<input
              name="email"
              type="email"
              maxlength="100"
              autocomplete="email"
              required
          /></label>
          <label
            >New password<input
              name="password"
              type="password"
              minlength="4"
              maxlength="128"
              autocomplete="new-password"
              required
          /></label>
          <label
            >Confirm new password<input
              name="confirmPassword"
              type="password"
              minlength="4"
              maxlength="128"
              autocomplete="new-password"
              required
          /></label>
          <p id="recoveryMessage" class="login-error" role="status" aria-live="polite"></p>
          <button id="recoveryButton" class="login-button">Change password</button>
          <p class="account-link"><a href="/login">Back to sign in</a></p>
        </form>
      </section>
    </main>
    <footer>Developed and Copyright &copy; 2026 by <strong>SAJIB AHMED</strong></footer>
    <script src="/static/forgot-password.js?v=1"></script>
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
| 6 | <code>    &lt;title&gt;Forgot password &#124; PSTU Library&lt;/title&gt;</code> | title: HTML structure/content |
| 7 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/login.css?v=recovery-5&quot; /&gt;</code> | link: stylesheet/resource load |
| 8 | <code>  &lt;/head&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 9 | <code>  &lt;body&gt;</code> | body: HTML structure/content |
| 10 | <code>    &lt;main class=&quot;login-screen&quot;&gt;</code> | main: primary page content |
| 11 | <code>      &lt;section class=&quot;login-brand&quot;&gt;</code> | section: related UI content grouping |
| 12 | <code>        &lt;div class=&quot;brand-badge&quot;&gt;PSTU&lt;/div&gt;</code> | div: layout/dynamic content container |
| 13 | <code>        &lt;p&gt;Patuakhali Science and Technology University&lt;/p&gt;</code> | p: description/help text |
| 14 | <code>        &lt;h1&gt;Central Library&lt;br /&gt;Student Portal&lt;/h1&gt;</code> | h1: page heading; br: HTML structure/content |
| 15 | <code>        &lt;span&gt;Member password recovery&lt;/span&gt;</code> | span: HTML structure/content |
| 16 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 17 | <code>      &lt;section class=&quot;login-panel&quot;&gt;</code> | section: related UI content grouping |
| 18 | <code>        &lt;form id=&quot;recoveryForm&quot;&gt;</code> | form: submit-able input grouping |
| 19 | <code>          &lt;div class=&quot;form-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 20 | <code>            &lt;span&gt;Members only&lt;/span&gt;</code> | span: HTML structure/content |
| 21 | <code>            &lt;h2&gt;Forgot password?&lt;/h2&gt;</code> | h2: section/dialog heading |
| 22 | <code>            &lt;p&gt;</code> | p: description/help text |
| 23 | <code>              All details must match your library membership record. Staff accounts cannot use this</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 24 | <code>              form.</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 25 | <code>            &lt;/p&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 26 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 27 | <code>          &lt;label</code> | label: field-এর readable label |
| 28 | <code>            &gt;Member ID&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 29 | <code>              name=&quot;memberId&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 30 | <code>              maxlength=&quot;25&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 31 | <code>              placeholder=&quot;Example: PSTU-0001&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 32 | <code>              autocomplete=&quot;username&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 33 | <code>              required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 34 | <code>              autofocus</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 35 | <code>          /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 36 | <code>          &lt;label&gt;ID / Roll number&lt;input name=&quot;rollNo&quot; maxlength=&quot;40&quot; required /&gt;&lt;/label&gt;</code> | label: field-এর readable label; input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 37 | <code>          &lt;label&gt;Registration No.&lt;input name=&quot;registrationNo&quot; maxlength=&quot;40&quot; required /&gt;&lt;/label&gt;</code> | label: field-এর readable label; input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 38 | <code>          &lt;label</code> | label: field-এর readable label |
| 39 | <code>            &gt;Registered phone number&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 40 | <code>              name=&quot;phone&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 41 | <code>              type=&quot;tel&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 42 | <code>              inputmode=&quot;numeric&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 43 | <code>              pattern=&quot;[0-9]{11}&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 44 | <code>              minlength=&quot;11&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 45 | <code>              maxlength=&quot;11&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 46 | <code>              autocomplete=&quot;tel&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 47 | <code>              required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 48 | <code>          /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 49 | <code>          &lt;label</code> | label: field-এর readable label |
| 50 | <code>            &gt;Registered email&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 51 | <code>              name=&quot;email&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 52 | <code>              type=&quot;email&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 53 | <code>              maxlength=&quot;100&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 54 | <code>              autocomplete=&quot;email&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 55 | <code>              required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 56 | <code>          /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 57 | <code>          &lt;label</code> | label: field-এর readable label |
| 58 | <code>            &gt;New password&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 59 | <code>              name=&quot;password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 60 | <code>              type=&quot;password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 61 | <code>              minlength=&quot;4&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 62 | <code>              maxlength=&quot;128&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 63 | <code>              autocomplete=&quot;new-password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 64 | <code>              required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 65 | <code>          /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 66 | <code>          &lt;label</code> | label: field-এর readable label |
| 67 | <code>            &gt;Confirm new password&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 68 | <code>              name=&quot;confirmPassword&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 69 | <code>              type=&quot;password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 70 | <code>              minlength=&quot;4&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 71 | <code>              maxlength=&quot;128&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 72 | <code>              autocomplete=&quot;new-password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 73 | <code>              required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 74 | <code>          /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 75 | <code>          &lt;p id=&quot;recoveryMessage&quot; class=&quot;login-error&quot; role=&quot;status&quot; aria-live=&quot;polite&quot;&gt;&lt;/p&gt;</code> | p: description/help text |
| 76 | <code>          &lt;button id=&quot;recoveryButton&quot; class=&quot;login-button&quot;&gt;Change password&lt;/button&gt;</code> | button: action/submit/cancel control |
| 77 | <code>          &lt;p class=&quot;account-link&quot;&gt;&lt;a href=&quot;/login&quot;&gt;Back to sign in&lt;/a&gt;&lt;/p&gt;</code> | p: description/help text; a: HTML structure/content |
| 78 | <code>        &lt;/form&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 79 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 80 | <code>    &lt;/main&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 81 | <code>    &lt;footer&gt;Developed and Copyright &amp;copy; 2026 by &lt;strong&gt;SAJIB AHMED&lt;/strong&gt;&lt;/footer&gt;</code> | footer: developer credit/footer; strong: HTML structure/content |
| 82 | <code>    &lt;script src=&quot;/static/forgot-password.js?v=1&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 83 | <code>  &lt;/body&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 84 | <code>&lt;/html&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
