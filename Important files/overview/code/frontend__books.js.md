# frontend/books.js

Book search, inventory rows, restock এবং available stock reduction forms পরিচালনা করে।

Source: [মূল file](../../frontend/books.js)। Snapshot 2026-10-04; 82 lines; SHA-256 `82a0aeed2d6c23c02b62ebe6c46e4f8c5ff5681dabccf549097eddeb8f6bf497`।

## Function / object / element inventory

### `render()` — L15

এই page-এর current state ও search/filter থেকে tables/metrics/options তৈরি করে, DOM update করে এবং generated action buttons-এর events bind করে। পাশের পূর্ণ code-এ page-specific fields দেখা যাবে।

### `openRestock(id)` — L42

Existing book metadata form-এ ভরে quantity=1 দেয়, modal open করে এবং quantity select করে।

### `openReduction(id)` — L54

Book ID/form max available copies বসিয়ে reduction modal খোলে।

## সম্পূর্ণ original source

```javascript
(() => {
  const {
    $,
    $$,
    state,
    escapeHtml,
    table,
    toast,
    loadData,
    openModal,
    postForm,
    openRequestedModal,
  } = LibraryApp;

  function render() {
    const query = $("#bookSearch").value.trim().toLowerCase();
    const books = state.books.filter((book) =>
      `${book.title} ${book.author_name} ${book.category_name}`.toLowerCase().includes(query),
    );
    $("#bookCount").textContent = `${books.length} ${books.length === 1 ? "title" : "titles"}`;
    $("#bookTable").innerHTML = table(
      ["Title", "Author", "Category", "Available", "Total", "Actions"],
      books.map(
        (book) => `
      <tr><td><b>${escapeHtml(book.title)}</b></td><td>${escapeHtml(book.author_name)}</td><td>${escapeHtml(book.category_name)}</td><td>${book.available_quantity}</td><td>${book.quantity}</td><td><div class="row-actions"><button class="button small secondary" data-restock="${book.book_id}">Restock</button><button class="button small danger-quiet" data-reduce="${book.book_id}">Reduce</button></div></td></tr>`,
      ),
    );
    $("#authorOptions").innerHTML = (state.meta.authors || [])
      .map((item) => `<option value="${escapeHtml(item.name)}"></option>`)
      .join("");
    $("#categoryOptions").innerHTML = (state.meta.categories || [])
      .map((item) => `<option value="${escapeHtml(item.name)}"></option>`)
      .join("");
    $$("[data-restock]").forEach((button) => {
      button.onclick = () => openRestock(button.dataset.restock);
    });
    $$("[data-reduce]").forEach((button) => {
      button.onclick = () => openReduction(button.dataset.reduce);
    });
  }

  function openRestock(id) {
    const book = state.books.find((item) => item.book_id == id);
    const form = $("#bookModal form");
    form.elements.title.value = book.title;
    form.elements.author.value = book.author_name;
    form.elements.category.value = book.category_name;
    form.elements.publisher.value = book.publisher || "PSTU Library";
    form.elements.quantity.value = 1;
    openModal("bookModal");
    form.elements.quantity.select();
  }

  function openReduction(id) {
    const book = state.books.find((item) => item.book_id == id);
    const form = $("#reduceStockModal form");
    form.elements.bookId.value = book.book_id;
    form.elements.quantity.value = 1;
    form.elements.quantity.max = book.available_quantity;
    $("#reduceStockBook").textContent =
      `${book.title} has ${book.available_quantity} available copies.`;
    openModal("reduceStockModal");
  }

  $$("form[data-kind]").forEach((form) => {
    form.onsubmit = async (event) => {
      event.preventDefault();
      const data = Object.fromEntries(new FormData(form));
      if (!state.online) {
        toast("Connect to the database before making changes", true);
        return;
      }
      const path = form.dataset.kind === "book" ? "/books" : `/books/${data.bookId}/reduce`;
      if (await postForm(form, path)) await loadData(render);
    };
  });
  $("#bookSearch").oninput = render;
  loadData(() => {
    render();
    openRequestedModal("bookModal");
  });
})();
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>(() =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 2 | <code>  const {</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 3 | <code>    $,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 4 | <code>    $$,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 5 | <code>    state,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 6 | <code>    escapeHtml,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 7 | <code>    table,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 8 | <code>    toast,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 9 | <code>    loadData,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 10 | <code>    openModal,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 11 | <code>    postForm,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 12 | <code>    openRequestedModal,</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 13 | <code>  } = LibraryApp;</code> | Local state, DOM reference বা callback/result assign করে। |
| 14 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 15 | <code>  function render() {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 16 | <code>    const query = $(&quot;#bookSearch&quot;).value.trim().toLowerCase();</code> | Local state, DOM reference বা callback/result assign করে। |
| 17 | <code>    const books = state.books.filter((book) =&gt;</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 18 | <code>      `${book.title} ${book.author_name} ${book.category_name}`.toLowerCase().includes(query),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 19 | <code>    );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 20 | <code>    $(&quot;#bookCount&quot;).textContent = `${books.length} ${books.length === 1 ? &quot;title&quot; : &quot;titles&quot;}`;</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 21 | <code>    $(&quot;#bookTable&quot;).innerHTML = table(</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 22 | <code>      [&quot;Title&quot;, &quot;Author&quot;, &quot;Category&quot;, &quot;Available&quot;, &quot;Total&quot;, &quot;Actions&quot;],</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 23 | <code>      books.map(</code> | প্রতিটি record থেকে display row/option/metric বা transformed value তৈরি করে। |
| 24 | <code>        (book) =&gt; `</code> | Local state, DOM reference বা callback/result assign করে। |
| 25 | <code>      &lt;tr&gt;&lt;td&gt;&lt;b&gt;${escapeHtml(book.title)}&lt;/b&gt;&lt;/td&gt;&lt;td&gt;${escapeHtml(book.author_name)}&lt;/td&gt;&lt;td&gt;${escapeHtml(book.category_name)}&lt;/td&gt;&lt;td&gt;${book.available_quantity}&lt;/td&gt;&lt;td&gt;${book.quantity}&lt;/td&gt;&lt;td&gt;&lt;div class=&quot;row-actions&quot;&gt;&lt;button class=&quot;button small secondary&quot; data-restock=&quot;${book.book_id}&quot;&gt;Restock&lt;/button&gt;&lt;button class=&quot;button small danger-quiet&quot; data-reduce=&quot;${book.book_id}&quot;&gt;Reduce&lt;/button&gt;&lt;/div&gt;&lt;/td&gt;&lt;/tr&gt;`,</code> | User/database values escaped display markup-এ রূপান্তর করে। |
| 26 | <code>      ),</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 27 | <code>    );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 28 | <code>    $(&quot;#authorOptions&quot;).innerHTML = (state.meta.authors &#124;&#124; [])</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 29 | <code>      .map((item) =&gt; `&lt;option value=&quot;${escapeHtml(item.name)}&quot;&gt;&lt;/option&gt;`)</code> | User/database values escaped display markup-এ রূপান্তর করে। |
| 30 | <code>      .join(&quot;&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 31 | <code>    $(&quot;#categoryOptions&quot;).innerHTML = (state.meta.categories &#124;&#124; [])</code> | Generated markup DOM-এ বসায়; data values escapeHtml দিয়ে escaped হতে হবে। |
| 32 | <code>      .map((item) =&gt; `&lt;option value=&quot;${escapeHtml(item.name)}&quot;&gt;&lt;/option&gt;`)</code> | User/database values escaped display markup-এ রূপান্তর করে। |
| 33 | <code>      .join(&quot;&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 34 | <code>    $$(&quot;[data-restock]&quot;).forEach((button) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 35 | <code>      button.onclick = () =&gt; openRestock(button.dataset.restock);</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 36 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 37 | <code>    $$(&quot;[data-reduce]&quot;).forEach((button) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 38 | <code>      button.onclick = () =&gt; openReduction(button.dataset.reduce);</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 39 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 40 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 41 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 42 | <code>  function openRestock(id) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 43 | <code>    const book = state.books.find((item) =&gt; item.book_id == id);</code> | Local state, DOM reference বা callback/result assign করে। |
| 44 | <code>    const form = $(&quot;#bookModal form&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 45 | <code>    form.elements.title.value = book.title;</code> | Local state, DOM reference বা callback/result assign করে। |
| 46 | <code>    form.elements.author.value = book.author_name;</code> | Local state, DOM reference বা callback/result assign করে। |
| 47 | <code>    form.elements.category.value = book.category_name;</code> | Local state, DOM reference বা callback/result assign করে। |
| 48 | <code>    form.elements.publisher.value = book.publisher &#124;&#124; &quot;PSTU Library&quot;;</code> | Local state, DOM reference বা callback/result assign করে। |
| 49 | <code>    form.elements.quantity.value = 1;</code> | Local state, DOM reference বা callback/result assign করে। |
| 50 | <code>    openModal(&quot;bookModal&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 51 | <code>    form.elements.quantity.select();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 52 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 53 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 54 | <code>  function openReduction(id) {</code> | Reusable JavaScript function; নিচের block সেই interaction/render logic চালায়। |
| 55 | <code>    const book = state.books.find((item) =&gt; item.book_id == id);</code> | Local state, DOM reference বা callback/result assign করে। |
| 56 | <code>    const form = $(&quot;#reduceStockModal form&quot;);</code> | Local state, DOM reference বা callback/result assign করে। |
| 57 | <code>    form.elements.bookId.value = book.book_id;</code> | Local state, DOM reference বা callback/result assign করে। |
| 58 | <code>    form.elements.quantity.value = 1;</code> | Local state, DOM reference বা callback/result assign করে। |
| 59 | <code>    form.elements.quantity.max = book.available_quantity;</code> | Local state, DOM reference বা callback/result assign করে। |
| 60 | <code>    $(&quot;#reduceStockBook&quot;).textContent =</code> | Plain text DOM-এ বসায়; HTML হিসেবে interpret হয় না। |
| 61 | <code>      `${book.title} has ${book.available_quantity} available copies.`;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 62 | <code>    openModal(&quot;reduceStockModal&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 63 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 64 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 65 | <code>  $$(&quot;form[data-kind]&quot;).forEach((form) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 66 | <code>    form.onsubmit = async (event) =&gt; {</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 67 | <code>      event.preventDefault();</code> | Default form navigation বন্ধ করে controlled API submission চালাতে দেয়। |
| 68 | <code>      const data = Object.fromEntries(new FormData(form));</code> | Form fields বা filters URL-encoded request body/query parameters-এ রূপান্তর করে। |
| 69 | <code>      if (!state.online) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 70 | <code>        toast(&quot;Connect to the database before making changes&quot;, true);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 71 | <code>        return;</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 72 | <code>      }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 73 | <code>      const path = form.dataset.kind === &quot;book&quot; ? &quot;/books&quot; : `/books/${data.bookId}/reduce`;</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 74 | <code>      if (await postForm(form, path)) await loadData(render);</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 75 | <code>    };</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 76 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 77 | <code>  $(&quot;#bookSearch&quot;).oninput = render;</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 78 | <code>  loadData(() =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 79 | <code>    render();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 80 | <code>    openRequestedModal(&quot;bookModal&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 81 | <code>  });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 82 | <code>})();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
