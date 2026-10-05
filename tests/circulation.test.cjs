const assert = require("node:assert/strict");
const { test } = require("node:test");
const fs = require("node:fs");
const vm = require("node:vm");

function setup(state, values = {}) {
  const nodes = {};
  const messages = [];
  let submitted = 0;
  const app = {
    state,
    $: (key) => (nodes[key] ||= { value: "", innerHTML: "", addEventListener() {} }),
    $$: () => [],
    escapeHtml: String,
    memberId: (id) => `Member-${id}`,
    toast: (text) => messages.push(text),
    api: async () => [],
    loadData: (fn) => fn(),
    sortIssues: (items) => items,
    issueRows: () => "",
    postForm: async () => {
      submitted++;
      return false;
    },
    openRequestedModal() {},
  };
  app.$("#issueFilter").value = "ALL";
  vm.runInNewContext(fs.readFileSync("frontend/circulation.js", "utf8"), {
    LibraryApp: app,
    window: { setTimeout() {} },
    FormData: function () {
      return Object.entries(values);
    },
  });
  return {
    nodes,
    messages,
    get submitted() {
      return submitted;
    },
  };
}

test("members with two active loans remain eligible but members with three do not", () => {
  const state = {
    online: true,
    books: [],
    fines: [],
    students: [
      { student_id: 1, name: "Two loans", department: "QA" },
      { student_id: 2, name: "Three loans", department: "QA" },
    ],
    issues: [1, 1, 2, 2, 2].map((id) => ({ student_id: id, status: "ISSUED" })),
  };
  const result = setup(state);
  assert.match(result.nodes["#studentOptions"].innerHTML, /Two loans/);
  assert.doesNotMatch(result.nodes["#studentOptions"].innerHTML, /Three loans/);
});

test("duplicate physical copies are rejected before submission", async () => {
  const result = setup(
    { online: true, books: [], students: [], fines: [], issues: [] },
    { studentId: "1", bookId: "1", copyId: "2", bookId2: "1", copyId2: "2" },
  );
  await result.nodes["#issueModal form"].onsubmit({ preventDefault() {} });
  assert.equal(result.submitted, 0);
  assert.match(result.messages.join(" "), /different copies/);
});

test("selected copies cannot exceed remaining loan allowance", async () => {
  const result = setup(
    {
      online: true,
      books: [],
      students: [],
      fines: [],
      issues: [
        { student_id: 1, status: "ISSUED" },
        { student_id: 1, status: "ISSUED" },
      ],
    },
    { studentId: "1", bookId: "1", copyId: "2", bookId2: "1", copyId2: "3" },
  );
  await result.nodes["#issueModal form"].onsubmit({ preventDefault() {} });
  assert.equal(result.submitted, 0);
  assert.match(result.messages.join(" "), /1 more copies/);
});
