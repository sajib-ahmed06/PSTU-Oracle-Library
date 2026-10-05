"use strict";

// Staff view for creating holds and issuing reserved copies.
window.ReservationDesk = {
  create(context) {
    const { $, state, api, escapeHtml: e, toast, memberId, action, reservationTable } = context;
    async function renderManagement() {
      try {
        const reservations = state.reservations || (await api("/reservations"));
        $("#reservationCount").textContent =
          `${reservations.filter((r) => r.status === "ACTIVE").length} active reservations`;
        reservationTable(reservations);
        const memberOptions =
          '<option value="">Choose a member</option>' +
          state.students
            .filter((s) => s.membership_status === "ACTIVE")
            .map(
              (s) =>
                `<option value="${s.student_id}">${e(s.name)} / ${e(s.roll_no || memberId(s.student_id))}</option>`,
            )
            .join("");
        const selectedMember = $("#reserveMember").value;
        $("#reserveMember").innerHTML = memberOptions;
        $("#reserveMember").value = selectedMember;
        const previous = $("#reserveBook").value;
        $("#reserveBook").innerHTML =
          '<option value="">Choose an available book</option>' +
          state.books
            .filter((b) => Number(b.available_quantity) > 0)
            .map(
              (b) =>
                `<option value="${b.book_id}">${e(b.title)} (${b.available_quantity} available)</option>`,
            )
            .join("");
        $("#reserveBook").value = previous;
      } catch (error) {
        toast(error.message, true);
      }
    }

    function bind() {
      $("#reserveForm").onsubmit = async (event) => {
        event.preventDefault();
        const form = event.currentTarget;
        if (await action($("button", form), "/reservations", new FormData(form))) form.reset();
      };
    }
    return { render: renderManagement, bind };
  },
};
