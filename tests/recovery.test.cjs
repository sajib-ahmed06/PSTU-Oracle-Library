const assert = require("node:assert/strict");
const { test } = require("node:test");
const fs = require("node:fs");
const vm = require("node:vm");

function page(fetch) {
  const fields = {
    memberId: "PSTU-0007",
    phone: "01700000007",
    password: "Secret1234",
    confirmPassword: "Secret1234",
    rollNo: "007",
    registrationNo: "REG-007",
    email: "member@example.com",
  };
  const form = {
    elements: {
      password: { value: fields.password },
      confirmPassword: { value: fields.confirmPassword },
    },
    setAttribute() {},
    reset() {
      this.resetCalled = true;
    },
  };
  const nodes = {
    "#recoveryForm": form,
    "#recoveryButton": { disabled: false },
    "#recoveryMessage": { textContent: "" },
  };
  const redirects = [];
  vm.runInNewContext(fs.readFileSync("frontend/forgot-password.js", "utf8"), {
    document: { querySelector: (s) => nodes[s] },
    fetch,
    FormData: class {
      constructor() {
        return Object.entries(fields);
      }
    },
    URLSearchParams,
    AbortSignal,
    TypeError,
    encodeURIComponent,
    window: { location: { replace: (path) => redirects.push(path) } },
  });
  return { nodes, redirects, submit: () => form.onsubmit({ preventDefault() {} }) };
}

test("recovery sends member and phone and returns to login with Member ID", async () => {
  const p = page(async (path, options) => {
    assert.equal(path, "/api/auth/reset-password");
    assert.equal(options.body.get("memberId"), "PSTU-0007");
    assert.equal(options.body.get("phone"), "01700000007");
    assert.equal(options.body.get("rollNo"), "007");
    assert.equal(options.body.get("registrationNo"), "REG-007");
    assert.equal(options.body.get("email"), "member@example.com");
    return {
      ok: true,
      json: async () => ({ member_id: "PSTU-0007", message: "Password changed" }),
    };
  });
  await p.submit();
  assert.deepEqual(p.redirects, ["/login?memberId=PSTU-0007&recovered=1"]);
  assert.equal(p.nodes["#recoveryForm"].resetCalled, true);
});

test("password mismatch never sends an recovery request", async () => {
  let calls = 0;
  const p = page(async () => {
    calls++;
  });
  p.nodes["#recoveryForm"].elements.confirmPassword.value = "different";
  await p.submit();
  assert.equal(calls, 0);
  assert.match(p.nodes["#recoveryMessage"].textContent, /Passwords do not match/);
});

test("repeated clicks submit once and recovery errors keep the form available", async () => {
  let finish,
    calls = 0;
  const p = page(() => {
    calls++;
    return new Promise((resolve) => {
      finish = resolve;
    });
  });
  const first = p.submit();
  await p.submit();
  assert.equal(calls, 1);
  finish({ ok: false, json: async () => ({ detail: "Member details do not match" }) });
  await first;
  assert.equal(p.nodes["#recoveryButton"].disabled, false);
  assert.match(p.nodes["#recoveryMessage"].textContent, /do not match/);
  assert.equal(p.redirects.length, 0);
});
