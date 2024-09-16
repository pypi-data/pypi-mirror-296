proc_htmx("[data-ref=sheet]", (sheet) => {
  const overlay = sheet.querySelector("[data-ref=sheet-overlay]");
  const trigger = sheet.querySelector("[data-ref=sheet-trigger]");
  const portal = sheet.querySelector("[data-ref=sheet-portal]");

  function openSheet() {
    portal.dataset.state = "open";
    portal.style.display = "block";
  }

  function toggleClose() {
    portal.dataset.state = "closed";
  }

  trigger.addEventListener("click", openSheet);

  overlay.addEventListener("mousedown", toggleClose);

  portal.addEventListener("animationend", () => {
    if (portal.dataset.state === "closed") {
      portal.style.display = "none";
    }
  });

  htmx.on("htmx:historyRestore", () => {
    toggleClose();
    portal.style.display = "none";
  });

  document.addEventListener("click", (e) => {
    if (e.target.closest(".sheet-close-button")) toggleClose();
  });
});
