// SecAuditAI - Client-side Utilities
document.addEventListener("DOMContentLoaded", () => {
  // Auto-hide alert boxes if needed or handle interactive items
  const quickSearchInputs = document.querySelectorAll(".table-quick-search");
  quickSearchInputs.forEach((input) => {
    input.addEventListener("input", (e) => {
      const term = e.target.value.toLowerCase();
      const targetTable = document.querySelector(e.target.dataset.targetTable);
      if (!targetTable) return;
      const rows = targetTable.querySelectorAll("tbody tr");
      rows.forEach((row) => {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(term) ? "" : "none";
      });
    });
  });

  // Handle score select changes to toggle NA justifications
  const applicableSelects = document.querySelectorAll(".applicable-toggle");
  applicableSelects.forEach((select) => {
    select.addEventListener("change", (e) => {
      const isApplicable = e.target.value === "true";
      const naGroup = document.querySelector(".na-justification-group");
      const incGroup = document.querySelector(".inclusion-justification-group");
      if (naGroup) {
        naGroup.style.display = isApplicable ? "none" : "block";
      }
      if (incGroup) {
        incGroup.style.display = isApplicable ? "block" : "none";
      }
    });
  });
});

function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = "flex";
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = "none";
  }
}
