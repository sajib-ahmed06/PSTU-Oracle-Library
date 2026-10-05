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
    "#activationForm": form,
    "#activationButton": { disabled: false },
    "#activationMessage": { textContent: "" },
  };
  const redirects = [];
  vm.runInNewContext(fs.readFileSync("frontend/activate-account.js", "utf8"), {
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

test("activation sends member and phone and returns to login with Member ID", async () => {
  const p = page(async (path, options) => {
    assert.equal(path, "/api/auth/activate");
    assert.equal(options.body.get("memberId"), "PSTU-0007");
    assert.equal(options.body.get("phone"), "01700000007");
    return {
      ok: true,
      json: async () => ({ member_id: "PSTU-0007", message: "Account activated" }),
    };
  });
  await p.submit();
  assert.deepEqual(p.redirects, ["/login?memberId=PSTU-0007&activated=1"]);
  assert.equal(p.nodes["#activationForm"].resetCalled, true);
});

test("password mismatch never sends an activation request", async () => {
  let calls = 0;
  const p = page(async () => {
    calls++;
  });
  p.nodes["#activationForm"].elements.confirmPassword.value = "different";
  await p.submit();
  assert.equal(calls, 0);
  assert.match(p.nodes["#activationMessage"].textContent, /Passwords do not match/);
});

test("repeated clicks submit once and activation errors keep the form available", async () => {
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
  finish({ ok: false, json: async () => ({ detail: "Account already activated" }) });
  await first;
  assert.equal(p.nodes["#activationButton"].disabled, false);
  assert.match(p.nodes["#activationMessage"].textContent, /already activated/);
  assert.equal(p.redirects.length, 0);
});
