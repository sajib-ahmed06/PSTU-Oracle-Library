const assert = require("node:assert/strict");
const { test } = require("node:test");
const fs = require("node:fs");
const vm = require("node:vm");
function render(
  state,
  collection = { total: 0, today: 0, month: 0, date: "2026-10-05", month_start: "2026-10-01" },
) {
  const nodes = {};
  const app = {
    state,
    $: (key) => (nodes[key] ||= {}),
    $$: () => [],
    escapeHtml: (value) => String(value ?? ""),
    memberId: (id) => `PSTU-${id}`,
    table: (headers, rows) => rows.join(""),
    toast() {},
    api: async () => collection,
    loadData: (fn) => {
      nodes.ready = fn();
      return nodes.ready;
    },
  };
  vm.runInNewContext(fs.readFileSync("frontend/fines.js", "utf8"), {
    LibraryApp: app,
    window: { setInterval() {} },
    document: { hidden: false },
  });
  return nodes;
}

test("fine collection shows total, today's and current month's actual receipts separately", async () => {
  const nodes = render(
    { students: [], issues: [], fines: [] },
    { total: 1250.5, today: 100, month: 450.5, date: "2026-10-05", month_start: "2026-10-01" },
  );
  await nodes.ready;
  const html = nodes["#fineCollection"].innerHTML;
  assert.match(html, /Total fine collection.*Tk 1,250.5/);
  assert.match(html, /Today’s fine collection.*Tk 100/);
  assert.match(html, /Monthly fine collection.*Tk 450.5/);
  assert.match(html, /2026-10-05/);
});
test("unpaid fines appear before newer paid records, with the largest balance first", () => {
  const nodes = render({
    students: [],
    issues: [],
    fines: [
      {
        fine_id: 999,
        title: "Paid history",
        amount: 200,
        paid_amount: 200,
        balance: 0,
        payment_status: "PAID",
      },
      {
        fine_id: 2,
        title: "Small outstanding",
        amount: 10,
        paid_amount: 0,
        balance: 10,
        payment_status: "UNPAID",
      },
      {
        fine_id: 1,
        title: "Large outstanding",
        amount: 100,
        paid_amount: 0,
        balance: 100,
        payment_status: "UNPAID",
      },
    ],
  });
  const html = nodes["#fineTable"].innerHTML;
  assert.ok(html.indexOf("Large outstanding") < html.indexOf("Small outstanding"));
  assert.ok(html.indexOf("Small outstanding") < html.indexOf("Paid history"));
});

test("overdue loans display return action and combine with unpaid fines", () => {
  const nodes = render({
    students: [],
    issues: [
      {
        issue_id: 1,
        student_id: 1,
        student: "Member",
        title: "Overdue book",
        status: "ISSUED",
        due_date: "2026-10-01",
        overdue_days: 3,
        current_fine: 30,
      },
      { issue_id: 2, status: "ISSUED", overdue_days: 0, current_fine: 0, title: "On time" },
    ],
    fines: [
      {
        fine_id: 1,
        issue_id: 3,
        student_id: 2,
        student: "Returned",
        title: "Returned book",
        amount: 20,
        payment_status: "UNPAID",
      },
      { fine_id: 2, issue_id: 4, amount: 100, payment_status: "PAID" },
    ],
  });
  assert.match(nodes["#fineSummary"].innerHTML, /Tk 50/);
  assert.match(nodes["#overdueTable"].innerHTML, /Return book/);
  assert.match(nodes["#overdueTable"].innerHTML, /3 days/);
  assert.doesNotMatch(nodes["#overdueTable"].innerHTML, /On time/);
});
test("returned overdue book moves to history without changing outstanding total", () => {
  const nodes = render({
    students: [],
    issues: [
      {
        issue_id: 1,
        status: "RETURNED",
        overdue_days: 0,
        current_fine: 0,
        return_date: "2026-10-04",
      },
    ],
    fines: [
      {
        fine_id: 1,
        issue_id: 1,
        student_id: 1,
        student: "Member",
        title: "Book",
        amount: 30,
        payment_status: "UNPAID",
      },
    ],
  });
  assert.match(nodes["#fineSummary"].innerHTML, /Tk 30/);
  assert.match(nodes["#overdueTable"].innerHTML, /No overdue books/);
  assert.match(nodes["#fineTable"].innerHTML, /2026-10-04/);
  assert.match(nodes["#fineTable"].innerHTML, /Pay full fine/);
});

test("legacy partial payments preserve the remaining balance", () => {
  const nodes = render({
    students: [],
    issues: [{ issue_id: 1, status: "RETURNED", copy_no: 2, return_date: "2026-10-04" }],
    fines: [
      {
        fine_id: 1,
        issue_id: 1,
        amount: 100,
        paid_amount: 35.25,
        balance: 64.75,
        payment_status: "UNPAID",
      },
    ],
  });
  assert.match(nodes["#fineSummary"].innerHTML, /Tk 64.75/);
  assert.doesNotMatch(nodes["#fineSummary"].innerHTML, /Tk 100/);
  assert.match(nodes["#fineTable"].innerHTML, /Tk 35.25/);
  assert.match(nodes["#fineTable"].innerHTML, /PARTIAL/);
  assert.match(nodes["#fineTable"].innerHTML, /Copy #2/);
});

test("fully paid fine has zero outstanding and retains receipts", () => {
  const nodes = render({
    students: [],
    issues: [],
    fines: [{ fine_id: 1, amount: 100, paid_amount: 100, balance: 0, payment_status: "PAID" }],
  });
  assert.match(nodes["#fineSummary"].innerHTML, /Tk 0/);
  assert.doesNotMatch(nodes["#fineTable"].innerHTML, /data-pay=/);
  assert.match(nodes["#fineTable"].innerHTML, /Receipts/);
});
test("existing fine for the same issue is not double counted", () => {
  const nodes = render({
    students: [],
    issues: [{ issue_id: 1, student_id: 1, status: "ISSUED", overdue_days: 3, current_fine: 30 }],
    fines: [{ fine_id: 1, issue_id: 1, amount: 30, payment_status: "UNPAID" }],
  });
  assert.match(nodes["#fineSummary"].innerHTML, /Tk 30/);
  assert.doesNotMatch(nodes["#fineSummary"].innerHTML, /Tk 60/);
});
