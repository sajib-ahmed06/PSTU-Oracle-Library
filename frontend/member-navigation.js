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
