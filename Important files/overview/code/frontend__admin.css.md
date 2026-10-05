# frontend/admin.css

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../frontend/admin.css)। Snapshot 2026-10-04; 381 lines; SHA-256 `99adb13466cfebceef01151f3beaae11bd9b4487b27ba812e9ecb01b1db81121`।

## Function / object / element inventory

CSS selector/property rules source order-এ cascade করে। Later matching declaration আগের equivalent specificity rule override করতে পারে। Media/supports queries condition অনুযায়ী override দেয়। নিচের প্রতিটি line selector/property reading notes দেয়।

## সম্পূর্ণ original source

```css
body[data-page="overview"] {
  background: #f4f6f2;
}
.admin-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 24px;
}
.admin-heading h1 {
  font-size: 30px;
  color: #2a422e;
  font-weight: 650;
  letter-spacing: -0.6px;
}
.admin-heading p:not(.eyebrow) {
  font-size: 12px;
  color: #788970;
  margin: 8px 0 0;
}
.admin-heading-tools {
  display: flex;
  align-items: center;
  gap: 20px;
}
.admin-heading-tools .button {
  background: #fff;
}
.admin-welcome {
  position: relative;
  overflow: hidden;
  border-radius: 18px;
  min-height: 270px;
  padding: 34px 40px;
  margin-bottom: 22px;
  color: #fff;
  background:
    linear-gradient(90deg, #163d2df7, #163d2dd6 42%, #163d2d0a 85%),
    url("/static/assets/member-library-hero.webp") center/cover;
}
.admin-welcome > div {
  max-width: 520px;
}
.admin-welcome .cover-label {
  color: #d1e0c1;
  font-size: 9px;
  letter-spacing: 2px;
}
.admin-welcome h2 {
  font:
    500 37px/1.2 Georgia,
    serif;
  margin: 12px 0;
  letter-spacing: -0.4px;
}
.admin-welcome p {
  font-size: 12px;
  color: #d7e3d0;
  max-width: 410px;
  line-height: 1.8;
}
.admin-welcome .button {
  display: inline-block;
  margin-top: 8px;
  background: #edf0dc;
  color: #294a31;
  box-shadow: none;
  font-size: 11px;
}
.admin-cover-note {
  position: absolute;
  right: 30px;
  bottom: 27px;
  font:
    italic 17px Georgia,
    serif;
  text-shadow: 0 2px 6px #000;
}
.admin-shortcuts {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 15px;
  margin-bottom: 32px;
}
.admin-shortcuts a {
  display: flex;
  align-items: center;
  gap: 14px;
  background: #fff;
  border: 1px solid #e0e7d9;
  border-radius: 12px;
  padding: 20px;
  text-decoration: none;
  transition:
    border-color 0.2s,
    box-shadow 0.2s;
}
.admin-shortcuts a:hover {
  border-color: #96b084;
  box-shadow: 0 5px 15px #33553010;
}
.shortcut-mark {
  display: grid;
  place-items: center;
  width: 37px;
  height: 39px;
  background: #edf3e6;
  border-radius: 9px;
  color: #648451;
  font-size: 10px;
  font-weight: 700;
  flex-shrink: 0;
}
.admin-shortcuts strong {
  font-size: 12px;
  color: #344b32;
}
.admin-shortcuts small {
  display: block;
  font-size: 10px;
  color: #8b987f;
  margin-top: 5px;
}
.admin-shortcuts b {
  margin-left: auto;
  color: #819373;
  font-weight: 500;
}
.dashboard-section-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
  margin-bottom: 17px;
}
.dashboard-section-heading h2 {
  color: #314831;
  font-size: 19px;
  font-weight: 650;
  margin: 5px 0 0;
}
.dashboard-section-heading > span {
  font-size: 11px;
  color: #8a957f;
}
.metric-details {
  display: grid;
  gap: 6px;
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid #e4ebe5;
  color: #64786b;
  font-size: 11px;
  line-height: 1.5;
}
.metric-details-link {
  display: inline-block;
  margin-top: 14px;
  color: #176044;
  font-size: 11px;
  font-weight: 700;
  text-decoration: none;
}
.metric-details-link:hover {
  text-decoration: underline;
}
.attention-details {
  margin: 24px 0 32px;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}
.attention-details table {
  min-width: 0;
  width: 100%;
}
.attention-details td,
.attention-details th {
  padding: 12px 10px;
}
.attention-details td:first-child {
  min-width: 140px;
  white-space: normal;
}
@media (max-width: 1000px) {
  .attention-details {
    grid-template-columns: 1fr;
  }
}
.attention-details .surface-heading {
  align-items: flex-start;
  gap: 16px;
}
.attention-details .surface-heading p,
.fine-estimate-note {
  margin: 8px 0 0;
  color: #6e7d72;
  font-size: 12px;
  line-height: 1.6;
}
.attention-details td small {
  display: block;
  margin-top: 5px;
  color: #6e7d72;
}
.fine-estimate-note {
  padding: 12px 0;
}
#stats {
  grid-template-columns: repeat(6, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 30px;
}
#stats .metric {
  min-height: 153px;
  padding: 19px 17px;
}
#stats .metric-top {
  align-items: flex-start;
}
#stats .metric-mark {
  width: 28px;
  flex-shrink: 0;
}
#stats .metric strong {
  font-size: 29px;
  margin-top: 17px;
}
.desk-priorities {
  margin-bottom: 30px;
}
.priority-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}
.priority-card {
  background: #fff;
  padding: 21px 24px;
  border-radius: 12px;
  border: 1px solid #e1e7dc;
  display: flex;
  justify-content: space-between;
  gap: 20px;
  align-items: center;
  text-decoration: none;
}
.priority-card:hover {
  background: #fafcf6;
}
.priority-card strong {
  font-size: 13px;
  color: #3c5036;
  display: block;
}
.priority-card small {
  font-size: 11px;
  color: #86947b;
  display: block;
  margin-top: 6px;
}
.priority-count {
  font-size: 29px;
  color: #567b40;
  font-weight: 650;
}
.priority-card.urgent .priority-count {
  color: #b07354;
}
.dashboard-grid {
  gap: 22px;
}
.health-note {
  border-radius: 10px;
  background: #eef4e7;
  padding: 17px;
}
.health-note b {
  color: #65864c;
}
.health-row {
  padding: 17px 0;
}
.health-row div {
  color: #708463;
}
.health-row progress {
  height: 7px;
  border-radius: 10px;
  overflow: hidden;
}
.health-row:nth-child(2) progress::-webkit-progress-value {
  background: #b99a65;
}
.health-row:nth-child(3) progress::-webkit-progress-value {
  background: #82a6a0;
}
@media (max-width: 1200px) {
  #stats {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
  .admin-shortcuts {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .dashboard-grid {
    grid-template-columns: minmax(0, 1.7fr) minmax(260px, 1fr);
  }
}
@media (max-width: 800px) {
  .admin-heading-tools .current-date {
    display: none;
  }
  .admin-welcome {
    padding: 30px;
  }
  .admin-welcome h2 {
    font-size: 31px;
  }
  .admin-cover-note {
    display: none;
  }
  .priority-grid {
    grid-template-columns: 1fr;
  }
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  .dashboard-section-heading > span {
    display: none;
  }
}
@media (max-width: 500px) {
  .admin-heading h1 {
    font-size: 24px;
  }
  .admin-heading p:not(.eyebrow) {
    font-size: 11px;
  }
  .admin-heading-tools .button {
    font-size: 10px;
    padding: 10px;
  }
  .admin-welcome {
    padding: 28px 22px;
  }
  .admin-welcome h2 {
    font-size: 30px;
  }
  .admin-shortcuts {
    gap: 10px;
  }
  .admin-shortcuts a {
    padding: 15px 12px;
    gap: 10px;
  }
  .admin-shortcuts b {
    display: none;
  }
  .admin-shortcuts strong {
    font-size: 11px;
  }
  .admin-shortcuts small {
    font-size: 9px;
  }
  #stats {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
  }
  #stats .metric {
    padding: 17px 14px;
  }
  #stats .metric-top {
    gap: 8px;
  }
  #stats .metric-top > span:not(.metric-mark) {
    font-size: 10px;
  }
  .shortcut-mark {
    width: 29px;
    height: 34px;
  }
}
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>body[data-page=&quot;overview&quot;] {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 2 | <code>  background: #f4f6f2;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 3 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 4 | <code>.admin-heading {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 5 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 6 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 7 | <code>  justify-content: space-between;</code> | CSS properties: justify-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 8 | <code>  gap: 20px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 9 | <code>  margin-bottom: 24px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 10 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 11 | <code>.admin-heading h1 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 12 | <code>  font-size: 30px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 13 | <code>  color: #2a422e;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 14 | <code>  font-weight: 650;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 15 | <code>  letter-spacing: -0.6px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 16 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 17 | <code>.admin-heading p:not(.eyebrow) {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 18 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 19 | <code>  color: #788970;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 20 | <code>  margin: 8px 0 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 21 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 22 | <code>.admin-heading-tools {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 23 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 24 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 25 | <code>  gap: 20px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 26 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 27 | <code>.admin-heading-tools .button {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 28 | <code>  background: #fff;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 29 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 30 | <code>.admin-welcome {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 31 | <code>  position: relative;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 32 | <code>  overflow: hidden;</code> | CSS properties: overflow; enclosing selector-এর presentation নির্ধারণ করে। |
| 33 | <code>  border-radius: 18px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 34 | <code>  min-height: 270px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 35 | <code>  padding: 34px 40px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 36 | <code>  margin-bottom: 22px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 37 | <code>  color: #fff;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 38 | <code>  background:</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 39 | <code>    linear-gradient(90deg, #163d2df7, #163d2dd6 42%, #163d2d0a 85%),</code> | Style rule/block-এর closing বা continuation। |
| 40 | <code>    url(&quot;/static/assets/member-library-hero.webp&quot;) center/cover;</code> | Style rule/block-এর closing বা continuation। |
| 41 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 42 | <code>.admin-welcome &gt; div {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 43 | <code>  max-width: 520px;</code> | CSS properties: max-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 44 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 45 | <code>.admin-welcome .cover-label {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 46 | <code>  color: #d1e0c1;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 47 | <code>  font-size: 9px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 48 | <code>  letter-spacing: 2px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 49 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 50 | <code>.admin-welcome h2 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 51 | <code>  font:</code> | CSS properties: font; enclosing selector-এর presentation নির্ধারণ করে। |
| 52 | <code>    500 37px/1.2 Georgia,</code> | Style rule/block-এর closing বা continuation। |
| 53 | <code>    serif;</code> | Style rule/block-এর closing বা continuation। |
| 54 | <code>  margin: 12px 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 55 | <code>  letter-spacing: -0.4px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 56 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 57 | <code>.admin-welcome p {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 58 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 59 | <code>  color: #d7e3d0;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 60 | <code>  max-width: 410px;</code> | CSS properties: max-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 61 | <code>  line-height: 1.8;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 62 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 63 | <code>.admin-welcome .button {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 64 | <code>  display: inline-block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 65 | <code>  margin-top: 8px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 66 | <code>  background: #edf0dc;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 67 | <code>  color: #294a31;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 68 | <code>  box-shadow: none;</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 69 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 70 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 71 | <code>.admin-cover-note {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 72 | <code>  position: absolute;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 73 | <code>  right: 30px;</code> | CSS properties: right; enclosing selector-এর presentation নির্ধারণ করে। |
| 74 | <code>  bottom: 27px;</code> | CSS properties: bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 75 | <code>  font:</code> | CSS properties: font; enclosing selector-এর presentation নির্ধারণ করে। |
| 76 | <code>    italic 17px Georgia,</code> | Style rule/block-এর closing বা continuation। |
| 77 | <code>    serif;</code> | Style rule/block-এর closing বা continuation। |
| 78 | <code>  text-shadow: 0 2px 6px #000;</code> | CSS properties: text-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 79 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 80 | <code>.admin-shortcuts {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 81 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 82 | <code>  grid-template-columns: repeat(4, minmax(0, 1fr));</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 83 | <code>  gap: 15px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 84 | <code>  margin-bottom: 32px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 85 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 86 | <code>.admin-shortcuts a {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 87 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 88 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 89 | <code>  gap: 14px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 90 | <code>  background: #fff;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 91 | <code>  border: 1px solid #e0e7d9;</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 92 | <code>  border-radius: 12px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 93 | <code>  padding: 20px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 94 | <code>  text-decoration: none;</code> | CSS properties: text-decoration; enclosing selector-এর presentation নির্ধারণ করে। |
| 95 | <code>  transition:</code> | CSS properties: transition; enclosing selector-এর presentation নির্ধারণ করে। |
| 96 | <code>    border-color 0.2s,</code> | Style rule/block-এর closing বা continuation। |
| 97 | <code>    box-shadow 0.2s;</code> | Style rule/block-এর closing বা continuation। |
| 98 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 99 | <code>.admin-shortcuts a:hover {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 100 | <code>  border-color: #96b084;</code> | CSS properties: border-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 101 | <code>  box-shadow: 0 5px 15px #33553010;</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 102 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 103 | <code>.shortcut-mark {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 104 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 105 | <code>  place-items: center;</code> | CSS properties: place-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 106 | <code>  width: 37px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 107 | <code>  height: 39px;</code> | CSS properties: height; enclosing selector-এর presentation নির্ধারণ করে। |
| 108 | <code>  background: #edf3e6;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 109 | <code>  border-radius: 9px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 110 | <code>  color: #648451;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 111 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 112 | <code>  font-weight: 700;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 113 | <code>  flex-shrink: 0;</code> | CSS properties: flex-shrink; enclosing selector-এর presentation নির্ধারণ করে। |
| 114 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 115 | <code>.admin-shortcuts strong {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 116 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 117 | <code>  color: #344b32;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 118 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 119 | <code>.admin-shortcuts small {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 120 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 121 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 122 | <code>  color: #8b987f;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 123 | <code>  margin-top: 5px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 124 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 125 | <code>.admin-shortcuts b {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 126 | <code>  margin-left: auto;</code> | CSS properties: margin-left; enclosing selector-এর presentation নির্ধারণ করে। |
| 127 | <code>  color: #819373;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 128 | <code>  font-weight: 500;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 129 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 130 | <code>.dashboard-section-heading {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 131 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 132 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 133 | <code>  justify-content: space-between;</code> | CSS properties: justify-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 134 | <code>  gap: 15px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 135 | <code>  margin-bottom: 17px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 136 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 137 | <code>.dashboard-section-heading h2 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 138 | <code>  color: #314831;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 139 | <code>  font-size: 19px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 140 | <code>  font-weight: 650;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 141 | <code>  margin: 5px 0 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 142 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 143 | <code>.dashboard-section-heading &gt; span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 144 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 145 | <code>  color: #8a957f;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 146 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 147 | <code>.metric-details {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 148 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 149 | <code>  gap: 6px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 150 | <code>  margin-top: 16px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 151 | <code>  padding-top: 12px;</code> | CSS properties: padding-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 152 | <code>  border-top: 1px solid #e4ebe5;</code> | CSS properties: border-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 153 | <code>  color: #64786b;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 154 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 155 | <code>  line-height: 1.5;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 156 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 157 | <code>.metric-details-link {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 158 | <code>  display: inline-block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 159 | <code>  margin-top: 14px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 160 | <code>  color: #176044;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 161 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 162 | <code>  font-weight: 700;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 163 | <code>  text-decoration: none;</code> | CSS properties: text-decoration; enclosing selector-এর presentation নির্ধারণ করে। |
| 164 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 165 | <code>.metric-details-link:hover {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 166 | <code>  text-decoration: underline;</code> | CSS properties: text-decoration; enclosing selector-এর presentation নির্ধারণ করে। |
| 167 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 168 | <code>.attention-details {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 169 | <code>  margin: 24px 0 32px;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 170 | <code>  grid-template-columns: repeat(2, minmax(0, 1fr));</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 171 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 172 | <code>.attention-details table {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 173 | <code>  min-width: 0;</code> | CSS properties: min-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 174 | <code>  width: 100%;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 175 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 176 | <code>.attention-details td,</code> | Style rule/block-এর closing বা continuation। |
| 177 | <code>.attention-details th {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 178 | <code>  padding: 12px 10px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 179 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 180 | <code>.attention-details td:first-child {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 181 | <code>  min-width: 140px;</code> | CSS properties: min-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 182 | <code>  white-space: normal;</code> | CSS properties: white-space; enclosing selector-এর presentation নির্ধারণ করে। |
| 183 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 184 | <code>@media (max-width: 1000px) {</code> | Viewport condition অনুযায়ী responsive styles apply করে। |
| 185 | <code>  .attention-details {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 186 | <code>    grid-template-columns: 1fr;</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 187 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 188 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 189 | <code>.attention-details .surface-heading {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 190 | <code>  align-items: flex-start;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 191 | <code>  gap: 16px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 192 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 193 | <code>.attention-details .surface-heading p,</code> | Style rule/block-এর closing বা continuation। |
| 194 | <code>.fine-estimate-note {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 195 | <code>  margin: 8px 0 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 196 | <code>  color: #6e7d72;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 197 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 198 | <code>  line-height: 1.6;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 199 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 200 | <code>.attention-details td small {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 201 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 202 | <code>  margin-top: 5px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 203 | <code>  color: #6e7d72;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 204 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 205 | <code>.fine-estimate-note {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 206 | <code>  padding: 12px 0;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 207 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 208 | <code>#stats {</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 209 | <code>  grid-template-columns: repeat(6, minmax(0, 1fr));</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 210 | <code>  gap: 14px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 211 | <code>  margin-bottom: 30px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 212 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 213 | <code>#stats .metric {</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 214 | <code>  min-height: 153px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 215 | <code>  padding: 19px 17px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 216 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 217 | <code>#stats .metric-top {</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 218 | <code>  align-items: flex-start;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 219 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 220 | <code>#stats .metric-mark {</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 221 | <code>  width: 28px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 222 | <code>  flex-shrink: 0;</code> | CSS properties: flex-shrink; enclosing selector-এর presentation নির্ধারণ করে। |
| 223 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 224 | <code>#stats .metric strong {</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 225 | <code>  font-size: 29px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 226 | <code>  margin-top: 17px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 227 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 228 | <code>.desk-priorities {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 229 | <code>  margin-bottom: 30px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 230 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 231 | <code>.priority-grid {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 232 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 233 | <code>  grid-template-columns: repeat(4, minmax(0, 1fr));</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 234 | <code>  gap: 16px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 235 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 236 | <code>.priority-card {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 237 | <code>  background: #fff;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 238 | <code>  padding: 21px 24px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 239 | <code>  border-radius: 12px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 240 | <code>  border: 1px solid #e1e7dc;</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 241 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 242 | <code>  justify-content: space-between;</code> | CSS properties: justify-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 243 | <code>  gap: 20px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 244 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 245 | <code>  text-decoration: none;</code> | CSS properties: text-decoration; enclosing selector-এর presentation নির্ধারণ করে। |
| 246 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 247 | <code>.priority-card:hover {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 248 | <code>  background: #fafcf6;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 249 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 250 | <code>.priority-card strong {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 251 | <code>  font-size: 13px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 252 | <code>  color: #3c5036;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 253 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 254 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 255 | <code>.priority-card small {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 256 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 257 | <code>  color: #86947b;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 258 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 259 | <code>  margin-top: 6px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 260 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 261 | <code>.priority-count {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 262 | <code>  font-size: 29px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 263 | <code>  color: #567b40;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 264 | <code>  font-weight: 650;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 265 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 266 | <code>.priority-card.urgent .priority-count {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 267 | <code>  color: #b07354;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 268 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 269 | <code>.dashboard-grid {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 270 | <code>  gap: 22px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 271 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 272 | <code>.health-note {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 273 | <code>  border-radius: 10px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 274 | <code>  background: #eef4e7;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 275 | <code>  padding: 17px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 276 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 277 | <code>.health-note b {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 278 | <code>  color: #65864c;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 279 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 280 | <code>.health-row {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 281 | <code>  padding: 17px 0;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 282 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 283 | <code>.health-row div {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 284 | <code>  color: #708463;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 285 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 286 | <code>.health-row progress {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 287 | <code>  height: 7px;</code> | CSS properties: height; enclosing selector-এর presentation নির্ধারণ করে। |
| 288 | <code>  border-radius: 10px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 289 | <code>  overflow: hidden;</code> | CSS properties: overflow; enclosing selector-এর presentation নির্ধারণ করে। |
| 290 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 291 | <code>.health-row:nth-child(2) progress::-webkit-progress-value {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 292 | <code>  background: #b99a65;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 293 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 294 | <code>.health-row:nth-child(3) progress::-webkit-progress-value {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 295 | <code>  background: #82a6a0;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 296 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 297 | <code>@media (max-width: 1200px) {</code> | Viewport condition অনুযায়ী responsive styles apply করে। |
| 298 | <code>  #stats {</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 299 | <code>    grid-template-columns: repeat(3, minmax(0, 1fr));</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 300 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 301 | <code>  .admin-shortcuts {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 302 | <code>    grid-template-columns: repeat(2, minmax(0, 1fr));</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 303 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 304 | <code>  .dashboard-grid {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 305 | <code>    grid-template-columns: minmax(0, 1.7fr) minmax(260px, 1fr);</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 306 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 307 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 308 | <code>@media (max-width: 800px) {</code> | Viewport condition অনুযায়ী responsive styles apply করে। |
| 309 | <code>  .admin-heading-tools .current-date {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 310 | <code>    display: none;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 311 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 312 | <code>  .admin-welcome {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 313 | <code>    padding: 30px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 314 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 315 | <code>  .admin-welcome h2 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 316 | <code>    font-size: 31px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 317 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 318 | <code>  .admin-cover-note {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 319 | <code>    display: none;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 320 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 321 | <code>  .priority-grid {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 322 | <code>    grid-template-columns: 1fr;</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 323 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 324 | <code>  .dashboard-grid {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 325 | <code>    grid-template-columns: 1fr;</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 326 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 327 | <code>  .dashboard-section-heading &gt; span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 328 | <code>    display: none;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 329 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 330 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 331 | <code>@media (max-width: 500px) {</code> | Viewport condition অনুযায়ী responsive styles apply করে। |
| 332 | <code>  .admin-heading h1 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 333 | <code>    font-size: 24px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 334 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 335 | <code>  .admin-heading p:not(.eyebrow) {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 336 | <code>    font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 337 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 338 | <code>  .admin-heading-tools .button {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 339 | <code>    font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 340 | <code>    padding: 10px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 341 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 342 | <code>  .admin-welcome {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 343 | <code>    padding: 28px 22px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 344 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 345 | <code>  .admin-welcome h2 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 346 | <code>    font-size: 30px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 347 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 348 | <code>  .admin-shortcuts {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 349 | <code>    gap: 10px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 350 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 351 | <code>  .admin-shortcuts a {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 352 | <code>    padding: 15px 12px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 353 | <code>    gap: 10px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 354 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 355 | <code>  .admin-shortcuts b {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 356 | <code>    display: none;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 357 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 358 | <code>  .admin-shortcuts strong {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 359 | <code>    font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 360 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 361 | <code>  .admin-shortcuts small {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 362 | <code>    font-size: 9px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 363 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 364 | <code>  #stats {</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 365 | <code>    grid-template-columns: repeat(2, minmax(0, 1fr));</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 366 | <code>    gap: 10px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 367 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 368 | <code>  #stats .metric {</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 369 | <code>    padding: 17px 14px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 370 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 371 | <code>  #stats .metric-top {</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 372 | <code>    gap: 8px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 373 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 374 | <code>  #stats .metric-top &gt; span:not(.metric-mark) {</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 375 | <code>    font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 376 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 377 | <code>  .shortcut-mark {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 378 | <code>    width: 29px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 379 | <code>    height: 34px;</code> | CSS properties: height; enclosing selector-এর presentation নির্ধারণ করে। |
| 380 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 381 | <code>}</code> | Style rule/block-এর closing বা continuation। |
