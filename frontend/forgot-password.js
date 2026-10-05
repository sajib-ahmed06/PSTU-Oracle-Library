(() => {
  const form = document.querySelector("#recoveryForm");
  const button = document.querySelector("#recoveryButton");
  const message = document.querySelector("#recoveryMessage");
  form.onsubmit = async (event) => {
    event.preventDefault();
    if (button.disabled) return;
    if (form.elements.password.value !== form.elements.confirmPassword.value) {
      message.textContent = "Passwords do not match";
      return;
    }
    button.disabled = true;
    form.setAttribute("aria-busy", "true");
    message.textContent = "Changing password...";
    try {
      const response = await fetch("/api/auth/reset-password", {
        method: "POST",
        body: new URLSearchParams(new FormData(form)),
        signal: AbortSignal.timeout(30000),
      });
      const data = await response.json();
      if (!response.ok)
        throw new Error(typeof data.detail === "string" ? data.detail : "Password change failed");
      if (!data.member_id) throw new Error("Unexpected server response. Please try signing in");
      form.reset();
      message.textContent = data.message;
      window.location.replace(`/login?memberId=${encodeURIComponent(data.member_id)}&recovered=1`);
    } catch (error) {
      message.textContent =
        error instanceof TypeError
          ? "Cannot reach the server. Please try again"
          : ["TimeoutError", "AbortError"].includes(error.name)
            ? "Password change timed out. Try signing in before resetting again"
            : error.message;
    } finally {
      button.disabled = false;
      form.setAttribute("aria-busy", "false");
    }
  };
})();
