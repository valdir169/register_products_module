(function () {
  const modal = document.getElementById("product-modal");

  // Abrir: cualquier elemento con data-open-modal
  document
    .querySelectorAll("[data-open-modal]")
    .forEach((btn) => btn.addEventListener("click", () => modal.showModal()));

  // Cerrar: botones con data-close-modal
  modal
    .querySelectorAll("[data-close-modal]")
    .forEach((btn) => btn.addEventListener("click", () => modal.close()));

  // Cerrar al hacer clic en el fondo oscuro
  modal.addEventListener("click", (e) => {
    if (e.target === modal) modal.close();
  });

  if (modal.dataset.reopen === "true") {
    modal.showModal();
    // Evita que F5 reenvíe el POST: deja la URL como un GET al listado
    if (modal.dataset.resetUrl) {
      history.replaceState(null, "", modal.dataset.resetUrl);
    }
  }
})();
