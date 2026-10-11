(function () {
  const form = document.getElementById("search-form");
  const input = document.getElementById("search-input");
  const clear = document.getElementById("search-clear");
  const results = document.getElementById("results");
  if (!form || !input || !results) return;

  const DELAY = 300; // ms de espera tras dejar de escribir
  let timer = null;
  let controller = null;

  function toggleClear() {
    clear.classList.toggle("hidden", input.value === "");
  }

  async function search() {
    const url = new URL(form.action, window.location.origin);
    const q = input.value.trim();
    if (q) url.searchParams.set("q", q);

    // Cancela la petición anterior si aún no terminó
    if (controller) controller.abort();
    controller = new AbortController();

    try {
      const res = await fetch(url, { signal: controller.signal });
      if (!res.ok) return;
      const doc = new DOMParser().parseFromString(await res.text(), "text/html");
      const fresh = doc.getElementById("results");
      if (fresh) results.innerHTML = fresh.innerHTML;
      history.replaceState(null, "", url.toString()); // la URL refleja la búsqueda
    } catch (err) {
      if (err.name !== "AbortError") console.error(err);
    }
  }

  input.addEventListener("input", () => {
    toggleClear();
    clearTimeout(timer);
    timer = setTimeout(search, DELAY);
  });

  // Enter busca al instante, sin recargar
  form.addEventListener("submit", e => {
    e.preventDefault();
    clearTimeout(timer);
    search();
  });

  clear.addEventListener("click", () => {
    input.value = "";
    toggleClear();
    clearTimeout(timer);
    search();
    input.focus();
  });

  // Escape también limpia
  input.addEventListener("keydown", e => {
    if (e.key === "Escape" && input.value) clear.click();
  });
})();