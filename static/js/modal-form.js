(function () {
  const SKIP = new Set(["csrfmiddlewaretoken"]);

  function init(modal) {
    const form = modal.querySelector("form");
    const title = modal.querySelector("[data-modal-title]");
    const source = document.getElementById(modal.dataset.records);
    const records = source
      ? Object.fromEntries(JSON.parse(source.textContent).map(r => [r.id, r]))
      : {};

    function getRecords() {
      const source = document.getElementById(modal.dataset.records);
      return source
      ? Object.fromEntries(JSON.parse(source.textContent).map(r => [r.id, r]))
      : {};
    }

    function clear() {
      form.querySelectorAll("[data-field-error]").forEach(el => el.remove());
      for (const el of form.elements) {
        if (!el.name || SKIP.has(el.name)) continue;
        if (el.tagName === "SELECT") el.selectedIndex = 0;
        else el.value = "";
      }
    }

    modal.openCreate = function () {
      clear();
      form.action = modal.dataset.createUrl;
      title.textContent = modal.dataset.createTitle;
      modal.showModal();
    };

    modal.openEdit = function (id, url) {
      const record = getRecords()[id];
      if (!record) return;
      clear();
      for (const el of form.elements) {
        if (el.name && !SKIP.has(el.name)) el.value = record[el.name] ?? "";
      }
      form.action = url;
      title.textContent = modal.dataset.editTitle;
      modal.showModal();
    };

    // Cerrar con los botones o haciendo clic en el fondo
    modal.addEventListener("click", e => {
      if (e.target === modal || e.target.closest("[data-modal-close]")) modal.close();
    });

    // Reabrir si el servidor devolvió errores
    if (modal.dataset.reopen === "true") {
      modal.showModal();
      if (modal.dataset.resetUrl) history.replaceState(null, "", modal.dataset.resetUrl);
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("dialog[data-form-modal]").forEach(init);
  });

  // Un solo listener para todos los botones, presentes o futuros
  document.addEventListener("click", e => {
    const create = e.target.closest("[data-modal-create]");
    if (create) {
      document.getElementById(create.dataset.modalCreate)?.openCreate();
      return;
    }
    const edit = e.target.closest("[data-modal-edit]");
    if (edit) {
      document.getElementById(edit.dataset.modalEdit)?.openEdit(edit.dataset.id, edit.dataset.url);
    }
  });
})();