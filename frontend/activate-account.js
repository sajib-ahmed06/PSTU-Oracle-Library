(() => {
  const form = document.querySelector("#activationForm");
  const button = document.querySelector("#activationButton");
  const message = document.querySelector("#activationMessage");
  form.onsubmit = async (event) => {
    event.preventDefault();
    if (button.disabled) return;
    if (form.elements.password.value !== form.elements.confirmPassword.value) {
      message.textContent = "Passwords do not match";
      return;
    }
    button.disabled = true;
    form.setAttribute("aria-busy", "true");
    message.textContent = "Activating...";
    try {
      const response = await fetch("/api/auth/activate", {
        method: "POST",
        body: new URLSearchParams(new FormData(form)),
        signal: AbortSignal.timeout(30000),
      });
      const data = await response.json();
      if (!response.ok)
        throw new Error(typeof data.detail === "string" ? data.detail : "Activation failed");
      if (!data.member_id) throw new Error("Unexpected server response. Please try signing in");
      form.reset();
      message.textContent = data.message;
      window.location.replace(`/login?memberId=${encodeURIComponent(data.member_id)}&activated=1`);
    } catch (error) {
      message.textContent =
        error instanceof TypeError
          ? "Cannot reach the server. Please try again"
          : ["TimeoutError", "AbortError"].includes(error.name)
            ? "Activation timed out. Try signing in before activating again"
            : error.message;
    } finally {
      button.disabled = false;
      form.setAttribute("aria-busy", "false");
    }
  };
})();
