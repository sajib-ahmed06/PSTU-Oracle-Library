const assert = require("node:assert/strict");
const { test } = require("node:test");
const fs = require("node:fs");
const vm = require("node:vm");

function dashboard() {
  const nodes = {};
  const $ = (key) => (nodes[key] ||= { innerHTML: "", textContent: "" });
  class Clock extends Date {
    static now() {
      return Date.UTC(2026, 9, 4, 6);
    }
  }
  const state = {
    books: [{ quantity: 10, available_quantity: 5 }],
    students: [
      { student_id: 1, membership_status: "ACTIVE" },
      { student_id: 2, membership_status: "DISABLED" },
    ],
    reservations: [{ status: "ACTIVE" }],
    meta: { authors: [{ id: 1 }], categories: [{ id: 1 }] },
    issues: [
      {
        issue_id: 1,
        student_id: 1,
        student: "Upcoming member",
        title: "Algorithms",
        status: "ISSUED",
        due_date: "2026-10-07",
        copy_no: 2,
        overdue_days: 0,
      },
      {
        issue_id: 2,
        student_id: 1,
        student: "Overdue member",
        title: "Java",
        status: "ISSUED",
        due_date: "2026-10-01",
        overdue_days: 3,
        current_fine: 30,
      },
      {
        issue_id: 3,
        student_id: 2,
        title: "Future book",
        status: "ISSUED",
        due_date: "2026-10-10",
        overdue_days: 0,
      },
      {
        issue_id: 4,
        student_id: 2,
        title: "Returned book",
        status: "RETURNED",
        due_date: "2026-10-05",
      },
    ],
    fines: [
      {
        fine_id: 1,
        issue_id: 5,
        student_id: 1,
        student: "Fine member",
        title: "Database",
        amount: 100,
        paid_amount: 20,
        balance: 80,
        payment_status: "UNPAID",
      },
    ],
  };
  const context = vm.createContext({
    window: {},
    Date: Clock,
    Intl,
    LibraryApp: {
      $,
      state,
      loadData: (render) => render(),
      sortIssues: (rows) => rows,
      issueRows: () => "",
      table: (headers, rows) => rows.join(""),
      escapeHtml: String,
      memberId: (id) => `PSTU-${id}`,
    },
  });
  vm.runInContext(fs.readFileSync("frontend/notifications.js", "utf8"), context);
  const render = () => vm.runInContext(fs.readFileSync("frontend/dashboard.js", "utf8"), context);
  render();
  return { nodes, state, render };
}

test("dashboard shows detailed counts, upcoming borrowers and recorded plus estimated fines", () => {
  const p = dashboard();
  assert.match(p.nodes["#stats"].innerHTML, /1 due within 3 days/);
  assert.match(p.nodes["#stats"].innerHTML, /1 disabled memberships/);
  assert.match(p.nodes["#stats"].innerHTML, /Tk 110 combined outstanding/);
  assert.match(
    p.nodes["#dueSoonTable"].innerHTML,
    /Upcoming member.*Algorithms.*2026-10-07.*3 days left/,
  );
  assert.doesNotMatch(p.nodes["#dueSoonTable"].innerHTML, /Future book|Returned book/);
  assert.match(p.nodes["#fineAttentionTable"].innerHTML, /Fine member.*Tk 80.*Unpaid fine/);
  assert.match(p.nodes["#fineAttentionTable"].innerHTML, /Overdue member.*Tk 30.*Overdue estimate/);
});

test("recorded fines replace estimates rather than counting the same loan twice", () => {
  const p = dashboard();
  p.state.fines[0].issue_id = 2;
  p.render();
  assert.equal(p.nodes["#fineAttentionTotal"].textContent, "Tk 80 recorded + estimated");
  assert.doesNotMatch(p.nodes["#fineAttentionTable"].innerHTML, /Overdue estimate/);
  p.state.fines[0].payment_status = "PAID";
  p.render();
  assert.equal(p.nodes["#fineAttentionTotal"].textContent, "Tk 0 recorded + estimated");
});
