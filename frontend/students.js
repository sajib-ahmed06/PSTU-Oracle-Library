(() => {
  const {
    $,
    $$,
    state,
    escapeHtml,
    memberId,
    table,
    toast,
    api,
    loadData,
    postForm,
    openRequestedModal,
    openModal,
  } = LibraryApp;

  function render() {
    const query = $("#studentSearch").value.trim().toLowerCase();
    const students = state.students.filter((student) =>
      `${memberId(student.student_id)} ${student.roll_no || ""} ${student.registration_no || ""} ${student.academic_session || ""} ${student.name} ${student.department} ${student.phone} ${student.email}`
        .toLowerCase()
        .includes(query),
    );
    $("#studentCount").textContent =
      `${students.length} ${students.length === 1 ? "member" : "members"}`;
    $("#studentTable").innerHTML = table(
      [
        "Member ID",
        "ID / Roll",
        "Registration No.",
        "Student",
        "Session",
        "Department",
        "Phone",
        "Email",
        "Status",
        "Action",
      ],
      students.map((student) => {
        const status = student.membership_status || "ACTIVE";
        const action = status === "ACTIVE" ? "Disable" : "Enable";
        return `<tr><td><span class="member-id">${memberId(student.student_id)}</span></td><td>${escapeHtml(student.roll_no || "Not assigned")}</td><td>${escapeHtml(student.registration_no || "Not assigned")}</td><td><b>${escapeHtml(student.name)}</b></td><td>${escapeHtml(student.academic_session || "Not assigned")}</td><td>${escapeHtml(student.department)}</td><td>${escapeHtml(student.phone)}</td><td>${escapeHtml(student.email)}</td><td><span class="pill ${status.toLowerCase()}">${status}</span></td><td><div class="row-actions"><button class="button small secondary" data-identity="${student.student_id}">Edit</button><button class="button small ${action === "Disable" ? "danger-quiet" : "primary"}" data-toggle="${student.student_id}">${action}</button></div></td></tr>`;
      }),
    );
    $$("[data-identity]").forEach((button) => {
      button.onclick = () => {
        const member = state.students.find((item) => item.student_id == button.dataset.identity);
        const form = $("#identityModal form");
        form.elements.student_id.value = member.student_id;
        for (const field of [
          "academic_session",
          "name",
          "department",
          "phone",
          "email",
          "membership_status",
        ]) {
          form.elements[field].value =
            member[field] || (field === "membership_status" ? "ACTIVE" : "");
        }
        form.elements.roll_no.value = member.roll_no || "";
        form.elements.registration_no.value = member.registration_no || "";
        $("#identityMember").textContent = `${memberId(member.student_id)} - ${member.name}`;
        openModal("identityModal");
      };
    });
    $$("[data-toggle]").forEach((button) => {
      button.onclick = () => toggleMembership(button.dataset.toggle);
    });
  }

  async function toggleMembership(id) {
    const student = state.students.find((item) => item.student_id == id);
    const disabling = (student.membership_status || "ACTIVE") === "ACTIVE";
    if (!confirm(`${disabling ? "Disable" : "Enable"} ${student.name}'s membership?`)) return;
    if (!state.online) {
      toast("Connect to the database before making changes", true);
      return;
    }
    try {
      await api(`/students/${id}/toggle`, { method: "POST" });
      toast("Membership updated");
      await loadData(render);
    } catch (error) {
      toast(error.message, true);
    }
  }

  const form = $("#studentModal form");
  form.onsubmit = async (event) => {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(form));
    if (!state.online) {
      toast("Connect to the database before making changes", true);
      return;
    }
    if (await postForm(form, "/students")) await loadData(render);
  };
  $("#identityModal form").onsubmit = async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    if (await postForm(form, `/students/${form.elements.student_id.value}/edit`))
      await loadData(render);
  };
  $("#studentSearch").oninput = render;
  loadData(() => {
    render();
    openRequestedModal("studentModal");
  });
})();
