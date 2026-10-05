# frontend/member-navigation.js

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../frontend/member-navigation.js)। Snapshot 2026-10-04; 27 lines; SHA-256 `d04c0dc6912a95b727ab77e0c76af4f83e7c9e6ede4020fcecf7640799095422`।

## Function / object / element inventory

## সম্পূর্ণ original source

```javascript
(() => {
  const links = [...document.querySelectorAll(".member-sidebar nav a")];
  const select = (id) =>
    links.forEach((link) => {
      const active = link.getAttribute("href") === `#${id}`;
      link.classList.toggle("selected", active);
      if (active) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
  select("overview");
  links.forEach((link) => link.addEventListener("click", () => select(link.hash.slice(1))));
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
        if (visible.length) select(visible[0].target.id);
      },
      { rootMargin: "-5% 0px -65% 0px", threshold: 0 },
    );
    ["overview", "loans", "reservations", "catalogue", "fines", "security"].forEach((id) => {
      const element = document.getElementById(id);
      if (element) observer.observe(element);
    });
  }
})();
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>(() =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 2 | <code>  const links = [...document.querySelectorAll(&quot;.member-sidebar nav a&quot;)];</code> | Local state, DOM reference বা callback/result assign করে। |
| 3 | <code>  const select = (id) =&gt;</code> | Local state, DOM reference বা callback/result assign করে। |
| 4 | <code>    links.forEach((link) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 5 | <code>      const active = link.getAttribute(&quot;href&quot;) === `#${id}`;</code> | Local state, DOM reference বা callback/result assign করে। |
| 6 | <code>      link.classList.toggle(&quot;selected&quot;, active);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 7 | <code>      if (active) link.setAttribute(&quot;aria-current&quot;, &quot;location&quot;);</code> | DOM/ARIA state update করে যাতে browser ও assistive technology সঠিক state পায়। |
| 8 | <code>      else link.removeAttribute(&quot;aria-current&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 9 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 10 | <code>  select(&quot;overview&quot;);</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 11 | <code>  links.forEach((link) =&gt; link.addEventListener(&quot;click&quot;, () =&gt; select(link.hash.slice(1))));</code> | User/browser event handler bind করে; সংশ্লিষ্ট click/input/submit/change হলে callback চলে। |
| 12 | <code>  if (&quot;IntersectionObserver&quot; in window) {</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 13 | <code>    const observer = new IntersectionObserver(</code> | Local state, DOM reference বা callback/result assign করে। |
| 14 | <code>      (entries) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 15 | <code>        const visible = entries</code> | Local state, DOM reference বা callback/result assign করে। |
| 16 | <code>          .filter((entry) =&gt; entry.isIntersecting)</code> | Search/eligibility/status condition মেলে এমন records নির্বাচন করে। |
| 17 | <code>          .sort((a, b) =&gt; a.boundingClientRect.top - b.boundingClientRect.top);</code> | Local state, DOM reference বা callback/result assign করে। |
| 18 | <code>        if (visible.length) select(visible[0].target.id);</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 19 | <code>      },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 20 | <code>      { rootMargin: &quot;-5% 0px -65% 0px&quot;, threshold: 0 },</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 21 | <code>    );</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 22 | <code>    [&quot;overview&quot;, &quot;loans&quot;, &quot;reservations&quot;, &quot;catalogue&quot;, &quot;fines&quot;, &quot;security&quot;].forEach((id) =&gt; {</code> | Local state, DOM reference বা callback/result assign করে। |
| 23 | <code>      const element = document.getElementById(id);</code> | Local state, DOM reference বা callback/result assign করে। |
| 24 | <code>      if (element) observer.observe(element);</code> | Condition অনুযায়ী action/label/value নির্বাচন করে। |
| 25 | <code>    });</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 26 | <code>  }</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
| 27 | <code>})();</code> | Expression/template literal বা enclosing callback/function-এর structural continuation। |
