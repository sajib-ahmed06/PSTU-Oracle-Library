const assert = require("node:assert/strict");
const { test } = require("node:test");
const fs = require("node:fs");
const vm = require("node:vm");

async function page(snapshot, role = "student") {
  const nodes = {};
  const button = { disabled: false, dataset: { reserve: "3" } };
  const requests = [];
  const state = { online: false, ...snapshot };
  const collectButton = { disabled: false, dataset: { collect: "12" } };
  const $ = (selector) =>
    (nodes[selector] ||= {
      value: "",
      textContent: "",
      innerHTML: "",
      classList: { add() {}, remove() {} },
    });
  const app = {
    $,
    $$: (selector) => {
      if (selector === "[data-reserve]") return [button];
      if (selector === "[data-collect]" && role !== "student") return [collectButton];
      return [];
    },
    state,
    escapeHtml: String,
    memberId: (id) => `PSTU-${id}`,
    table: (headers, rows) => rows.join(""),
    toast() {},
    loadData: async (render) => {
      state.online = true;
      await render();
    },
    api: async (path, options) => {
      requests.push({ path, options });
      return options ? { message: "Reserved" } : snapshot;
    },
  };
  vm.runInNewContext(
    fs.readFileSync("frontend/notifications.js", "utf8") +
      "\n" +
      fs.readFileSync("frontend/member-dashboard.js", "utf8") +
      "\n" +
      fs.readFileSync("frontend/reservation-desk.js", "utf8") +
      "\n" +
      fs.readFileSync("frontend/reservations.js", "utf8"),
    {
      LibraryApp: app,
      document: { body: { dataset: { page: role } }, hidden: false },
      window: { setInterval() {} },
      confirm: () => true,
      URLSearchParams,
    },
  );
  await $("#refreshButton").onclick();
  return { nodes, button, collectButton, requests };
}

const snapshot = () => ({
  member: { student_id: 17, name: "Member", roll_no: "007", registration_no: "009" },
  books: [
    {
      book_id: 3,
      title: "Book",
      author_name: "Author",
      category_name: "Science",
      quantity: 2,
      available_quantity: 1,
    },
  ],
  reservations: [],
  issues: [],
  fines: [],
});

test("student catalogue reserves a book without sending a member identity", async () => {
  const p = await page(snapshot());
  assert.match(p.nodes["#catalogueTable"].innerHTML, /Reserve for 3 days/);
  await p.button.onclick();
  const request = p.requests.find((r) => r.options);
  assert.equal(request.path, "/reservations");
  assert.equal(request.options.body.get("bookId"), "3");
  assert.equal(request.options.body.has("studentId"), false);
});

test("member dashboard prominently shows personal due reminders and unpaid fine details", async () => {
  const data = snapshot();
  const due = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Asia/Dhaka",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(new Date(Date.now() + 2 * 86400000));
  data.issues = [
    {
      issue_id: 19,
      student_id: 17,
      title: "Upcoming return",
      status: "ISSUED",
      due_date: due,
      copy_no: 3,
    },
  ];
  data.fines = [
    {
      fine_id: 9,
      issue_id: 20,
      student_id: 17,
      title: "Unpaid book",
      amount: 50,
      paid_amount: 0,
      balance: 50,
      payment_status: "UNPAID",
    },
  ];
  const p = await page(data);
  assert.match(p.nodes["#memberAlerts"].innerHTML, /Book return is due in 2 days/);
  assert.match(p.nodes["#memberAlerts"].innerHTML, /Upcoming return.*Copy #3/);
  assert.match(p.nodes["#memberAlerts"].innerHTML, /Tk 50 outstanding/);
  assert.match(p.nodes["#memberAlerts"].innerHTML, /href="\/student#loans"/);
  assert.match(p.nodes["#memberAlerts"].innerHTML, /href="\/student#fines"/);
});

test("active hold displays deadline and prevents duplicate title reservations", async () => {
  const data = snapshot();
  data.reservations = [
    {
      reservation_id: 1,
      book_id: 3,
      title: "Book",
      copy_no: 2,
      reserved_at: "2026-10-04 12:00:00",
      expires_at: "2026-10-07 12:00:00",
      status: "ACTIVE",
    },
  ];
  const p = await page(data);
  assert.match(p.nodes["#reservationTable"].innerHTML, /2026-10-07 12:00:00/);
  assert.match(p.nodes["#catalogueTable"].innerHTML, /disabled>Already reserved/);
  assert.doesNotMatch(p.nodes["#reservationTable"].innerHTML, /data-collect/);
});

test("expired holds release reservation allowance and overdue fines remain visible", async () => {
  const data = snapshot();
  data.reservations = [{ reservation_id: 1, book_id: 3, title: "Book", status: "EXPIRED" }];
  data.issues = [
    { issue_id: 1, title: "Loan", status: "ISSUED", current_fine: 30, due_date: "2026-10-01" },
  ];
  const p = await page(data);
  assert.match(p.nodes["#studentStats"].innerHTML, /Tk 30/);
  assert.match(p.nodes["#loanTable"].innerHTML, /2026-10-01/);
  assert.match(p.nodes["#catalogueTable"].innerHTML, /Reserve for 3 days/);
  assert.doesNotMatch(p.nodes["#reservationTable"].innerHTML, /data-cancel/);
});

test("available-book filter excludes out-of-stock titles without fetching again", async () => {
  const data = snapshot();
  data.books.push({
    book_id: 4,
    title: "Unavailable title",
    author_name: "Author",
    category_name: "Science",
    quantity: 1,
    available_quantity: 0,
  });
  const p = await page(data);
  const requests = p.requests.length;
  p.nodes["#availabilityFilter"].value = "available";
  p.nodes["#availabilityFilter"].onchange();
  assert.doesNotMatch(p.nodes["#catalogueTable"].innerHTML, /Unavailable title/);
  assert.match(p.nodes["#catalogueCount"].textContent, /1 of 2 titles/);
  assert.equal(p.requests.length, requests);
});

test("borrowing filter separates returned books from current loans", async () => {
  const data = snapshot();
  data.issues = [
    { issue_id: 1, title: "Current book", status: "ISSUED" },
    { issue_id: 2, title: "Returned book", status: "RETURNED" },
  ];
  const p = await page(data);
  p.nodes["#loanFilter"].value = "RETURNED";
  p.nodes["#loanFilter"].onchange();
  assert.match(p.nodes["#loanTable"].innerHTML, /Returned book/);
  assert.doesNotMatch(p.nodes["#loanTable"].innerHTML, /Current book/);
});

test("staff desk lists active members and available books without member dashboard reads", async () => {
  const data = snapshot();
  data.students = [
    { student_id: 17, name: "Active member", membership_status: "ACTIVE" },
    { student_id: 18, name: "Disabled member", membership_status: "DISABLED" },
  ];
  data.books.push({ book_id: 4, title: "Unavailable book", available_quantity: 0 });
  const p = await page(data, "reservations");
  assert.match(p.nodes["#reserveMember"].innerHTML, /Active member/);
  assert.doesNotMatch(p.nodes["#reserveMember"].innerHTML, /Disabled member/);
  assert.match(p.nodes["#reserveBook"].innerHTML, /Book/);
  assert.doesNotMatch(p.nodes["#reserveBook"].innerHTML, /Unavailable book/);
  assert.equal(
    p.requests.some((request) => request.path === "/student/dashboard"),
    false,
  );
});

test("staff can collect a reserved copy through the shared action coordinator", async () => {
  const data = snapshot();
  data.students = [];
  data.reservations = [{ reservation_id: 12, student_id: 17, title: "Book", status: "ACTIVE" }];
  const p = await page(data, "reservations");
  assert.match(p.nodes["#reservationTable"].innerHTML, /data-collect="12"/);
  await p.collectButton.onclick();
  const request = p.requests.find((item) => item.options);
  assert.equal(request.path, "/reservations/12/collect");
  assert.equal(request.options.method, "POST");
  assert.equal(p.collectButton.disabled, false);
});
