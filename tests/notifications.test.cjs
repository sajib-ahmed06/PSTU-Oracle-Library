const assert = require("node:assert/strict");
const { test } = require("node:test");
const fs = require("node:fs");
const vm = require("node:vm");

function notifications(storage = new Map()) {
  const nodes = new Map();
  const buttons = ["all", "reservation", "fine"].map((filter) => ({
    dataset: { alertFilter: filter },
    setAttribute() {},
  }));
  const $ = (selector) => {
    if (!nodes.has(selector))
      nodes.set(selector, {
        hidden: selector === "#notificationPanel",
        textContent: "",
        innerHTML: "",
        disabled: false,
        setAttribute(name, value) {
          this[name] = value;
        },
        querySelectorAll: (selector) => (selector === "[data-alert-filter]" ? buttons : []),
        contains: () => true,
        focus() {},
      });
    return nodes.get(selector);
  };
  const messages = [];
  const window = {
    localStorage: {
      getItem: (key) => storage.get(key),
      setItem: (key, value) => storage.set(key, value),
    },
  };
  vm.runInNewContext(fs.readFileSync("frontend/notifications.js", "utf8"), {
    window,
    document: { addEventListener() {} },
    Date,
    Intl,
  });
  const manager = window.LibraryNotifications.create({
    $,
    escapeHtml: String,
    toast: (message) => messages.push(message),
  });
  return { library: window.LibraryNotifications, manager, $, messages, buttons, storage };
}

const staff = { user_id: 1, username: "admin", user_type: "ADMIN" };

test("daily overdue updates show today's fine, daily rate and return/payment action", () => {
  const p = notifications();
  const member = { user_type: "STUDENT", student_id: 2 };
  const data = {
    issues: [
      {
        issue_id: 18,
        student_id: 2,
        status: "ISSUED",
        title: "Java",
        due_date: "2026-10-01",
        overdue_days: 3,
        current_fine: 30,
      },
    ],
  };
  const first = p.library.buildItems(data, member, Date.UTC(2026, 9, 4, 6))[0];
  assert.match(first.note, /Tk 30 estimated today.*3 overdue day.*Tk 10\/day until return/);
  assert.match(first.note, /Return the book and pay the final fine/);
  data.issues[0].overdue_days = 4;
  data.issues[0].current_fine = 40;
  const next = p.library.buildItems(data, member, Date.UTC(2026, 9, 5, 6))[0];
  assert.match(next.note, /Tk 40 estimated today/);
  assert.notEqual(first.key, next.key);
});

test("urgent overdue and unpaid fines outrank newer reservations and due reminders", () => {
  const p = notifications();
  const data = snapshot();
  data.reservations[0].reservation_id = 999;
  data.issues = [
    { issue_id: 1, status: "ISSUED", current_fine: 50, due_date: "2026-10-01" },
    { issue_id: 100, status: "ISSUED", due_date: "2026-10-07" },
  ];
  const alerts = p.library.buildItems(data, staff, Date.UTC(2026, 9, 4, 6));
  assert.deepEqual(
    Array.from(alerts, (item) => item.key.split(":")[0]),
    ["overdue", "fine", "due", "reservation"],
  );
});

test("return reminders start exactly three Dhaka calendar days before the due date", () => {
  const p = notifications();
  const data = {
    issues: [
      {
        issue_id: 15,
        student_id: 2,
        student: "Rahim",
        title: "Algorithms",
        status: "ISSUED",
        due_date: "2026-10-07",
        issue_date: "2026-09-22",
        copy_no: 4,
      },
    ],
  };
  assert.equal(p.library.buildItems(data, staff, Date.UTC(2026, 9, 3, 17, 59, 59)).length, 0);
  const alerts = p.library.buildItems(data, staff, Date.UTC(2026, 9, 3, 18));
  assert.equal(alerts.length, 1);
  assert.equal(alerts[0].type, "due");
  assert.match(alerts[0].title, /3 days/);
  assert.match(alerts[0].detail, /Rahim.*Algorithms.*Copy #4/);
  assert.match(alerts[0].note, /2026-09-22.*2026-10-07/);
  assert.equal(alerts[0].href, "/circulation");
});

test("due-day reminders become overdue fine alerts and returned loans disappear", () => {
  const p = notifications();
  const now = Date.UTC(2026, 9, 4, 6);
  const issue = {
    issue_id: 15,
    student_id: 2,
    title: "Algorithms",
    status: "ISSUED",
    due_date: "2026-10-04",
  };
  const member = { user_type: "STUDENT", student_id: 2 };
  let alerts = p.library.buildItems({ issues: [issue] }, member, now);
  assert.match(alerts[0].title, /due today/);
  assert.equal(alerts[0].href, "/student#loans");
  issue.due_date = "2026-10-03";
  issue.current_fine = 10;
  alerts = p.library.buildItems({ issues: [issue] }, member, now);
  assert.equal(alerts.length, 1);
  assert.equal(alerts[0].type, "fine");
  issue.status = "RETURNED";
  assert.equal(p.library.buildItems({ issues: [issue] }, member, now).length, 0);
  issue.status = "ISSUED";
  issue.student_id = 3;
  assert.equal(p.library.buildItems({ issues: [issue] }, member, now).length, 0);
});

test("invalid dates are ignored and reminders distinguish each day of the window", () => {
  const p = notifications();
  assert.equal(p.library.daysUntilDue("2026-02-30"), null);
  assert.equal(p.library.daysUntilDue(null), null);
  const data = { issues: [{ issue_id: 7, status: "ISSUED", due_date: "2026-10-07" }] };
  const early = p.library.buildItems(data, staff, Date.UTC(2026, 9, 4))[0];
  const next = p.library.buildItems(data, staff, Date.UTC(2026, 9, 5))[0];
  assert.notEqual(early.key, next.key);
  assert.match(next.title, /2 days/);
});
const snapshot = () => ({
  reservations: [
    {
      reservation_id: 8,
      student_id: 2,
      student: "Rahim",
      title: "Clean Code",
      copy_no: 3,
      status: "ACTIVE",
      expires_at: "2099-10-07 12:00:00",
    },
  ],
  fines: [
    {
      fine_id: 4,
      issue_id: 9,
      student_id: 2,
      student: "Rahim",
      title: "Database",
      amount: 100,
      paid_amount: 20,
      balance: 80,
      payment_status: "UNPAID",
    },
  ],
  issues: [],
});

test("alerts show active holds and remaining fines, excluding paid and expired records", () => {
  const p = notifications();
  const data = snapshot();
  data.reservations.push({
    ...data.reservations[0],
    reservation_id: 9,
    expires_at: "2000-01-01 12:00:00",
  });
  data.fines.push({ ...data.fines[0], fine_id: 5, payment_status: "PAID", balance: 0 });
  const alerts = p.library.buildItems(data, staff);
  assert.equal(alerts.length, 2);
  assert.match(alerts.find((alert) => alert.type === "fine").note, /Tk 80 outstanding/);
  assert.equal(alerts.find((alert) => alert.type === "reservation").href, "/reservations");
});

test("student alerts are scoped to their own member ID and dashboard sections", () => {
  const p = notifications();
  const data = snapshot();
  data.reservations.push({ ...data.reservations[0], reservation_id: 10, student_id: 3 });
  data.fines.push({ ...data.fines[0], fine_id: 6, student_id: 3 });
  const alerts = p.library.buildItems(data, { user_type: "STUDENT", student_id: 2 });
  assert.equal(alerts.length, 2);
  assert.ok(alerts.every((alert) => alert.href.startsWith("/student#")));
  assert.ok(alerts.every((alert) => !alert.detail.includes("Rahim")));
});

test("overdue estimates appear without double counting a recorded fine", () => {
  const p = notifications();
  const data = snapshot();
  data.issues = [
    { issue_id: 9, status: "ISSUED", current_fine: 80 },
    { issue_id: 10, status: "ISSUED", current_fine: 30, title: "Java", student: "Karim" },
    { issue_id: 11, status: "RETURNED", current_fine: 50 },
  ];
  const alerts = p.library.buildItems(data, staff);
  assert.equal(alerts.length, 3);
  assert.match(alerts.find((alert) => alert.key.startsWith("overdue:")).note, /Tk 30 estimated/);
});

test("read status survives navigation and stays separate for different accounts", () => {
  const storage = new Map();
  const first = notifications(storage);
  first.manager.setSession(staff);
  first.manager.update(snapshot());
  assert.equal(first.$("#notificationBadge").textContent, "2");
  first.$("#notificationReadAll").onclick();
  assert.equal(first.$("#notificationBadge").hidden, true);
  assert.match(first.$("#notificationList").innerHTML, /Clean Code/);
  assert.ok([...storage.values()].every((value) => !value.includes("Rahim")));
  const second = notifications(storage);
  second.manager.setSession(staff);
  second.manager.update(snapshot());
  assert.equal(second.$("#notificationBadge").hidden, true);
  second.manager.setSession({ ...staff, user_id: 2 });
  assert.equal(second.$("#notificationBadge").textContent, "2");
});

test("new requests announce once and resolved records disappear after refresh", () => {
  const p = notifications();
  p.manager.setSession(staff);
  p.manager.update(snapshot());
  assert.equal(p.messages.length, 0);
  const data = snapshot();
  data.reservations.push({ ...data.reservations[0], reservation_id: 12 });
  p.manager.update(data);
  p.manager.update(data);
  assert.equal(p.messages.length, 1);
  data.reservations = [];
  data.fines = [];
  p.manager.update(data);
  assert.equal(p.$("#notificationBadge").hidden, true);
});

test("offline state retains alerts and shows their freshness clearly", () => {
  const p = notifications();
  p.manager.setSession(staff);
  p.manager.update(snapshot());
  p.manager.update({}, false);
  assert.equal(p.$("#notificationBadge").textContent, "2");
  assert.match(p.$("#notificationFreshness").textContent, /Connection lost/);
  p.buttons[2].onclick();
  assert.doesNotMatch(p.$("#notificationList").innerHTML, /Clean Code/);
  assert.match(p.$("#notificationList").innerHTML, /Database/);
});
