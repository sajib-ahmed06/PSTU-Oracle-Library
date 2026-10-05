const assert = require("node:assert/strict");
const { test } = require("node:test");
const fs = require("node:fs");
const vm = require("node:vm");

test("membership table displays and searches roll and registration", () => {
  const nodes = {
    "#studentSearch": { value: "" },
    "#studentCount": {},
    "#studentTable": {},
    "#studentModal form": {},
    "#identityModal form": {},
  };
  const members = [
    {
      student_id: 1,
      name: "First",
      department: "CSE",
      phone: "01700000001",
      email: "first@example.com",
      membership_status: "ACTIVE",
      roll_no: "001-AB",
      registration_no: "REG-001",
      academic_session: "2023-2024",
    },
    {
      student_id: 2,
      name: "Legacy",
      department: "CSE",
      phone: "01700000002",
      email: "legacy@example.com",
      membership_status: "ACTIVE",
      roll_no: null,
      registration_no: null,
    },
  ];
  const app = {
    $: (key) => nodes[key],
    $$: () => [],
    state: { students: members },
    escapeHtml: (value) => String(value),
    memberId: (id) => `PSTU-${id}`,
    table: (headers, rows) => headers.join("|") + rows.join(""),
    toast() {},
    api() {},
    loadData: (render) => render(),
    postForm() {},
    openRequestedModal() {},
    openModal() {},
  };
  vm.runInNewContext(fs.readFileSync("frontend/students.js", "utf8"), { LibraryApp: app });
  assert.match(nodes["#studentTable"].innerHTML, /001-AB/);
  assert.match(nodes["#studentTable"].innerHTML, /REG-001/);
  assert.match(nodes["#studentTable"].innerHTML, /Not assigned/);
  assert.match(nodes["#studentTable"].innerHTML, /2023-2024/);
  nodes["#studentSearch"].value = "2023-2024";
  nodes["#studentSearch"].oninput();
  assert.equal(nodes["#studentCount"].textContent, "1 member");
  nodes["#studentSearch"].value = "reg-001";
  nodes["#studentSearch"].oninput();
  assert.equal(nodes["#studentCount"].textContent, "1 member");
  assert.doesNotMatch(nodes["#studentTable"].innerHTML, /Legacy/);
  nodes["#studentSearch"].value = "001-ab";
  nodes["#studentSearch"].oninput();
  assert.equal(nodes["#studentCount"].textContent, "1 member");
});
