const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const { test } = require("node:test");
const source = fs.readFileSync("frontend/login.js", "utf8");

function page(fetch) {
  const element = (extra = {}) => ({
    textContent: "",
    disabled: false,
    attributes: {},
    setAttribute(key, value) {
      this.attributes[key] = value;
    },
    ...extra,
  });
  const form = element({
    values: { username: " admin ", password: "test1234" },
    elements: { username: { focus() {} } },
  });
  const nodes = {
    "#loginForm": form,
    "#password": element({ type: "password" }),
    "#togglePassword": element(),
    "#loginButton": element(),
    "#loginError": element(),
  };
  const redirects = [];
  const context = {
    document: { querySelector: (selector) => nodes[selector] },
    window: { location: { replace: (path) => redirects.push(path) } },
    FormData: class {
      constructor(form) {
        return Object.entries(form.values);
      }
    },
    URLSearchParams,
    AbortController,
    setTimeout,
    clearTimeout,
    TypeError,
    fetch,
  };
  vm.runInNewContext(source, context);
  return { nodes, redirects, submit: () => form.onsubmit({ preventDefault() {} }) };
}

test("password visibility updates accessible toggle state", () => {
  const { nodes } = page(() => {});
  nodes["#togglePassword"].onclick();
  assert.equal(nodes["#password"].type, "text");
  assert.equal(nodes["#togglePassword"].attributes["aria-pressed"], "true");
  nodes["#togglePassword"].onclick();
  assert.equal(nodes["#password"].type, "password");
});

test("successful login trims username and redirects", async () => {
  const p = page(async (_, options) => {
    assert.equal(options.body.get("username"), "admin");
    return { ok: true, json: async () => ({ username: "admin", user_type: "ADMIN" }) };
  });
  await p.submit();
  assert.deepEqual(p.redirects, ["/"]);
});

test("malformed successful response cannot redirect", async () => {
  const p = page(async () => ({
    ok: true,
    json: async () => {
      throw new Error("Invalid JSON");
    },
  }));
  await p.submit();
  assert.equal(p.redirects.length, 0);
  assert.match(p.nodes["#loginError"].textContent, /unexpected response/);
  assert.equal(p.nodes["#loginButton"].disabled, false);
});

test("student login opens the personal dashboard", async () => {
  const p = page(async () => ({
    ok: true,
    json: async () => ({ username: "studentqa", user_type: "STUDENT" }),
  }));
  await p.submit();
  assert.deepEqual(p.redirects, ["/student"]);
});

test("wrong password and network errors show useful messages", async () => {
  const p = page(async () => ({
    ok: false,
    json: async () => ({ detail: "Incorrect username or password" }),
  }));
  await p.submit();
  assert.equal(p.nodes["#loginError"].textContent, "Incorrect username or password");
  const offline = page(async () => {
    throw new TypeError("Failed to fetch");
  });
  await offline.submit();
  assert.match(offline.nodes["#loginError"].textContent, /Cannot reach the server/);
});

test("repeated submission sends only one pending request", async () => {
  let resolve,
    calls = 0;
  const p = page(() => {
    calls++;
    return new Promise((done) => {
      resolve = done;
    });
  });
  const pending = p.submit();
  await p.submit();
  assert.equal(calls, 1);
  resolve({ ok: true, json: async () => ({ username: "admin", user_type: "ADMIN" }) });
  await pending;
});
