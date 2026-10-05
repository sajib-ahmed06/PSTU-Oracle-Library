# frontend/login.html

এই page-এর semantic HTML structure: header placeholder, content sections, forms/dialogs এবং stylesheet/script links। Matching controller JavaScript interactions চালায়।

Source: [মূল file](../../frontend/login.html)। Snapshot 2026-10-04; 76 lines; SHA-256 `d99ea8d8d5ccce8ddb848b27de78e496a968d0aa7f2b7e58befc8d642adf3d75`।

## Function / object / element inventory

- DOM IDs: `loginForm`, `password`, `togglePassword`, `loginError`, `loginButton`
- Form keys: `username`, `password`
- Loaded/linked resources: `/static/login.css?v=activate-4`, `/activate-account`, `/forgot-password`, `/static/login.js?v=recovery-5`

## সম্পূর্ণ original source

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Sign in | PSTU Central Library</title>
    <link rel="stylesheet" href="/static/login.css?v=activate-4" />
  </head>
  <body>
    <main class="login-screen">
      <section class="login-brand">
        <div class="brand-badge">PSTU</div>
        <p>Patuakhali Science and Technology University</p>
        <h1>Central Library<br />Management System</h1>
        <span>Secure library operations portal</span>
      </section>

      <section class="login-panel">
        <form id="loginForm">
          <div class="form-heading">
            <span>Authorized access</span>
            <h2>Welcome back</h2>
            <p>Sign in to continue to the library dashboard.</p>
          </div>
          <label>
            Member ID / Staff username
            <input
              name="username"
              maxlength="100"
              autocapitalize="none"
              spellcheck="false"
              autocomplete="username"
              placeholder="PSTU-0001 or staff username"
              required
              autofocus
            />
          </label>
          <label>
            Password
            <span class="password-field">
              <input
                id="password"
                name="password"
                maxlength="128"
                type="password"
                autocomplete="current-password"
                placeholder="Enter password"
                required
              />
              <button
                id="togglePassword"
                type="button"
                aria-label="Show password"
                aria-controls="password"
                aria-pressed="false"
              >
                Show
              </button>
            </span>
          </label>
          <p id="loginError" class="login-error" role="alert"></p>
          <button id="loginButton" class="login-button" type="submit">Sign in</button>
          <p class="account-link">
            First time here? <a href="/activate-account">Activate account</a>
          </p>
          <p class="account-link">
            <a href="/forgot-password">Forgot password?</a> <span>Members only</span>
          </p>
          <div class="secure-note"><i></i><span>Protected Oracle XE session</span></div>
        </form>
      </section>
    </main>
    <footer>Developed and Copyright &copy; 2026 by <strong>SAJIB AHMED</strong></footer>
    <script src="/static/login.js?v=recovery-5"></script>
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
| 6 | <code>    &lt;title&gt;Sign in &#124; PSTU Central Library&lt;/title&gt;</code> | title: HTML structure/content |
| 7 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/login.css?v=activate-4&quot; /&gt;</code> | link: stylesheet/resource load |
| 8 | <code>  &lt;/head&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 9 | <code>  &lt;body&gt;</code> | body: HTML structure/content |
| 10 | <code>    &lt;main class=&quot;login-screen&quot;&gt;</code> | main: primary page content |
| 11 | <code>      &lt;section class=&quot;login-brand&quot;&gt;</code> | section: related UI content grouping |
| 12 | <code>        &lt;div class=&quot;brand-badge&quot;&gt;PSTU&lt;/div&gt;</code> | div: layout/dynamic content container |
| 13 | <code>        &lt;p&gt;Patuakhali Science and Technology University&lt;/p&gt;</code> | p: description/help text |
| 14 | <code>        &lt;h1&gt;Central Library&lt;br /&gt;Management System&lt;/h1&gt;</code> | h1: page heading; br: HTML structure/content |
| 15 | <code>        &lt;span&gt;Secure library operations portal&lt;/span&gt;</code> | span: HTML structure/content |
| 16 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 17 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 18 | <code>      &lt;section class=&quot;login-panel&quot;&gt;</code> | section: related UI content grouping |
| 19 | <code>        &lt;form id=&quot;loginForm&quot;&gt;</code> | form: submit-able input grouping |
| 20 | <code>          &lt;div class=&quot;form-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 21 | <code>            &lt;span&gt;Authorized access&lt;/span&gt;</code> | span: HTML structure/content |
| 22 | <code>            &lt;h2&gt;Welcome back&lt;/h2&gt;</code> | h2: section/dialog heading |
| 23 | <code>            &lt;p&gt;Sign in to continue to the library dashboard.&lt;/p&gt;</code> | p: description/help text |
| 24 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 25 | <code>          &lt;label&gt;</code> | label: field-এর readable label |
| 26 | <code>            Member ID / Staff username</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 27 | <code>            &lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 28 | <code>              name=&quot;username&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 29 | <code>              maxlength=&quot;100&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 30 | <code>              autocapitalize=&quot;none&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 31 | <code>              spellcheck=&quot;false&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 32 | <code>              autocomplete=&quot;username&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 33 | <code>              placeholder=&quot;PSTU-0001 or staff username&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 34 | <code>              required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 35 | <code>              autofocus</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 36 | <code>            /&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 37 | <code>          &lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 38 | <code>          &lt;label&gt;</code> | label: field-এর readable label |
| 39 | <code>            Password</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 40 | <code>            &lt;span class=&quot;password-field&quot;&gt;</code> | span: HTML structure/content |
| 41 | <code>              &lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 42 | <code>                id=&quot;password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 43 | <code>                name=&quot;password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 44 | <code>                maxlength=&quot;128&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 45 | <code>                type=&quot;password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 46 | <code>                autocomplete=&quot;current-password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 47 | <code>                placeholder=&quot;Enter password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 48 | <code>                required</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 49 | <code>              /&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 50 | <code>              &lt;button</code> | button: action/submit/cancel control |
| 51 | <code>                id=&quot;togglePassword&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 52 | <code>                type=&quot;button&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 53 | <code>                aria-label=&quot;Show password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 54 | <code>                aria-controls=&quot;password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 55 | <code>                aria-pressed=&quot;false&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 56 | <code>              &gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 57 | <code>                Show</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 58 | <code>              &lt;/button&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 59 | <code>            &lt;/span&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 60 | <code>          &lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 61 | <code>          &lt;p id=&quot;loginError&quot; class=&quot;login-error&quot; role=&quot;alert&quot;&gt;&lt;/p&gt;</code> | p: description/help text |
| 62 | <code>          &lt;button id=&quot;loginButton&quot; class=&quot;login-button&quot; type=&quot;submit&quot;&gt;Sign in&lt;/button&gt;</code> | button: action/submit/cancel control |
| 63 | <code>          &lt;p class=&quot;account-link&quot;&gt;</code> | p: description/help text |
| 64 | <code>            First time here? &lt;a href=&quot;/activate-account&quot;&gt;Activate account&lt;/a&gt;</code> | a: HTML structure/content |
| 65 | <code>          &lt;/p&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 66 | <code>          &lt;p class=&quot;account-link&quot;&gt;</code> | p: description/help text |
| 67 | <code>            &lt;a href=&quot;/forgot-password&quot;&gt;Forgot password?&lt;/a&gt; &lt;span&gt;Members only&lt;/span&gt;</code> | a: HTML structure/content; span: HTML structure/content |
| 68 | <code>          &lt;/p&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 69 | <code>          &lt;div class=&quot;secure-note&quot;&gt;&lt;i&gt;&lt;/i&gt;&lt;span&gt;Protected Oracle XE session&lt;/span&gt;&lt;/div&gt;</code> | div: layout/dynamic content container; i: HTML structure/content; span: HTML structure/content |
| 70 | <code>        &lt;/form&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 71 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 72 | <code>    &lt;/main&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 73 | <code>    &lt;footer&gt;Developed and Copyright &amp;copy; 2026 by &lt;strong&gt;SAJIB AHMED&lt;/strong&gt;&lt;/footer&gt;</code> | footer: developer credit/footer; strong: HTML structure/content |
| 74 | <code>    &lt;script src=&quot;/static/login.js?v=recovery-5&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 75 | <code>  &lt;/body&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 76 | <code>&lt;/html&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
