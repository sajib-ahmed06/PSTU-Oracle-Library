(() => {
  const {
    $,
    $$,
    state,
    escapeHtml,
    memberId,
    toast,
    api,
    loadData,
    sortIssues,
    issueRows,
    dateFromToday,
    postForm,
    openRequestedModal,
  } = LibraryApp;

  const heldCount = (id) =>
    (state.reservations || []).filter((r) => r.student_id == id && r.status === "ACTIVE").length;

  function eligibleStudents() {
    return state.students.filter(
      (student) =>
        (student.membership_status || "ACTIVE") === "ACTIVE" &&
        state.issues.filter(
          (issue) => issue.student_id == student.student_id && issue.status === "ISSUED",
        ).length +
          heldCount(student.student_id) <
          3 &&
        !state.fines.some(
          (fine) => fine.student_id == student.student_id && fine.payment_status === "UNPAID",
        ),
    );
  }

  function renderMembers(query = "") {
    const eligible = eligibleStudents();
    const search = query.trim().toLowerCase();
    const matches = eligible.filter((student) =>
      `${memberId(student.student_id)} ${student.roll_no || ""} ${student.registration_no || ""} ${student.name} ${student.department}`
        .toLowerCase()
        .includes(search),
    );
    $("#studentOptions").innerHTML = matches.length
      ? matches
          .map(
            (student) =>
              `<option value="${student.student_id}">${memberId(student.student_id)} / Roll: ${escapeHtml(student.roll_no || "Not assigned")} / Reg: ${escapeHtml(student.registration_no || "Not assigned")} - ${escapeHtml(student.name)} (${escapeHtml(student.department)})</option>`,
          )
          .join("")
      : '<option value="">No matching eligible member</option>';
    $("#eligibilityNote").textContent =
      `${matches.length} of ${eligible.length} eligible members shown`;
    updateAllowance();
  }

  function updateAllowance() {
    const id = $("#studentOptions").value;
    const count = state.issues.filter(
      (issue) => issue.student_id == id && issue.status === "ISSUED",
    ).length;
    $("#loanAllowance").textContent =
      `${count} copies currently borrowed. You can issue up to ${3 - count - heldCount(id)} more, with ${heldCount(id)} active reservations. Use Reservations to issue a held copy.`;
  }

  const copyRequests = {};
  async function renderCopies(suffix = "") {
    const book = $(`#bookOptions${suffix}`);
    const copy = $(`#copyOptions${suffix}`);
    const version = (copyRequests[suffix] = (copyRequests[suffix] || 0) + 1);
    copy.innerHTML = '<option value="">Loading copies...</option>';
    copy.disabled = true;
    if (!book.value) {
      copy.innerHTML = '<option value="">Select a book first</option>';
      return;
    }
    try {
      const copies = await api(`/books/${book.value}/copies`);
      if (version !== copyRequests[suffix]) return;
      copy.innerHTML =
        copies
          .filter((item) => item.status === "AVAILABLE")
          .map((item) => `<option value="${item.copy_id}">Copy #${item.copy_no}</option>`)
          .join("") || '<option value="">No available copies</option>';
      copy.disabled = false;
    } catch (error) {
      if (version === copyRequests[suffix]) {
        copy.innerHTML = '<option value="">Unable to load copies</option>';
        toast(error.message, true);
      }
    }
  }

  function render() {
    const filter = $("#issueFilter").value;
    const issues = sortIssues(
      filter === "ALL" ? state.issues : state.issues.filter((issue) => issue.status === filter),
    );
    $("#issueCount").textContent = `${issues.length} ${issues.length === 1 ? "record" : "records"}`;
    $("#issueTable").innerHTML = issueRows(issues, true);
    $("#bookOptions").innerHTML = state.books
      .filter((book) => book.available_quantity > 0)
      .map(
        (book) =>
          `<option value="${book.book_id}">${escapeHtml(book.title)} (${book.available_quantity} available)</option>`,
      )
      .join("");
    for (const suffix of ["2", "3"]) {
      $(`#bookOptions${suffix}`).innerHTML =
        '<option value="">No additional book</option>' + $("#bookOptions").innerHTML;
      renderCopies(suffix);
    }
    renderCopies();
    renderMembers($("#issueMemberSearch").value);
    $$("[data-return]").forEach((button) => {
      button.onclick = () => returnBook(button.dataset.return);
    });
  }

  async function returnBook(id) {
    if (!confirm("Confirm this book return?")) return;
    if (!state.online) {
      toast("Connect to the database before making changes", true);
      return;
    }
    try {
      await api(`/issues/${id}/return`, { method: "POST" });
      toast("Book returned");
      await loadData(render);
    } catch (error) {
      toast(error.message, true);
    }
  }

  const form = $("#issueModal form");
  form.onsubmit = async (event) => {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(form));
    if (!state.online) {
      toast("Connect to the database before making changes", true);
      return;
    }
    const copies = [];
    for (const suffix of ["", "2", "3"]) {
      if (data[`bookId${suffix}`]) {
        if (!data[`copyId${suffix}`]) {
          toast("Select an available copy for each book", true);
          return;
        }
        copies.push(data[`copyId${suffix}`]);
      }
    }
    const active = state.issues.filter(
      (issue) => issue.student_id == data.studentId && issue.status === "ISSUED",
    ).length;
    if (active + heldCount(data.studentId) + copies.length > 3) {
      toast(`This member can borrow ${3 - active - heldCount(data.studentId)} more copies`, true);
      return;
    }
    if (new Set(copies).size !== copies.length) {
      toast("Select different copies for each loan", true);
      return;
    }
    if (await postForm(form, "/issues")) await loadData(render);
  };
  $("#issueFilter").onchange = render;
  $("#issueMemberSearch").oninput = (event) => renderMembers(event.target.value);
  $("#studentOptions").onchange = updateAllowance;
  for (const suffix of ["", "2", "3"])
    $(`#bookOptions${suffix}`).onchange = () => renderCopies(suffix);
  form.addEventListener("reset", () =>
    window.setTimeout(() => {
      for (const suffix of ["", "2", "3"]) renderCopies(suffix);
      updateAllowance();
    }, 0),
  );
  loadData(() => {
    render();
    openRequestedModal("issueModal");
  });
})();
