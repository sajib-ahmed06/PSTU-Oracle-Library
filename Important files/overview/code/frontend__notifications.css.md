# frontend/notifications.css

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../frontend/notifications.css)। Snapshot 2026-10-04; 212 lines; SHA-256 `a522d8b934029a11052cdd5aec9a867fca634b9b3e6cdccd19c1dbf9d2916b8d`।

## Function / object / element inventory

CSS selector/property rules source order-এ cascade করে। Later matching declaration আগের equivalent specificity rule override করতে পারে। Media/supports queries condition অনুযায়ী override দেয়। নিচের প্রতিটি line selector/property reading notes দেয়।

## সম্পূর্ণ original source

```css
.notification-center {
  position: relative;
  flex-shrink: 0;
}
.notification-button {
  position: relative;
  display: grid;
  place-items: center;
  width: 44px;
  height: 44px;
  border: 1px solid #d5e3db;
  border-radius: 14px;
  background: #f3f8f4;
  color: #14573f;
  cursor: pointer;
}
.notification-button:hover {
  background: #e5f1e9;
}
.notification-button svg {
  width: 22px;
  height: 22px;
}
.notification-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  min-width: 20px;
  padding: 2px 5px;
  border: 2px solid white;
  border-radius: 20px;
  background: #bd3a2e;
  color: white;
  font-size: 11px;
  font-weight: 800;
}
.notification-panel {
  position: absolute;
  top: 56px;
  right: 0;
  width: min(420px, calc(100vw - 32px));
  border: 1px solid #dbe7df;
  border-radius: 20px;
  background: white;
  box-shadow: 0 22px 65px #133a2929;
  z-index: 100;
  overflow: hidden;
  text-align: left;
}
.notification-panel[hidden],
.notification-badge[hidden] {
  display: none;
}
.notification-heading {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 20px 20px 12px;
}
.notification-heading h2 {
  margin: 0;
  color: #163e2e;
  font-size: 20px;
}
.notification-heading p {
  margin: 5px 0 0;
  color: #65776c;
  font-size: 12px;
}
.notification-close {
  border: 0;
  background: #f0f5f1;
  border-radius: 10px;
  width: 32px;
  height: 32px;
  color: #476353;
  cursor: pointer;
  font-size: 22px;
}
.notification-controls {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  padding: 0 16px 12px;
  border-bottom: 1px solid #e9eee9;
}
.notification-controls button {
  border: 0;
  background: transparent;
  padding: 7px 10px;
  border-radius: 8px;
  color: #65776c;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
}
.notification-controls button[aria-pressed="true"] {
  background: #e9f3ec;
  color: #14573f;
}
.notification-controls #notificationReadAll {
  margin-left: auto;
  color: #14573f;
}
.notification-controls button:disabled {
  opacity: 0.45;
  cursor: default;
}
.notification-list {
  max-height: min(420px, 60vh);
  overflow-y: auto;
  overscroll-behavior: contain;
}
.notification-item {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  padding: 16px 20px;
  color: #263f30;
  text-decoration: none;
  border-bottom: 1px solid #eef2ef;
}
.notification-item:hover {
  background: #f3f8f4;
}
.notification-item.is-unread {
  background: #f7fbf8;
}
.notification-symbol {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  flex: 0 0 36px;
  border-radius: 12px;
  background: #dfeee4;
  color: #14573f;
  font-weight: 800;
}
.notification-symbol.fine {
  background: #fff0db;
  color: #925908;
  font-size: 21px;
}
.notification-symbol.due {
  background: #e5edf9;
  color: #315f9a;
}
.notification-copy {
  display: grid;
  gap: 5px;
  min-width: 0;
}
.notification-copy strong {
  font-size: 13px;
  line-height: 1.4;
}
.notification-copy span {
  font-size: 12px;
  line-height: 1.5;
  overflow-wrap: anywhere;
}
.notification-copy small {
  font-size: 11px;
  line-height: 1.5;
  color: #6c7b70;
}
.notification-unread-dot {
  width: 7px;
  height: 7px;
  flex: 0 0 7px;
  margin: 6px 0 0 auto;
  border-radius: 50%;
  background: #16835c;
}
.is-read .notification-unread-dot {
  visibility: hidden;
}
.notification-empty {
  display: grid;
  gap: 8px;
  padding: 36px 20px;
  text-align: center;
  color: #3e5c48;
}
.notification-empty span {
  font-size: 13px;
  color: #6c7b70;
}
.notification-freshness {
  margin: 0;
  padding: 12px 16px;
  background: #f4f7f4;
  font-size: 11px;
  color: #697c6e;
}
.notification-button:focus-visible,
.notification-panel button:focus-visible,
.notification-item:focus-visible {
  outline: 3px solid #85b69a;
  outline-offset: 2px;
}
@media (max-width: 700px) {
  .notification-panel {
    position: fixed;
    top: 110px;
    left: 16px;
    right: 16px;
    width: auto;
  }
}
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>.notification-center {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 2 | <code>  position: relative;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 3 | <code>  flex-shrink: 0;</code> | CSS properties: flex-shrink; enclosing selector-এর presentation নির্ধারণ করে। |
| 4 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 5 | <code>.notification-button {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 6 | <code>  position: relative;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 7 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 8 | <code>  place-items: center;</code> | CSS properties: place-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 9 | <code>  width: 44px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 10 | <code>  height: 44px;</code> | CSS properties: height; enclosing selector-এর presentation নির্ধারণ করে। |
| 11 | <code>  border: 1px solid #d5e3db;</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 12 | <code>  border-radius: 14px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 13 | <code>  background: #f3f8f4;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 14 | <code>  color: #14573f;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 15 | <code>  cursor: pointer;</code> | CSS properties: cursor; enclosing selector-এর presentation নির্ধারণ করে। |
| 16 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 17 | <code>.notification-button:hover {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 18 | <code>  background: #e5f1e9;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 19 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 20 | <code>.notification-button svg {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 21 | <code>  width: 22px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 22 | <code>  height: 22px;</code> | CSS properties: height; enclosing selector-এর presentation নির্ধারণ করে। |
| 23 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 24 | <code>.notification-badge {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 25 | <code>  position: absolute;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 26 | <code>  top: -5px;</code> | CSS properties: top; enclosing selector-এর presentation নির্ধারণ করে। |
| 27 | <code>  right: -5px;</code> | CSS properties: right; enclosing selector-এর presentation নির্ধারণ করে। |
| 28 | <code>  min-width: 20px;</code> | CSS properties: min-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 29 | <code>  padding: 2px 5px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 30 | <code>  border: 2px solid white;</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 31 | <code>  border-radius: 20px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 32 | <code>  background: #bd3a2e;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 33 | <code>  color: white;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 34 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 35 | <code>  font-weight: 800;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 36 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 37 | <code>.notification-panel {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 38 | <code>  position: absolute;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 39 | <code>  top: 56px;</code> | CSS properties: top; enclosing selector-এর presentation নির্ধারণ করে। |
| 40 | <code>  right: 0;</code> | CSS properties: right; enclosing selector-এর presentation নির্ধারণ করে। |
| 41 | <code>  width: min(420px, calc(100vw - 32px));</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 42 | <code>  border: 1px solid #dbe7df;</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 43 | <code>  border-radius: 20px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 44 | <code>  background: white;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 45 | <code>  box-shadow: 0 22px 65px #133a2929;</code> | CSS properties: box-shadow; enclosing selector-এর presentation নির্ধারণ করে। |
| 46 | <code>  z-index: 100;</code> | CSS properties: z-index; enclosing selector-এর presentation নির্ধারণ করে। |
| 47 | <code>  overflow: hidden;</code> | CSS properties: overflow; enclosing selector-এর presentation নির্ধারণ করে। |
| 48 | <code>  text-align: left;</code> | CSS properties: text-align; enclosing selector-এর presentation নির্ধারণ করে। |
| 49 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 50 | <code>.notification-panel[hidden],</code> | Style rule/block-এর closing বা continuation। |
| 51 | <code>.notification-badge[hidden] {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 52 | <code>  display: none;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 53 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 54 | <code>.notification-heading {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 55 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 56 | <code>  justify-content: space-between;</code> | CSS properties: justify-content; enclosing selector-এর presentation নির্ধারণ করে। |
| 57 | <code>  align-items: center;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 58 | <code>  gap: 16px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 59 | <code>  padding: 20px 20px 12px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 60 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 61 | <code>.notification-heading h2 {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 62 | <code>  margin: 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 63 | <code>  color: #163e2e;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 64 | <code>  font-size: 20px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 65 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 66 | <code>.notification-heading p {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 67 | <code>  margin: 5px 0 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 68 | <code>  color: #65776c;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 69 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 70 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 71 | <code>.notification-close {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 72 | <code>  border: 0;</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 73 | <code>  background: #f0f5f1;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 74 | <code>  border-radius: 10px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 75 | <code>  width: 32px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 76 | <code>  height: 32px;</code> | CSS properties: height; enclosing selector-এর presentation নির্ধারণ করে। |
| 77 | <code>  color: #476353;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 78 | <code>  cursor: pointer;</code> | CSS properties: cursor; enclosing selector-এর presentation নির্ধারণ করে। |
| 79 | <code>  font-size: 22px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 80 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 81 | <code>.notification-controls {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 82 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 83 | <code>  gap: 6px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 84 | <code>  flex-wrap: wrap;</code> | CSS properties: flex-wrap; enclosing selector-এর presentation নির্ধারণ করে। |
| 85 | <code>  padding: 0 16px 12px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 86 | <code>  border-bottom: 1px solid #e9eee9;</code> | CSS properties: border-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 87 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 88 | <code>.notification-controls button {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 89 | <code>  border: 0;</code> | CSS properties: border; enclosing selector-এর presentation নির্ধারণ করে। |
| 90 | <code>  background: transparent;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 91 | <code>  padding: 7px 10px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 92 | <code>  border-radius: 8px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 93 | <code>  color: #65776c;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 94 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 95 | <code>  font-weight: 700;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 96 | <code>  cursor: pointer;</code> | CSS properties: cursor; enclosing selector-এর presentation নির্ধারণ করে। |
| 97 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 98 | <code>.notification-controls button[aria-pressed=&quot;true&quot;] {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 99 | <code>  background: #e9f3ec;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 100 | <code>  color: #14573f;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 101 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 102 | <code>.notification-controls #notificationReadAll {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 103 | <code>  margin-left: auto;</code> | CSS properties: margin-left; enclosing selector-এর presentation নির্ধারণ করে। |
| 104 | <code>  color: #14573f;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 105 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 106 | <code>.notification-controls button:disabled {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 107 | <code>  opacity: 0.45;</code> | CSS properties: opacity; enclosing selector-এর presentation নির্ধারণ করে। |
| 108 | <code>  cursor: default;</code> | CSS properties: cursor; enclosing selector-এর presentation নির্ধারণ করে। |
| 109 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 110 | <code>.notification-list {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 111 | <code>  max-height: min(420px, 60vh);</code> | CSS properties: max-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 112 | <code>  overflow-y: auto;</code> | CSS properties: overflow-y; enclosing selector-এর presentation নির্ধারণ করে। |
| 113 | <code>  overscroll-behavior: contain;</code> | CSS properties: overscroll-behavior; enclosing selector-এর presentation নির্ধারণ করে। |
| 114 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 115 | <code>.notification-item {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 116 | <code>  display: flex;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 117 | <code>  gap: 12px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 118 | <code>  align-items: flex-start;</code> | CSS properties: align-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 119 | <code>  padding: 16px 20px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 120 | <code>  color: #263f30;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 121 | <code>  text-decoration: none;</code> | CSS properties: text-decoration; enclosing selector-এর presentation নির্ধারণ করে। |
| 122 | <code>  border-bottom: 1px solid #eef2ef;</code> | CSS properties: border-bottom; enclosing selector-এর presentation নির্ধারণ করে। |
| 123 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 124 | <code>.notification-item:hover {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 125 | <code>  background: #f3f8f4;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 126 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 127 | <code>.notification-item.is-unread {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 128 | <code>  background: #f7fbf8;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 129 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 130 | <code>.notification-symbol {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 131 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 132 | <code>  place-items: center;</code> | CSS properties: place-items; enclosing selector-এর presentation নির্ধারণ করে। |
| 133 | <code>  width: 36px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 134 | <code>  height: 36px;</code> | CSS properties: height; enclosing selector-এর presentation নির্ধারণ করে। |
| 135 | <code>  flex: 0 0 36px;</code> | CSS properties: flex; enclosing selector-এর presentation নির্ধারণ করে। |
| 136 | <code>  border-radius: 12px;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 137 | <code>  background: #dfeee4;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 138 | <code>  color: #14573f;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 139 | <code>  font-weight: 800;</code> | CSS properties: font-weight; enclosing selector-এর presentation নির্ধারণ করে। |
| 140 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 141 | <code>.notification-symbol.fine {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 142 | <code>  background: #fff0db;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 143 | <code>  color: #925908;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 144 | <code>  font-size: 21px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 145 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 146 | <code>.notification-symbol.due {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 147 | <code>  background: #e5edf9;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 148 | <code>  color: #315f9a;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 149 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 150 | <code>.notification-copy {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 151 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 152 | <code>  gap: 5px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 153 | <code>  min-width: 0;</code> | CSS properties: min-width; enclosing selector-এর presentation নির্ধারণ করে। |
| 154 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 155 | <code>.notification-copy strong {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 156 | <code>  font-size: 13px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 157 | <code>  line-height: 1.4;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 158 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 159 | <code>.notification-copy span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 160 | <code>  font-size: 12px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 161 | <code>  line-height: 1.5;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 162 | <code>  overflow-wrap: anywhere;</code> | CSS properties: overflow-wrap; enclosing selector-এর presentation নির্ধারণ করে। |
| 163 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 164 | <code>.notification-copy small {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 165 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 166 | <code>  line-height: 1.5;</code> | CSS properties: line-height; enclosing selector-এর presentation নির্ধারণ করে। |
| 167 | <code>  color: #6c7b70;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 168 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 169 | <code>.notification-unread-dot {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 170 | <code>  width: 7px;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 171 | <code>  height: 7px;</code> | CSS properties: height; enclosing selector-এর presentation নির্ধারণ করে। |
| 172 | <code>  flex: 0 0 7px;</code> | CSS properties: flex; enclosing selector-এর presentation নির্ধারণ করে। |
| 173 | <code>  margin: 6px 0 0 auto;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 174 | <code>  border-radius: 50%;</code> | CSS properties: border-radius; enclosing selector-এর presentation নির্ধারণ করে। |
| 175 | <code>  background: #16835c;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 176 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 177 | <code>.is-read .notification-unread-dot {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 178 | <code>  visibility: hidden;</code> | CSS properties: visibility; enclosing selector-এর presentation নির্ধারণ করে। |
| 179 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 180 | <code>.notification-empty {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 181 | <code>  display: grid;</code> | CSS properties: display; enclosing selector-এর presentation নির্ধারণ করে। |
| 182 | <code>  gap: 8px;</code> | CSS properties: gap; enclosing selector-এর presentation নির্ধারণ করে। |
| 183 | <code>  padding: 36px 20px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 184 | <code>  text-align: center;</code> | CSS properties: text-align; enclosing selector-এর presentation নির্ধারণ করে। |
| 185 | <code>  color: #3e5c48;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 186 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 187 | <code>.notification-empty span {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 188 | <code>  font-size: 13px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 189 | <code>  color: #6c7b70;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 190 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 191 | <code>.notification-freshness {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 192 | <code>  margin: 0;</code> | CSS properties: margin; enclosing selector-এর presentation নির্ধারণ করে। |
| 193 | <code>  padding: 12px 16px;</code> | CSS properties: padding; enclosing selector-এর presentation নির্ধারণ করে। |
| 194 | <code>  background: #f4f7f4;</code> | CSS properties: background; enclosing selector-এর presentation নির্ধারণ করে। |
| 195 | <code>  font-size: 11px;</code> | CSS properties: font-size; enclosing selector-এর presentation নির্ধারণ করে। |
| 196 | <code>  color: #697c6e;</code> | CSS properties: color; enclosing selector-এর presentation নির্ধারণ করে। |
| 197 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 198 | <code>.notification-button:focus-visible,</code> | CSS properties: notification-button; enclosing selector-এর presentation নির্ধারণ করে। |
| 199 | <code>.notification-panel button:focus-visible,</code> | CSS properties: button; enclosing selector-এর presentation নির্ধারণ করে। |
| 200 | <code>.notification-item:focus-visible {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 201 | <code>  outline: 3px solid #85b69a;</code> | CSS properties: outline; enclosing selector-এর presentation নির্ধারণ করে। |
| 202 | <code>  outline-offset: 2px;</code> | CSS properties: outline-offset; enclosing selector-এর presentation নির্ধারণ করে। |
| 203 | <code>}</code> | Style rule/block-এর closing বা continuation। |
| 204 | <code>@media (max-width: 700px) {</code> | Viewport condition অনুযায়ী responsive styles apply করে। |
| 205 | <code>  .notification-panel {</code> | Selector-এর matched elements-এর styles শুরু করে; properties layout/color/spacing/interaction নির্ধারণ করে। |
| 206 | <code>    position: fixed;</code> | CSS properties: position; enclosing selector-এর presentation নির্ধারণ করে। |
| 207 | <code>    top: 110px;</code> | CSS properties: top; enclosing selector-এর presentation নির্ধারণ করে। |
| 208 | <code>    left: 16px;</code> | CSS properties: left; enclosing selector-এর presentation নির্ধারণ করে। |
| 209 | <code>    right: 16px;</code> | CSS properties: right; enclosing selector-এর presentation নির্ধারণ করে। |
| 210 | <code>    width: auto;</code> | CSS properties: width; enclosing selector-এর presentation নির্ধারণ করে। |
| 211 | <code>  }</code> | Style rule/block-এর closing বা continuation। |
| 212 | <code>}</code> | Style rule/block-এর closing বা continuation। |
