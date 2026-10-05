const assert = require("node:assert/strict");
const { test } = require("node:test");
const fs = require("node:fs");
const vm = require("node:vm");

function app(fetch, options = {}) {
  const timers = [],
    events = {},
    redirects = [];
  const node = () => ({
    innerHTML: "",
    textContent: "",
    classList: { toggle() {}, add() {} },
    setAttribute() {},
  });
  const nodes = {};
  const document = {
    hidden: false,
    body: { dataset: { page: "overview" } },
    querySelector: (selector) => (nodes[selector] ||= node()),
    querySelectorAll: () => [],
    addEventListener: (name, fn) => {
      events[name] = fn;
    },
  };
  const context = vm.createContext({
    document,
    window: {
      LibraryNotifications: options.notifications,
      location: { replace: (path) => redirects.push(path) },
      setInterval: (fn) => {
        timers.push(fn);
        return 1;
      },
      addEventListener: (name, fn) => {
        events[name] = fn;
      },
    },
    fetch,
    AbortSignal,
    TypeError,
    URLSearchParams,
    Intl,
    Date: options.Date || Date,
    setTimeout: (fn) => {
      fn();
      return 1;
    },
    clearTimeout() {},
  });
  vm.runInContext(fs.readFileSync("frontend/shared.js", "utf8"), context);
  return { library: vm.runInContext("LibraryApp", context), timers, events, redirects };
}
const response = (status, value) => ({ status, ok: status < 400, json: async () => value });

test("circulation sorts overdue and upcoming returns ahead of active loans and returned history", () => {
  const p = app(async (path) => response(200, data(path)));
  const items = [
    { issue_id: 99, status: "RETURNED", issue_date: "2099-01-01" },
    { issue_id: 5, status: "ISSUED", due_date: p.library.dateFromToday(10) },
    { issue_id: 3, status: "ISSUED", due_date: p.library.dateFromToday(-2) },
    { issue_id: 4, status: "ISSUED", due_date: p.library.dateFromToday(2) },
    { issue_id: 2, status: "ISSUED", due_date: p.library.dateFromToday(-10) },
  ];
  assert.deepEqual(
    Array.from(p.library.sortIssues(items), (item) => item.issue_id),
    [2, 3, 4, 5, 99],
  );
  assert.equal(items[0].issue_id, 99);
});
const data = (path) =>
  path === "/api/snapshot"
    ? { books: [], students: [], issues: [], fines: [], meta: { authors: [], categories: [] } }
    : path === "/api/auth/session"
      ? { username: "admin", user_type: "ADMIN" }
      : path === "/api/meta"
        ? { authors: [], categories: [] }
        : [];

test("temporary read failure retries and load becomes connected", async () => {
  let reads = 0;
  const p = app(async (path) =>
    path === "/api/snapshot" && ++reads === 1 ? response(503, {}) : response(200, data(path)),
  );
  assert.equal(await p.library.loadData(() => {}), true);
  assert.equal(reads, 2);
});

test("overlapping refreshes share one data load", async () => {
  let reads = 0,
    renders = 0;
  const p = app(async (path) => {
    if (path === "/api/snapshot") reads++;
    return response(200, data(path));
  });
  await Promise.all([p.library.loadData(() => renders++), p.library.loadData(() => renders++)]);
  assert.equal(reads, 1);
  assert.equal(renders, 1);
});

test("older server without snapshot uses existing routes and stays connected", async () => {
  const paths = [];
  const p = app(async (path) => {
    paths.push(path);
    if (path === "/api/snapshot") return response(404, { detail: "Not Found" });
    return response(200, path === "/api/books" ? [{ book_id: 1 }] : data(path));
  });
  assert.equal(await p.library.loadData(() => {}), true);
  assert.equal(p.library.state.books[0].book_id, 1);
  assert.equal(await p.library.loadData(() => {}), true);
  assert.equal(paths.filter((path) => path === "/api/snapshot").length, 1);
  for (const name of ["books", "students", "issues", "fines", "meta"]) {
    assert.equal(paths.filter((path) => path === `/api/${name}`).length, 2);
  }
});

test("snapshot database errors stay offline without falling back", async () => {
  const paths = [];
  const p = app(async (path) => {
    paths.push(path);
    return path === "/api/auth/session"
      ? response(200, data(path))
      : response(503, { detail: "Unavailable" });
  });
  assert.equal(await p.library.loadData(() => {}), false);
  assert.equal(paths.includes("/api/books"), false);
});

test("mutation failures are not automatically replayed", async () => {
  let writes = 0;
  const p = app(async (path) => {
    if (path === "/api/auth/session") return response(200, data(path));
    writes++;
    return response(503, { detail: "Database unavailable" });
  });
  await assert.rejects(p.library.api("/issues", { method: "POST" }), /Database unavailable/);
  assert.equal(writes, 1);
});

test("monitor restores live data after outage", async () => {
  let offline = true;
  const p = app(async (path) =>
    path !== "/api/auth/session" && offline
      ? response(503, { detail: "Unavailable" })
      : response(200, data(path)),
  );
  assert.equal(await p.library.loadData(() => {}), false);
  offline = false;
  await p.timers[0]();
  assert.equal(p.library.state.online, true);
});

test("live notifications refresh from the shared snapshot after 30 seconds", async () => {
  let now = 0;
  class Clock extends Date {
    static now() {
      return now;
    }
  }
  let reads = 0;
  const updates = [];
  const sessions = [];
  const p = app(
    async (path) => {
      if (path === "/api/snapshot") {
        reads++;
        return response(200, { ...data(path), reservations: [{ reservation_id: reads }] });
      }
      return response(200, data(path));
    },
    {
      Date: Clock,
      notifications: {
        create: () => ({
          setSession: (session) => sessions.push(session),
          update: (snapshot, online) =>
            updates.push({ reservation: snapshot.reservations[0].reservation_id, online }),
        }),
      },
    },
  );
  await p.library.loadData(() => {});
  now = 31000;
  await p.timers[0]();
  assert.equal(reads, 2);
  assert.equal(sessions[0].user_type, "ADMIN");
  assert.deepEqual(updates, [
    { reservation: 1, online: true },
    { reservation: 2, online: true },
  ]);
});

test("notification freshness becomes offline without clearing the last snapshot", async () => {
  let offline = false;
  const updates = [];
  const p = app(
    async (path) => {
      if (offline && path !== "/api/auth/session") return response(503, { detail: "Unavailable" });
      return response(200, { ...data(path), reservations: [{ reservation_id: 8 }] });
    },
    {
      notifications: {
        create: () => ({
          setSession() {},
          update: (snapshot, online) =>
            updates.push({ reservation: snapshot.reservations[0].reservation_id, online }),
        }),
      },
    },
  );
  await p.library.loadData(() => {});
  offline = true;
  await p.timers[0]();
  assert.deepEqual(updates.at(-1), { reservation: 8, online: false });
  assert.equal(p.library.state.reservations[0].reservation_id, 8);
});
