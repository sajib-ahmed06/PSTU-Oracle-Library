# frontend/polish.css

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../frontend/polish.css)। Snapshot 2026-10-04; 237 lines; SHA-256 `ebaafd27ce2c6c08d5f9887c1ef50d4f3716cc3b603906f677997a75c53c6d15`।

## Function / object / element inventory

CSS selector/property rules source order-এ cascade করে। Later matching declaration আগের equivalent specificity rule override করতে পারে। Media/supports queries condition অনুযায়ী override দেয়। নিচের প্রতিটি line selector/property reading notes দেয়।

## সম্পূর্ণ original source

```css
/* Shared finishing touches for management and member workspaces. */
body {
  font-family: "Segoe UI", Arial, sans-serif;
  background: #f4f6f3;
}
.app-header {
  min-height: 80px;
  border-bottom-color: #e4e9e1;
}
.brand-mark {
  border-radius: 12px;
  box-shadow: 0 5px 14px #123b301a;
}
.user-menu button {
  border-radius: 8px;
  background: #f7f9f5;
}
.main-nav {
  background: #fff;
  color: #61725f;
  box-shadow: 0 3px 12px #233d2410;
  border-bottom: 1px solid #e3e9df;
}
.main-nav a {
  border-radius: 0;
  border-bottom: 2px solid transparent;
  font-size: 12px;
}
.main-nav a.active {
  border-bottom-color: #287345;
  background: #edf4e8;
  color: #285a37;
}
.main-nav a:hover {
  background: #f0f5ec;
  color: #285a37;
}
.main-nav a:focus-visible,
a.text-link:focus-visible {
  outline: 3px solid #9dbb88;
  outline-offset: -3px;
}
.workspace {
  padding-top: 32px;
}
.page-heading {
  align-items: center;
  border-bottom-color: #dfe6d9;
  padding-bottom: 20px;
  min-height: 106px;
}
.page-heading h1 {
  color: #253d2b;
  font-size: 30px;
  font-weight: 650;
  letter-spacing: -0.6px;
}
.heading-copy {
  line-height: 1.8;
  color: #73806b;
}
.surface,
.toolbar,
.command-strip {
  border-color: #e0e6db;
  border-radius: 14px;
  box-shadow: 0 5px 18px #29402404;
}
.surface-heading {
  min-height: 82px;
  padding: 20px 24px;
  border-bottom-color: #e8ede3;
}
.surface-heading h2 {
  font-size: 18px;
  color: #344a31;
  font-weight: 650;
}
.section-label,
.eyebrow {
  color: #668259;
  letter-spacing: 1.5px;
}
.toolbar {
  padding: 17px 22px;
  gap: 18px;
}
.toolbar strong {
  color: #344b30;
  font-weight: 650;
}
.command-strip {
  padding: 20px 24px;
  border-left: 4px solid #6e9659;
}
.button {
  border-radius: 8px;
  font-size: 12px;
}
.button.secondary {
  background: #fff;
  border-color: #dce5d6;
  color: #52644a;
}
.button.secondary:hover {
  background: #f1f5eb;
}
.button.primary {
  background: #215e3d;
  box-shadow: 0 3px 8px #214f3012;
}
.button.primary:hover {
  background: #174b2e;
}
input,
select {
  border-radius: 8px;
  border-color: #dce4d6;
  background: #fcfdf9;
}
.metric {
  border-radius: 12px;
  border-top-width: 2px;
  border-color: #e0e6dc;
  box-shadow: none;
  padding: 21px;
}
.metric strong {
  color: #2e4931;
  font-weight: 650;
}
.metric span {
  color: #75846c;
}
.metric small {
  color: #8b9783;
  line-height: 1.6;
}
th {
  background: #f6f8f2;
  color: #7a8b71;
  border-bottom-color: #e8ede3;
  padding-top: 17px;
  padding-bottom: 17px;
}
td {
  border-bottom-color: #edf1e8;
  padding-top: 17px;
  padding-bottom: 17px;
  color: #4b5c44;
}
tbody tr:hover {
  background: #f9fbf5;
}
.pill {
  padding: 6px 10px;
}
.empty-state {
  gap: 9px;
  align-content: center;
}
.empty-state span {
  margin-top: 0;
}
.modal form {
  border-radius: 16px;
  padding: 28px;
}
.modal-heading {
  padding-bottom: 19px;
}
.modal-heading h2 {
  color: #314b33;
}
.account-form label {
  color: #64755b;
}
.form-note {
  line-height: 1.8;
  color: #7b8871;
}
.form-surface {
  padding: 24px;
}
.form-surface > h2 {
  margin-bottom: 12px;
  color: #344b30;
}
.form-surface .account-form {
  padding: 12px 0 0;
}
#reserveForm.horizontal-form {
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) auto;
}
#reserveForm select {
  width: 100%;
  display: block;
  margin-top: 7px;
}
.app-footer {
  border-top-color: #e5eade;
}
@media (max-width: 700px) {
  .page-heading {
    align-items: flex-start;
    gap: 16px;
  }
  .page-heading h1 {
    font-size: 25px;
  }
  .toolbar {
    padding: 16px;
  }
  .surface-heading {
    padding: 18px;
  }
  .command-strip {
    padding: 18px;
  }
  .form-surface {
    padding: 18px;
  }
  #reserveForm.horizontal-form {
    grid-template-columns: 1fr;
  }
  .modal form {
    padding: 22px;
  }
}
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    scroll-behavior: auto !important;
    transition: none !important;
  }
}
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>/* Shared finishing touches for management and member workspaces. */</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 2 | <code>body {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 3 | <code>  font-family: &quot;Segoe UI&quot;, Arial, sans-serif;</code> | CSS properties: font-family; enclosing selector-এর presentation নির্ধারণ করে। |
| 4 | <code>  background: #f4f6f3;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 5 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 6 | <code>.app-header {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 7 | <code>  min-height: 80px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 8 | <code>  border-bottom-color: #e4e9e1;</code> | CSS properties: border-bottom-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 9 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 10 | <code>.brand-mark {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 11 | <code>  border-radius: 12px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 12 | <code>  box-shadow: 0 5px 14px #123b301a;</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 13 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 14 | <code>.user-menu button {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 15 | <code>  border-radius: 8px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 16 | <code>  background: #f7f9f5;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 17 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 18 | <code>.main-nav {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 19 | <code>  background: #fff;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 20 | <code>  color: #61725f;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 21 | <code>  box-shadow: 0 3px 12px #233d2410;</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 22 | <code>  border-bottom: 1px solid #e3e9df;</code> | CSS properties: border-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 23 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 24 | <code>.main-nav a {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 25 | <code>  border-radius: 0;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 26 | <code>  border-bottom: 2px solid transparent;</code> | CSS properties: border-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 27 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 28 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 29 | <code>.main-nav a.active {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 30 | <code>  border-bottom-color: #287345;</code> | CSS properties: border-bottom-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 31 | <code>  background: #edf4e8;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 32 | <code>  color: #285a37;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 33 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 34 | <code>.main-nav a:hover {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 35 | <code>  background: #f0f5ec;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 36 | <code>  color: #285a37;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 37 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 38 | <code>.main-nav a:focus-visible,</code> | CSS properties: a; enclosing selector-এর presentation নির্ধারণ করে। |
| 39 | <code>a.text-link:focus-visible {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 40 | <code>  outline: 3px solid #9dbb88;</code> | CSS properties: outline; enclosing selector-এর presentation নির্ধারণ করে। |
| 41 | <code>  outline-offset: -3px;</code> | CSS properties: outline-offset; enclosing selector-এর presentation নির্ধারণ করে। |
| 42 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 43 | <code>.workspace {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 44 | <code>  padding-top: 32px;</code> | CSS properties: padding-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 45 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 46 | <code>.page-heading {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 47 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 48 | <code>  border-bottom-color: #dfe6d9;</code> | CSS properties: border-bottom-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 49 | <code>  padding-bottom: 20px;</code> | CSS properties: padding-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 50 | <code>  min-height: 106px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 51 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 52 | <code>.page-heading h1 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 53 | <code>  color: #253d2b;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 54 | <code>  font-size: 30px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 55 | <code>  font-weight: 650;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 56 | <code>  letter-spacing: -0.6px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 57 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 58 | <code>.heading-copy {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 59 | <code>  line-height: 1.8;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 60 | <code>  color: #73806b;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 61 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 62 | <code>.surface,</code> | Style rule/block-এর closing বা continuation। |
| 63 | <code>.toolbar,</code> | Style rule/block-এর closing বা continuation। |
| 64 | <code>.command-strip {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 65 | <code>  border-color: #e0e6db;</code> | CSS properties: border-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 66 | <code>  border-radius: 14px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 67 | <code>  box-shadow: 0 5px 18px #29402404;</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 68 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 69 | <code>.surface-heading {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 70 | <code>  min-height: 82px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 71 | <code>  padding: 20px 24px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 72 | <code>  border-bottom-color: #e8ede3;</code> | CSS properties: border-bottom-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 73 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 74 | <code>.surface-heading h2 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 75 | <code>  font-size: 18px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 76 | <code>  color: #344a31;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 77 | <code>  font-weight: 650;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 78 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 79 | <code>.section-label,</code> | Style rule/block-এর closing বা continuation। |
| 80 | <code>.eyebrow {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 81 | <code>  color: #668259;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 82 | <code>  letter-spacing: 1.5px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 83 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 84 | <code>.toolbar {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 85 | <code>  padding: 17px 22px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 86 | <code>  gap: 18px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 87 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 88 | <code>.toolbar strong {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 89 | <code>  color: #344b30;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 90 | <code>  font-weight: 650;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 91 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 92 | <code>.command-strip {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 93 | <code>  padding: 20px 24px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 94 | <code>  border-left: 4px solid #6e9659;</code> | CSS properties: border-left; enclosing selector-এর presentation নির্ধারণ করে। |
| 95 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 96 | <code>.button {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 97 | <code>  border-radius: 8px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 98 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 99 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 100 | <code>.button.secondary {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 101 | <code>  background: #fff;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 102 | <code>  border-color: #dce5d6;</code> | CSS properties: border-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 103 | <code>  color: #52644a;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 104 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 105 | <code>.button.secondary:hover {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 106 | <code>  background: #f1f5eb;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 107 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 108 | <code>.button.primary {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 109 | <code>  background: #215e3d;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 110 | <code>  box-shadow: 0 3px 8px #214f3012;</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 111 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 112 | <code>.button.primary:hover {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 113 | <code>  background: #174b2e;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 114 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 115 | <code>input,</code> | Style rule/block-এর closing বা continuation। |
| 116 | <code>select {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 117 | <code>  border-radius: 8px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 118 | <code>  border-color: #dce4d6;</code> | CSS properties: border-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 119 | <code>  background: #fcfdf9;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 120 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 121 | <code>.metric {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 122 | <code>  border-radius: 12px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 123 | <code>  border-top-width: 2px;</code> | CSS properties: border-top-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 124 | <code>  border-color: #e0e6dc;</code> | CSS properties: border-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 125 | <code>  box-shadow: none;</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 126 | <code>  padding: 21px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 127 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 128 | <code>.metric strong {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 129 | <code>  color: #2e4931;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 130 | <code>  font-weight: 650;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 131 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 132 | <code>.metric span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 133 | <code>  color: #75846c;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 134 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 135 | <code>.metric small {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 136 | <code>  color: #8b9783;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 137 | <code>  line-height: 1.6;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 138 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 139 | <code>th {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 140 | <code>  background: #f6f8f2;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 141 | <code>  color: #7a8b71;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 142 | <code>  border-bottom-color: #e8ede3;</code> | CSS properties: border-bottom-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 143 | <code>  padding-top: 17px;</code> | CSS properties: padding-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 144 | <code>  padding-bottom: 17px;</code> | CSS properties: padding-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 145 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 146 | <code>td {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 147 | <code>  border-bottom-color: #edf1e8;</code> | CSS properties: border-bottom-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 148 | <code>  padding-top: 17px;</code> | CSS properties: padding-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 149 | <code>  padding-bottom: 17px;</code> | CSS properties: padding-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 150 | <code>  color: #4b5c44;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 151 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 152 | <code>tbody tr:hover {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 153 | <code>  background: #f9fbf5;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 154 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 155 | <code>.pill {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 156 | <code>  padding: 6px 10px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 157 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 158 | <code>.empty-state {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 159 | <code>  gap: 9px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 160 | <code>  align-content: center;</code> | CSS properties: align-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 161 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 162 | <code>.empty-state span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 163 | <code>  margin-top: 0;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 164 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 165 | <code>.modal form {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 166 | <code>  border-radius: 16px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 167 | <code>  padding: 28px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 168 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 169 | <code>.modal-heading {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 170 | <code>  padding-bottom: 19px;</code> | CSS properties: padding-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 171 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 172 | <code>.modal-heading h2 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 173 | <code>  color: #314b33;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 174 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 175 | <code>.account-form label {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 176 | <code>  color: #64755b;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 177 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 178 | <code>.form-note {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 179 | <code>  line-height: 1.8;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 180 | <code>  color: #7b8871;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 181 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 182 | <code>.form-surface {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 183 | <code>  padding: 24px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 184 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 185 | <code>.form-surface &gt; h2 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 186 | <code>  margin-bottom: 12px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 187 | <code>  color: #344b30;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 188 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 189 | <code>.form-surface .account-form {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 190 | <code>  padding: 12px 0 0;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 191 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 192 | <code>#reserveForm.horizontal-form {</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 193 | <code>  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) auto;</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 194 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 195 | <code>#reserveForm select {</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 196 | <code>  width: 100%;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 197 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 198 | <code>  margin-top: 7px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 199 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 200 | <code>.app-footer {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 201 | <code>  border-top-color: #e5eade;</code> | CSS properties: border-top-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 202 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 203 | <code>@media (max-width: 700px) {</code> | Viewport condition অনুযায়ী responsive styles apply করে। |
| 204 | <code>  .page-heading {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 205 | <code>    align-items: flex-start;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 206 | <code>    gap: 16px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 207 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 208 | <code>  .page-heading h1 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 209 | <code>    font-size: 25px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 210 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 211 | <code>  .toolbar {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 212 | <code>    padding: 16px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 213 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 214 | <code>  .surface-heading {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 215 | <code>    padding: 18px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 216 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 217 | <code>  .command-strip {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 218 | <code>    padding: 18px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 219 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 220 | <code>  .form-surface {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 221 | <code>    padding: 18px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 222 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 223 | <code>  #reserveForm.horizontal-form {</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 224 | <code>    grid-template-columns: 1fr;</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 225 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 226 | <code>  .modal form {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 227 | <code>    padding: 22px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 228 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 229 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 230 | <code>@media (prefers-reduced-motion: reduce) {</code> | Viewport condition অনুযায়ী responsive styles apply করে। |
| 231 | <code>  *,</code> | Style rule/block-এর closing বা continuation। |
| 232 | <code>  *::before,</code> | Style rule/block-এর closing বা continuation। |
| 233 | <code>  *::after {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 234 | <code>    scroll-behavior: auto !important;</code> | CSS properties: scroll-behavior; enclosing selector-এর presentation নির্ধারণ করে। |
| 235 | <code>    transition: none !important;</code> | CSS properties: transition; enclosing selector-এর presentation নির্ধারণ করে। |
| 236 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 237 | <code>}</code> | Style rule/block-এর closing বা continuation। |
