(() => {
  const form = document.querySelector("#loginForm");
  const password = document.querySelector("#password");
  const togglePassword = document.querySelector("#togglePassword");
  const loginButton = document.querySelector("#loginButton");
  const loginError = document.querySelector("#loginError");
  let submitting = false;
  const query = new URLSearchParams(window.location.search || "");
  const activatedMember = query.get("memberId");
  if (activatedMember && /^PSTU-[0-9]{1,20}$/i.test(activatedMember)) {
    form.elements.username.value = activatedMember;
    if (query.get("activated") === "1") {
      loginError.textContent = "Account activated. Sign in with your Member ID and password";
      password.focus?.();
    }
    if (query.get("recovered") === "1") {
      loginError.textContent = "Password changed. Sign in with your Member ID and new password";
      password.focus?.();
    }
  }

  togglePassword.onclick = () => {
    const showing = password.type === "text";
    password.type = showing ? "password" : "text";
    togglePassword.textContent = showing ? "Show" : "Hide";
    togglePassword.setAttribute("aria-label", showing ? "Show password" : "Hide password");
    togglePassword.setAttribute("aria-pressed", String(!showing));
  };

  form.onsubmit = async (event) => {
    event.preventDefault();
    if (submitting) return;
    const body = new URLSearchParams(new FormData(form));
    body.set("username", String(body.get("username") || "").trim());
    if (!body.get("username")) {
      loginError.textContent = "Enter your Member ID or staff username";
      form.elements.username.focus();
      return;
    }
    submitting = true;
    loginError.textContent = "";
    loginButton.disabled = true;
    loginButton.textContent = "Signing in...";
    form.setAttribute("aria-busy", "true");
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 30000);

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        signal: controller.signal,
        body,
      });
      let data;
      try {
        data = await response.json();
      } catch (error) {
        if (controller.signal.aborted) throw error;
        throw new Error("The server returned an unexpected response. Please try again");
      }
      if (!response.ok)
        throw new Error(typeof data?.detail === "string" ? data.detail : "Sign in failed");
      if (!data?.username || !["ADMIN", "LIBRARIAN", "STUDENT"].includes(data.user_type)) {
        throw new Error("The server returned an unexpected response. Please try again");
      }
      window.location.replace(data.user_type === "STUDENT" ? "/student" : "/");
    } catch (error) {
      loginError.textContent = controller.signal.aborted
        ? "Sign in timed out. Please try again"
        : error instanceof TypeError
          ? "Cannot reach the server. Check your connection and try again"
          : error.message;
    } finally {
      clearTimeout(timer);
      submitting = false;
      loginButton.disabled = false;
      loginButton.textContent = "Sign in";
      form.setAttribute("aria-busy", "false");
    }
  };
})();
