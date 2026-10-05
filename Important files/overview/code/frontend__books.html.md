# frontend/books.html

এই page-এর semantic HTML structure: header placeholder, content sections, forms/dialogs এবং stylesheet/script links। Matching controller JavaScript interactions চালায়।

Source: [মূল file](../../frontend/books.html)। Snapshot 2026-10-04; 86 lines; SHA-256 `d2f2b380c7c5d213fed6548e27225f3ac53dd1d498cad288d821bb990cd66dd2`।

## Function / object / element inventory

- DOM IDs: `appHeader`, `bookSearch`, `bookCount`, `bookTable`, `bookModal`, `authorOptions`, `categoryOptions`, `reduceStockModal`, `reduceStockBook`, `toast`
- Form keys: `title`, `author`, `category`, `publisher`, `quantity`, `bookId`, `quantity`
- Loaded/linked resources: `/static/styles.css?v=members-audit-1`, `/static/polish.css?v=1`, `/static/notifications.css?v=due-2`, `/static/notifications.js?v=reminders-4`, `/static/shared.js?v=priority-3`, `/static/books.js`

## সম্পূর্ণ original source

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Books | PSTU Library</title>
    <link rel="stylesheet" href="/static/styles.css?v=members-audit-1" />
    <link rel="stylesheet" href="/static/polish.css?v=1" />
    <link rel="stylesheet" href="/static/notifications.css?v=due-2" />
  </head>
  <body data-page="books">
    <div id="appHeader"></div>
    <main class="workspace">
      <section class="page-heading">
        <div>
          <p class="eyebrow">Collection</p>
          <h1>Book inventory</h1>
          <p class="heading-copy">Manage titles and physical stock from one register.</p>
        </div>
        <button class="button primary" data-open="bookModal">Add or restock</button>
      </section>
      <section class="toolbar">
        <label class="search-field"
          ><span>Search books</span
          ><input id="bookSearch" type="search" placeholder="Title, author or category" /></label
        ><span class="record-count" id="bookCount"></span>
      </section>
      <section class="surface"><div class="table-wrap" id="bookTable"></div></section>
    </main>
    <div class="modal" id="bookModal" aria-hidden="true">
      <form data-kind="book">
        <div class="modal-heading">
          <div>
            <span class="section-label">Inventory</span>
            <h2>Add or restock book</h2>
          </div>
          <button type="button" class="icon-button cancel" aria-label="Close">&times;</button>
        </div>
        <label>Title<input name="title" required /></label
        ><label
          >Author<input
            name="author"
            list="authorOptions"
            placeholder="Type an author name"
            required /><datalist id="authorOptions"></datalist></label
        ><label
          >Category<input
            name="category"
            list="categoryOptions"
            placeholder="Type a category"
            required /><datalist id="categoryOptions"></datalist></label
        ><label>Publisher<input name="publisher" value="PSTU Library" /></label
        ><label
          >Copies to add<input name="quantity" type="number" value="1" min="1" required
        /></label>
        <div class="form-actions">
          <button type="button" class="button secondary cancel">Cancel</button
          ><button class="button primary">Save stock</button>
        </div>
      </form>
    </div>
    <div class="modal" id="reduceStockModal" aria-hidden="true">
      <form data-kind="reduceStock">
        <div class="modal-heading">
          <div>
            <span class="section-label">Inventory adjustment</span>
            <h2>Reduce stock</h2>
          </div>
          <button type="button" class="icon-button cancel" aria-label="Close">&times;</button>
        </div>
        <p class="form-note" id="reduceStockBook"></p>
        <input name="bookId" type="hidden" /><label
          >Lost or damaged copies<input name="quantity" type="number" value="1" min="1" required
        /></label>
        <div class="form-actions">
          <button type="button" class="button secondary cancel">Cancel</button
          ><button class="button danger">Reduce stock</button>
        </div>
      </form>
    </div>
    <div id="toast" role="status" aria-live="polite"></div>
    <script src="/static/notifications.js?v=reminders-4"></script>
    <script src="/static/shared.js?v=priority-3"></script>
    <script src="/static/books.js"></script>
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
| 6 | <code>    &lt;title&gt;Books &#124; PSTU Library&lt;/title&gt;</code> | title: HTML structure/content |
| 7 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/styles.css?v=members-audit-1&quot; /&gt;</code> | link: stylesheet/resource load |
| 8 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/polish.css?v=1&quot; /&gt;</code> | link: stylesheet/resource load |
| 9 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/notifications.css?v=due-2&quot; /&gt;</code> | link: stylesheet/resource load |
| 10 | <code>  &lt;/head&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 11 | <code>  &lt;body data-page=&quot;books&quot;&gt;</code> | body: HTML structure/content |
| 12 | <code>    &lt;div id=&quot;appHeader&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 13 | <code>    &lt;main class=&quot;workspace&quot;&gt;</code> | main: primary page content |
| 14 | <code>      &lt;section class=&quot;page-heading&quot;&gt;</code> | section: related UI content grouping |
| 15 | <code>        &lt;div&gt;</code> | div: layout/dynamic content container |
| 16 | <code>          &lt;p class=&quot;eyebrow&quot;&gt;Collection&lt;/p&gt;</code> | p: description/help text |
| 17 | <code>          &lt;h1&gt;Book inventory&lt;/h1&gt;</code> | h1: page heading |
| 18 | <code>          &lt;p class=&quot;heading-copy&quot;&gt;Manage titles and physical stock from one register.&lt;/p&gt;</code> | p: description/help text |
| 19 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 20 | <code>        &lt;button class=&quot;button primary&quot; data-open=&quot;bookModal&quot;&gt;Add or restock&lt;/button&gt;</code> | button: action/submit/cancel control |
| 21 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 22 | <code>      &lt;section class=&quot;toolbar&quot;&gt;</code> | section: related UI content grouping |
| 23 | <code>        &lt;label class=&quot;search-field&quot;</code> | label: field-এর readable label |
| 24 | <code>          &gt;&lt;span&gt;Search books&lt;/span</code> | span: HTML structure/content |
| 25 | <code>          &gt;&lt;input id=&quot;bookSearch&quot; type=&quot;search&quot; placeholder=&quot;Title, author or category&quot; /&gt;&lt;/label</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 26 | <code>        &gt;&lt;span class=&quot;record-count&quot; id=&quot;bookCount&quot;&gt;&lt;/span&gt;</code> | span: HTML structure/content |
| 27 | <code>      &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 28 | <code>      &lt;section class=&quot;surface&quot;&gt;&lt;div class=&quot;table-wrap&quot; id=&quot;bookTable&quot;&gt;&lt;/div&gt;&lt;/section&gt;</code> | section: related UI content grouping; div: layout/dynamic content container |
| 29 | <code>    &lt;/main&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 30 | <code>    &lt;div class=&quot;modal&quot; id=&quot;bookModal&quot; aria-hidden=&quot;true&quot;&gt;</code> | div: layout/dynamic content container |
| 31 | <code>      &lt;form data-kind=&quot;book&quot;&gt;</code> | form: submit-able input grouping |
| 32 | <code>        &lt;div class=&quot;modal-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 33 | <code>          &lt;div&gt;</code> | div: layout/dynamic content container |
| 34 | <code>            &lt;span class=&quot;section-label&quot;&gt;Inventory&lt;/span&gt;</code> | span: HTML structure/content |
| 35 | <code>            &lt;h2&gt;Add or restock book&lt;/h2&gt;</code> | h2: section/dialog heading |
| 36 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 37 | <code>          &lt;button type=&quot;button&quot; class=&quot;icon-button cancel&quot; aria-label=&quot;Close&quot;&gt;&amp;times;&lt;/button&gt;</code> | button: action/submit/cancel control |
| 38 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 39 | <code>        &lt;label&gt;Title&lt;input name=&quot;title&quot; required /&gt;&lt;/label</code> | label: field-এর readable label; input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 40 | <code>        &gt;&lt;label</code> | label: field-এর readable label |
| 41 | <code>          &gt;Author&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 42 | <code>            name=&quot;author&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 43 | <code>            list=&quot;authorOptions&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 44 | <code>            placeholder=&quot;Type an author name&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 45 | <code>            required /&gt;&lt;datalist id=&quot;authorOptions&quot;&gt;&lt;/datalist&gt;&lt;/label</code> | datalist: HTML structure/content |
| 46 | <code>        &gt;&lt;label</code> | label: field-এর readable label |
| 47 | <code>          &gt;Category&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 48 | <code>            name=&quot;category&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 49 | <code>            list=&quot;categoryOptions&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 50 | <code>            placeholder=&quot;Type a category&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 51 | <code>            required /&gt;&lt;datalist id=&quot;categoryOptions&quot;&gt;&lt;/datalist&gt;&lt;/label</code> | datalist: HTML structure/content |
| 52 | <code>        &gt;&lt;label&gt;Publisher&lt;input name=&quot;publisher&quot; value=&quot;PSTU Library&quot; /&gt;&lt;/label</code> | label: field-এর readable label; input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 53 | <code>        &gt;&lt;label</code> | label: field-এর readable label |
| 54 | <code>          &gt;Copies to add&lt;input name=&quot;quantity&quot; type=&quot;number&quot; value=&quot;1&quot; min=&quot;1&quot; required</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 55 | <code>        /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 56 | <code>        &lt;div class=&quot;form-actions&quot;&gt;</code> | div: layout/dynamic content container |
| 57 | <code>          &lt;button type=&quot;button&quot; class=&quot;button secondary cancel&quot;&gt;Cancel&lt;/button</code> | button: action/submit/cancel control |
| 58 | <code>          &gt;&lt;button class=&quot;button primary&quot;&gt;Save stock&lt;/button&gt;</code> | button: action/submit/cancel control |
| 59 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 60 | <code>      &lt;/form&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 61 | <code>    &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 62 | <code>    &lt;div class=&quot;modal&quot; id=&quot;reduceStockModal&quot; aria-hidden=&quot;true&quot;&gt;</code> | div: layout/dynamic content container |
| 63 | <code>      &lt;form data-kind=&quot;reduceStock&quot;&gt;</code> | form: submit-able input grouping |
| 64 | <code>        &lt;div class=&quot;modal-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 65 | <code>          &lt;div&gt;</code> | div: layout/dynamic content container |
| 66 | <code>            &lt;span class=&quot;section-label&quot;&gt;Inventory adjustment&lt;/span&gt;</code> | span: HTML structure/content |
| 67 | <code>            &lt;h2&gt;Reduce stock&lt;/h2&gt;</code> | h2: section/dialog heading |
| 68 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 69 | <code>          &lt;button type=&quot;button&quot; class=&quot;icon-button cancel&quot; aria-label=&quot;Close&quot;&gt;&amp;times;&lt;/button&gt;</code> | button: action/submit/cancel control |
| 70 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 71 | <code>        &lt;p class=&quot;form-note&quot; id=&quot;reduceStockBook&quot;&gt;&lt;/p&gt;</code> | p: description/help text |
| 72 | <code>        &lt;input name=&quot;bookId&quot; type=&quot;hidden&quot; /&gt;&lt;label</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation; label: field-এর readable label |
| 73 | <code>          &gt;Lost or damaged copies&lt;input name=&quot;quantity&quot; type=&quot;number&quot; value=&quot;1&quot; min=&quot;1&quot; required</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 74 | <code>        /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 75 | <code>        &lt;div class=&quot;form-actions&quot;&gt;</code> | div: layout/dynamic content container |
| 76 | <code>          &lt;button type=&quot;button&quot; class=&quot;button secondary cancel&quot;&gt;Cancel&lt;/button</code> | button: action/submit/cancel control |
| 77 | <code>          &gt;&lt;button class=&quot;button danger&quot;&gt;Reduce stock&lt;/button&gt;</code> | button: action/submit/cancel control |
| 78 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 79 | <code>      &lt;/form&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 80 | <code>    &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 81 | <code>    &lt;div id=&quot;toast&quot; role=&quot;status&quot; aria-live=&quot;polite&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 82 | <code>    &lt;script src=&quot;/static/notifications.js?v=reminders-4&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 83 | <code>    &lt;script src=&quot;/static/shared.js?v=priority-3&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 84 | <code>    &lt;script src=&quot;/static/books.js&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 85 | <code>  &lt;/body&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 86 | <code>&lt;/html&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
