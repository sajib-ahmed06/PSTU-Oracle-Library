(() => {
  const { $, state, api, escapeHtml, table, toast, loadData } = LibraryApp;

  async function renderAccounts() {
    try {
      const accounts = await api("/accounts");
      $("#accountCount").textContent = `${accounts.length} accounts`;
      $("#accountTable").innerHTML = table(
        ["Account ID", "Username", "Role", "Status", "Actions"],
        accounts.map((account) => {
          const isAdmin = account.user_type === "ADMIN";
          const toggleLabel = account.account_status === "ACTIVE" ? "Disable" : "Enable";
          const actions = isAdmin
            ? '<span class="complete-text">Current administrator</span>'
            : `<div class="row-actions"><button class="button small ${toggleLabel === "Disable" ? "danger-quiet" : "primary"}" data-account-toggle="${account.user_id}">${toggleLabel}</button><button class="button small danger" data-account-delete="${account.user_id}">Delete</button></div>`;
          return `<tr><td><span class="member-id">ACC-${String(account.user_id).padStart(4, "0")}</span></td><td><b>${escapeHtml(account.username)}</b></td><td><span class="pill ${account.user_type.toLowerCase()}">${account.user_type}</span></td><td><span class="pill ${account.account_status.toLowerCase()}">${account.account_status}</span></td><td>${actions}</td></tr>`;
        }),
      );
      document.querySelectorAll("[data-account-toggle]").forEach((button) => {
        button.onclick = () => toggleAccount(button.dataset.accountToggle, button.textContent);
      });
      document.querySelectorAll("[data-account-delete]").forEach((button) => {
        button.onclick = () => deleteAccount(button.dataset.accountDelete);
      });
    } catch (error) {
      toast(error.message, true);
    }
  }

  async function submitForm(form, path, successMessage) {
    const button = $("button", form);
    button.disabled = true;
    try {
      const response = await api(path, {
        method: "POST",
        body: new URLSearchParams(new FormData(form)),
      });
      toast(successMessage || response.message);
      form.reset();
      return true;
    } catch (error) {
      toast(error.message, true);
      return false;
    } finally {
      button.disabled = false;
    }
  }

  async function toggleAccount(id, action) {
    if (!confirm(`${action} this librarian account?`)) return;
    try {
      const result = await api(`/accounts/${id}/toggle`, { method: "POST" });
      toast(result.message);
      await renderAccounts();
    } catch (error) {
      toast(error.message, true);
    }
  }

  async function deleteAccount(id) {
    if (!confirm("Permanently delete this librarian account?")) return;
    try {
      const result = await api(`/accounts/${id}`, { method: "DELETE" });
      toast(result.message);
      await renderAccounts();
    } catch (error) {
      toast(error.message, true);
    }
  }

  $("#librarianForm").onsubmit = async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    if (form.elements.password.value !== form.elements.confirmPassword.value) {
      toast("Passwords do not match", true);
      return;
    }
    if (await submitForm(form, "/accounts/librarians", "Librarian account created"))
      await renderAccounts();
  };

  $("#credentialsForm").onsubmit = async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    if (form.elements.newPassword.value !== form.elements.confirmPassword.value) {
      toast("New passwords do not match", true);
      return;
    }
    if (await submitForm(form, "/auth/change-credentials", "Administrator credentials updated")) {
      const session = await api("/auth/session");
      $("#sessionUser").textContent = `${session.username} - ${session.user_type}`;
    }
  };

  loadData(renderAccounts);
})();
