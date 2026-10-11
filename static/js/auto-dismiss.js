document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-auto-dismiss]").forEach(el => {
    const delay = parseInt(el.dataset.autoDismiss, 10) || 3000;
    setTimeout(() => {
      // desaparece con transición de opacidad
      el.classList.add("opacity-0"); 
      //elimina el elemento del DOM después de la transición
      setTimeout(() => el.remove(), 500);    
    }, delay);
  });
});