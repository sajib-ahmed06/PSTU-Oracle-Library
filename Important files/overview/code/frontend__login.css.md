# frontend/login.css

Photo background, translucent glass login card, autofill readability, focus indication ও responsive sign-in layout।

Source: [মূল file](../../frontend/login.css)। Snapshot 2026-10-04; 314 lines; SHA-256 `4e51afcdd4953a2e0d01da45e8298cc3f0a5b114d27c239a816a1cc291f21bb1`।

## Function / object / element inventory

CSS selector/property rules source order-এ cascade করে। Later matching declaration আগের equivalent specificity rule override করতে পারে। Media/supports queries condition অনুযায়ী override দেয়। নিচের প্রতিটি line selector/property reading notes দেয়।

## সম্পূর্ণ original source

```css
/* A translucent sign-in card keeps the campus photograph visible. */
:root {
  --green: #0b4a37;
  --ink: #fff;
  --muted: #e1ebe7;
  --line: rgba(255, 255, 255, 0.42);
}

* {
  box-sizing: border-box;
}
body {
  min-width: 320px;
  min-height: 100vh;
  min-height: 100svh;
  margin: 0;
  display: flex;
  flex-direction: column;
  background-color: #123c30;
  background-image:
    linear-gradient(90deg, rgba(4, 24, 19, 0.64), rgba(4, 24, 19, 0.12)),
    url("/static/assets/pstu-library.jpg"), url("/static/assets/library-dashboard.png");
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
  background-attachment: fixed;
  color: var(--ink);
  font-family: "Segoe UI", Arial, sans-serif;
}
button,
input {
  font: inherit;
}
.login-screen {
  flex: 1;
  width: min(1400px, 100%);
  margin: auto;
  padding: clamp(28px, 5vw, 80px);
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(360px, 0.8fr);
  align-items: center;
  gap: clamp(32px, 6vw, 100px);
}
.login-brand {
  padding: 20px 0;
  text-shadow: 0 2px 18px rgba(0, 0, 0, 0.45);
}
.brand-badge {
  width: 82px;
  height: 54px;
  display: grid;
  place-items: center;
  margin-bottom: 28px;
  border: 1px solid var(--line);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.14);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  font-size: 15px;
  font-weight: 800;
  letter-spacing: 2px;
}
.login-brand p {
  max-width: 500px;
  margin: 0 0 18px;
  font-size: 12px;
  font-weight: 600;
  line-height: 1.7;
  letter-spacing: 1.4px;
  text-transform: uppercase;
}
.login-brand h1 {
  margin: 0;
  font-size: clamp(36px, 4.4vw, 64px);
  line-height: 1.12;
  letter-spacing: -1.5px;
}
.login-brand > span {
  display: block;
  margin-top: 24px;
  color: var(--muted);
  font-size: 14px;
}
.login-panel {
  padding: clamp(28px, 3vw, 44px);
  border: 1px solid var(--line);
  border-radius: 26px;
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.24), rgba(255, 255, 255, 0.09)),
    rgba(8, 36, 28, 0.42);
  box-shadow:
    0 24px 64px rgba(0, 0, 0, 0.28),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(18px) saturate(125%);
  -webkit-backdrop-filter: blur(18px) saturate(125%);
}
.login-panel form {
  width: 100%;
}
.form-heading {
  margin-bottom: 28px;
}
.form-heading > span {
  color: #c6f7de;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1.6px;
  text-transform: uppercase;
}
.form-heading h2 {
  margin: 10px 0;
  font-size: 32px;
  letter-spacing: -0.7px;
}
.form-heading p {
  margin: 0;
  color: var(--muted);
  font-size: 13px;
  line-height: 1.6;
}
label {
  display: block;
  margin: 20px 0;
  font-size: 13px;
  font-weight: 600;
}
input {
  width: 100%;
  min-height: 50px;
  margin-top: 9px;
  padding: 12px 14px;
  border: 1px solid var(--line);
  border-radius: 11px;
  background: rgba(255, 255, 255, 0.14);
  color: #fff;
  outline: none;
}
input::placeholder {
  color: #d5e1db;
  font-size: 12px;
  opacity: 1;
}
input:focus {
  border-color: #b5f4d2;
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 0 0 0 3px rgba(181, 244, 210, 0.18);
}
.password-field {
  position: relative;
  display: block;
}
.password-field input {
  padding-right: 66px;
}
.password-field button {
  position: absolute;
  right: 9px;
  bottom: 9px;
  min-height: 32px;
  padding: 5px 8px;
  border: 0;
  border-radius: 6px;
  background: #0b4a37;
  color: #fff;
  cursor: pointer;
  font-size: 11px;
  font-weight: 700;
}
.login-error {
  min-height: 20px;
  margin: 4px 0 10px;
  color: #ffe0d8;
  font-size: 12px;
  line-height: 1.5;
}
.login-button {
  width: 100%;
  min-height: 50px;
  border: 1px solid rgba(255, 255, 255, 0.22);
  border-radius: 11px;
  background: #0b4a37;
  color: #fff;
  cursor: pointer;
  font-weight: 700;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
}
.login-button:hover {
  background: #083e2e;
}
.login-button:disabled {
  cursor: wait;
  opacity: 0.65;
}
button:focus-visible {
  outline: 3px solid #b5f4d2;
  outline-offset: 3px;
}
.secure-note {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  margin-top: 24px;
  color: var(--muted);
  font-size: 11px;
}
.secure-note i {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #9bf0bc;
  box-shadow: 0 0 0 4px rgba(155, 240, 188, 0.12);
}
.account-link {
  color: var(--muted);
  text-align: center;
  font-size: 13px;
  margin: 18px 0 0;
}
.account-link a {
  color: #c6f7de;
  font-weight: 700;
  text-underline-offset: 4px;
}
.account-link a:focus-visible {
  outline: 3px solid #b5f4d2;
  outline-offset: 4px;
}
footer {
  min-height: 54px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 5px;
  padding: 16px;
  background: rgba(4, 24, 19, 0.4);
  color: #e1ebe7;
  font-size: 10px;
  text-align: center;
}
footer strong {
  color: #c6f7de;
  letter-spacing: 0.8px;
}

@media (max-width: 850px) {
  body {
    background-attachment: scroll;
  }
  .login-screen {
    max-width: 560px;
    grid-template-columns: 1fr;
    gap: 24px;
    padding: 32px 24px;
  }
  .login-brand {
    padding: 0;
  }
  .brand-badge {
    margin-bottom: 18px;
  }
  .login-brand h1 {
    font-size: 38px;
  }
  .login-brand > span {
    margin-top: 16px;
  }
}
@media (max-width: 430px) {
  .login-screen {
    padding: 24px 18px;
  }
  .login-brand h1 {
    font-size: 32px;
  }
  .login-brand p {
    font-size: 10px;
  }
  .login-panel {
    padding: 26px 22px;
    border-radius: 20px;
  }
}
@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .login-panel {
    background: rgba(8, 36, 28, 0.88);
  }
}

/* Saved credentials must stay legible against the glass surface. */
input:autofill {
  color: #fff;
  background: #29493e;
}
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus {
  -webkit-text-fill-color: #fff;
  caret-color: #fff;
  -webkit-box-shadow: 0 0 0 1000px #29493e inset;
}
@media (max-height: 650px) and (min-width: 851px) {
  .login-screen {
    padding-top: 24px;
    padding-bottom: 24px;
  }
  .login-panel {
    padding: 26px 32px;
  }
  .form-heading {
    margin-bottom: 18px;
  }
}
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>/* A translucent sign-in card keeps the campus photograph visible. */</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 2 | <code>:root {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 3 | <code>  --green: #0b4a37;</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 4 | <code>  --ink: #fff;</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 5 | <code>  --muted: #e1ebe7;</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 6 | <code>  --line: rgba(255, 255, 255, 0.42);</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 7 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 8 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 9 | <code>* {</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 10 | <code>  box-sizing: border-box;</code> | CSS properties: box-sizing; enclosing selector-এর presentation নির্ধারণ করে। |
| 11 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 12 | <code>body {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 13 | <code>  min-width: 320px;</code> | CSS properties: min-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 14 | <code>  min-height: 100vh;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 15 | <code>  min-height: 100svh;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 16 | <code>  margin: 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 17 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 18 | <code>  flex-direction: column;</code> | CSS properties: flex-direction; enclosing selector-এর presentation নির্ধারণ করে। |
| 19 | <code>  background-color: #123c30;</code> | CSS properties: background-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 20 | <code>  background-image:</code> | CSS properties: background-image; enclosing selector-এর presentation নির্ধারণ করে। |
| 21 | <code>    linear-gradient(90deg, rgba(4, 24, 19, 0.64), rgba(4, 24, 19, 0.12)),</code> | Style rule/block-এর closing বা continuation। |
| 22 | <code>    url(&quot;/static/assets/pstu-library.jpg&quot;), url(&quot;/static/assets/library-dashboard.png&quot;);</code> | Style rule/block-এর closing বা continuation। |
| 23 | <code>  background-position: center;</code> | CSS properties: background-position; enclosing selector-এর presentation নির্ধারণ করে। |
| 24 | <code>  background-size: cover;</code> | CSS properties: background-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 25 | <code>  background-repeat: no-repeat;</code> | CSS properties: background-repeat; enclosing selector-এর presentation নির্ধারণ করে। |
| 26 | <code>  background-attachment: fixed;</code> | CSS properties: background-attachment; enclosing selector-এর presentation নির্ধারণ করে। |
| 27 | <code>  color: var(--ink);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 28 | <code>  font-family: &quot;Segoe UI&quot;, Arial, sans-serif;</code> | CSS properties: font-family; enclosing selector-এর presentation নির্ধারণ করে। |
| 29 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 30 | <code>button,</code> | Style rule/block-এর closing বা continuation। |
| 31 | <code>input {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 32 | <code>  font: inherit;</code> | CSS properties: font; enclosing selector-এর presentation নির্ধারণ করে। |
| 33 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 34 | <code>.login-screen {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 35 | <code>  flex: 1;</code> | CSS properties: flex; enclosing selector-এর presentation নির্ধারণ করে। |
| 36 | <code>  width: min(1400px, 100%);</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 37 | <code>  margin: auto;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 38 | <code>  padding: clamp(28px, 5vw, 80px);</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 39 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 40 | <code>  grid-template-columns: minmax(0, 1.2fr) minmax(360px, 0.8fr);</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 41 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 42 | <code>  gap: clamp(32px, 6vw, 100px);</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 43 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 44 | <code>.login-brand {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 45 | <code>  padding: 20px 0;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 46 | <code>  text-shadow: 0 2px 18px rgba(0, 0, 0, 0.45);</code> | CSS properties: text-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 47 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 48 | <code>.brand-badge {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 49 | <code>  width: 82px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 50 | <code>  height: 54px;</code> | CSS properties: height; enclosing selector-এর presentation নির্ধারণ করে। |
| 51 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 52 | <code>  place-items: center;</code> | CSS properties: place-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 53 | <code>  margin-bottom: 28px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 54 | <code>  border: 1px solid var(--line);</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 55 | <code>  border-radius: 14px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 56 | <code>  background: rgba(255, 255, 255, 0.14);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 57 | <code>  backdrop-filter: blur(12px);</code> | CSS properties: backdrop-filter; enclosing selector-এর presentation নির্ধারণ করে। |
| 58 | <code>  -webkit-backdrop-filter: blur(12px);</code> | CSS properties: -webkit-backdrop-filter; enclosing selector-এর presentation নির্ধারণ করে। |
| 59 | <code>  font-size: 15px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 60 | <code>  font-weight: 800;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 61 | <code>  letter-spacing: 2px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 62 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 63 | <code>.login-brand p {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 64 | <code>  max-width: 500px;</code> | CSS properties: max-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 65 | <code>  margin: 0 0 18px;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 66 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 67 | <code>  font-weight: 600;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 68 | <code>  line-height: 1.7;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 69 | <code>  letter-spacing: 1.4px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 70 | <code>  text-transform: uppercase;</code> | CSS properties: text-transform; enclosing selector-এর presentation নির্ধারণ করে। |
| 71 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 72 | <code>.login-brand h1 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 73 | <code>  margin: 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 74 | <code>  font-size: clamp(36px, 4.4vw, 64px);</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 75 | <code>  line-height: 1.12;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 76 | <code>  letter-spacing: -1.5px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 77 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 78 | <code>.login-brand &gt; span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 79 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 80 | <code>  margin-top: 24px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 81 | <code>  color: var(--muted);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 82 | <code>  font-size: 14px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 83 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 84 | <code>.login-panel {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 85 | <code>  padding: clamp(28px, 3vw, 44px);</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 86 | <code>  border: 1px solid var(--line);</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 87 | <code>  border-radius: 26px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 88 | <code>  background:</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 89 | <code>    linear-gradient(135deg, rgba(255, 255, 255, 0.24), rgba(255, 255, 255, 0.09)),</code> | Style rule/block-এর closing বা continuation। |
| 90 | <code>    rgba(8, 36, 28, 0.42);</code> | Style rule/block-এর closing বা continuation। |
| 91 | <code>  box-shadow:</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 92 | <code>    0 24px 64px rgba(0, 0, 0, 0.28),</code> | Style rule/block-এর closing বা continuation। |
| 93 | <code>    inset 0 1px 0 rgba(255, 255, 255, 0.3);</code> | Style rule/block-এর closing বা continuation। |
| 94 | <code>  backdrop-filter: blur(18px) saturate(125%);</code> | CSS properties: backdrop-filter; enclosing selector-এর presentation নির্ধারণ করে। |
| 95 | <code>  -webkit-backdrop-filter: blur(18px) saturate(125%);</code> | CSS properties: -webkit-backdrop-filter; enclosing selector-এর presentation নির্ধারণ করে। |
| 96 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 97 | <code>.login-panel form {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 98 | <code>  width: 100%;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 99 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 100 | <code>.form-heading {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 101 | <code>  margin-bottom: 28px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 102 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 103 | <code>.form-heading &gt; span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 104 | <code>  color: #c6f7de;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 105 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 106 | <code>  font-weight: 700;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 107 | <code>  letter-spacing: 1.6px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 108 | <code>  text-transform: uppercase;</code> | CSS properties: text-transform; enclosing selector-এর presentation নির্ধারণ করে। |
| 109 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 110 | <code>.form-heading h2 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 111 | <code>  margin: 10px 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 112 | <code>  font-size: 32px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 113 | <code>  letter-spacing: -0.7px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 114 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 115 | <code>.form-heading p {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 116 | <code>  margin: 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 117 | <code>  color: var(--muted);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 118 | <code>  font-size: 13px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 119 | <code>  line-height: 1.6;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 120 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 121 | <code>label {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 122 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 123 | <code>  margin: 20px 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 124 | <code>  font-size: 13px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 125 | <code>  font-weight: 600;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 126 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 127 | <code>input {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 128 | <code>  width: 100%;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 129 | <code>  min-height: 50px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 130 | <code>  margin-top: 9px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 131 | <code>  padding: 12px 14px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 132 | <code>  border: 1px solid var(--line);</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 133 | <code>  border-radius: 11px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 134 | <code>  background: rgba(255, 255, 255, 0.14);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 135 | <code>  color: #fff;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 136 | <code>  outline: none;</code> | CSS properties: outline; enclosing selector-এর presentation নির্ধারণ করে। |
| 137 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 138 | <code>input::placeholder {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 139 | <code>  color: #d5e1db;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 140 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 141 | <code>  opacity: 1;</code> | CSS properties: opacity; enclosing selector-এর presentation নির্ধারণ করে। |
| 142 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 143 | <code>input:focus {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 144 | <code>  border-color: #b5f4d2;</code> | CSS properties: border-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 145 | <code>  background: rgba(255, 255, 255, 0.2);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 146 | <code>  box-shadow: 0 0 0 3px rgba(181, 244, 210, 0.18);</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 147 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 148 | <code>.password-field {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 149 | <code>  position: relative;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 150 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 151 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 152 | <code>.password-field input {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 153 | <code>  padding-right: 66px;</code> | CSS properties: padding-right; enclosing selector-এর presentation নির্ধারণ করে। |
| 154 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 155 | <code>.password-field button {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 156 | <code>  position: absolute;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 157 | <code>  right: 9px;</code> | CSS properties: right; enclosing selector-এর presentation নির্ধারণ করে। |
| 158 | <code>  bottom: 9px;</code> | CSS properties: bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 159 | <code>  min-height: 32px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 160 | <code>  padding: 5px 8px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 161 | <code>  border: 0;</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 162 | <code>  border-radius: 6px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 163 | <code>  background: #0b4a37;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 164 | <code>  color: #fff;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 165 | <code>  cursor: pointer;</code> | CSS properties: cursor; enclosing selector-এর presentation নির্ধারণ করে। |
| 166 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 167 | <code>  font-weight: 700;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 168 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 169 | <code>.login-error {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 170 | <code>  min-height: 20px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 171 | <code>  margin: 4px 0 10px;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 172 | <code>  color: #ffe0d8;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 173 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 174 | <code>  line-height: 1.5;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 175 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 176 | <code>.login-button {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 177 | <code>  width: 100%;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 178 | <code>  min-height: 50px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 179 | <code>  border: 1px solid rgba(255, 255, 255, 0.22);</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 180 | <code>  border-radius: 11px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 181 | <code>  background: #0b4a37;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 182 | <code>  color: #fff;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 183 | <code>  cursor: pointer;</code> | CSS properties: cursor; enclosing selector-এর presentation নির্ধারণ করে। |
| 184 | <code>  font-weight: 700;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 185 | <code>  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 186 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 187 | <code>.login-button:hover {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 188 | <code>  background: #083e2e;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 189 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 190 | <code>.login-button:disabled {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 191 | <code>  cursor: wait;</code> | CSS properties: cursor; enclosing selector-এর presentation নির্ধারণ করে। |
| 192 | <code>  opacity: 0.65;</code> | CSS properties: opacity; enclosing selector-এর presentation নির্ধারণ করে। |
| 193 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 194 | <code>button:focus-visible {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 195 | <code>  outline: 3px solid #b5f4d2;</code> | CSS properties: outline; enclosing selector-এর presentation নির্ধারণ করে। |
| 196 | <code>  outline-offset: 3px;</code> | CSS properties: outline-offset; enclosing selector-এর presentation নির্ধারণ করে। |
| 197 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 198 | <code>.secure-note {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 199 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 200 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 201 | <code>  justify-content: center;</code> | CSS properties: justify-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 202 | <code>  gap: 9px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 203 | <code>  margin-top: 24px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 204 | <code>  color: var(--muted);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 205 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 206 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 207 | <code>.secure-note i {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 208 | <code>  width: 7px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 209 | <code>  height: 7px;</code> | CSS properties: height; enclosing selector-এর presentation নির্ধারণ করে। |
| 210 | <code>  border-radius: 50%;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 211 | <code>  background: #9bf0bc;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 212 | <code>  box-shadow: 0 0 0 4px rgba(155, 240, 188, 0.12);</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 213 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 214 | <code>.account-link {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 215 | <code>  color: var(--muted);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 216 | <code>  text-align: center;</code> | CSS properties: text-align; enclosing selector-এর presentation নির্ধারণ করে। |
| 217 | <code>  font-size: 13px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 218 | <code>  margin: 18px 0 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 219 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 220 | <code>.account-link a {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 221 | <code>  color: #c6f7de;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 222 | <code>  font-weight: 700;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 223 | <code>  text-underline-offset: 4px;</code> | CSS properties: text-underline-offset; enclosing selector-এর presentation নির্ধারণ করে। |
| 224 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 225 | <code>.account-link a:focus-visible {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 226 | <code>  outline: 3px solid #b5f4d2;</code> | CSS properties: outline; enclosing selector-এর presentation নির্ধারণ করে। |
| 227 | <code>  outline-offset: 4px;</code> | CSS properties: outline-offset; enclosing selector-এর presentation নির্ধারণ করে। |
| 228 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 229 | <code>footer {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 230 | <code>  min-height: 54px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 231 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 232 | <code>  flex-wrap: wrap;</code> | CSS properties: flex-wrap; enclosing selector-এর presentation নির্ধারণ করে। |
| 233 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 234 | <code>  justify-content: center;</code> | CSS properties: justify-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 235 | <code>  gap: 5px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 236 | <code>  padding: 16px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 237 | <code>  background: rgba(4, 24, 19, 0.4);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 238 | <code>  color: #e1ebe7;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 239 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 240 | <code>  text-align: center;</code> | CSS properties: text-align; enclosing selector-এর presentation নির্ধারণ করে। |
| 241 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 242 | <code>footer strong {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 243 | <code>  color: #c6f7de;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 244 | <code>  letter-spacing: 0.8px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 245 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 246 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 247 | <code>@media (max-width: 850px) {</code> | Viewport condition অনুযায়ী responsive styles apply করে। |
| 248 | <code>  body {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 249 | <code>    background-attachment: scroll;</code> | CSS properties: background-attachment; enclosing selector-এর presentation নির্ধারণ করে। |
| 250 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 251 | <code>  .login-screen {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 252 | <code>    max-width: 560px;</code> | CSS properties: max-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 253 | <code>    grid-template-columns: 1fr;</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 254 | <code>    gap: 24px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 255 | <code>    padding: 32px 24px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 256 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 257 | <code>  .login-brand {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 258 | <code>    padding: 0;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 259 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 260 | <code>  .brand-badge {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 261 | <code>    margin-bottom: 18px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 262 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 263 | <code>  .login-brand h1 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 264 | <code>    font-size: 38px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 265 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 266 | <code>  .login-brand &gt; span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 267 | <code>    margin-top: 16px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 268 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 269 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 270 | <code>@media (max-width: 430px) {</code> | Viewport condition অনুযায়ী responsive styles apply করে। |
| 271 | <code>  .login-screen {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 272 | <code>    padding: 24px 18px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 273 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 274 | <code>  .login-brand h1 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 275 | <code>    font-size: 32px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 276 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 277 | <code>  .login-brand p {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 278 | <code>    font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 279 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 280 | <code>  .login-panel {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 281 | <code>    padding: 26px 22px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 282 | <code>    border-radius: 20px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 283 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 284 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 285 | <code>@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {</code> | Browser feature support অনুযায়ী fallback style নির্বাচন করে। |
| 286 | <code>  .login-panel {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 287 | <code>    background: rgba(8, 36, 28, 0.88);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 288 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 289 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 290 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 291 | <code>/* Saved credentials must stay legible against the glass surface. */</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 292 | <code>input:autofill {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 293 | <code>  color: #fff;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 294 | <code>  background: #29493e;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 295 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 296 | <code>input:-webkit-autofill,</code> | CSS properties: input; enclosing selector-এর presentation নির্ধারণ করে। |
| 297 | <code>input:-webkit-autofill:hover,</code> | CSS properties: input, -webkit-autofill; enclosing selector-এর presentation নির্ধারণ করে। |
| 298 | <code>input:-webkit-autofill:focus {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 299 | <code>  -webkit-text-fill-color: #fff;</code> | CSS properties: -webkit-text-fill-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 300 | <code>  caret-color: #fff;</code> | CSS properties: caret-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 301 | <code>  -webkit-box-shadow: 0 0 0 1000px #29493e inset;</code> | CSS properties: -webkit-box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 302 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 303 | <code>@media (max-height: 650px) and (min-width: 851px) {</code> | Viewport condition অনুযায়ী responsive styles apply করে। |
| 304 | <code>  .login-screen {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 305 | <code>    padding-top: 24px;</code> | CSS properties: padding-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 306 | <code>    padding-bottom: 24px;</code> | CSS properties: padding-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 307 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 308 | <code>  .login-panel {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 309 | <code>    padding: 26px 32px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 310 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 311 | <code>  .form-heading {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 312 | <code>    margin-bottom: 18px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 313 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 314 | <code>}</code> | Style rule/block-এর closing বা continuation। |
