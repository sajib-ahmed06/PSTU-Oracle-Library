# frontend/styles.css

Management pages-এর shared design tokens, header, navigation, tables, metrics, forms, dialogs এবং responsive styles।

Source: [মূল file](../../frontend/styles.css)। Snapshot 2026-10-04; 1030 lines; SHA-256 `002d89fdef971b4f52dd4c84f4781ab0857e29bc89adc15b8dbc1f4823927dc1`।

## Function / object / element inventory

CSS selector/property rules source order-এ cascade করে। Later matching declaration আগের equivalent specificity rule override করতে পারে। Media/supports queries condition অনুযায়ী override দেয়। নিচের প্রতিটি line selector/property reading notes দেয়।

## সম্পূর্ণ original source

```css
:root {
  --ink: #17201d;
  --muted: #65706b;
  --canvas: #f4f6f5;
  --paper: #ffffff;
  --line: #dce2de;
  --green: #126348;
  --green-dark: #0b3f30;
  --green-soft: #e5f1eb;
  --blue: #356c8c;
  --blue-soft: #e6eff4;
  --gold: #a86d17;
  --gold-soft: #fbefd9;
  --red: #963c34;
  --red-soft: #f5e5e2;
  --slate: #55645e;
  --shadow: 0 12px 35px rgba(26, 43, 36, 0.08);
}

* {
  box-sizing: border-box;
}
body {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  margin: 0;
  min-width: 320px;
  background: var(--canvas);
  color: var(--ink);
  font-family: Arial, sans-serif;
  line-height: 1.45;
}
button,
input,
select {
  font: inherit;
}
a {
  color: inherit;
}

.app-header {
  min-height: 82px;
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 28px;
  padding: 14px max(28px, calc((100vw - 1440px) / 2));
  background: var(--paper);
  border-bottom: 1px solid var(--line);
}
.brand-block {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 235px;
}
.brand-mark {
  display: grid;
  place-items: center;
  width: 58px;
  height: 44px;
  flex: 0 0 58px;
  border-radius: 8px;
  background: var(--green-dark);
  color: #fff;
  box-shadow: 0 8px 20px rgba(11, 63, 48, 0.22);
  font:
    800 12px Arial,
    sans-serif;
  letter-spacing: 1.2px;
}
.brand-block strong,
.brand-block small {
  display: block;
}
.brand-block strong {
  color: var(--green-dark);
  font-size: 17px;
}
.brand-block small {
  margin-top: 2px;
  color: var(--muted);
  font-size: 10px;
}
.university-name {
  color: var(--green);
  font-size: 11px;
  font-weight: 700;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 1.1px;
}
.connection {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--muted);
  font-size: 11px;
  white-space: nowrap;
}
.connection i {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: #d39a3f;
}
.connection i.online {
  background: #49a875;
  box-shadow: 0 0 0 3px #e0f2e8;
}
.header-tools {
  display: flex;
  align-items: center;
  gap: 16px;
}
.user-menu {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-left: 15px;
  border-left: 1px solid var(--line);
}
.user-menu span {
  max-width: 145px;
  overflow: hidden;
  color: var(--green-dark);
  font-size: 10px;
  font-weight: 700;
  text-overflow: ellipsis;
  text-transform: uppercase;
  white-space: nowrap;
}
.user-menu button {
  min-height: 32px;
  padding: 6px 9px;
  border: 1px solid var(--line);
  background: #f2f5f3;
  color: var(--slate);
  font-size: 10px;
}

.main-nav {
  min-height: 52px;
  background: #17211d;
  color: #cdd7d2;
  box-shadow: 0 6px 20px rgba(18, 29, 24, 0.12);
}
.nav-inner {
  width: min(1440px, calc(100% - 56px));
  min-height: 52px;
  margin: auto;
  display: flex;
  align-items: stretch;
  overflow-x: auto;
}
.main-nav a {
  display: flex;
  align-items: center;
  min-height: 52px;
  padding: 0 22px;
  border-bottom: 3px solid transparent;
  text-decoration: none;
  font-size: 12px;
  font-weight: 700;
  white-space: nowrap;
}
.main-nav a:hover {
  background: #28352f;
  color: #fff;
}
.main-nav a.active {
  border-bottom-color: #62bc91;
  background: #293a33;
  color: #fff;
}
.admin-only {
  display: none !important;
}
.admin-only.visible {
  display: flex !important;
}
.workspace {
  width: min(1440px, calc(100% - 56px));
  flex: 1;
  margin: 0 auto;
  padding: 30px 0 54px;
}
.page-heading {
  min-height: 102px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
  margin-bottom: 24px;
  border-bottom: 1px solid var(--line);
}
.eyebrow,
.section-label {
  margin: 0 0 5px;
  color: var(--green);
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
}
h1 {
  margin: 0;
  font-size: 30px;
  line-height: 1.2;
  letter-spacing: 0;
}
h2 {
  margin: 0;
  font-size: 18px;
  letter-spacing: 0;
}
.heading-copy {
  margin: 7px 0 0;
  color: var(--muted);
  font-size: 12px;
}
.heading-actions {
  display: flex;
  align-items: center;
  gap: 14px;
}
.current-date,
.record-count {
  color: var(--muted);
  font-size: 11px;
  white-space: nowrap;
}

.button,
button {
  min-height: 40px;
  border: 0;
  border-radius: 7px;
  padding: 9px 16px;
  cursor: pointer;
  text-decoration: none;
  text-align: center;
  font-weight: 600;
  transition:
    background 0.15s ease,
    border-color 0.15s ease,
    transform 0.15s ease,
    box-shadow 0.15s ease;
}
.button:hover {
  transform: translateY(-1px);
}
.button.primary {
  background: var(--green);
  color: #fff;
}
.button.primary:hover {
  background: #0d503b;
}
.button.secondary {
  border: 1px solid #d4dcd8;
  background: #edf1ef;
  color: #25312c;
}
.button.secondary:hover {
  background: #e2e8e5;
}
.button.danger {
  background: var(--red);
  color: #fff;
}
.button.danger-quiet {
  background: var(--red-soft);
  color: var(--red);
}
.button.light {
  background: #fff;
  color: var(--green-dark);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.14);
}
.button.glass {
  border: 1px solid rgba(255, 255, 255, 0.32);
  background: rgba(13, 32, 25, 0.56);
  color: #fff;
  backdrop-filter: blur(8px);
}
.button.small {
  min-height: 32px;
  padding: 6px 10px;
  font-size: 11px;
}
.button:disabled,
button:disabled {
  cursor: wait;
  opacity: 0.55;
}
.icon-button {
  width: 34px;
  min-height: 34px;
  padding: 0;
  background: transparent;
  color: var(--muted);
  font-size: 25px;
  line-height: 1;
}

.command-strip {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 16px 18px;
  margin-bottom: 18px;
  background: var(--paper);
  border: 1px solid var(--line);
  border-left: 4px solid var(--green);
  box-shadow: var(--shadow);
}
.command-strip strong {
  display: block;
  font-size: 14px;
}
.command-actions,
.row-actions,
.heading-actions {
  display: flex;
  gap: 8px;
}

.dashboard-cover {
  position: relative;
  min-height: 270px;
  display: flex;
  align-items: stretch;
  justify-content: space-between;
  gap: 28px;
  margin-bottom: 22px;
  overflow: hidden;
  border-radius: 8px;
  background-color: #102b22;
  background-image: url("/static/assets/library-dashboard.png");
  background-position: center;
  background-size: cover;
  box-shadow: 0 22px 55px rgba(16, 43, 34, 0.2);
  color: #fff;
}
.cover-content {
  width: min(610px, 70%);
  padding: 34px 38px;
  background: rgba(7, 32, 24, 0.82);
}
.cover-label {
  margin: 0 0 9px;
  color: #8be0b4;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
}
.dashboard-cover h1 {
  color: #fff;
  font-size: 36px;
  line-height: 1.12;
}
.dashboard-cover p:not(.cover-label) {
  max-width: 440px;
  margin: 12px 0 22px;
  color: #d2dfda;
  font-size: 12px;
}
.cover-actions {
  display: flex;
  gap: 9px;
  flex-wrap: wrap;
}
.cover-meta {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 20px;
  color: #fff;
  font-size: 11px;
}
.cover-meta span {
  min-height: 40px;
  display: flex;
  align-items: center;
  padding: 0 13px;
  border-radius: 7px;
  background: rgba(11, 30, 23, 0.6);
  backdrop-filter: blur(8px);
}

.metric-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 20px;
}
.metric-grid.compact {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}
.metric {
  min-height: 144px;
  padding: 18px;
  background: var(--paper);
  border: 1px solid var(--line);
  border-top: 3px solid var(--green);
  border-radius: 7px;
  box-shadow: var(--shadow);
}
.metric.blue {
  border-top-color: var(--blue);
}
.metric.gold {
  border-top-color: var(--gold);
}
.metric.red {
  border-top-color: var(--red);
}
.metric.slate {
  border-top-color: var(--slate);
}
.metric-top {
  display: flex;
  align-items: center;
  gap: 10px;
}
.metric span {
  display: block;
  color: var(--muted);
  font-size: 11px;
}
.metric .metric-mark {
  display: grid;
  width: 30px;
  height: 30px;
  place-items: center;
  border-radius: 7px;
  background: var(--green-soft);
  color: var(--green);
  font-size: 9px;
  font-weight: 800;
}
.metric.blue .metric-mark {
  background: var(--blue-soft);
  color: var(--blue);
}
.metric.gold .metric-mark {
  background: var(--gold-soft);
  color: var(--gold);
}
.metric.red .metric-mark {
  background: var(--red-soft);
  color: var(--red);
}
.metric.slate .metric-mark {
  background: #e8edeb;
  color: var(--slate);
}
.metric strong {
  display: block;
  margin-top: 13px;
  font-size: 27px;
  line-height: 1.1;
}
.metric small {
  display: block;
  margin-top: 9px;
  color: #829089;
  font-size: 10px;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: minmax(0, 2.1fr) minmax(285px, 0.9fr);
  gap: 18px;
}
.surface {
  overflow: hidden;
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 8px;
  box-shadow: var(--shadow);
}
.surface-heading {
  min-height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding: 16px 20px;
  border-bottom: 1px solid var(--line);
}
.text-link {
  color: var(--green);
  font-size: 11px;
  font-weight: 700;
  text-decoration: none;
}
.health-list {
  padding: 6px 20px 4px;
}
.health-row {
  padding: 15px 0;
  border-bottom: 1px solid #edf0ee;
}
.health-row div {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 12px;
}
progress {
  width: 100%;
  height: 6px;
  display: block;
  border: 0;
  background: #e7ece9;
}
progress::-webkit-progress-bar {
  background: #e7ece9;
}
progress::-webkit-progress-value {
  background: var(--green);
}
progress::-moz-progress-bar {
  background: var(--green);
}
.health-note {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 12px 20px 20px;
  padding: 14px;
  background: var(--green-soft);
}
.health-note b {
  color: var(--green);
  font-size: 22px;
}
.health-note span {
  color: #53645d;
  font-size: 10px;
}

.toolbar {
  min-height: 68px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding: 11px 16px;
  margin-bottom: 14px;
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 8px;
  box-shadow: 0 8px 25px rgba(26, 43, 36, 0.04);
}
.search-field,
.filter-field {
  display: grid;
  grid-template-columns: auto minmax(240px, 430px);
  align-items: center;
  gap: 12px;
  color: var(--muted);
  font-size: 11px;
}
input,
select {
  min-height: 40px;
  padding: 9px 11px;
  border: 1px solid #cbd5d0;
  border-radius: 3px;
  background: #fff;
  color: var(--ink);
  outline: none;
}
input:focus,
select:focus {
  border-color: var(--green);
  box-shadow: 0 0 0 3px rgba(18, 99, 72, 0.1);
}

.table-wrap {
  width: 100%;
  overflow-x: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th,
td {
  padding: 14px 18px;
  border-bottom: 1px solid #e7ebe8;
  text-align: left;
  font-size: 12px;
  white-space: nowrap;
}
th {
  height: 48px;
  background: #f7f9f8;
  color: #62706a;
  font-size: 9px;
  text-transform: uppercase;
  letter-spacing: 0.7px;
}
tbody tr:hover {
  background: #fbfcfb;
}
tbody tr:last-child td {
  border-bottom: 0;
}
.member-id {
  color: var(--green);
  font:
    700 11px Consolas,
    monospace;
}
.pill {
  display: inline-block;
  padding: 5px 8px;
  border-radius: 12px;
  background: var(--green-soft);
  color: var(--green);
  font-size: 9px;
  font-weight: 700;
}
.pill.issued,
.pill.unpaid {
  background: var(--gold-soft);
  color: #865612;
}
.pill.overdue {
  background: var(--red-soft);
  color: var(--red);
}
.pill.disabled {
  background: #e9ecea;
  color: #5e6863;
}
.complete-text {
  color: var(--muted);
  font-size: 10px;
}
.pill.admin {
  background: #e6eff4;
  color: var(--blue);
}
.pill.librarian {
  background: var(--green-soft);
  color: var(--green);
}
.empty-state {
  display: grid;
  place-items: center;
  min-height: 210px;
  padding: 35px;
  text-align: center;
  color: var(--muted);
}
.empty-state strong {
  color: var(--ink);
}
.empty-state span {
  margin-top: -60px;
  font-size: 11px;
}

.modal {
  display: none;
  position: fixed;
  inset: 0;
  z-index: 20;
  place-items: center;
  padding: 20px;
  background: rgba(17, 25, 22, 0.62);
}
.modal.open {
  display: grid;
}
.modal form {
  width: min(480px, 100%);
  max-height: calc(100vh - 40px);
  overflow-y: auto;
  padding: 24px;
  background: var(--paper);
  border-radius: 5px;
  box-shadow: 0 24px 70px rgba(0, 0, 0, 0.25);
}
.modal-heading {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 18px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--line);
}
.modal label {
  display: block;
  margin: 13px 0;
  font-size: 11px;
  font-weight: 700;
}
.modal input,
.modal select {
  display: block;
  width: 100%;
  margin-top: 6px;
}
.form-note {
  margin: -4px 0 16px;
  color: var(--muted);
  font-size: 11px;
}
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 22px;
}
.account-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(340px, 0.65fr);
  gap: 18px;
  margin-bottom: 18px;
}
.account-form {
  padding: 20px;
}
.account-form label {
  display: block;
  margin: 0 0 14px;
  font-size: 11px;
  font-weight: 700;
}
.account-form input {
  display: block;
  width: 100%;
  margin-top: 6px;
}
.account-form > .button {
  width: 100%;
  margin-top: 5px;
}
.credentials-surface {
  margin-top: 18px;
}
.horizontal-form {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr)) auto;
  align-items: end;
  gap: 12px;
}
.horizontal-form label {
  margin: 0;
}
.horizontal-form > .button {
  width: auto;
  margin: 0;
  white-space: nowrap;
}

#toast {
  position: fixed;
  right: 24px;
  bottom: 24px;
  z-index: 40;
  max-width: min(390px, calc(100% - 48px));
  padding: 12px 16px;
  border-radius: 4px;
  background: #1e2924;
  color: #fff;
  box-shadow: 0 10px 35px #0003;
  opacity: 0;
  transform: translateY(20px);
  pointer-events: none;
  transition: 0.2s ease;
  font-size: 12px;
}
#toast.show {
  opacity: 1;
  transform: none;
}
#toast.error {
  background: #7d3029;
}

.app-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 18px;
  min-height: 82px;
  padding: 18px 20px;
  border-top: 1px solid var(--line);
  background: var(--paper);
  text-align: center;
}
.footer-line {
  width: 54px;
  height: 1px;
  background: #b9cbc3;
}
.footer-credit {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--muted);
  font-size: 10px;
}
.footer-credit strong {
  position: relative;
  color: var(--green-dark);
  font-family: "Trebuchet MS", Arial, sans-serif;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 1.1px;
}
.footer-credit strong::after {
  content: "";
  position: absolute;
  right: 0;
  bottom: -4px;
  left: 0;
  height: 2px;
  background: #55a982;
}

@media (max-width: 1050px) {
  .metric-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  .account-grid {
    grid-template-columns: 1fr;
  }
  .horizontal-form {
    grid-template-columns: 1fr 1fr;
  }
  .university-name {
    text-align: left;
  }
}
@media (max-width: 760px) {
  .app-header {
    grid-template-columns: 1fr auto;
    padding: 12px 18px;
  }
  .university-name {
    display: none;
  }
  .connection span,
  .user-menu span {
    display: none;
  }
  .header-tools {
    gap: 9px;
  }
  .user-menu {
    padding-left: 9px;
  }
  .nav-inner,
  .workspace {
    width: calc(100% - 32px);
  }
  .main-nav a {
    padding: 0 14px;
  }
  .workspace {
    padding-top: 24px;
  }
  .dashboard-cover {
    min-height: 330px;
  }
  .cover-content {
    width: 100%;
    padding: 28px 24px;
    background: rgba(7, 32, 24, 0.86);
  }
  .cover-meta {
    position: absolute;
    top: 10px;
    right: 10px;
  }
  .cover-meta span {
    display: none;
  }
  .dashboard-cover h1 {
    margin-top: 28px;
    font-size: 31px;
  }
  .page-heading {
    min-height: auto;
    flex-direction: column;
    padding-bottom: 20px;
  }
  .heading-actions {
    width: 100%;
    justify-content: space-between;
  }
  .command-strip {
    align-items: flex-start;
    flex-direction: column;
  }
  .command-actions {
    width: 100%;
    overflow-x: auto;
  }
  .command-actions .button {
    white-space: nowrap;
  }
  .metric-grid,
  .metric-grid.compact {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .toolbar {
    align-items: stretch;
    flex-direction: column;
  }
  .horizontal-form {
    grid-template-columns: 1fr;
  }
  .search-field,
  .filter-field {
    grid-template-columns: 1fr;
    gap: 5px;
  }
}
@media (max-width: 440px) {
  .brand-block {
    min-width: 0;
  }
  .brand-block small {
    display: none;
  }
  .brand-mark {
    width: 50px;
    flex-basis: 50px;
    font-size: 10px;
  }
  .connection span {
    display: none;
  }
  .metric-grid,
  .metric-grid.compact {
    grid-template-columns: 1fr;
  }
  .metric {
    min-height: 112px;
  }
  .row-actions {
    flex-direction: column;
  }
  .app-footer {
    gap: 10px;
  }
  .footer-line {
    width: 22px;
  }
  .footer-credit {
    align-items: center;
    flex-direction: column;
    gap: 3px;
  }
}

button:focus-visible,
a:focus-visible {
  outline: 3px solid var(--green);
  outline-offset: 3px;
}
button:disabled {
  cursor: wait;
  opacity: 0.6;
}
body:has(.modal.open) {
  overflow: hidden;
}
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation: none !important;
    transition: none !important;
  }
}

.audit-filters {
  align-items: end;
}
.audit-filters label {
  display: grid;
  gap: 6px;
  flex: 1;
  font-size: 12px;
}
.audit-filters input,
.audit-filters select {
  width: 100%;
  min-width: 0;
}
.audit-pagination {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 18px 0;
}
.audit-record-id {
  display: block;
  color: var(--muted);
  font-size: 10px;
}
.modal .audit-detail-form {
  width: min(880px, 100%);
}
#auditValues td {
  white-space: normal;
  overflow-wrap: anywhere;
}
.audit-changed {
  background: var(--gold-soft);
}
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>:root {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 2 | <code>  --ink: #17201d;</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 3 | <code>  --muted: #65706b;</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 4 | <code>  --canvas: #f4f6f5;</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 5 | <code>  --paper: #ffffff;</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 6 | <code>  --line: #dce2de;</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 7 | <code>  --green: #126348;</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 8 | <code>  --green-dark: #0b3f30;</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 9 | <code>  --green-soft: #e5f1eb;</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 10 | <code>  --blue: #356c8c;</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 11 | <code>  --blue-soft: #e6eff4;</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 12 | <code>  --gold: #a86d17;</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 13 | <code>  --gold-soft: #fbefd9;</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 14 | <code>  --red: #963c34;</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 15 | <code>  --red-soft: #f5e5e2;</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 16 | <code>  --slate: #55645e;</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 17 | <code>  --shadow: 0 12px 35px rgba(26, 43, 36, 0.08);</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 18 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 19 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 20 | <code>* {</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 21 | <code>  box-sizing: border-box;</code> | CSS properties: box-sizing; enclosing selector-এর presentation নির্ধারণ করে। |
| 22 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 23 | <code>body {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 24 | <code>  min-height: 100vh;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 25 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 26 | <code>  flex-direction: column;</code> | CSS properties: flex-direction; enclosing selector-এর presentation নির্ধারণ করে। |
| 27 | <code>  margin: 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 28 | <code>  min-width: 320px;</code> | CSS properties: min-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 29 | <code>  background: var(--canvas);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 30 | <code>  color: var(--ink);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 31 | <code>  font-family: Arial, sans-serif;</code> | CSS properties: font-family; enclosing selector-এর presentation নির্ধারণ করে। |
| 32 | <code>  line-height: 1.45;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 33 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 34 | <code>button,</code> | Style rule/block-এর closing বা continuation। |
| 35 | <code>input,</code> | Style rule/block-এর closing বা continuation। |
| 36 | <code>select {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 37 | <code>  font: inherit;</code> | CSS properties: font; enclosing selector-এর presentation নির্ধারণ করে। |
| 38 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 39 | <code>a {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 40 | <code>  color: inherit;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 41 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 42 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 43 | <code>.app-header {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 44 | <code>  min-height: 82px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 45 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 46 | <code>  grid-template-columns: auto 1fr auto;</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 47 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 48 | <code>  gap: 28px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 49 | <code>  padding: 14px max(28px, calc((100vw - 1440px) / 2));</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 50 | <code>  background: var(--paper);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 51 | <code>  border-bottom: 1px solid var(--line);</code> | CSS properties: border-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 52 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 53 | <code>.brand-block {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 54 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 55 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 56 | <code>  gap: 12px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 57 | <code>  min-width: 235px;</code> | CSS properties: min-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 58 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 59 | <code>.brand-mark {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 60 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 61 | <code>  place-items: center;</code> | CSS properties: place-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 62 | <code>  width: 58px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 63 | <code>  height: 44px;</code> | CSS properties: height; enclosing selector-এর presentation নির্ধারণ করে। |
| 64 | <code>  flex: 0 0 58px;</code> | CSS properties: flex; enclosing selector-এর presentation নির্ধারণ করে। |
| 65 | <code>  border-radius: 8px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 66 | <code>  background: var(--green-dark);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 67 | <code>  color: #fff;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 68 | <code>  box-shadow: 0 8px 20px rgba(11, 63, 48, 0.22);</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 69 | <code>  font:</code> | CSS properties: font; enclosing selector-এর presentation নির্ধারণ করে। |
| 70 | <code>    800 12px Arial,</code> | Style rule/block-এর closing বা continuation। |
| 71 | <code>    sans-serif;</code> | Style rule/block-এর closing বা continuation। |
| 72 | <code>  letter-spacing: 1.2px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 73 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 74 | <code>.brand-block strong,</code> | Style rule/block-এর closing বা continuation। |
| 75 | <code>.brand-block small {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 76 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 77 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 78 | <code>.brand-block strong {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 79 | <code>  color: var(--green-dark);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 80 | <code>  font-size: 17px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 81 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 82 | <code>.brand-block small {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 83 | <code>  margin-top: 2px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 84 | <code>  color: var(--muted);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 85 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 86 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 87 | <code>.university-name {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 88 | <code>  color: var(--green);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 89 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 90 | <code>  font-weight: 700;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 91 | <code>  text-align: center;</code> | CSS properties: text-align; enclosing selector-এর presentation নির্ধারণ করে। |
| 92 | <code>  text-transform: uppercase;</code> | CSS properties: text-transform; enclosing selector-এর presentation নির্ধারণ করে। |
| 93 | <code>  letter-spacing: 1.1px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 94 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 95 | <code>.connection {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 96 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 97 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 98 | <code>  gap: 8px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 99 | <code>  color: var(--muted);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 100 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 101 | <code>  white-space: nowrap;</code> | CSS properties: white-space; enclosing selector-এর presentation নির্ধারণ করে। |
| 102 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 103 | <code>.connection i {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 104 | <code>  width: 9px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 105 | <code>  height: 9px;</code> | CSS properties: height; enclosing selector-এর presentation নির্ধারণ করে। |
| 106 | <code>  border-radius: 50%;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 107 | <code>  background: #d39a3f;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 108 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 109 | <code>.connection i.online {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 110 | <code>  background: #49a875;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 111 | <code>  box-shadow: 0 0 0 3px #e0f2e8;</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 112 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 113 | <code>.header-tools {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 114 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 115 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 116 | <code>  gap: 16px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 117 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 118 | <code>.user-menu {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 119 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 120 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 121 | <code>  gap: 8px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 122 | <code>  padding-left: 15px;</code> | CSS properties: padding-left; enclosing selector-এর presentation নির্ধারণ করে। |
| 123 | <code>  border-left: 1px solid var(--line);</code> | CSS properties: border-left; enclosing selector-এর presentation নির্ধারণ করে। |
| 124 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 125 | <code>.user-menu span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 126 | <code>  max-width: 145px;</code> | CSS properties: max-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 127 | <code>  overflow: hidden;</code> | CSS properties: overflow; enclosing selector-এর presentation নির্ধারণ করে। |
| 128 | <code>  color: var(--green-dark);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 129 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 130 | <code>  font-weight: 700;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 131 | <code>  text-overflow: ellipsis;</code> | CSS properties: text-overflow; enclosing selector-এর presentation নির্ধারণ করে। |
| 132 | <code>  text-transform: uppercase;</code> | CSS properties: text-transform; enclosing selector-এর presentation নির্ধারণ করে। |
| 133 | <code>  white-space: nowrap;</code> | CSS properties: white-space; enclosing selector-এর presentation নির্ধারণ করে। |
| 134 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 135 | <code>.user-menu button {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 136 | <code>  min-height: 32px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 137 | <code>  padding: 6px 9px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 138 | <code>  border: 1px solid var(--line);</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 139 | <code>  background: #f2f5f3;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 140 | <code>  color: var(--slate);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 141 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 142 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 143 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 144 | <code>.main-nav {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 145 | <code>  min-height: 52px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 146 | <code>  background: #17211d;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 147 | <code>  color: #cdd7d2;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 148 | <code>  box-shadow: 0 6px 20px rgba(18, 29, 24, 0.12);</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 149 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 150 | <code>.nav-inner {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 151 | <code>  width: min(1440px, calc(100% - 56px));</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 152 | <code>  min-height: 52px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 153 | <code>  margin: auto;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 154 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 155 | <code>  align-items: stretch;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 156 | <code>  overflow-x: auto;</code> | CSS properties: overflow-x; enclosing selector-এর presentation নির্ধারণ করে। |
| 157 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 158 | <code>.main-nav a {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 159 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 160 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 161 | <code>  min-height: 52px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 162 | <code>  padding: 0 22px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 163 | <code>  border-bottom: 3px solid transparent;</code> | CSS properties: border-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 164 | <code>  text-decoration: none;</code> | CSS properties: text-decoration; enclosing selector-এর presentation নির্ধারণ করে। |
| 165 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 166 | <code>  font-weight: 700;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 167 | <code>  white-space: nowrap;</code> | CSS properties: white-space; enclosing selector-এর presentation নির্ধারণ করে। |
| 168 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 169 | <code>.main-nav a:hover {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 170 | <code>  background: #28352f;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 171 | <code>  color: #fff;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 172 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 173 | <code>.main-nav a.active {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 174 | <code>  border-bottom-color: #62bc91;</code> | CSS properties: border-bottom-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 175 | <code>  background: #293a33;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 176 | <code>  color: #fff;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 177 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 178 | <code>.admin-only {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 179 | <code>  display: none !important;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 180 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 181 | <code>.admin-only.visible {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 182 | <code>  display: flex !important;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 183 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 184 | <code>.workspace {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 185 | <code>  width: min(1440px, calc(100% - 56px));</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 186 | <code>  flex: 1;</code> | CSS properties: flex; enclosing selector-এর presentation নির্ধারণ করে। |
| 187 | <code>  margin: 0 auto;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 188 | <code>  padding: 30px 0 54px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 189 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 190 | <code>.page-heading {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 191 | <code>  min-height: 102px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 192 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 193 | <code>  justify-content: space-between;</code> | CSS properties: justify-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 194 | <code>  align-items: flex-start;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 195 | <code>  gap: 24px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 196 | <code>  margin-bottom: 24px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 197 | <code>  border-bottom: 1px solid var(--line);</code> | CSS properties: border-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 198 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 199 | <code>.eyebrow,</code> | Style rule/block-এর closing বা continuation। |
| 200 | <code>.section-label {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 201 | <code>  margin: 0 0 5px;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 202 | <code>  color: var(--green);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 203 | <code>  font-size: 9px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 204 | <code>  font-weight: 700;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 205 | <code>  text-transform: uppercase;</code> | CSS properties: text-transform; enclosing selector-এর presentation নির্ধারণ করে। |
| 206 | <code>  letter-spacing: 1px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 207 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 208 | <code>h1 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 209 | <code>  margin: 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 210 | <code>  font-size: 30px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 211 | <code>  line-height: 1.2;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 212 | <code>  letter-spacing: 0;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 213 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 214 | <code>h2 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 215 | <code>  margin: 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 216 | <code>  font-size: 18px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 217 | <code>  letter-spacing: 0;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 218 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 219 | <code>.heading-copy {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 220 | <code>  margin: 7px 0 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 221 | <code>  color: var(--muted);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 222 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 223 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 224 | <code>.heading-actions {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 225 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 226 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 227 | <code>  gap: 14px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 228 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 229 | <code>.current-date,</code> | Style rule/block-এর closing বা continuation। |
| 230 | <code>.record-count {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 231 | <code>  color: var(--muted);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 232 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 233 | <code>  white-space: nowrap;</code> | CSS properties: white-space; enclosing selector-এর presentation নির্ধারণ করে। |
| 234 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 235 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 236 | <code>.button,</code> | Style rule/block-এর closing বা continuation। |
| 237 | <code>button {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 238 | <code>  min-height: 40px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 239 | <code>  border: 0;</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 240 | <code>  border-radius: 7px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 241 | <code>  padding: 9px 16px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 242 | <code>  cursor: pointer;</code> | CSS properties: cursor; enclosing selector-এর presentation নির্ধারণ করে। |
| 243 | <code>  text-decoration: none;</code> | CSS properties: text-decoration; enclosing selector-এর presentation নির্ধারণ করে। |
| 244 | <code>  text-align: center;</code> | CSS properties: text-align; enclosing selector-এর presentation নির্ধারণ করে। |
| 245 | <code>  font-weight: 600;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 246 | <code>  transition:</code> | CSS properties: transition; enclosing selector-এর presentation নির্ধারণ করে। |
| 247 | <code>    background 0.15s ease,</code> | Style rule/block-এর closing বা continuation। |
| 248 | <code>    border-color 0.15s ease,</code> | Style rule/block-এর closing বা continuation। |
| 249 | <code>    transform 0.15s ease,</code> | Style rule/block-এর closing বা continuation। |
| 250 | <code>    box-shadow 0.15s ease;</code> | Style rule/block-এর closing বা continuation। |
| 251 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 252 | <code>.button:hover {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 253 | <code>  transform: translateY(-1px);</code> | CSS properties: transform; enclosing selector-এর presentation নির্ধারণ করে। |
| 254 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 255 | <code>.button.primary {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 256 | <code>  background: var(--green);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 257 | <code>  color: #fff;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 258 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 259 | <code>.button.primary:hover {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 260 | <code>  background: #0d503b;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 261 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 262 | <code>.button.secondary {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 263 | <code>  border: 1px solid #d4dcd8;</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 264 | <code>  background: #edf1ef;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 265 | <code>  color: #25312c;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 266 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 267 | <code>.button.secondary:hover {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 268 | <code>  background: #e2e8e5;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 269 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 270 | <code>.button.danger {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 271 | <code>  background: var(--red);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 272 | <code>  color: #fff;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 273 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 274 | <code>.button.danger-quiet {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 275 | <code>  background: var(--red-soft);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 276 | <code>  color: var(--red);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 277 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 278 | <code>.button.light {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 279 | <code>  background: #fff;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 280 | <code>  color: var(--green-dark);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 281 | <code>  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.14);</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 282 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 283 | <code>.button.glass {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 284 | <code>  border: 1px solid rgba(255, 255, 255, 0.32);</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 285 | <code>  background: rgba(13, 32, 25, 0.56);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 286 | <code>  color: #fff;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 287 | <code>  backdrop-filter: blur(8px);</code> | CSS properties: backdrop-filter; enclosing selector-এর presentation নির্ধারণ করে। |
| 288 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 289 | <code>.button.small {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 290 | <code>  min-height: 32px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 291 | <code>  padding: 6px 10px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 292 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 293 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 294 | <code>.button:disabled,</code> | CSS properties: button; enclosing selector-এর presentation নির্ধারণ করে। |
| 295 | <code>button:disabled {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 296 | <code>  cursor: wait;</code> | CSS properties: cursor; enclosing selector-এর presentation নির্ধারণ করে। |
| 297 | <code>  opacity: 0.55;</code> | CSS properties: opacity; enclosing selector-এর presentation নির্ধারণ করে। |
| 298 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 299 | <code>.icon-button {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 300 | <code>  width: 34px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 301 | <code>  min-height: 34px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 302 | <code>  padding: 0;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 303 | <code>  background: transparent;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 304 | <code>  color: var(--muted);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 305 | <code>  font-size: 25px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 306 | <code>  line-height: 1;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 307 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 308 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 309 | <code>.command-strip {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 310 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 311 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 312 | <code>  justify-content: space-between;</code> | CSS properties: justify-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 313 | <code>  gap: 20px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 314 | <code>  padding: 16px 18px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 315 | <code>  margin-bottom: 18px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 316 | <code>  background: var(--paper);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 317 | <code>  border: 1px solid var(--line);</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 318 | <code>  border-left: 4px solid var(--green);</code> | CSS properties: border-left; enclosing selector-এর presentation নির্ধারণ করে। |
| 319 | <code>  box-shadow: var(--shadow);</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 320 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 321 | <code>.command-strip strong {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 322 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 323 | <code>  font-size: 14px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 324 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 325 | <code>.command-actions,</code> | Style rule/block-এর closing বা continuation। |
| 326 | <code>.row-actions,</code> | Style rule/block-এর closing বা continuation। |
| 327 | <code>.heading-actions {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 328 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 329 | <code>  gap: 8px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 330 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 331 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 332 | <code>.dashboard-cover {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 333 | <code>  position: relative;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 334 | <code>  min-height: 270px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 335 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 336 | <code>  align-items: stretch;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 337 | <code>  justify-content: space-between;</code> | CSS properties: justify-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 338 | <code>  gap: 28px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 339 | <code>  margin-bottom: 22px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 340 | <code>  overflow: hidden;</code> | CSS properties: overflow; enclosing selector-এর presentation নির্ধারণ করে। |
| 341 | <code>  border-radius: 8px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 342 | <code>  background-color: #102b22;</code> | CSS properties: background-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 343 | <code>  background-image: url(&quot;/static/assets/library-dashboard.png&quot;);</code> | CSS properties: background-image; enclosing selector-এর presentation নির্ধারণ করে। |
| 344 | <code>  background-position: center;</code> | CSS properties: background-position; enclosing selector-এর presentation নির্ধারণ করে। |
| 345 | <code>  background-size: cover;</code> | CSS properties: background-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 346 | <code>  box-shadow: 0 22px 55px rgba(16, 43, 34, 0.2);</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 347 | <code>  color: #fff;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 348 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 349 | <code>.cover-content {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 350 | <code>  width: min(610px, 70%);</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 351 | <code>  padding: 34px 38px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 352 | <code>  background: rgba(7, 32, 24, 0.82);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 353 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 354 | <code>.cover-label {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 355 | <code>  margin: 0 0 9px;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 356 | <code>  color: #8be0b4;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 357 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 358 | <code>  font-weight: 700;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 359 | <code>  letter-spacing: 1px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 360 | <code>  text-transform: uppercase;</code> | CSS properties: text-transform; enclosing selector-এর presentation নির্ধারণ করে। |
| 361 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 362 | <code>.dashboard-cover h1 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 363 | <code>  color: #fff;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 364 | <code>  font-size: 36px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 365 | <code>  line-height: 1.12;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 366 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 367 | <code>.dashboard-cover p:not(.cover-label) {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 368 | <code>  max-width: 440px;</code> | CSS properties: max-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 369 | <code>  margin: 12px 0 22px;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 370 | <code>  color: #d2dfda;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 371 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 372 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 373 | <code>.cover-actions {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 374 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 375 | <code>  gap: 9px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 376 | <code>  flex-wrap: wrap;</code> | CSS properties: flex-wrap; enclosing selector-এর presentation নির্ধারণ করে। |
| 377 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 378 | <code>.cover-meta {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 379 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 380 | <code>  align-items: flex-start;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 381 | <code>  gap: 10px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 382 | <code>  padding: 20px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 383 | <code>  color: #fff;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 384 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 385 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 386 | <code>.cover-meta span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 387 | <code>  min-height: 40px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 388 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 389 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 390 | <code>  padding: 0 13px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 391 | <code>  border-radius: 7px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 392 | <code>  background: rgba(11, 30, 23, 0.6);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 393 | <code>  backdrop-filter: blur(8px);</code> | CSS properties: backdrop-filter; enclosing selector-এর presentation নির্ধারণ করে। |
| 394 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 395 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 396 | <code>.metric-grid {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 397 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 398 | <code>  grid-template-columns: repeat(5, minmax(0, 1fr));</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 399 | <code>  gap: 14px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 400 | <code>  margin-bottom: 20px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 401 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 402 | <code>.metric-grid.compact {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 403 | <code>  grid-template-columns: repeat(3, minmax(0, 1fr));</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 404 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 405 | <code>.metric {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 406 | <code>  min-height: 144px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 407 | <code>  padding: 18px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 408 | <code>  background: var(--paper);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 409 | <code>  border: 1px solid var(--line);</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 410 | <code>  border-top: 3px solid var(--green);</code> | CSS properties: border-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 411 | <code>  border-radius: 7px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 412 | <code>  box-shadow: var(--shadow);</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 413 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 414 | <code>.metric.blue {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 415 | <code>  border-top-color: var(--blue);</code> | CSS properties: border-top-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 416 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 417 | <code>.metric.gold {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 418 | <code>  border-top-color: var(--gold);</code> | CSS properties: border-top-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 419 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 420 | <code>.metric.red {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 421 | <code>  border-top-color: var(--red);</code> | CSS properties: border-top-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 422 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 423 | <code>.metric.slate {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 424 | <code>  border-top-color: var(--slate);</code> | CSS properties: border-top-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 425 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 426 | <code>.metric-top {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 427 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 428 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 429 | <code>  gap: 10px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 430 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 431 | <code>.metric span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 432 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 433 | <code>  color: var(--muted);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 434 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 435 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 436 | <code>.metric .metric-mark {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 437 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 438 | <code>  width: 30px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 439 | <code>  height: 30px;</code> | CSS properties: height; enclosing selector-এর presentation নির্ধারণ করে। |
| 440 | <code>  place-items: center;</code> | CSS properties: place-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 441 | <code>  border-radius: 7px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 442 | <code>  background: var(--green-soft);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 443 | <code>  color: var(--green);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 444 | <code>  font-size: 9px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 445 | <code>  font-weight: 800;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 446 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 447 | <code>.metric.blue .metric-mark {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 448 | <code>  background: var(--blue-soft);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 449 | <code>  color: var(--blue);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 450 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 451 | <code>.metric.gold .metric-mark {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 452 | <code>  background: var(--gold-soft);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 453 | <code>  color: var(--gold);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 454 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 455 | <code>.metric.red .metric-mark {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 456 | <code>  background: var(--red-soft);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 457 | <code>  color: var(--red);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 458 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 459 | <code>.metric.slate .metric-mark {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 460 | <code>  background: #e8edeb;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 461 | <code>  color: var(--slate);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 462 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 463 | <code>.metric strong {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 464 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 465 | <code>  margin-top: 13px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 466 | <code>  font-size: 27px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 467 | <code>  line-height: 1.1;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 468 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 469 | <code>.metric small {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 470 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 471 | <code>  margin-top: 9px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 472 | <code>  color: #829089;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 473 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 474 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 475 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 476 | <code>.dashboard-grid {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 477 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 478 | <code>  grid-template-columns: minmax(0, 2.1fr) minmax(285px, 0.9fr);</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 479 | <code>  gap: 18px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 480 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 481 | <code>.surface {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 482 | <code>  overflow: hidden;</code> | CSS properties: overflow; enclosing selector-এর presentation নির্ধারণ করে। |
| 483 | <code>  background: var(--paper);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 484 | <code>  border: 1px solid var(--line);</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 485 | <code>  border-radius: 8px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 486 | <code>  box-shadow: var(--shadow);</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 487 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 488 | <code>.surface-heading {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 489 | <code>  min-height: 72px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 490 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 491 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 492 | <code>  justify-content: space-between;</code> | CSS properties: justify-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 493 | <code>  gap: 18px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 494 | <code>  padding: 16px 20px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 495 | <code>  border-bottom: 1px solid var(--line);</code> | CSS properties: border-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 496 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 497 | <code>.text-link {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 498 | <code>  color: var(--green);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 499 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 500 | <code>  font-weight: 700;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 501 | <code>  text-decoration: none;</code> | CSS properties: text-decoration; enclosing selector-এর presentation নির্ধারণ করে। |
| 502 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 503 | <code>.health-list {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 504 | <code>  padding: 6px 20px 4px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 505 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 506 | <code>.health-row {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 507 | <code>  padding: 15px 0;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 508 | <code>  border-bottom: 1px solid #edf0ee;</code> | CSS properties: border-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 509 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 510 | <code>.health-row div {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 511 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 512 | <code>  justify-content: space-between;</code> | CSS properties: justify-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 513 | <code>  margin-bottom: 8px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 514 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 515 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 516 | <code>progress {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 517 | <code>  width: 100%;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 518 | <code>  height: 6px;</code> | CSS properties: height; enclosing selector-এর presentation নির্ধারণ করে। |
| 519 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 520 | <code>  border: 0;</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 521 | <code>  background: #e7ece9;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 522 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 523 | <code>progress::-webkit-progress-bar {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 524 | <code>  background: #e7ece9;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 525 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 526 | <code>progress::-webkit-progress-value {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 527 | <code>  background: var(--green);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 528 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 529 | <code>progress::-moz-progress-bar {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 530 | <code>  background: var(--green);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 531 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 532 | <code>.health-note {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 533 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 534 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 535 | <code>  gap: 12px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 536 | <code>  margin: 12px 20px 20px;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 537 | <code>  padding: 14px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 538 | <code>  background: var(--green-soft);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 539 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 540 | <code>.health-note b {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 541 | <code>  color: var(--green);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 542 | <code>  font-size: 22px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 543 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 544 | <code>.health-note span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 545 | <code>  color: #53645d;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 546 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 547 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 548 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 549 | <code>.toolbar {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 550 | <code>  min-height: 68px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 551 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 552 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 553 | <code>  justify-content: space-between;</code> | CSS properties: justify-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 554 | <code>  gap: 18px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 555 | <code>  padding: 11px 16px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 556 | <code>  margin-bottom: 14px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 557 | <code>  background: var(--paper);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 558 | <code>  border: 1px solid var(--line);</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 559 | <code>  border-radius: 8px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 560 | <code>  box-shadow: 0 8px 25px rgba(26, 43, 36, 0.04);</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 561 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 562 | <code>.search-field,</code> | Style rule/block-এর closing বা continuation। |
| 563 | <code>.filter-field {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 564 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 565 | <code>  grid-template-columns: auto minmax(240px, 430px);</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 566 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 567 | <code>  gap: 12px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 568 | <code>  color: var(--muted);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 569 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 570 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 571 | <code>input,</code> | Style rule/block-এর closing বা continuation। |
| 572 | <code>select {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 573 | <code>  min-height: 40px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 574 | <code>  padding: 9px 11px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 575 | <code>  border: 1px solid #cbd5d0;</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 576 | <code>  border-radius: 3px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 577 | <code>  background: #fff;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 578 | <code>  color: var(--ink);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 579 | <code>  outline: none;</code> | CSS properties: outline; enclosing selector-এর presentation নির্ধারণ করে। |
| 580 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 581 | <code>input:focus,</code> | CSS properties: input; enclosing selector-এর presentation নির্ধারণ করে। |
| 582 | <code>select:focus {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 583 | <code>  border-color: var(--green);</code> | CSS properties: border-color; enclosing selector-এর presentation নির্ধারণ করে। |
| 584 | <code>  box-shadow: 0 0 0 3px rgba(18, 99, 72, 0.1);</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 585 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 586 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 587 | <code>.table-wrap {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 588 | <code>  width: 100%;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 589 | <code>  overflow-x: auto;</code> | CSS properties: overflow-x; enclosing selector-এর presentation নির্ধারণ করে। |
| 590 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 591 | <code>table {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 592 | <code>  width: 100%;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 593 | <code>  border-collapse: collapse;</code> | CSS properties: border-collapse; enclosing selector-এর presentation নির্ধারণ করে। |
| 594 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 595 | <code>th,</code> | Style rule/block-এর closing বা continuation। |
| 596 | <code>td {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 597 | <code>  padding: 14px 18px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 598 | <code>  border-bottom: 1px solid #e7ebe8;</code> | CSS properties: border-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 599 | <code>  text-align: left;</code> | CSS properties: text-align; enclosing selector-এর presentation নির্ধারণ করে। |
| 600 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 601 | <code>  white-space: nowrap;</code> | CSS properties: white-space; enclosing selector-এর presentation নির্ধারণ করে। |
| 602 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 603 | <code>th {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 604 | <code>  height: 48px;</code> | CSS properties: height; enclosing selector-এর presentation নির্ধারণ করে। |
| 605 | <code>  background: #f7f9f8;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 606 | <code>  color: #62706a;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 607 | <code>  font-size: 9px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 608 | <code>  text-transform: uppercase;</code> | CSS properties: text-transform; enclosing selector-এর presentation নির্ধারণ করে। |
| 609 | <code>  letter-spacing: 0.7px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 610 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 611 | <code>tbody tr:hover {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 612 | <code>  background: #fbfcfb;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 613 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 614 | <code>tbody tr:last-child td {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 615 | <code>  border-bottom: 0;</code> | CSS properties: border-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 616 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 617 | <code>.member-id {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 618 | <code>  color: var(--green);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 619 | <code>  font:</code> | CSS properties: font; enclosing selector-এর presentation নির্ধারণ করে। |
| 620 | <code>    700 11px Consolas,</code> | Style rule/block-এর closing বা continuation। |
| 621 | <code>    monospace;</code> | Style rule/block-এর closing বা continuation। |
| 622 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 623 | <code>.pill {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 624 | <code>  display: inline-block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 625 | <code>  padding: 5px 8px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 626 | <code>  border-radius: 12px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 627 | <code>  background: var(--green-soft);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 628 | <code>  color: var(--green);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 629 | <code>  font-size: 9px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 630 | <code>  font-weight: 700;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 631 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 632 | <code>.pill.issued,</code> | Style rule/block-এর closing বা continuation। |
| 633 | <code>.pill.unpaid {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 634 | <code>  background: var(--gold-soft);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 635 | <code>  color: #865612;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 636 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 637 | <code>.pill.overdue {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 638 | <code>  background: var(--red-soft);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 639 | <code>  color: var(--red);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 640 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 641 | <code>.pill.disabled {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 642 | <code>  background: #e9ecea;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 643 | <code>  color: #5e6863;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 644 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 645 | <code>.complete-text {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 646 | <code>  color: var(--muted);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 647 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 648 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 649 | <code>.pill.admin {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 650 | <code>  background: #e6eff4;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 651 | <code>  color: var(--blue);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 652 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 653 | <code>.pill.librarian {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 654 | <code>  background: var(--green-soft);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 655 | <code>  color: var(--green);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 656 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 657 | <code>.empty-state {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 658 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 659 | <code>  place-items: center;</code> | CSS properties: place-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 660 | <code>  min-height: 210px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 661 | <code>  padding: 35px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 662 | <code>  text-align: center;</code> | CSS properties: text-align; enclosing selector-এর presentation নির্ধারণ করে। |
| 663 | <code>  color: var(--muted);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 664 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 665 | <code>.empty-state strong {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 666 | <code>  color: var(--ink);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 667 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 668 | <code>.empty-state span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 669 | <code>  margin-top: -60px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 670 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 671 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 672 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 673 | <code>.modal {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 674 | <code>  display: none;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 675 | <code>  position: fixed;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 676 | <code>  inset: 0;</code> | CSS properties: inset; enclosing selector-এর presentation নির্ধারণ করে। |
| 677 | <code>  z-index: 20;</code> | CSS properties: z-index; enclosing selector-এর presentation নির্ধারণ করে। |
| 678 | <code>  place-items: center;</code> | CSS properties: place-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 679 | <code>  padding: 20px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 680 | <code>  background: rgba(17, 25, 22, 0.62);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 681 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 682 | <code>.modal.open {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 683 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 684 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 685 | <code>.modal form {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 686 | <code>  width: min(480px, 100%);</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 687 | <code>  max-height: calc(100vh - 40px);</code> | CSS properties: max-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 688 | <code>  overflow-y: auto;</code> | CSS properties: overflow-y; enclosing selector-এর presentation নির্ধারণ করে। |
| 689 | <code>  padding: 24px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 690 | <code>  background: var(--paper);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 691 | <code>  border-radius: 5px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 692 | <code>  box-shadow: 0 24px 70px rgba(0, 0, 0, 0.25);</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 693 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 694 | <code>.modal-heading {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 695 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 696 | <code>  align-items: flex-start;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 697 | <code>  justify-content: space-between;</code> | CSS properties: justify-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 698 | <code>  gap: 20px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 699 | <code>  margin-bottom: 18px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 700 | <code>  padding-bottom: 15px;</code> | CSS properties: padding-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 701 | <code>  border-bottom: 1px solid var(--line);</code> | CSS properties: border-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 702 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 703 | <code>.modal label {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 704 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 705 | <code>  margin: 13px 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 706 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 707 | <code>  font-weight: 700;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 708 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 709 | <code>.modal input,</code> | Style rule/block-এর closing বা continuation। |
| 710 | <code>.modal select {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 711 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 712 | <code>  width: 100%;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 713 | <code>  margin-top: 6px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 714 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 715 | <code>.form-note {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 716 | <code>  margin: -4px 0 16px;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 717 | <code>  color: var(--muted);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 718 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 719 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 720 | <code>.form-actions {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 721 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 722 | <code>  justify-content: flex-end;</code> | CSS properties: justify-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 723 | <code>  gap: 8px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 724 | <code>  margin-top: 22px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 725 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 726 | <code>.account-grid {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 727 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 728 | <code>  grid-template-columns: minmax(0, 1.35fr) minmax(340px, 0.65fr);</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 729 | <code>  gap: 18px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 730 | <code>  margin-bottom: 18px;</code> | CSS properties: margin-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 731 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 732 | <code>.account-form {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 733 | <code>  padding: 20px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 734 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 735 | <code>.account-form label {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 736 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 737 | <code>  margin: 0 0 14px;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 738 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 739 | <code>  font-weight: 700;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 740 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 741 | <code>.account-form input {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 742 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 743 | <code>  width: 100%;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 744 | <code>  margin-top: 6px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 745 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 746 | <code>.account-form &gt; .button {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 747 | <code>  width: 100%;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 748 | <code>  margin-top: 5px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 749 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 750 | <code>.credentials-surface {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 751 | <code>  margin-top: 18px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 752 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 753 | <code>.horizontal-form {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 754 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 755 | <code>  grid-template-columns: repeat(4, minmax(0, 1fr)) auto;</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 756 | <code>  align-items: end;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 757 | <code>  gap: 12px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 758 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 759 | <code>.horizontal-form label {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 760 | <code>  margin: 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 761 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 762 | <code>.horizontal-form &gt; .button {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 763 | <code>  width: auto;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 764 | <code>  margin: 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 765 | <code>  white-space: nowrap;</code> | CSS properties: white-space; enclosing selector-এর presentation নির্ধারণ করে। |
| 766 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 767 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 768 | <code>#toast {</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 769 | <code>  position: fixed;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 770 | <code>  right: 24px;</code> | CSS properties: right; enclosing selector-এর presentation নির্ধারণ করে। |
| 771 | <code>  bottom: 24px;</code> | CSS properties: bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 772 | <code>  z-index: 40;</code> | CSS properties: z-index; enclosing selector-এর presentation নির্ধারণ করে। |
| 773 | <code>  max-width: min(390px, calc(100% - 48px));</code> | CSS properties: max-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 774 | <code>  padding: 12px 16px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 775 | <code>  border-radius: 4px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 776 | <code>  background: #1e2924;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 777 | <code>  color: #fff;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 778 | <code>  box-shadow: 0 10px 35px #0003;</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 779 | <code>  opacity: 0;</code> | CSS properties: opacity; enclosing selector-এর presentation নির্ধারণ করে। |
| 780 | <code>  transform: translateY(20px);</code> | CSS properties: transform; enclosing selector-এর presentation নির্ধারণ করে। |
| 781 | <code>  pointer-events: none;</code> | CSS properties: pointer-events; enclosing selector-এর presentation নির্ধারণ করে। |
| 782 | <code>  transition: 0.2s ease;</code> | CSS properties: transition; enclosing selector-এর presentation নির্ধারণ করে। |
| 783 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 784 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 785 | <code>#toast.show {</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 786 | <code>  opacity: 1;</code> | CSS properties: opacity; enclosing selector-এর presentation নির্ধারণ করে। |
| 787 | <code>  transform: none;</code> | CSS properties: transform; enclosing selector-এর presentation নির্ধারণ করে। |
| 788 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 789 | <code>#toast.error {</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 790 | <code>  background: #7d3029;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 791 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 792 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 793 | <code>.app-footer {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 794 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 795 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 796 | <code>  justify-content: center;</code> | CSS properties: justify-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 797 | <code>  gap: 18px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 798 | <code>  min-height: 82px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 799 | <code>  padding: 18px 20px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 800 | <code>  border-top: 1px solid var(--line);</code> | CSS properties: border-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 801 | <code>  background: var(--paper);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 802 | <code>  text-align: center;</code> | CSS properties: text-align; enclosing selector-এর presentation নির্ধারণ করে। |
| 803 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 804 | <code>.footer-line {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 805 | <code>  width: 54px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 806 | <code>  height: 1px;</code> | CSS properties: height; enclosing selector-এর presentation নির্ধারণ করে। |
| 807 | <code>  background: #b9cbc3;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 808 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 809 | <code>.footer-credit {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 810 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 811 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 812 | <code>  gap: 6px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 813 | <code>  color: var(--muted);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 814 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 815 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 816 | <code>.footer-credit strong {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 817 | <code>  position: relative;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 818 | <code>  color: var(--green-dark);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 819 | <code>  font-family: &quot;Trebuchet MS&quot;, Arial, sans-serif;</code> | CSS properties: font-family; enclosing selector-এর presentation নির্ধারণ করে। |
| 820 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 821 | <code>  font-weight: 800;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 822 | <code>  letter-spacing: 1.1px;</code> | CSS properties: letter-spacing; enclosing selector-এর presentation নির্ধারণ করে। |
| 823 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 824 | <code>.footer-credit strong::after {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 825 | <code>  content: &quot;&quot;;</code> | CSS properties: content; enclosing selector-এর presentation নির্ধারণ করে। |
| 826 | <code>  position: absolute;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 827 | <code>  right: 0;</code> | CSS properties: right; enclosing selector-এর presentation নির্ধারণ করে। |
| 828 | <code>  bottom: -4px;</code> | CSS properties: bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 829 | <code>  left: 0;</code> | CSS properties: left; enclosing selector-এর presentation নির্ধারণ করে। |
| 830 | <code>  height: 2px;</code> | CSS properties: height; enclosing selector-এর presentation নির্ধারণ করে। |
| 831 | <code>  background: #55a982;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 832 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 833 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 834 | <code>@media (max-width: 1050px) {</code> | Viewport condition অনুযায়ী responsive styles apply করে। |
| 835 | <code>  .metric-grid {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 836 | <code>    grid-template-columns: repeat(3, minmax(0, 1fr));</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 837 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 838 | <code>  .dashboard-grid {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 839 | <code>    grid-template-columns: 1fr;</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 840 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 841 | <code>  .account-grid {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 842 | <code>    grid-template-columns: 1fr;</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 843 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 844 | <code>  .horizontal-form {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 845 | <code>    grid-template-columns: 1fr 1fr;</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 846 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 847 | <code>  .university-name {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 848 | <code>    text-align: left;</code> | CSS properties: text-align; enclosing selector-এর presentation নির্ধারণ করে। |
| 849 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 850 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 851 | <code>@media (max-width: 760px) {</code> | Viewport condition অনুযায়ী responsive styles apply করে। |
| 852 | <code>  .app-header {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 853 | <code>    grid-template-columns: 1fr auto;</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 854 | <code>    padding: 12px 18px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 855 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 856 | <code>  .university-name {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 857 | <code>    display: none;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 858 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 859 | <code>  .connection span,</code> | Style rule/block-এর closing বা continuation। |
| 860 | <code>  .user-menu span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 861 | <code>    display: none;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 862 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 863 | <code>  .header-tools {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 864 | <code>    gap: 9px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 865 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 866 | <code>  .user-menu {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 867 | <code>    padding-left: 9px;</code> | CSS properties: padding-left; enclosing selector-এর presentation নির্ধারণ করে। |
| 868 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 869 | <code>  .nav-inner,</code> | Style rule/block-এর closing বা continuation। |
| 870 | <code>  .workspace {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 871 | <code>    width: calc(100% - 32px);</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 872 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 873 | <code>  .main-nav a {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 874 | <code>    padding: 0 14px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 875 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 876 | <code>  .workspace {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 877 | <code>    padding-top: 24px;</code> | CSS properties: padding-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 878 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 879 | <code>  .dashboard-cover {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 880 | <code>    min-height: 330px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 881 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 882 | <code>  .cover-content {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 883 | <code>    width: 100%;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 884 | <code>    padding: 28px 24px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 885 | <code>    background: rgba(7, 32, 24, 0.86);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 886 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 887 | <code>  .cover-meta {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 888 | <code>    position: absolute;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 889 | <code>    top: 10px;</code> | CSS properties: top; enclosing selector-এর presentation নির্ধারণ করে। |
| 890 | <code>    right: 10px;</code> | CSS properties: right; enclosing selector-এর presentation নির্ধারণ করে। |
| 891 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 892 | <code>  .cover-meta span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 893 | <code>    display: none;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 894 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 895 | <code>  .dashboard-cover h1 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 896 | <code>    margin-top: 28px;</code> | CSS properties: margin-top; enclosing selector-এর presentation নির্ধারণ করে। |
| 897 | <code>    font-size: 31px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 898 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 899 | <code>  .page-heading {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 900 | <code>    min-height: auto;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 901 | <code>    flex-direction: column;</code> | CSS properties: flex-direction; enclosing selector-এর presentation নির্ধারণ করে। |
| 902 | <code>    padding-bottom: 20px;</code> | CSS properties: padding-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 903 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 904 | <code>  .heading-actions {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 905 | <code>    width: 100%;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 906 | <code>    justify-content: space-between;</code> | CSS properties: justify-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 907 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 908 | <code>  .command-strip {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 909 | <code>    align-items: flex-start;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 910 | <code>    flex-direction: column;</code> | CSS properties: flex-direction; enclosing selector-এর presentation নির্ধারণ করে। |
| 911 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 912 | <code>  .command-actions {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 913 | <code>    width: 100%;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 914 | <code>    overflow-x: auto;</code> | CSS properties: overflow-x; enclosing selector-এর presentation নির্ধারণ করে। |
| 915 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 916 | <code>  .command-actions .button {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 917 | <code>    white-space: nowrap;</code> | CSS properties: white-space; enclosing selector-এর presentation নির্ধারণ করে। |
| 918 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 919 | <code>  .metric-grid,</code> | Style rule/block-এর closing বা continuation। |
| 920 | <code>  .metric-grid.compact {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 921 | <code>    grid-template-columns: repeat(2, minmax(0, 1fr));</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 922 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 923 | <code>  .toolbar {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 924 | <code>    align-items: stretch;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 925 | <code>    flex-direction: column;</code> | CSS properties: flex-direction; enclosing selector-এর presentation নির্ধারণ করে। |
| 926 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 927 | <code>  .horizontal-form {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 928 | <code>    grid-template-columns: 1fr;</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 929 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 930 | <code>  .search-field,</code> | Style rule/block-এর closing বা continuation। |
| 931 | <code>  .filter-field {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 932 | <code>    grid-template-columns: 1fr;</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 933 | <code>    gap: 5px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 934 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 935 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 936 | <code>@media (max-width: 440px) {</code> | Viewport condition অনুযায়ী responsive styles apply করে। |
| 937 | <code>  .brand-block {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 938 | <code>    min-width: 0;</code> | CSS properties: min-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 939 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 940 | <code>  .brand-block small {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 941 | <code>    display: none;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 942 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 943 | <code>  .brand-mark {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 944 | <code>    width: 50px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 945 | <code>    flex-basis: 50px;</code> | CSS properties: flex-basis; enclosing selector-এর presentation নির্ধারণ করে। |
| 946 | <code>    font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 947 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 948 | <code>  .connection span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 949 | <code>    display: none;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 950 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 951 | <code>  .metric-grid,</code> | Style rule/block-এর closing বা continuation। |
| 952 | <code>  .metric-grid.compact {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 953 | <code>    grid-template-columns: 1fr;</code> | CSS properties: grid-template-columns; enclosing selector-এর presentation নির্ধারণ করে। |
| 954 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 955 | <code>  .metric {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 956 | <code>    min-height: 112px;</code> | CSS properties: min-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 957 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 958 | <code>  .row-actions {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 959 | <code>    flex-direction: column;</code> | CSS properties: flex-direction; enclosing selector-এর presentation নির্ধারণ করে। |
| 960 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 961 | <code>  .app-footer {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 962 | <code>    gap: 10px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 963 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 964 | <code>  .footer-line {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 965 | <code>    width: 22px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 966 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 967 | <code>  .footer-credit {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 968 | <code>    align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 969 | <code>    flex-direction: column;</code> | CSS properties: flex-direction; enclosing selector-এর presentation নির্ধারণ করে। |
| 970 | <code>    gap: 3px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 971 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 972 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 973 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 974 | <code>button:focus-visible,</code> | CSS properties: button; enclosing selector-এর presentation নির্ধারণ করে। |
| 975 | <code>a:focus-visible {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 976 | <code>  outline: 3px solid var(--green);</code> | CSS properties: outline; enclosing selector-এর presentation নির্ধারণ করে। |
| 977 | <code>  outline-offset: 3px;</code> | CSS properties: outline-offset; enclosing selector-এর presentation নির্ধারণ করে। |
| 978 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 979 | <code>button:disabled {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 980 | <code>  cursor: wait;</code> | CSS properties: cursor; enclosing selector-এর presentation নির্ধারণ করে। |
| 981 | <code>  opacity: 0.6;</code> | CSS properties: opacity; enclosing selector-এর presentation নির্ধারণ করে। |
| 982 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 983 | <code>body:has(.modal.open) {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 984 | <code>  overflow: hidden;</code> | CSS properties: overflow; enclosing selector-এর presentation নির্ধারণ করে। |
| 985 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 986 | <code>@media (prefers-reduced-motion: reduce) {</code> | Viewport condition অনুযায়ী responsive styles apply করে। |
| 987 | <code>  *,</code> | Style rule/block-এর closing বা continuation। |
| 988 | <code>  *::before,</code> | Style rule/block-এর closing বা continuation। |
| 989 | <code>  *::after {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 990 | <code>    animation: none !important;</code> | CSS properties: animation; enclosing selector-এর presentation নির্ধারণ করে। |
| 991 | <code>    transition: none !important;</code> | CSS properties: transition; enclosing selector-এর presentation নির্ধারণ করে। |
| 992 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 993 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 994 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 995 | <code>.audit-filters {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 996 | <code>  align-items: end;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 997 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 998 | <code>.audit-filters label {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 999 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 1000 | <code>  gap: 6px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 1001 | <code>  flex: 1;</code> | CSS properties: flex; enclosing selector-এর presentation নির্ধারণ করে। |
| 1002 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 1003 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 1004 | <code>.audit-filters input,</code> | Style rule/block-এর closing বা continuation। |
| 1005 | <code>.audit-filters select {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 1006 | <code>  width: 100%;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 1007 | <code>  min-width: 0;</code> | CSS properties: min-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 1008 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 1009 | <code>.audit-pagination {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 1010 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 1011 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 1012 | <code>  justify-content: space-between;</code> | CSS properties: justify-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 1013 | <code>  gap: 12px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 1014 | <code>  padding: 18px 0;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 1015 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 1016 | <code>.audit-record-id {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 1017 | <code>  display: block;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 1018 | <code>  color: var(--muted);</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 1019 | <code>  font-size: 10px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 1020 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 1021 | <code>.modal .audit-detail-form {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 1022 | <code>  width: min(880px, 100%);</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 1023 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 1024 | <code>#auditValues td {</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 1025 | <code>  white-space: normal;</code> | CSS properties: white-space; enclosing selector-এর presentation নির্ধারণ করে। |
| 1026 | <code>  overflow-wrap: anywhere;</code> | CSS properties: overflow-wrap; enclosing selector-এর presentation নির্ধারণ করে। |
| 1027 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 1028 | <code>.audit-changed {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 1029 | <code>  background: var(--gold-soft);</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 1030 | <code>}</code> | Style rule/block-এর closing বা continuation। |
