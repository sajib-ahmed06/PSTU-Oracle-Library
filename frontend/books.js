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
