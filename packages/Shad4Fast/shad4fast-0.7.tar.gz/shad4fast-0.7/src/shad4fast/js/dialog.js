proc_htmx("[data-ref=dialog]", (dialog) => {
  const overlay = dialog.querySelector("[data-ref=dialog-overlay]");
  const trigger = dialog.querySelector("[data-ref=dialog-trigger]");
  const portal = dialog.querySelector("[data-ref=dialog-portal]");

  function openDialog() {
    portal.dataset.state = "open";
    portal.style.display = "block";
  }

  function toggleClose() {
    portal.dataset.state = "closed";
  }

  trigger.addEventListener("click",openDialog);

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
    if (e.target.closest(".dialog-close-button")) toggleClose();
  });
});
