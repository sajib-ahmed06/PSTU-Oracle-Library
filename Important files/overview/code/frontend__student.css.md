# frontend/student.css

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../frontend/student.css)। Snapshot 2026-10-04; 952 lines; SHA-256 `b2d0e55f2ebcf40af0101e793082dd998422218a47910a3882da256112766c7b`।

## Function / object / element inventory

CSS selector/property rules source order-এ cascade করে। Later matching declaration আগের equivalent specificity rule override করতে পারে। Media/supports queries condition অনুযায়ী override দেয়। নিচের প্রতিটি line selector/property reading notes দেয়।

## সম্পূর্ণ original source

```css
.member-alert-panel {
  margin-bottom: 24px;
}
.member-alert-list {
  display: grid;
  gap: 12px;
  padding: 0 20px 20px;
}
.member-reminder {
  display: flex;
  align-items: center;
  gap: 14px;
  border: 1px solid #dce6ef;
  border-radius: 14px;
  padding: 16px;
  background: #f2f7fc;
  color: #254962;
  text-decoration: none;
}
.member-reminder.fine {
  border-color: #ecdbbd;
  background: #fff8ed;
  color: #76511a;
}
.member-reminder.clear {
  background: #f2f7f1;
  color: #375b3b;
  border-color: #dfe8da;
}
.member-reminder div {
  display: grid;
  gap: 5px;
  min-width: 0;
}
.member-reminder strong {
  font-size: 14px;
}
.member-reminder span:not(.visit-mark),
.member-reminder small {
  font-size: 12px;
  line-height: 1.6;
  overflow-wrap: anywhere;
}
.member-reminder > b {
  margin-left: auto;
}
.member-reminder:focus-visible {
  outline: 3px solid #85b69a;
  outline-offset: 2px;
}
body[data-page="student"] {
  background: #f5f6f2;
  font-family: "Segoe UI", Arial, sans-serif;
}
body[data-page="student"] .main-nav {
  display: none;
}
.member-layout {
  display: grid;
  grid-template-columns: 220px minmax(0, 1fr);
  width: min(1500px, 100%);
  margin: 0 auto;
}
.member-sidebar {
  padding: 35px 22px;
  border-right: 1px solid #e2e6de;
  align-self: start;
  position: sticky;
  top: 0;
}
.portal-title {
  display: flex;
  gap: 12px;
  align-items: center;
  color: #153f31;
  text-decoration: none;
  font-size: 20px;
  font-weight: 750;
}
.portal-title small {
  display: block;
  font-size: 9px;
  letter-spacing: 1.8px;
  margin-top: 3px;
  font-weight: 600;
  color: #788477;
}
.portal-symbol {
  display: grid;
  place-items: center;
  width: 40px;
  height: 44px;
  border-radius: 11px;
  background: #184b39;
  color: #fff;
  font-family: Georgia, serif;
  font-size: 29px;
}
.sidebar-label {
  margin: 38px 0 16px;
  font-size: 9px;
  color: #889184;
  letter-spacing: 1.7px;
  font-weight: 700;
}
.member-sidebar nav {
  display: grid;
  gap: 6px;
}
.member-sidebar nav a {
  display: flex;
  gap: 13px;
  padding: 13px 10px;
  border-radius: 8px;
  text-decoration: none;
  color: #5d695f;
  font-size: 12px;
  font-weight: 600;
}
.member-sidebar nav a span {
  color: #8a9c8c;
  font-size: 10px;
}
.member-sidebar nav a:hover,
.member-sidebar nav a:focus-visible {
  background: #e6eee5;
  color: #154630;
}
.sidebar-guide {
  border: 1px solid #dce4d8;
  border-radius: 13px;
  padding: 18px 15px;
  background: #edf1e7;
  margin-top: 40px;
}
.sidebar-guide strong {
  display: block;
  margin-top: 12px;
  color: #294832;
  font-family: Georgia, serif;
  font-size: 19px;
  font-weight: 500;
}
.sidebar-guide p {
  font-size: 11px;
  line-height: 1.8;
  color: #6b7668;
}
.sidebar-guide a {
  font-size: 11px;
  font-weight: 700;
  color: #2c603d;
  text-decoration: none;
}
.member-main {
  min-width: 0;
  padding: 30px 34px 48px;
}
.member-topline {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 25px;
}
.member-topline .eyebrow {
  font-size: 9px;
  letter-spacing: 2px;
  margin-bottom: 6px;
}
.member-topline h1 {
  font-size: 27px;
  margin: 0;
  font-weight: 650;
  color: #243c2b;
}
.member-topline .button {
  background: #fff;
  font-size: 11px;
  border-radius: 8px;
}
.member-hero {
  position: relative;
  overflow: hidden;
  border-radius: 18px;
  background:
    linear-gradient(
      90deg,
      rgba(10, 41, 29, 0.97),
      rgba(10, 41, 29, 0.83) 40%,
      rgba(10, 41, 29, 0.08) 78%
    ),
    url("/static/assets/member-library-hero.webp") center/cover;
  min-height: 285px;
  display: flex;
  align-items: center;
  color: #fff;
  padding: 35px 38px;
}
.hero-copy {
  max-width: 520px;
  position: relative;
  z-index: 1;
}
.hero-kicker {
  font-size: 9px;
  letter-spacing: 2px;
  color: #cdddbc;
  font-weight: 650;
}
.member-hero h2 {
  font:
    500 clamp(29px, 3vw, 42px)/1.18 Georgia,
    serif;
  margin: 17px 0 13px;
  letter-spacing: -0.6px;
}
.member-hero p {
  max-width: 365px;
  color: #d3dfd3;
  font-size: 12px;
  line-height: 1.8;
}
.hero-actions {
  display: flex;
  align-items: center;
  gap: 22px;
  margin-top: 23px;
  flex-wrap: wrap;
}
.hero-actions .button {
  background: #e9edda;
  color: #183f2a;
  border: 0;
  font-size: 11px;
  border-radius: 8px;
  padding: 12px 17px;
}
.hero-actions > a:not(.button) {
  color: #e2eadb;
  font-size: 11px;
  text-underline-offset: 5px;
}
.hero-caption {
  position: absolute;
  bottom: 23px;
  right: 26px;
  font:
    italic 18px Georgia,
    serif;
  color: #faf5e6;
  text-shadow: 0 2px 8px #000;
}
.member-profile {
  display: flex;
  align-items: center;
  gap: 9px;
  margin: 17px 2px 22px;
  color: #72806e;
  font-size: 10px;
  flex-wrap: wrap;
}
.member-profile p {
  margin: 0;
  overflow-wrap: anywhere;
}
.profile-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #648f58;
}
.profile-note {
  margin-left: auto;
  color: #84917d;
}
.member-stats {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 23px;
}
.member-stat {
  background: #fff;
  padding: 20px 22px;
  border: 1px solid #e1e6dc;
  border-radius: 12px;
}
.member-stat > span {
  font-size: 10px;
  color: #75806f;
}
.member-stat strong {
  display: block;
  margin: 10px 0 7px;
  font-size: 29px;
  font-weight: 650;
  letter-spacing: -0.6px;
  color: #224630;
}
.member-stat small {
  color: #8a9583;
  font-size: 10px;
}
.member-stat:nth-child(2) strong {
  color: #9b7438;
}
.member-stat:nth-child(3) strong {
  color: #9b5b4c;
}
.member-panel {
  background: #fff;
  border: 1px solid #e0e6dc;
  border-radius: 14px;
  overflow: hidden;
  margin-bottom: 24px;
  scroll-margin-top: 20px;
  min-width: 0;
}
.panel-heading {
  padding: 23px 25px 19px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 18px;
}
.member-main .section-label {
  font-size: 8px;
  letter-spacing: 1.8px;
  color: #75886c;
}
.panel-heading h2 {
  font-size: 19px;
  font-weight: 650;
  color: #2e4832;
  margin: 7px 0 0;
}
.section-description {
  color: #7b8575;
  font-size: 11px;
  line-height: 1.8;
  margin: 8px 0 0;
  max-width: 520px;
}
.small-tag {
  border: 1px solid #e4e9df;
  border-radius: 20px;
  padding: 5px 10px;
  font-size: 9px;
  color: #78866e;
  white-space: nowrap;
}
.member-feature-grid {
  display: grid;
  grid-template-columns: 1.15fr 1fr;
  gap: 22px;
}
.next-step {
  min-height: 220px;
}
#memberNextStep {
  padding: 0 25px 22px;
}
.next-visit-item {
  display: flex;
  align-items: center;
  gap: 13px;
  padding: 12px 0;
  border-top: 1px solid #edf0e9;
}
.visit-mark {
  width: 34px;
  height: 36px;
  display: grid;
  place-items: center;
  border-radius: 8px;
  background: #eff3e9;
  color: #5f7d4b;
  font-size: 10px;
  font-weight: 700;
  flex-shrink: 0;
}
.next-visit-item strong {
  font-size: 12px;
  display: block;
  color: #364b33;
}
.next-visit-item small {
  color: #87917e;
  font-size: 10px;
  display: block;
  margin-top: 4px;
}
.next-visit-item a {
  margin-left: auto;
  font-size: 10px;
  color: #537944;
  white-space: nowrap;
}
.discovery-card {
  position: relative;
  min-height: 220px;
  border-radius: 14px;
  overflow: hidden;
  margin-bottom: 24px;
  background: #244331;
}
.discovery-card img {
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.discovery-card::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, rgba(15, 39, 24, 0.86), rgba(15, 39, 24, 0.1));
}
.discovery-card > div {
  position: relative;
  z-index: 1;
  padding: 26px;
  color: #fff;
}
.discovery-card .section-label {
  color: #e0e9d0;
}
.discovery-card h2 {
  font:
    500 26px/1.3 Georgia,
    serif;
  margin: 13px 0 19px;
}
.discovery-card a {
  color: #edf2dc;
  font-size: 11px;
  text-decoration: none;
}
.member-info-strip {
  background: #f4f7ef;
  color: #75826c;
  font-size: 10px;
  padding: 12px 25px;
  border-top: 1px solid #ebefe5;
  border-bottom: 1px solid #ebefe5;
}
.member-main table {
  font-size: 11px;
}
.member-main th {
  background: #f7f9f4;
  color: #85907c;
  font-size: 9px;
  padding: 14px 20px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.member-main td {
  padding: 17px 20px;
}
.member-main .pill {
  font-size: 9px;
}
.member-main .button.small {
  font-size: 10px;
  border-radius: 6px;
}
.member-main .empty-state {
  padding: 30px 20px;
}
.member-main .empty-state strong {
  color: #55704b;
  font-size: 13px;
}
.member-main .empty-state span {
  color: #89927e;
  font-size: 11px;
  margin-top: 7px;
}
.catalogue-search {
  color: #85907b;
  font-size: 9px;
  width: 270px;
  flex-shrink: 0;
}
.catalogue-search input {
  width: 100%;
  margin-top: 7px;
  border-radius: 8px;
  font-size: 11px;
  padding: 11px 12px;
  background: #f8faf5;
}
.member-catalogue {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  padding: 4px 25px 25px;
}
.book-card {
  border: 1px solid #e4e9de;
  border-radius: 11px;
  padding: 17px;
  display: flex;
  flex-direction: column;
  min-width: 0;
  background: #fcfdf9;
}
.book-card-top {
  display: flex;
  gap: 13px;
  align-items: flex-start;
  margin-bottom: 16px;
}
.book-spine {
  background: #39644b;
  color: #e4ecd3;
  width: 44px;
  height: 61px;
  border-left: 5px solid #214c34;
  border-radius: 2px 5px 5px 2px;
  flex-shrink: 0;
  display: grid;
  place-items: center;
  font:
    21px Georgia,
    serif;
  box-shadow: 3px 3px 0 #e7eadf;
}
.book-card:nth-child(3n + 2) .book-spine {
  background: #b08956;
  border-color: #8c6a3e;
}
.book-card:nth-child(3n) .book-spine {
  background: #68848a;
  border-color: #4f6b72;
}
.book-card h3 {
  font-size: 12px;
  color: #354b32;
  margin: 2px 0 5px;
  line-height: 1.6;
  overflow-wrap: anywhere;
}
.book-card p {
  margin: 0;
  font-size: 10px;
  color: #8a947e;
  line-height: 1.7;
}
.book-card-category {
  color: #788c6b;
  font-size: 8px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  margin-bottom: 10px;
}
.book-card-stock {
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  font-size: 9px;
  color: #859079;
  margin-bottom: 13px;
}
.book-card-stock b {
  color: #567644;
  font-weight: 600;
}
.book-card .button {
  width: 100%;
  margin-top: auto;
  min-height: 34px;
}
.book-card .button:disabled {
  background: #edf0e8;
  border-color: #e3e7dc;
  color: #909a82;
  cursor: default;
}
.member-catalogue > .empty-state {
  grid-column: 1/-1;
}
.member-bottom-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr);
  gap: 22px;
}
.security-panel .account-form {
  padding: 0 25px 25px;
}
.security-panel label {
  font-size: 10px;
  color: #76836e;
}
.security-panel input {
  border-radius: 7px;
  font-size: 12px;
  background: #fbfcf8;
}
.security-panel .button {
  font-size: 11px;
  border-radius: 7px;
}
.member-main a:focus-visible {
  outline: 3px solid #92b879;
  outline-offset: 4px;
}
@media (max-width: 1150px) {
  .member-layout {
    grid-template-columns: 180px minmax(0, 1fr);
  }
  .member-sidebar {
    padding: 30px 14px;
  }
  .member-main {
    padding: 25px 22px;
  }
  .member-stats {
    gap: 10px;
  }
  .member-stat {
    padding: 17px 15px;
  }
  .member-catalogue {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .member-bottom-grid {
    grid-template-columns: 1fr;
  }
  .profile-note {
    display: none;
  }
}
@media (max-width: 800px) {
  .member-layout {
    display: block;
  }
  .member-sidebar {
    position: static;
    padding: 16px 22px 0;
    border: 0;
  }
  .portal-title,
  .sidebar-label,
  .sidebar-guide {
    display: none;
  }
  .member-sidebar nav {
    display: flex;
    overflow-x: auto;
    gap: 6px;
    padding-bottom: 5px;
  }
  .member-sidebar nav a {
    flex-shrink: 0;
    padding: 10px 12px;
    background: #eaf0e4;
  }
  .member-sidebar nav a span {
    display: none;
  }
  .member-main {
    padding-top: 20px;
  }
  .member-feature-grid {
    grid-template-columns: 1fr;
  }
  .member-stats {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .hero-caption {
    display: none;
  }
  .member-hero {
    padding: 30px;
  }
  .catalogue-search {
    width: 220px;
  }
}
@media (max-width: 500px) {
  .member-main {
    padding: 18px 14px 30px;
  }
  .member-sidebar {
    padding: 15px 14px 0;
  }
  .member-topline h1 {
    font-size: 23px;
  }
  .member-topline .button {
    padding: 9px 12px;
  }
  .member-hero {
    padding: 27px 22px;
    min-height: 290px;
    background-position: 60% center;
  }
  .hero-actions {
    gap: 16px;
  }
  .member-hero h2 {
    font-size: 32px;
  }
  .panel-heading {
    padding: 20px 18px;
    flex-wrap: wrap;
    gap: 12px;
  }
  .catalogue-search {
    width: 100%;
  }
  .member-catalogue {
    grid-template-columns: 1fr;
    padding: 0 18px 20px;
  }
  .member-stat strong {
    font-size: 25px;
  }
  .member-profile {
    font-size: 9px;
    line-height: 1.8;
  }
  .member-info-strip {
    padding: 12px 18px;
  }
  .security-panel .account-form {
    padding: 0 18px 20px;
  }
}
@media (prefers-reduced-motion: no-preference) {
  html {
    scroll-behavior: smooth;
  }
}

/* More comfortable reading, clear section states, and collection controls. */
.member-main {
  padding-top: 34px;
}
.member-topline {
  margin-bottom: 27px;
}
.member-sidebar nav a.selected {
  background: #e1ebd9;
  color: #2d5a37;
  box-shadow: inset 3px 0 #77995f;
}
.member-sidebar nav a.selected span {
  color: #456d36;
}
.member-hero {
  box-shadow: 0 14px 30px #203f2410;
}
.member-hero h2 {
  max-width: 540px;
}
.member-profile {
  font-size: 11px;
  margin-bottom: 25px;
}
.member-stat {
  box-shadow: 0 4px 15px #2a4a2204;
  padding: 22px;
}
.member-stat > span {
  font-size: 11px;
  line-height: 1.6;
}
.member-stat small {
  font-size: 11px;
}
.member-stat strong {
  margin: 12px 0 8px;
}
.member-panel {
  box-shadow: 0 4px 16px #36532b04;
}
.panel-heading {
  padding-top: 26px;
  padding-bottom: 22px;
}
.panel-heading h2 {
  font-size: 21px;
}
.section-description {
  font-size: 12px;
  color: #718066;
}
.next-visit-item {
  padding: 15px 0;
}
.next-visit-item strong {
  font-size: 13px;
}
.next-visit-item small {
  font-size: 11px;
}
.next-visit-item a {
  font-size: 11px;
}
.member-filter {
  display: grid;
  gap: 6px;
  font-size: 10px;
  color: #79896e;
}
.member-filter select {
  min-height: 37px;
  font-size: 11px;
  background: #f8faf4;
  min-width: 155px;
}
.catalogue-tools {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  align-items: center;
  margin: 0 25px 22px;
  padding: 14px 17px;
  border-radius: 10px;
  background: #f3f7ed;
}
.catalogue-tools p {
  margin: 0;
  font-size: 11px;
  color: #728365;
}
.catalogue-tools .member-filter {
  display: flex;
  align-items: center;
  gap: 10px;
}
.book-card {
  padding: 21px;
  background: #fdfefb;
  transition:
    border-color 0.15s,
    box-shadow 0.15s;
}
.book-card:hover {
  border-color: #afc09c;
  box-shadow: 0 7px 20px #35512a0a;
}
.book-card h3 {
  font-size: 13px;
  line-height: 1.6;
}
.book-card p {
  font-size: 11px;
}
.book-card-category {
  font-size: 9px;
}
.book-card-stock {
  font-size: 10px;
  margin-bottom: 17px;
}
.book-spine {
  height: 69px;
  width: 48px;
}
.book-card .button {
  min-height: 38px;
}
.member-main th {
  font-size: 10px;
}
.member-main td {
  font-size: 12px;
  padding-top: 20px;
  padding-bottom: 20px;
}
.member-main .pill {
  font-size: 9px;
}
.member-info-strip {
  font-size: 11px;
}
.member-main .empty-state {
  gap: 9px;
  align-content: center;
}
.member-main .empty-state span {
  margin-top: 0;
}
.member-main input:focus-visible,
.member-main select:focus-visible {
  border-color: #70964f;
  box-shadow: 0 0 0 3px #9abc7926;
}
@media (max-width: 800px) {
  .member-sidebar nav {
    scrollbar-width: thin;
  }
  .member-sidebar nav a {
    min-height: 40px;
  }
  .member-sidebar nav a.selected {
    box-shadow: inset 0 -2px #77995f;
  }
  .member-main {
    padding-top: 22px;
  }
  .member-stat {
    padding: 19px;
  }
}
@media (max-width: 500px) {
  .member-stat {
    padding: 17px 14px;
  }
  .member-stat > span,
  .member-stat small {
    font-size: 10px;
  }
  .member-profile {
    font-size: 10px;
  }
  .catalogue-tools {
    flex-direction: column;
    align-items: stretch;
    margin: 0 18px 20px;
    gap: 12px;
  }
  .catalogue-tools .member-filter {
    justify-content: space-between;
  }
  .member-filter select {
    min-width: 140px;
  }
  .panel-heading h2 {
    font-size: 20px;
  }
  .next-visit-item {
    gap: 10px;
  }
  .next-visit-item strong {
    font-size: 12px;
  }
  .next-visit-item small {
    font-size: 10px;
  }
  .next-visit-item a {
    font-size: 10px;
  }
  .member-topline {
    margin-bottom: 23px;
  }
}
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>.member-alert-panel {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 2 | <code>  margin-bottom: 24px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 3 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 4 | <code>.member-alert-list {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 5 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 6 | <code>  gap: 12px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 7 | <code>  padding: 0 20px 20px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 8 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 9 | <code>.member-reminder {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 10 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 11 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 12 | <code>  gap: 14px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 13 | <code>  border: 1px solid #dce6ef;</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 14 | <code>  border-radius: 14px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 15 | <code>  padding: 16px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 16 | <code>  background: #f2f7fc;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 17 | <code>  color: #254962;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 18 | <code>  text-decoration: none;</code> | CSS properties: text-decoration; enclosing selector-এর presentation নির্ধারণ করে। |
| 19 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 20 | <code>.member-reminder.fine {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 21 | <code>  border-color: #ecdbbd;</code> | CSS properties: border-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 22 | <code>  background: #fff8ed;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 23 | <code>  color: #76511a;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 24 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 25 | <code>.member-reminder.clear {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 26 | <code>  background: #f2f7f1;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 27 | <code>  color: #375b3b;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 28 | <code>  border-color: #dfe8da;</code> | CSS properties: border-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 29 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 30 | <code>.member-reminder div {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 31 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 32 | <code>  gap: 5px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 33 | <code>  min-width: 0;</code> | CSS properties: min-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 34 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 35 | <code>.member-reminder strong {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 36 | <code>  font-size: 14px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 37 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 38 | <code>.member-reminder span:not(.visit-mark),</code> | CSS properties: span; enclosing selector-এর presentation নির্ধারণ করে। |
| 39 | <code>.member-reminder small {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 40 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 41 | <code>  line-height: 1.6;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 42 | <code>  overflow-wrap: anywhere;</code> | CSS properties: overflow-wrap; enclosing selector-এর presentation নির্ধারণ করে। |
| 43 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 44 | <code>.member-reminder &gt; b {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 45 | <code>  margin-left: auto;</code> | CSS properties: margin-left; enclosing selector-এর presentation নির্ধারণ করে। |
| 46 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 47 | <code>.member-reminder:focus-visible {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 48 | <code>  outline: 3px solid #85b69a;</code> | CSS properties: outline; enclosing selector-এর presentation নির্ধারণ করে। |
| 49 | <code>  outline-offset: 2px;</code> | CSS properties: outline-offset; enclosing selector-এর presentation নির্ধারণ করে। |
| 50 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 51 | <code>body[data-page=&quot;student&quot;] {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 52 | <code>  background: #f5f6f2;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 53 | <code>  font-family: &quot;Segoe UI&quot;, Arial, sans-serif;</code> | CSS properties: font-family; enclosing selector-এর presentation নির্ধারণ করে। |
| 54 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 55 | <code>body[data-page=&quot;student&quot;] .main-nav {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 56 | <code>  display: none;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 57 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 58 | <code>.member-layout {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 59 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 60 | <code>  grid-template-columns: 220px minmax(0, 1fr);</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 61 | <code>  width: min(1500px, 100%);</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 62 | <code>  margin: 0 auto;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 63 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 64 | <code>.member-sidebar {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 65 | <code>  padding: 35px 22px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 66 | <code>  border-right: 1px solid #e2e6de;</code> | CSS properties: border-right; enclosing selector-এর presentation নির্ধারণ করে। |
| 67 | <code>  align-self: start;</code> | CSS properties: align-self; enclosing selector-এর presentation নির্ধারণ করে। |
| 68 | <code>  position: sticky;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 69 | <code>  top: 0;</code> | CSS properties: top; enclosing selector-এর presentation নির্ধারণ করে। |
| 70 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 71 | <code>.portal-title {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 72 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 73 | <code>  gap: 12px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 74 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 75 | <code>  color: #153f31;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 76 | <code>  text-decoration: none;</code> | CSS properties: text-decoration; enclosing selector-এর presentation নির্ধারণ করে। |
| 77 | <code>  font-size: 20px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 78 | <code>  font-weight: 750;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 79 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 80 | <code>.portal-title small {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 81 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 82 | <code>  font-size: 9px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 83 | <code>  letter-spacing: 1.8px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 84 | <code>  margin-top: 3px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 85 | <code>  font-weight: 600;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 86 | <code>  color: #788477;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 87 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 88 | <code>.portal-symbol {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 89 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 90 | <code>  place-items: center;</code> | CSS properties: place-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 91 | <code>  width: 40px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 92 | <code>  height: 44px;</code> | CSS properties: height; enclosing selector-এর presentation নির্ধারণ করে। |
| 93 | <code>  border-radius: 11px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 94 | <code>  background: #184b39;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 95 | <code>  color: #fff;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 96 | <code>  font-family: Georgia, serif;</code> | CSS properties: font-family; enclosing selector-এর presentation নির্ধারণ করে। |
| 97 | <code>  font-size: 29px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 98 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 99 | <code>.sidebar-label {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 100 | <code>  margin: 38px 0 16px;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 101 | <code>  font-size: 9px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 102 | <code>  color: #889184;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 103 | <code>  letter-spacing: 1.7px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 104 | <code>  font-weight: 700;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 105 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 106 | <code>.member-sidebar nav {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 107 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 108 | <code>  gap: 6px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 109 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 110 | <code>.member-sidebar nav a {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 111 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 112 | <code>  gap: 13px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 113 | <code>  padding: 13px 10px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 114 | <code>  border-radius: 8px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 115 | <code>  text-decoration: none;</code> | CSS properties: text-decoration; enclosing selector-এর presentation নির্ধারণ করে। |
| 116 | <code>  color: #5d695f;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 117 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 118 | <code>  font-weight: 600;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 119 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 120 | <code>.member-sidebar nav a span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 121 | <code>  color: #8a9c8c;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 122 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 123 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 124 | <code>.member-sidebar nav a:hover,</code> | CSS properties: a; enclosing selector-এর presentation নির্ধারণ করে। |
| 125 | <code>.member-sidebar nav a:focus-visible {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 126 | <code>  background: #e6eee5;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 127 | <code>  color: #154630;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 128 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 129 | <code>.sidebar-guide {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 130 | <code>  border: 1px solid #dce4d8;</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 131 | <code>  border-radius: 13px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 132 | <code>  padding: 18px 15px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 133 | <code>  background: #edf1e7;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 134 | <code>  margin-top: 40px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 135 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 136 | <code>.sidebar-guide strong {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 137 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 138 | <code>  margin-top: 12px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 139 | <code>  color: #294832;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 140 | <code>  font-family: Georgia, serif;</code> | CSS properties: font-family; enclosing selector-এর presentation নির্ধারণ করে। |
| 141 | <code>  font-size: 19px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 142 | <code>  font-weight: 500;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 143 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 144 | <code>.sidebar-guide p {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 145 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 146 | <code>  line-height: 1.8;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 147 | <code>  color: #6b7668;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 148 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 149 | <code>.sidebar-guide a {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 150 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 151 | <code>  font-weight: 700;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 152 | <code>  color: #2c603d;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 153 | <code>  text-decoration: none;</code> | CSS properties: text-decoration; enclosing selector-এর presentation নির্ধারণ করে। |
| 154 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 155 | <code>.member-main {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 156 | <code>  min-width: 0;</code> | CSS properties: min-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 157 | <code>  padding: 30px 34px 48px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 158 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 159 | <code>.member-topline {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 160 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 161 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 162 | <code>  justify-content: space-between;</code> | CSS properties: justify-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 163 | <code>  gap: 16px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 164 | <code>  margin-bottom: 25px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 165 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 166 | <code>.member-topline .eyebrow {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 167 | <code>  font-size: 9px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 168 | <code>  letter-spacing: 2px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 169 | <code>  margin-bottom: 6px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 170 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 171 | <code>.member-topline h1 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 172 | <code>  font-size: 27px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 173 | <code>  margin: 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 174 | <code>  font-weight: 650;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 175 | <code>  color: #243c2b;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 176 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 177 | <code>.member-topline .button {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 178 | <code>  background: #fff;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 179 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 180 | <code>  border-radius: 8px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 181 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 182 | <code>.member-hero {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 183 | <code>  position: relative;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 184 | <code>  overflow: hidden;</code> | CSS properties: overflow; enclosing selector-এর presentation নির্ধারণ করে। |
| 185 | <code>  border-radius: 18px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 186 | <code>  background:</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 187 | <code>    linear-gradient(</code> | Style rule/block-এর closing বা continuation। |
| 188 | <code>      90deg,</code> | Style rule/block-এর closing বা continuation। |
| 189 | <code>      rgba(10, 41, 29, 0.97),</code> | Style rule/block-এর closing বা continuation। |
| 190 | <code>      rgba(10, 41, 29, 0.83) 40%,</code> | Style rule/block-এর closing বা continuation। |
| 191 | <code>      rgba(10, 41, 29, 0.08) 78%</code> | Style rule/block-এর closing বা continuation। |
| 192 | <code>    ),</code> | Style rule/block-এর closing বা continuation। |
| 193 | <code>    url(&quot;/static/assets/member-library-hero.webp&quot;) center/cover;</code> | Style rule/block-এর closing বা continuation। |
| 194 | <code>  min-height: 285px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 195 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 196 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 197 | <code>  color: #fff;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 198 | <code>  padding: 35px 38px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 199 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 200 | <code>.hero-copy {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 201 | <code>  max-width: 520px;</code> | CSS properties: max-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 202 | <code>  position: relative;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 203 | <code>  z-index: 1;</code> | CSS properties: z-index; enclosing selector-এর presentation নির্ধারণ করে। |
| 204 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 205 | <code>.hero-kicker {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 206 | <code>  font-size: 9px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 207 | <code>  letter-spacing: 2px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 208 | <code>  color: #cdddbc;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 209 | <code>  font-weight: 650;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 210 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 211 | <code>.member-hero h2 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 212 | <code>  font:</code> | CSS properties: font; enclosing selector-এর presentation নির্ধারণ করে। |
| 213 | <code>    500 clamp(29px, 3vw, 42px)/1.18 Georgia,</code> | Style rule/block-এর closing বা continuation। |
| 214 | <code>    serif;</code> | Style rule/block-এর closing বা continuation। |
| 215 | <code>  margin: 17px 0 13px;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 216 | <code>  letter-spacing: -0.6px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 217 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 218 | <code>.member-hero p {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 219 | <code>  max-width: 365px;</code> | CSS properties: max-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 220 | <code>  color: #d3dfd3;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 221 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 222 | <code>  line-height: 1.8;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 223 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 224 | <code>.hero-actions {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 225 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 226 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 227 | <code>  gap: 22px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 228 | <code>  margin-top: 23px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 229 | <code>  flex-wrap: wrap;</code> | CSS properties: flex-wrap; enclosing selector-এর presentation নির্ধারণ করে। |
| 230 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 231 | <code>.hero-actions .button {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 232 | <code>  background: #e9edda;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 233 | <code>  color: #183f2a;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 234 | <code>  border: 0;</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 235 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 236 | <code>  border-radius: 8px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 237 | <code>  padding: 12px 17px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 238 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 239 | <code>.hero-actions &gt; a:not(.button) {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 240 | <code>  color: #e2eadb;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 241 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 242 | <code>  text-underline-offset: 5px;</code> | CSS properties: text-underline-offset; enclosing selector-এর presentation নির্ধারণ করে। |
| 243 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 244 | <code>.hero-caption {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 245 | <code>  position: absolute;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 246 | <code>  bottom: 23px;</code> | CSS properties: bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 247 | <code>  right: 26px;</code> | CSS properties: right; enclosing selector-এর presentation নির্ধারণ করে। |
| 248 | <code>  font:</code> | CSS properties: font; enclosing selector-এর presentation নির্ধারণ করে। |
| 249 | <code>    italic 18px Georgia,</code> | Style rule/block-এর closing বা continuation। |
| 250 | <code>    serif;</code> | Style rule/block-এর closing বা continuation। |
| 251 | <code>  color: #faf5e6;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 252 | <code>  text-shadow: 0 2px 8px #000;</code> | CSS properties: text-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 253 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 254 | <code>.member-profile {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 255 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 256 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 257 | <code>  gap: 9px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 258 | <code>  margin: 17px 2px 22px;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 259 | <code>  color: #72806e;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 260 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 261 | <code>  flex-wrap: wrap;</code> | CSS properties: flex-wrap; enclosing selector-এর presentation নির্ধারণ করে। |
| 262 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 263 | <code>.member-profile p {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 264 | <code>  margin: 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 265 | <code>  overflow-wrap: anywhere;</code> | CSS properties: overflow-wrap; enclosing selector-এর presentation নির্ধারণ করে। |
| 266 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 267 | <code>.profile-dot {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 268 | <code>  width: 7px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 269 | <code>  height: 7px;</code> | CSS properties: height; enclosing selector-এর presentation নির্ধারণ করে। |
| 270 | <code>  border-radius: 50%;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 271 | <code>  background: #648f58;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 272 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 273 | <code>.profile-note {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 274 | <code>  margin-left: auto;</code> | CSS properties: margin-left; enclosing selector-এর presentation নির্ধারণ করে। |
| 275 | <code>  color: #84917d;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 276 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 277 | <code>.member-stats {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 278 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 279 | <code>  grid-template-columns: repeat(4, minmax(0, 1fr));</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 280 | <code>  gap: 14px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 281 | <code>  margin-bottom: 23px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 282 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 283 | <code>.member-stat {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 284 | <code>  background: #fff;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 285 | <code>  padding: 20px 22px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 286 | <code>  border: 1px solid #e1e6dc;</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 287 | <code>  border-radius: 12px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 288 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 289 | <code>.member-stat &gt; span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 290 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 291 | <code>  color: #75806f;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 292 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 293 | <code>.member-stat strong {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 294 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 295 | <code>  margin: 10px 0 7px;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 296 | <code>  font-size: 29px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 297 | <code>  font-weight: 650;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 298 | <code>  letter-spacing: -0.6px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 299 | <code>  color: #224630;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 300 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 301 | <code>.member-stat small {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 302 | <code>  color: #8a9583;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 303 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 304 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 305 | <code>.member-stat:nth-child(2) strong {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 306 | <code>  color: #9b7438;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 307 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 308 | <code>.member-stat:nth-child(3) strong {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 309 | <code>  color: #9b5b4c;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 310 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 311 | <code>.member-panel {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 312 | <code>  background: #fff;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 313 | <code>  border: 1px solid #e0e6dc;</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 314 | <code>  border-radius: 14px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 315 | <code>  overflow: hidden;</code> | CSS properties: overflow; enclosing selector-এর presentation নির্ধারণ করে। |
| 316 | <code>  margin-bottom: 24px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 317 | <code>  scroll-margin-top: 20px;</code> | CSS properties: scroll-margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 318 | <code>  min-width: 0;</code> | CSS properties: min-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 319 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 320 | <code>.panel-heading {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 321 | <code>  padding: 23px 25px 19px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 322 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 323 | <code>  justify-content: space-between;</code> | CSS properties: justify-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 324 | <code>  align-items: flex-start;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 325 | <code>  gap: 18px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 326 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 327 | <code>.member-main .section-label {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 328 | <code>  font-size: 8px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 329 | <code>  letter-spacing: 1.8px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 330 | <code>  color: #75886c;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 331 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 332 | <code>.panel-heading h2 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 333 | <code>  font-size: 19px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 334 | <code>  font-weight: 650;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 335 | <code>  color: #2e4832;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 336 | <code>  margin: 7px 0 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 337 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 338 | <code>.section-description {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 339 | <code>  color: #7b8575;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 340 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 341 | <code>  line-height: 1.8;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 342 | <code>  margin: 8px 0 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 343 | <code>  max-width: 520px;</code> | CSS properties: max-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 344 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 345 | <code>.small-tag {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 346 | <code>  border: 1px solid #e4e9df;</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 347 | <code>  border-radius: 20px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 348 | <code>  padding: 5px 10px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 349 | <code>  font-size: 9px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 350 | <code>  color: #78866e;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 351 | <code>  white-space: nowrap;</code> | CSS properties: white-space; enclosing selector-এর presentation নির্ধারণ করে। |
| 352 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 353 | <code>.member-feature-grid {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 354 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 355 | <code>  grid-template-columns: 1.15fr 1fr;</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 356 | <code>  gap: 22px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 357 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 358 | <code>.next-step {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 359 | <code>  min-height: 220px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 360 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 361 | <code>#memberNextStep {</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 362 | <code>  padding: 0 25px 22px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 363 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 364 | <code>.next-visit-item {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 365 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 366 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 367 | <code>  gap: 13px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 368 | <code>  padding: 12px 0;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 369 | <code>  border-top: 1px solid #edf0e9;</code> | CSS properties: border-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 370 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 371 | <code>.visit-mark {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 372 | <code>  width: 34px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 373 | <code>  height: 36px;</code> | CSS properties: height; enclosing selector-এর presentation নির্ধারণ করে। |
| 374 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 375 | <code>  place-items: center;</code> | CSS properties: place-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 376 | <code>  border-radius: 8px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 377 | <code>  background: #eff3e9;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 378 | <code>  color: #5f7d4b;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 379 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 380 | <code>  font-weight: 700;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 381 | <code>  flex-shrink: 0;</code> | CSS properties: flex-shrink; enclosing selector-এর presentation নির্ধারণ করে। |
| 382 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 383 | <code>.next-visit-item strong {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 384 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 385 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 386 | <code>  color: #364b33;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 387 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 388 | <code>.next-visit-item small {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 389 | <code>  color: #87917e;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 390 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 391 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 392 | <code>  margin-top: 4px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 393 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 394 | <code>.next-visit-item a {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 395 | <code>  margin-left: auto;</code> | CSS properties: margin-left; enclosing selector-এর presentation নির্ধারণ করে। |
| 396 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 397 | <code>  color: #537944;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 398 | <code>  white-space: nowrap;</code> | CSS properties: white-space; enclosing selector-এর presentation নির্ধারণ করে। |
| 399 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 400 | <code>.discovery-card {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 401 | <code>  position: relative;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 402 | <code>  min-height: 220px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 403 | <code>  border-radius: 14px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 404 | <code>  overflow: hidden;</code> | CSS properties: overflow; enclosing selector-এর presentation নির্ধারণ করে। |
| 405 | <code>  margin-bottom: 24px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 406 | <code>  background: #244331;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 407 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 408 | <code>.discovery-card img {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 409 | <code>  position: absolute;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 410 | <code>  width: 100%;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 411 | <code>  height: 100%;</code> | CSS properties: height; enclosing selector-এর presentation নির্ধারণ করে। |
| 412 | <code>  object-fit: cover;</code> | CSS properties: object-fit; enclosing selector-এর presentation নির্ধারণ করে। |
| 413 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 414 | <code>.discovery-card::after {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 415 | <code>  content: &quot;&quot;;</code> | CSS properties: content; enclosing selector-এর presentation নির্ধারণ করে। |
| 416 | <code>  position: absolute;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 417 | <code>  inset: 0;</code> | CSS properties: inset; enclosing selector-এর presentation নির্ধারণ করে। |
| 418 | <code>  background: linear-gradient(90deg, rgba(15, 39, 24, 0.86), rgba(15, 39, 24, 0.1));</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 419 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 420 | <code>.discovery-card &gt; div {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 421 | <code>  position: relative;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 422 | <code>  z-index: 1;</code> | CSS properties: z-index; enclosing selector-এর presentation নির্ধারণ করে। |
| 423 | <code>  padding: 26px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 424 | <code>  color: #fff;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 425 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 426 | <code>.discovery-card .section-label {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 427 | <code>  color: #e0e9d0;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 428 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 429 | <code>.discovery-card h2 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 430 | <code>  font:</code> | CSS properties: font; enclosing selector-এর presentation নির্ধারণ করে। |
| 431 | <code>    500 26px/1.3 Georgia,</code> | Style rule/block-এর closing বা continuation। |
| 432 | <code>    serif;</code> | Style rule/block-এর closing বা continuation। |
| 433 | <code>  margin: 13px 0 19px;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 434 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 435 | <code>.discovery-card a {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 436 | <code>  color: #edf2dc;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 437 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 438 | <code>  text-decoration: none;</code> | CSS properties: text-decoration; enclosing selector-এর presentation নির্ধারণ করে। |
| 439 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 440 | <code>.member-info-strip {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 441 | <code>  background: #f4f7ef;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 442 | <code>  color: #75826c;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 443 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 444 | <code>  padding: 12px 25px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 445 | <code>  border-top: 1px solid #ebefe5;</code> | CSS properties: border-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 446 | <code>  border-bottom: 1px solid #ebefe5;</code> | CSS properties: border-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 447 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 448 | <code>.member-main table {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 449 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 450 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 451 | <code>.member-main th {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 452 | <code>  background: #f7f9f4;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 453 | <code>  color: #85907c;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 454 | <code>  font-size: 9px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 455 | <code>  padding: 14px 20px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 456 | <code>  text-transform: uppercase;</code> | CSS properties: text-transform; enclosing selector-এর presentation নির্ধারণ করে। |
| 457 | <code>  letter-spacing: 0.5px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 458 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 459 | <code>.member-main td {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 460 | <code>  padding: 17px 20px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 461 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 462 | <code>.member-main .pill {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 463 | <code>  font-size: 9px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 464 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 465 | <code>.member-main .button.small {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 466 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 467 | <code>  border-radius: 6px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 468 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 469 | <code>.member-main .empty-state {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 470 | <code>  padding: 30px 20px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 471 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 472 | <code>.member-main .empty-state strong {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 473 | <code>  color: #55704b;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 474 | <code>  font-size: 13px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 475 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 476 | <code>.member-main .empty-state span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 477 | <code>  color: #89927e;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 478 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 479 | <code>  margin-top: 7px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 480 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 481 | <code>.catalogue-search {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 482 | <code>  color: #85907b;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 483 | <code>  font-size: 9px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 484 | <code>  width: 270px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 485 | <code>  flex-shrink: 0;</code> | CSS properties: flex-shrink; enclosing selector-এর presentation নির্ধারণ করে। |
| 486 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 487 | <code>.catalogue-search input {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 488 | <code>  width: 100%;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 489 | <code>  margin-top: 7px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 490 | <code>  border-radius: 8px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 491 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 492 | <code>  padding: 11px 12px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 493 | <code>  background: #f8faf5;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 494 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 495 | <code>.member-catalogue {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 496 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 497 | <code>  grid-template-columns: repeat(3, minmax(0, 1fr));</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 498 | <code>  gap: 16px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 499 | <code>  padding: 4px 25px 25px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 500 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 501 | <code>.book-card {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 502 | <code>  border: 1px solid #e4e9de;</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 503 | <code>  border-radius: 11px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 504 | <code>  padding: 17px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 505 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 506 | <code>  flex-direction: column;</code> | CSS properties: flex-direction; enclosing selector-এর presentation নির্ধারণ করে। |
| 507 | <code>  min-width: 0;</code> | CSS properties: min-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 508 | <code>  background: #fcfdf9;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 509 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 510 | <code>.book-card-top {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 511 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 512 | <code>  gap: 13px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 513 | <code>  align-items: flex-start;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 514 | <code>  margin-bottom: 16px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 515 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 516 | <code>.book-spine {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 517 | <code>  background: #39644b;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 518 | <code>  color: #e4ecd3;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 519 | <code>  width: 44px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 520 | <code>  height: 61px;</code> | CSS properties: height; enclosing selector-এর presentation নির্ধারণ করে। |
| 521 | <code>  border-left: 5px solid #214c34;</code> | CSS properties: border-left; enclosing selector-এর presentation নির্ধারণ করে। |
| 522 | <code>  border-radius: 2px 5px 5px 2px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 523 | <code>  flex-shrink: 0;</code> | CSS properties: flex-shrink; enclosing selector-এর presentation নির্ধারণ করে। |
| 524 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 525 | <code>  place-items: center;</code> | CSS properties: place-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 526 | <code>  font:</code> | CSS properties: font; enclosing selector-এর presentation নির্ধারণ করে। |
| 527 | <code>    21px Georgia,</code> | Style rule/block-এর closing বা continuation। |
| 528 | <code>    serif;</code> | Style rule/block-এর closing বা continuation। |
| 529 | <code>  box-shadow: 3px 3px 0 #e7eadf;</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 530 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 531 | <code>.book-card:nth-child(3n + 2) .book-spine {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 532 | <code>  background: #b08956;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 533 | <code>  border-color: #8c6a3e;</code> | CSS properties: border-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 534 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 535 | <code>.book-card:nth-child(3n) .book-spine {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 536 | <code>  background: #68848a;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 537 | <code>  border-color: #4f6b72;</code> | CSS properties: border-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 538 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 539 | <code>.book-card h3 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 540 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 541 | <code>  color: #354b32;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 542 | <code>  margin: 2px 0 5px;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 543 | <code>  line-height: 1.6;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 544 | <code>  overflow-wrap: anywhere;</code> | CSS properties: overflow-wrap; enclosing selector-এর presentation নির্ধারণ করে। |
| 545 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 546 | <code>.book-card p {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 547 | <code>  margin: 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 548 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 549 | <code>  color: #8a947e;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 550 | <code>  line-height: 1.7;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 551 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 552 | <code>.book-card-category {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 553 | <code>  color: #788c6b;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 554 | <code>  font-size: 8px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 555 | <code>  letter-spacing: 0.5px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 556 | <code>  text-transform: uppercase;</code> | CSS properties: text-transform; enclosing selector-এর presentation নির্ধারণ করে। |
| 557 | <code>  margin-bottom: 10px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 558 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 559 | <code>.book-card-stock {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 560 | <code>  margin-top: auto;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 561 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 562 | <code>  justify-content: space-between;</code> | CSS properties: justify-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 563 | <code>  font-size: 9px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 564 | <code>  color: #859079;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 565 | <code>  margin-bottom: 13px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 566 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 567 | <code>.book-card-stock b {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 568 | <code>  color: #567644;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 569 | <code>  font-weight: 600;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 570 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 571 | <code>.book-card .button {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 572 | <code>  width: 100%;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 573 | <code>  margin-top: auto;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 574 | <code>  min-height: 34px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 575 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 576 | <code>.book-card .button:disabled {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 577 | <code>  background: #edf0e8;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 578 | <code>  border-color: #e3e7dc;</code> | CSS properties: border-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 579 | <code>  color: #909a82;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 580 | <code>  cursor: default;</code> | CSS properties: cursor; enclosing selector-এর presentation নির্ধারণ করে। |
| 581 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 582 | <code>.member-catalogue &gt; .empty-state {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 583 | <code>  grid-column: 1/-1;</code> | CSS properties: grid-column; enclosing selector-এর presentation নির্ধারণ করে। |
| 584 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 585 | <code>.member-bottom-grid {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 586 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 587 | <code>  grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr);</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 588 | <code>  gap: 22px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 589 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 590 | <code>.security-panel .account-form {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 591 | <code>  padding: 0 25px 25px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 592 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 593 | <code>.security-panel label {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 594 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 595 | <code>  color: #76836e;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 596 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 597 | <code>.security-panel input {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 598 | <code>  border-radius: 7px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 599 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 600 | <code>  background: #fbfcf8;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 601 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 602 | <code>.security-panel .button {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 603 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 604 | <code>  border-radius: 7px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 605 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 606 | <code>.member-main a:focus-visible {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 607 | <code>  outline: 3px solid #92b879;</code> | CSS properties: outline; enclosing selector-এর presentation নির্ধারণ করে। |
| 608 | <code>  outline-offset: 4px;</code> | CSS properties: outline-offset; enclosing selector-এর presentation নির্ধারণ করে। |
| 609 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 610 | <code>@media (max-width: 1150px) {</code> | Viewport condition অনুযায়ী responsive styles apply করে। |
| 611 | <code>  .member-layout {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 612 | <code>    grid-template-columns: 180px minmax(0, 1fr);</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 613 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 614 | <code>  .member-sidebar {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 615 | <code>    padding: 30px 14px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 616 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 617 | <code>  .member-main {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 618 | <code>    padding: 25px 22px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 619 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 620 | <code>  .member-stats {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 621 | <code>    gap: 10px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 622 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 623 | <code>  .member-stat {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 624 | <code>    padding: 17px 15px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 625 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 626 | <code>  .member-catalogue {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 627 | <code>    grid-template-columns: repeat(2, minmax(0, 1fr));</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 628 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 629 | <code>  .member-bottom-grid {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 630 | <code>    grid-template-columns: 1fr;</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 631 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 632 | <code>  .profile-note {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 633 | <code>    display: none;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 634 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 635 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 636 | <code>@media (max-width: 800px) {</code> | Viewport condition অনুযায়ী responsive styles apply করে। |
| 637 | <code>  .member-layout {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 638 | <code>    display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 639 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 640 | <code>  .member-sidebar {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 641 | <code>    position: static;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 642 | <code>    padding: 16px 22px 0;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 643 | <code>    border: 0;</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 644 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 645 | <code>  .portal-title,</code> | Style rule/block-এর closing বা continuation। |
| 646 | <code>  .sidebar-label,</code> | Style rule/block-এর closing বা continuation। |
| 647 | <code>  .sidebar-guide {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 648 | <code>    display: none;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 649 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 650 | <code>  .member-sidebar nav {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 651 | <code>    display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 652 | <code>    overflow-x: auto;</code> | CSS properties: overflow-x; enclosing selector-এর presentation নির্ধারণ করে। |
| 653 | <code>    gap: 6px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 654 | <code>    padding-bottom: 5px;</code> | CSS properties: padding-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 655 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 656 | <code>  .member-sidebar nav a {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 657 | <code>    flex-shrink: 0;</code> | CSS properties: flex-shrink; enclosing selector-এর presentation নির্ধারণ করে। |
| 658 | <code>    padding: 10px 12px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 659 | <code>    background: #eaf0e4;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 660 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 661 | <code>  .member-sidebar nav a span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 662 | <code>    display: none;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 663 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 664 | <code>  .member-main {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 665 | <code>    padding-top: 20px;</code> | CSS properties: padding-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 666 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 667 | <code>  .member-feature-grid {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 668 | <code>    grid-template-columns: 1fr;</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 669 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 670 | <code>  .member-stats {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 671 | <code>    grid-template-columns: repeat(2, minmax(0, 1fr));</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 672 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 673 | <code>  .hero-caption {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 674 | <code>    display: none;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 675 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 676 | <code>  .member-hero {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 677 | <code>    padding: 30px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 678 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 679 | <code>  .catalogue-search {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 680 | <code>    width: 220px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 681 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 682 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 683 | <code>@media (max-width: 500px) {</code> | Viewport condition অনুযায়ী responsive styles apply করে। |
| 684 | <code>  .member-main {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 685 | <code>    padding: 18px 14px 30px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 686 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 687 | <code>  .member-sidebar {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 688 | <code>    padding: 15px 14px 0;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 689 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 690 | <code>  .member-topline h1 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 691 | <code>    font-size: 23px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 692 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 693 | <code>  .member-topline .button {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 694 | <code>    padding: 9px 12px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 695 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 696 | <code>  .member-hero {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 697 | <code>    padding: 27px 22px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 698 | <code>    min-height: 290px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 699 | <code>    background-position: 60% center;</code> | CSS properties: background-position; enclosing selector-এর presentation নির্ধারণ করে। |
| 700 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 701 | <code>  .hero-actions {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 702 | <code>    gap: 16px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 703 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 704 | <code>  .member-hero h2 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 705 | <code>    font-size: 32px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 706 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 707 | <code>  .panel-heading {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 708 | <code>    padding: 20px 18px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 709 | <code>    flex-wrap: wrap;</code> | CSS properties: flex-wrap; enclosing selector-এর presentation নির্ধারণ করে। |
| 710 | <code>    gap: 12px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 711 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 712 | <code>  .catalogue-search {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 713 | <code>    width: 100%;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 714 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 715 | <code>  .member-catalogue {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 716 | <code>    grid-template-columns: 1fr;</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 717 | <code>    padding: 0 18px 20px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 718 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 719 | <code>  .member-stat strong {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 720 | <code>    font-size: 25px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 721 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 722 | <code>  .member-profile {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 723 | <code>    font-size: 9px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 724 | <code>    line-height: 1.8;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 725 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 726 | <code>  .member-info-strip {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 727 | <code>    padding: 12px 18px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 728 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 729 | <code>  .security-panel .account-form {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 730 | <code>    padding: 0 18px 20px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 731 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 732 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 733 | <code>@media (prefers-reduced-motion: no-preference) {</code> | Viewport condition অনুযায়ী responsive styles apply করে। |
| 734 | <code>  html {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 735 | <code>    scroll-behavior: smooth;</code> | CSS properties: scroll-behavior; enclosing selector-এর presentation নির্ধারণ করে। |
| 736 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 737 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 738 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 739 | <code>/* More comfortable reading, clear section states, and collection controls. */</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 740 | <code>.member-main {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 741 | <code>  padding-top: 34px;</code> | CSS properties: padding-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 742 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 743 | <code>.member-topline {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 744 | <code>  margin-bottom: 27px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 745 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 746 | <code>.member-sidebar nav a.selected {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 747 | <code>  background: #e1ebd9;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 748 | <code>  color: #2d5a37;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 749 | <code>  box-shadow: inset 3px 0 #77995f;</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 750 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 751 | <code>.member-sidebar nav a.selected span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 752 | <code>  color: #456d36;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 753 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 754 | <code>.member-hero {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 755 | <code>  box-shadow: 0 14px 30px #203f2410;</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 756 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 757 | <code>.member-hero h2 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 758 | <code>  max-width: 540px;</code> | CSS properties: max-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 759 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 760 | <code>.member-profile {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 761 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 762 | <code>  margin-bottom: 25px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 763 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 764 | <code>.member-stat {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 765 | <code>  box-shadow: 0 4px 15px #2a4a2204;</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 766 | <code>  padding: 22px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 767 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 768 | <code>.member-stat &gt; span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 769 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 770 | <code>  line-height: 1.6;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 771 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 772 | <code>.member-stat small {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 773 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 774 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 775 | <code>.member-stat strong {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 776 | <code>  margin: 12px 0 8px;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 777 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 778 | <code>.member-panel {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 779 | <code>  box-shadow: 0 4px 16px #36532b04;</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 780 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 781 | <code>.panel-heading {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 782 | <code>  padding-top: 26px;</code> | CSS properties: padding-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 783 | <code>  padding-bottom: 22px;</code> | CSS properties: padding-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 784 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 785 | <code>.panel-heading h2 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 786 | <code>  font-size: 21px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 787 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 788 | <code>.section-description {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 789 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 790 | <code>  color: #718066;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 791 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 792 | <code>.next-visit-item {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 793 | <code>  padding: 15px 0;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 794 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 795 | <code>.next-visit-item strong {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 796 | <code>  font-size: 13px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 797 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 798 | <code>.next-visit-item small {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 799 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 800 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 801 | <code>.next-visit-item a {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 802 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 803 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 804 | <code>.member-filter {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 805 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 806 | <code>  gap: 6px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 807 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 808 | <code>  color: #79896e;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 809 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 810 | <code>.member-filter select {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 811 | <code>  min-height: 37px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 812 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 813 | <code>  background: #f8faf4;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 814 | <code>  min-width: 155px;</code> | CSS properties: min-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 815 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 816 | <code>.catalogue-tools {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 817 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 818 | <code>  justify-content: space-between;</code> | CSS properties: justify-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 819 | <code>  gap: 18px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 820 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 821 | <code>  margin: 0 25px 22px;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 822 | <code>  padding: 14px 17px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 823 | <code>  border-radius: 10px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 824 | <code>  background: #f3f7ed;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 825 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 826 | <code>.catalogue-tools p {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 827 | <code>  margin: 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 828 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 829 | <code>  color: #728365;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 830 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 831 | <code>.catalogue-tools .member-filter {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 832 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 833 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 834 | <code>  gap: 10px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 835 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 836 | <code>.book-card {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 837 | <code>  padding: 21px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 838 | <code>  background: #fdfefb;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 839 | <code>  transition:</code> | CSS properties: transition; enclosing selector-এর presentation নির্ধারণ করে। |
| 840 | <code>    border-color 0.15s,</code> | Style rule/block-এর closing বা continuation। |
| 841 | <code>    box-shadow 0.15s;</code> | Style rule/block-এর closing বা continuation। |
| 842 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 843 | <code>.book-card:hover {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 844 | <code>  border-color: #afc09c;</code> | CSS properties: border-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 845 | <code>  box-shadow: 0 7px 20px #35512a0a;</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 846 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 847 | <code>.book-card h3 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 848 | <code>  font-size: 13px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 849 | <code>  line-height: 1.6;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 850 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 851 | <code>.book-card p {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 852 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 853 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 854 | <code>.book-card-category {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 855 | <code>  font-size: 9px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 856 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 857 | <code>.book-card-stock {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 858 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 859 | <code>  margin-bottom: 17px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 860 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 861 | <code>.book-spine {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 862 | <code>  height: 69px;</code> | CSS properties: height; enclosing selector-এর presentation নির্ধারণ করে। |
| 863 | <code>  width: 48px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 864 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 865 | <code>.book-card .button {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 866 | <code>  min-height: 38px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 867 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 868 | <code>.member-main th {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 869 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 870 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 871 | <code>.member-main td {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 872 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 873 | <code>  padding-top: 20px;</code> | CSS properties: padding-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 874 | <code>  padding-bottom: 20px;</code> | CSS properties: padding-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 875 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 876 | <code>.member-main .pill {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 877 | <code>  font-size: 9px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 878 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 879 | <code>.member-info-strip {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 880 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 881 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 882 | <code>.member-main .empty-state {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 883 | <code>  gap: 9px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 884 | <code>  align-content: center;</code> | CSS properties: align-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 885 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 886 | <code>.member-main .empty-state span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 887 | <code>  margin-top: 0;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 888 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 889 | <code>.member-main input:focus-visible,</code> | CSS properties: input; enclosing selector-এর presentation নির্ধারণ করে। |
| 890 | <code>.member-main select:focus-visible {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 891 | <code>  border-color: #70964f;</code> | CSS properties: border-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 892 | <code>  box-shadow: 0 0 0 3px #9abc7926;</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 893 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 894 | <code>@media (max-width: 800px) {</code> | Viewport condition অনুযায়ী responsive styles apply করে। |
| 895 | <code>  .member-sidebar nav {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 896 | <code>    scrollbar-width: thin;</code> | CSS properties: scrollbar-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 897 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 898 | <code>  .member-sidebar nav a {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 899 | <code>    min-height: 40px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 900 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 901 | <code>  .member-sidebar nav a.selected {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 902 | <code>    box-shadow: inset 0 -2px #77995f;</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 903 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 904 | <code>  .member-main {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 905 | <code>    padding-top: 22px;</code> | CSS properties: padding-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 906 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 907 | <code>  .member-stat {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 908 | <code>    padding: 19px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 909 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 910 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 911 | <code>@media (max-width: 500px) {</code> | Viewport condition অনুযায়ী responsive styles apply করে। |
| 912 | <code>  .member-stat {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 913 | <code>    padding: 17px 14px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 914 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 915 | <code>  .member-stat &gt; span,</code> | Style rule/block-এর closing বা continuation। |
| 916 | <code>  .member-stat small {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 917 | <code>    font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 918 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 919 | <code>  .member-profile {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 920 | <code>    font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 921 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 922 | <code>  .catalogue-tools {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 923 | <code>    flex-direction: column;</code> | CSS properties: flex-direction; enclosing selector-এর presentation নির্ধারণ করে। |
| 924 | <code>    align-items: stretch;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 925 | <code>    margin: 0 18px 20px;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 926 | <code>    gap: 12px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 927 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 928 | <code>  .catalogue-tools .member-filter {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 929 | <code>    justify-content: space-between;</code> | CSS properties: justify-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 930 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 931 | <code>  .member-filter select {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 932 | <code>    min-width: 140px;</code> | CSS properties: min-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 933 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 934 | <code>  .panel-heading h2 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 935 | <code>    font-size: 20px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 936 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 937 | <code>  .next-visit-item {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 938 | <code>    gap: 10px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 939 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 940 | <code>  .next-visit-item strong {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 941 | <code>    font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 942 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 943 | <code>  .next-visit-item small {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 944 | <code>    font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 945 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 946 | <code>  .next-visit-item a {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 947 | <code>    font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 948 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 949 | <code>  .member-topline {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 950 | <code>    margin-bottom: 23px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 951 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 952 | <code>}</code> | Style rule/block-এর closing বা continuation। |
