# frontend/student.html

এই page-এর semantic HTML structure: header placeholder, content sections, forms/dialogs এবং stylesheet/script links। Matching controller JavaScript interactions চালায়।

Source: [মূল file](../../frontend/student.html)। Snapshot 2026-10-04; 226 lines; SHA-256 `c552017241acfc4ab33c27e7e4f265eb32267441afe142f784fddc05b6a42bfc`।

## Function / object / element inventory

- DOM IDs: `appHeader`, `overview`, `refreshButton`, `memberName`, `memberIdentity`, `studentStats`, `memberAlertHeading`, `memberAlerts`, `memberNextStep`, `loans`, `loanHeading`, `loanFilter`, `loanTable`, `reservations`, `reservationHeading`, `reservationTable`, `catalogue`, `catalogueHeading`, `bookSearch`, `catalogueCount`, `availabilityFilter`, `catalogueTable`, `fines`, `fineHeading`, `studentFineTable`, `security`, `securityHeading`, `studentPasswordForm`, `toast`
- Form keys: `currentPassword`, `newPassword`
- Loaded/linked resources: `/static/styles.css?v=members-audit-1`, `/static/polish.css?v=1`, `/static/notifications.css?v=due-2`, `/static/student.css?v=due-2`, `#overview`, `#overview`, `#loans`, `#reservations`, `#catalogue`, `#fines`, `#security`, `#loans`, `#catalogue`, `#reservations`, `/static/assets/member-reading-desk.webp`, `#catalogue`, `#catalogue`, `/static/notifications.js?v=reminders-4`, `/static/shared.js?v=priority-3`, `/static/member-dashboard.js?v=reminders-4`, `/static/reservations.js?v=priority-3`, `/static/member-navigation.js?v=1`

## সম্পূর্ণ original source

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>My dashboard | PSTU Library</title>
    <link rel="stylesheet" href="/static/styles.css?v=members-audit-1" />
    <link rel="stylesheet" href="/static/polish.css?v=1" />
    <link rel="stylesheet" href="/static/notifications.css?v=due-2" />
    <link rel="stylesheet" href="/static/student.css?v=due-2" />
  </head>
  <body data-page="student">
    <div id="appHeader"></div>
    <div class="member-layout">
      <aside class="member-sidebar">
        <a class="portal-title" href="#overview"
          ><span class="portal-symbol">P</span
          ><span>My Library<small>MEMBER PORTAL</small></span></a
        >
        <p class="sidebar-label">YOUR WORKSPACE</p>
        <nav aria-label="Member sections">
          <a href="#overview"><span>01</span> Overview</a
          ><a href="#loans"><span>02</span> My borrowing</a
          ><a href="#reservations"><span>03</span> Reservations</a
          ><a href="#catalogue"><span>04</span> Discover books</a
          ><a href="#fines"><span>05</span> Fines &amp; payments</a
          ><a href="#security"><span>06</span> Account security</a>
        </nav>
        <div class="sidebar-guide">
          <span class="section-label">A LITTLE REMINDER</span><strong>More time to explore.</strong>
          <p>
            Keep each book for 15 days from its issue date. Collect reserved copies within 3 days.
          </p>
          <a href="#loans">Check my due dates &rarr;</a>
        </div>
      </aside>
      <main class="member-main" id="overview">
        <div class="member-topline">
          <div>
            <p class="eyebrow">PSTU CENTRAL LIBRARY</p>
            <h1>My dashboard</h1>
          </div>
          <button id="refreshButton" class="button secondary">Refresh data</button>
        </div>
        <section class="member-hero" aria-labelledby="memberName">
          <div class="hero-copy">
            <span class="hero-kicker">YOUR NEXT CHAPTER STARTS HERE</span>
            <h2 id="memberName">Welcome to your library.</h2>
            <p>Find your next read, keep track of your books, and make room for new ideas.</p>
            <div class="hero-actions">
              <a class="button" href="#catalogue">Explore the collection &rarr;</a
              ><a href="#reservations">View my reservations</a>
            </div>
          </div>
          <span class="hero-caption">A space for curiosity.</span>
        </section>
        <div class="member-profile">
          <span class="profile-dot" aria-hidden="true"></span>
          <p id="memberIdentity">Loading your membership details...</p>
          <span class="profile-note">Your personal library workspace</span>
        </div>
        <section id="studentStats" class="member-stats" aria-label="My library summary"></section>
        <section class="member-panel member-alert-panel" aria-labelledby="memberAlertHeading">
          <div class="panel-heading">
            <div>
              <span class="section-label">RETURN REMINDERS &amp; FINES</span>
              <h2 id="memberAlertHeading">Stay ahead of your due dates</h2>
              <p class="section-description">
                Return reminders start 3 days before the due date. Unpaid fines and overdue
                estimates appear here too.
              </p>
            </div>
          </div>
          <div id="memberAlerts" class="member-alert-list" aria-live="polite"></div>
        </section>
        <div class="member-feature-grid">
          <article class="member-panel next-step">
            <div class="panel-heading">
              <div>
                <span class="section-label">STAY ON TRACK</span>
                <h2>Your next library visit</h2>
              </div>
              <span class="small-tag">At a glance</span>
            </div>
            <div id="memberNextStep" aria-live="polite">
              <p class="section-description">Your upcoming returns and pickups will appear here.</p>
            </div>
          </article>
          <article class="discovery-card">
            <img
              src="/static/assets/member-reading-desk.webp"
              alt="An open book and a stack of books on a sunlit reading desk"
              width="1672"
              height="941"
              loading="lazy"
            />
            <div>
              <span class="section-label">FIND YOUR NEXT READ</span>
              <h2>A whole collection.<br />A new possibility.</h2>
              <a href="#catalogue">Browse available books &rarr;</a>
            </div>
          </article>
        </div>
        <section class="member-panel" id="loans" aria-labelledby="loanHeading">
          <div class="panel-heading">
            <div>
              <span class="section-label">MY BORROWING</span>
              <h2 id="loanHeading">Books &amp; return dates</h2>
              <p class="section-description">
                Your current loans and reading history, all in one place.
              </p>
            </div>
            <label class="member-filter"
              >Show books<select id="loanFilter">
                <option value="all">All borrowing</option>
                <option value="ISSUED">Current loans</option>
                <option value="RETURNED">Returned books</option>
              </select></label
            >
          </div>
          <div id="loanTable" class="table-wrap"></div>
        </section>
        <section class="member-panel" id="reservations" aria-labelledby="reservationHeading">
          <div class="panel-heading">
            <div>
              <span class="section-label">SAVED FOR YOU</span>
              <h2 id="reservationHeading">My reservations</h2>
              <p class="section-description">
                A reserved copy is held for 3 days. Pick it up at the library desk before the
                deadline.
              </p>
            </div>
            <a class="text-link" href="#catalogue">Reserve a book &rarr;</a>
          </div>
          <div class="member-info-strip">
            Up to 3 loans and active reservations together. Uncollected reservations expire
            automatically.
          </div>
          <div id="reservationTable" class="table-wrap"></div>
        </section>
        <section
          class="member-panel catalogue-panel"
          id="catalogue"
          aria-labelledby="catalogueHeading"
        >
          <div class="panel-heading">
            <div>
              <span class="section-label">EXPLORE THE SHELVES</span>
              <h2 id="catalogueHeading">Book catalogue</h2>
              <p class="section-description">
                Search the collection and reserve an available copy.
              </p>
            </div>
            <label class="catalogue-search"
              >Search the collection<input
                id="bookSearch"
                type="search"
                placeholder="Title, author or category"
            /></label>
          </div>
          <div class="catalogue-tools">
            <p id="catalogueCount">Loading collection...</p>
            <label class="member-filter"
              >Availability<select id="availabilityFilter">
                <option value="all">All titles</option>
                <option value="available">Available now</option>
              </select></label
            >
          </div>
          <div id="catalogueTable" class="member-catalogue"></div>
        </section>
        <div class="member-bottom-grid">
          <section class="member-panel" id="fines" aria-labelledby="fineHeading">
            <div class="panel-heading">
              <div>
                <span class="section-label">PAYMENT OVERVIEW</span>
                <h2 id="fineHeading">My fines</h2>
                <p class="section-description">
                  Pay the full outstanding balance at the library desk. Overdue estimates are
                  finalized on return.
                </p>
              </div>
            </div>
            <div id="studentFineTable" class="table-wrap"></div>
          </section>
          <section
            class="member-panel security-panel"
            id="security"
            aria-labelledby="securityHeading"
          >
            <div class="panel-heading">
              <div>
                <span class="section-label">ACCOUNT SECURITY</span>
                <h2 id="securityHeading">Change password</h2>
                <p class="section-description">Keep your member account personal and secure.</p>
              </div>
            </div>
            <form id="studentPasswordForm" class="account-form">
              <label
                >Current password<input
                  name="currentPassword"
                  type="password"
                  autocomplete="current-password"
                  required /></label
              ><label
                >New password<input
                  name="newPassword"
                  type="password"
                  minlength="4"
                  maxlength="128"
                  autocomplete="new-password"
                  required /></label
              ><button class="button primary">Update password</button>
            </form>
          </section>
        </div>
      </main>
    </div>
    <div id="toast" role="status" aria-live="polite"></div>
    <script src="/static/notifications.js?v=reminders-4"></script>
    <script src="/static/shared.js?v=priority-3"></script>
    <script src="/static/member-dashboard.js?v=reminders-4"></script>
    <script src="/static/reservations.js?v=priority-3"></script>
    <script src="/static/member-navigation.js?v=1"></script>
  </body>
</html>
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>&lt;!doctype html&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 2 | <code>&lt;html lang=&quot;en&quot;&gt;</code> | html: HTML structure/content |
| 3 | <code>  &lt;head&gt;</code> | head: HTML structure/content |
| 4 | <code>    &lt;meta charset=&quot;utf-8&quot; /&gt;</code> | meta: encoding/viewport metadata |
| 5 | <code>    &lt;meta name=&quot;viewport&quot; content=&quot;width=device-width,initial-scale=1&quot; /&gt;</code> | meta: encoding/viewport metadata |
| 6 | <code>    &lt;title&gt;My dashboard &#124; PSTU Library&lt;/title&gt;</code> | title: HTML structure/content |
| 7 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/styles.css?v=members-audit-1&quot; /&gt;</code> | link: stylesheet/resource load |
| 8 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/polish.css?v=1&quot; /&gt;</code> | link: stylesheet/resource load |
| 9 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/notifications.css?v=due-2&quot; /&gt;</code> | link: stylesheet/resource load |
| 10 | <code>    &lt;link rel=&quot;stylesheet&quot; href=&quot;/static/student.css?v=due-2&quot; /&gt;</code> | link: stylesheet/resource load |
| 11 | <code>  &lt;/head&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 12 | <code>  &lt;body data-page=&quot;student&quot;&gt;</code> | body: HTML structure/content |
| 13 | <code>    &lt;div id=&quot;appHeader&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 14 | <code>    &lt;div class=&quot;member-layout&quot;&gt;</code> | div: layout/dynamic content container |
| 15 | <code>      &lt;aside class=&quot;member-sidebar&quot;&gt;</code> | aside: HTML structure/content |
| 16 | <code>        &lt;a class=&quot;portal-title&quot; href=&quot;#overview&quot;</code> | a: HTML structure/content |
| 17 | <code>          &gt;&lt;span class=&quot;portal-symbol&quot;&gt;P&lt;/span</code> | span: HTML structure/content |
| 18 | <code>          &gt;&lt;span&gt;My Library&lt;small&gt;MEMBER PORTAL&lt;/small&gt;&lt;/span&gt;&lt;/a</code> | span: HTML structure/content; small: HTML structure/content |
| 19 | <code>        &gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 20 | <code>        &lt;p class=&quot;sidebar-label&quot;&gt;YOUR WORKSPACE&lt;/p&gt;</code> | p: description/help text |
| 21 | <code>        &lt;nav aria-label=&quot;Member sections&quot;&gt;</code> | nav: HTML structure/content |
| 22 | <code>          &lt;a href=&quot;#overview&quot;&gt;&lt;span&gt;01&lt;/span&gt; Overview&lt;/a</code> | a: HTML structure/content; span: HTML structure/content |
| 23 | <code>          &gt;&lt;a href=&quot;#loans&quot;&gt;&lt;span&gt;02&lt;/span&gt; My borrowing&lt;/a</code> | a: HTML structure/content; span: HTML structure/content |
| 24 | <code>          &gt;&lt;a href=&quot;#reservations&quot;&gt;&lt;span&gt;03&lt;/span&gt; Reservations&lt;/a</code> | a: HTML structure/content; span: HTML structure/content |
| 25 | <code>          &gt;&lt;a href=&quot;#catalogue&quot;&gt;&lt;span&gt;04&lt;/span&gt; Discover books&lt;/a</code> | a: HTML structure/content; span: HTML structure/content |
| 26 | <code>          &gt;&lt;a href=&quot;#fines&quot;&gt;&lt;span&gt;05&lt;/span&gt; Fines &amp;amp; payments&lt;/a</code> | a: HTML structure/content; span: HTML structure/content |
| 27 | <code>          &gt;&lt;a href=&quot;#security&quot;&gt;&lt;span&gt;06&lt;/span&gt; Account security&lt;/a&gt;</code> | a: HTML structure/content; span: HTML structure/content |
| 28 | <code>        &lt;/nav&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 29 | <code>        &lt;div class=&quot;sidebar-guide&quot;&gt;</code> | div: layout/dynamic content container |
| 30 | <code>          &lt;span class=&quot;section-label&quot;&gt;A LITTLE REMINDER&lt;/span&gt;&lt;strong&gt;More time to explore.&lt;/strong&gt;</code> | span: HTML structure/content; strong: HTML structure/content |
| 31 | <code>          &lt;p&gt;</code> | p: description/help text |
| 32 | <code>            Keep each book for 15 days from its issue date. Collect reserved copies within 3 days.</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 33 | <code>          &lt;/p&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 34 | <code>          &lt;a href=&quot;#loans&quot;&gt;Check my due dates &amp;rarr;&lt;/a&gt;</code> | a: HTML structure/content |
| 35 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 36 | <code>      &lt;/aside&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 37 | <code>      &lt;main class=&quot;member-main&quot; id=&quot;overview&quot;&gt;</code> | main: primary page content |
| 38 | <code>        &lt;div class=&quot;member-topline&quot;&gt;</code> | div: layout/dynamic content container |
| 39 | <code>          &lt;div&gt;</code> | div: layout/dynamic content container |
| 40 | <code>            &lt;p class=&quot;eyebrow&quot;&gt;PSTU CENTRAL LIBRARY&lt;/p&gt;</code> | p: description/help text |
| 41 | <code>            &lt;h1&gt;My dashboard&lt;/h1&gt;</code> | h1: page heading |
| 42 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 43 | <code>          &lt;button id=&quot;refreshButton&quot; class=&quot;button secondary&quot;&gt;Refresh data&lt;/button&gt;</code> | button: action/submit/cancel control |
| 44 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 45 | <code>        &lt;section class=&quot;member-hero&quot; aria-labelledby=&quot;memberName&quot;&gt;</code> | section: related UI content grouping |
| 46 | <code>          &lt;div class=&quot;hero-copy&quot;&gt;</code> | div: layout/dynamic content container |
| 47 | <code>            &lt;span class=&quot;hero-kicker&quot;&gt;YOUR NEXT CHAPTER STARTS HERE&lt;/span&gt;</code> | span: HTML structure/content |
| 48 | <code>            &lt;h2 id=&quot;memberName&quot;&gt;Welcome to your library.&lt;/h2&gt;</code> | h2: section/dialog heading |
| 49 | <code>            &lt;p&gt;Find your next read, keep track of your books, and make room for new ideas.&lt;/p&gt;</code> | p: description/help text |
| 50 | <code>            &lt;div class=&quot;hero-actions&quot;&gt;</code> | div: layout/dynamic content container |
| 51 | <code>              &lt;a class=&quot;button&quot; href=&quot;#catalogue&quot;&gt;Explore the collection &amp;rarr;&lt;/a</code> | a: HTML structure/content |
| 52 | <code>              &gt;&lt;a href=&quot;#reservations&quot;&gt;View my reservations&lt;/a&gt;</code> | a: HTML structure/content |
| 53 | <code>            &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 54 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 55 | <code>          &lt;span class=&quot;hero-caption&quot;&gt;A space for curiosity.&lt;/span&gt;</code> | span: HTML structure/content |
| 56 | <code>        &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 57 | <code>        &lt;div class=&quot;member-profile&quot;&gt;</code> | div: layout/dynamic content container |
| 58 | <code>          &lt;span class=&quot;profile-dot&quot; aria-hidden=&quot;true&quot;&gt;&lt;/span&gt;</code> | span: HTML structure/content |
| 59 | <code>          &lt;p id=&quot;memberIdentity&quot;&gt;Loading your membership details...&lt;/p&gt;</code> | p: description/help text |
| 60 | <code>          &lt;span class=&quot;profile-note&quot;&gt;Your personal library workspace&lt;/span&gt;</code> | span: HTML structure/content |
| 61 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 62 | <code>        &lt;section id=&quot;studentStats&quot; class=&quot;member-stats&quot; aria-label=&quot;My library summary&quot;&gt;&lt;/section&gt;</code> | section: related UI content grouping |
| 63 | <code>        &lt;section class=&quot;member-panel member-alert-panel&quot; aria-labelledby=&quot;memberAlertHeading&quot;&gt;</code> | section: related UI content grouping |
| 64 | <code>          &lt;div class=&quot;panel-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 65 | <code>            &lt;div&gt;</code> | div: layout/dynamic content container |
| 66 | <code>              &lt;span class=&quot;section-label&quot;&gt;RETURN REMINDERS &amp;amp; FINES&lt;/span&gt;</code> | span: HTML structure/content |
| 67 | <code>              &lt;h2 id=&quot;memberAlertHeading&quot;&gt;Stay ahead of your due dates&lt;/h2&gt;</code> | h2: section/dialog heading |
| 68 | <code>              &lt;p class=&quot;section-description&quot;&gt;</code> | p: description/help text |
| 69 | <code>                Return reminders start 3 days before the due date. Unpaid fines and overdue</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 70 | <code>                estimates appear here too.</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 71 | <code>              &lt;/p&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 72 | <code>            &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 73 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 74 | <code>          &lt;div id=&quot;memberAlerts&quot; class=&quot;member-alert-list&quot; aria-live=&quot;polite&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 75 | <code>        &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 76 | <code>        &lt;div class=&quot;member-feature-grid&quot;&gt;</code> | div: layout/dynamic content container |
| 77 | <code>          &lt;article class=&quot;member-panel next-step&quot;&gt;</code> | article: HTML structure/content |
| 78 | <code>            &lt;div class=&quot;panel-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 79 | <code>              &lt;div&gt;</code> | div: layout/dynamic content container |
| 80 | <code>                &lt;span class=&quot;section-label&quot;&gt;STAY ON TRACK&lt;/span&gt;</code> | span: HTML structure/content |
| 81 | <code>                &lt;h2&gt;Your next library visit&lt;/h2&gt;</code> | h2: section/dialog heading |
| 82 | <code>              &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 83 | <code>              &lt;span class=&quot;small-tag&quot;&gt;At a glance&lt;/span&gt;</code> | span: HTML structure/content |
| 84 | <code>            &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 85 | <code>            &lt;div id=&quot;memberNextStep&quot; aria-live=&quot;polite&quot;&gt;</code> | div: layout/dynamic content container |
| 86 | <code>              &lt;p class=&quot;section-description&quot;&gt;Your upcoming returns and pickups will appear here.&lt;/p&gt;</code> | p: description/help text |
| 87 | <code>            &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 88 | <code>          &lt;/article&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 89 | <code>          &lt;article class=&quot;discovery-card&quot;&gt;</code> | article: HTML structure/content |
| 90 | <code>            &lt;img</code> | img: HTML structure/content |
| 91 | <code>              src=&quot;/static/assets/member-reading-desk.webp&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 92 | <code>              alt=&quot;An open book and a stack of books on a sunlit reading desk&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 93 | <code>              width=&quot;1672&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 94 | <code>              height=&quot;941&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 95 | <code>              loading=&quot;lazy&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 96 | <code>            /&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 97 | <code>            &lt;div&gt;</code> | div: layout/dynamic content container |
| 98 | <code>              &lt;span class=&quot;section-label&quot;&gt;FIND YOUR NEXT READ&lt;/span&gt;</code> | span: HTML structure/content |
| 99 | <code>              &lt;h2&gt;A whole collection.&lt;br /&gt;A new possibility.&lt;/h2&gt;</code> | h2: section/dialog heading; br: HTML structure/content |
| 100 | <code>              &lt;a href=&quot;#catalogue&quot;&gt;Browse available books &amp;rarr;&lt;/a&gt;</code> | a: HTML structure/content |
| 101 | <code>            &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 102 | <code>          &lt;/article&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 103 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 104 | <code>        &lt;section class=&quot;member-panel&quot; id=&quot;loans&quot; aria-labelledby=&quot;loanHeading&quot;&gt;</code> | section: related UI content grouping |
| 105 | <code>          &lt;div class=&quot;panel-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 106 | <code>            &lt;div&gt;</code> | div: layout/dynamic content container |
| 107 | <code>              &lt;span class=&quot;section-label&quot;&gt;MY BORROWING&lt;/span&gt;</code> | span: HTML structure/content |
| 108 | <code>              &lt;h2 id=&quot;loanHeading&quot;&gt;Books &amp;amp; return dates&lt;/h2&gt;</code> | h2: section/dialog heading |
| 109 | <code>              &lt;p class=&quot;section-description&quot;&gt;</code> | p: description/help text |
| 110 | <code>                Your current loans and reading history, all in one place.</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 111 | <code>              &lt;/p&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 112 | <code>            &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 113 | <code>            &lt;label class=&quot;member-filter&quot;</code> | label: field-এর readable label |
| 114 | <code>              &gt;Show books&lt;select id=&quot;loanFilter&quot;&gt;</code> | select: option থেকে value নির্বাচন |
| 115 | <code>                &lt;option value=&quot;all&quot;&gt;All borrowing&lt;/option&gt;</code> | option: select-এর choice |
| 116 | <code>                &lt;option value=&quot;ISSUED&quot;&gt;Current loans&lt;/option&gt;</code> | option: select-এর choice |
| 117 | <code>                &lt;option value=&quot;RETURNED&quot;&gt;Returned books&lt;/option&gt;</code> | option: select-এর choice |
| 118 | <code>              &lt;/select&gt;&lt;/label</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 119 | <code>            &gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 120 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 121 | <code>          &lt;div id=&quot;loanTable&quot; class=&quot;table-wrap&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 122 | <code>        &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 123 | <code>        &lt;section class=&quot;member-panel&quot; id=&quot;reservations&quot; aria-labelledby=&quot;reservationHeading&quot;&gt;</code> | section: related UI content grouping |
| 124 | <code>          &lt;div class=&quot;panel-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 125 | <code>            &lt;div&gt;</code> | div: layout/dynamic content container |
| 126 | <code>              &lt;span class=&quot;section-label&quot;&gt;SAVED FOR YOU&lt;/span&gt;</code> | span: HTML structure/content |
| 127 | <code>              &lt;h2 id=&quot;reservationHeading&quot;&gt;My reservations&lt;/h2&gt;</code> | h2: section/dialog heading |
| 128 | <code>              &lt;p class=&quot;section-description&quot;&gt;</code> | p: description/help text |
| 129 | <code>                A reserved copy is held for 3 days. Pick it up at the library desk before the</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 130 | <code>                deadline.</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 131 | <code>              &lt;/p&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 132 | <code>            &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 133 | <code>            &lt;a class=&quot;text-link&quot; href=&quot;#catalogue&quot;&gt;Reserve a book &amp;rarr;&lt;/a&gt;</code> | a: HTML structure/content |
| 134 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 135 | <code>          &lt;div class=&quot;member-info-strip&quot;&gt;</code> | div: layout/dynamic content container |
| 136 | <code>            Up to 3 loans and active reservations together. Uncollected reservations expire</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 137 | <code>            automatically.</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 138 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 139 | <code>          &lt;div id=&quot;reservationTable&quot; class=&quot;table-wrap&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 140 | <code>        &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 141 | <code>        &lt;section</code> | section: related UI content grouping |
| 142 | <code>          class=&quot;member-panel catalogue-panel&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 143 | <code>          id=&quot;catalogue&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 144 | <code>          aria-labelledby=&quot;catalogueHeading&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 145 | <code>        &gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 146 | <code>          &lt;div class=&quot;panel-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 147 | <code>            &lt;div&gt;</code> | div: layout/dynamic content container |
| 148 | <code>              &lt;span class=&quot;section-label&quot;&gt;EXPLORE THE SHELVES&lt;/span&gt;</code> | span: HTML structure/content |
| 149 | <code>              &lt;h2 id=&quot;catalogueHeading&quot;&gt;Book catalogue&lt;/h2&gt;</code> | h2: section/dialog heading |
| 150 | <code>              &lt;p class=&quot;section-description&quot;&gt;</code> | p: description/help text |
| 151 | <code>                Search the collection and reserve an available copy.</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 152 | <code>              &lt;/p&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 153 | <code>            &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 154 | <code>            &lt;label class=&quot;catalogue-search&quot;</code> | label: field-এর readable label |
| 155 | <code>              &gt;Search the collection&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 156 | <code>                id=&quot;bookSearch&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 157 | <code>                type=&quot;search&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 158 | <code>                placeholder=&quot;Title, author or category&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 159 | <code>            /&gt;&lt;/label&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 160 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 161 | <code>          &lt;div class=&quot;catalogue-tools&quot;&gt;</code> | div: layout/dynamic content container |
| 162 | <code>            &lt;p id=&quot;catalogueCount&quot;&gt;Loading collection...&lt;/p&gt;</code> | p: description/help text |
| 163 | <code>            &lt;label class=&quot;member-filter&quot;</code> | label: field-এর readable label |
| 164 | <code>              &gt;Availability&lt;select id=&quot;availabilityFilter&quot;&gt;</code> | select: option থেকে value নির্বাচন |
| 165 | <code>                &lt;option value=&quot;all&quot;&gt;All titles&lt;/option&gt;</code> | option: select-এর choice |
| 166 | <code>                &lt;option value=&quot;available&quot;&gt;Available now&lt;/option&gt;</code> | option: select-এর choice |
| 167 | <code>              &lt;/select&gt;&lt;/label</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 168 | <code>            &gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 169 | <code>          &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 170 | <code>          &lt;div id=&quot;catalogueTable&quot; class=&quot;member-catalogue&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 171 | <code>        &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 172 | <code>        &lt;div class=&quot;member-bottom-grid&quot;&gt;</code> | div: layout/dynamic content container |
| 173 | <code>          &lt;section class=&quot;member-panel&quot; id=&quot;fines&quot; aria-labelledby=&quot;fineHeading&quot;&gt;</code> | section: related UI content grouping |
| 174 | <code>            &lt;div class=&quot;panel-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 175 | <code>              &lt;div&gt;</code> | div: layout/dynamic content container |
| 176 | <code>                &lt;span class=&quot;section-label&quot;&gt;PAYMENT OVERVIEW&lt;/span&gt;</code> | span: HTML structure/content |
| 177 | <code>                &lt;h2 id=&quot;fineHeading&quot;&gt;My fines&lt;/h2&gt;</code> | h2: section/dialog heading |
| 178 | <code>                &lt;p class=&quot;section-description&quot;&gt;</code> | p: description/help text |
| 179 | <code>                  Pay the full outstanding balance at the library desk. Overdue estimates are</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 180 | <code>                  finalized on return.</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 181 | <code>                &lt;/p&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 182 | <code>              &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 183 | <code>            &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 184 | <code>            &lt;div id=&quot;studentFineTable&quot; class=&quot;table-wrap&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 185 | <code>          &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 186 | <code>          &lt;section</code> | section: related UI content grouping |
| 187 | <code>            class=&quot;member-panel security-panel&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 188 | <code>            id=&quot;security&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 189 | <code>            aria-labelledby=&quot;securityHeading&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 190 | <code>          &gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 191 | <code>            &lt;div class=&quot;panel-heading&quot;&gt;</code> | div: layout/dynamic content container |
| 192 | <code>              &lt;div&gt;</code> | div: layout/dynamic content container |
| 193 | <code>                &lt;span class=&quot;section-label&quot;&gt;ACCOUNT SECURITY&lt;/span&gt;</code> | span: HTML structure/content |
| 194 | <code>                &lt;h2 id=&quot;securityHeading&quot;&gt;Change password&lt;/h2&gt;</code> | h2: section/dialog heading |
| 195 | <code>                &lt;p class=&quot;section-description&quot;&gt;Keep your member account personal and secure.&lt;/p&gt;</code> | p: description/help text |
| 196 | <code>              &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 197 | <code>            &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 198 | <code>            &lt;form id=&quot;studentPasswordForm&quot; class=&quot;account-form&quot;&gt;</code> | form: submit-able input grouping |
| 199 | <code>              &lt;label</code> | label: field-এর readable label |
| 200 | <code>                &gt;Current password&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 201 | <code>                  name=&quot;currentPassword&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 202 | <code>                  type=&quot;password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 203 | <code>                  autocomplete=&quot;current-password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 204 | <code>                  required /&gt;&lt;/label</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 205 | <code>              &gt;&lt;label</code> | label: field-এর readable label |
| 206 | <code>                &gt;New password&lt;input</code> | input: user-entered field; name request key, required/pattern/maxlength browser validation |
| 207 | <code>                  name=&quot;newPassword&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 208 | <code>                  type=&quot;password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 209 | <code>                  minlength=&quot;4&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 210 | <code>                  maxlength=&quot;128&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 211 | <code>                  autocomplete=&quot;new-password&quot;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 212 | <code>                  required /&gt;&lt;/label</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 213 | <code>              &gt;&lt;button class=&quot;button primary&quot;&gt;Update password&lt;/button&gt;</code> | button: action/submit/cancel control |
| 214 | <code>            &lt;/form&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 215 | <code>          &lt;/section&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 216 | <code>        &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 217 | <code>      &lt;/main&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 218 | <code>    &lt;/div&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 219 | <code>    &lt;div id=&quot;toast&quot; role=&quot;status&quot; aria-live=&quot;polite&quot;&gt;&lt;/div&gt;</code> | div: layout/dynamic content container |
| 220 | <code>    &lt;script src=&quot;/static/notifications.js?v=reminders-4&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 221 | <code>    &lt;script src=&quot;/static/shared.js?v=priority-3&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 222 | <code>    &lt;script src=&quot;/static/member-dashboard.js?v=reminders-4&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 223 | <code>    &lt;script src=&quot;/static/reservations.js?v=priority-3&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 224 | <code>    &lt;script src=&quot;/static/member-navigation.js?v=1&quot;&gt;&lt;/script&gt;</code> | script: JavaScript controller load |
| 225 | <code>  &lt;/body&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
| 226 | <code>&lt;/html&gt;</code> | HTML closing structure অথবা text content; আগের open elements-এর অংশ। |
