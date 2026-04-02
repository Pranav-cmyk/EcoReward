let viewAllButtonState = false;

document.addEventListener("DOMContentLoaded", () => {
  const progressBar = document.getElementById("progress-bar");
  const percentText = document.querySelector(".progress-section-percent");
  const historyRemaining = document.getElementById("remaining-history-items");
  const viewAllButton = document.getElementById("history-section-view-all-btn");

  if (progressBar && percentText) {
    const targetPercent = parseInt(percentText.innerText) || 0;

    setTimeout(() => {
      progressBar.style.width = `${targetPercent}%`;
    }, 1000);
  }

  viewAllButton.addEventListener("click", () => {
    historyRemaining.classList.toggle("history-remaining-items-expanded");
    viewAllButtonState = !viewAllButtonState;

    if (viewAllButtonState) {
      viewAllButton.textContent = "Show Less";
    } else {
      viewAllButton.textContent = "View All";
    }
  });
});
