const videoInput = document.querySelector("#video");
const videoForm = document.querySelector(".video-upload-form");
const videoLabel = document.querySelector("label[for='video']");
const videoUploadSectionHeading = document.querySelector(
  "#video-upload-section-heading",
);
const confirmBTN = document.querySelector("#submit-btn");
let AIResults = "";

const videoElement = document.createElement("video");
const statusText = document.getElementById("status-text");

// Trash Icons
const TrashIconMapping = {
  "Dry Waste": "fa-trash",
  "Wet Waste": "fa-recycle",
  "Mixed Waste": "fa-mix",
  "Hazardous Waste": "fa-biohazard",
};

// Update These Three in the dom after AI Results
const verifiedWrapper = document.getElementById(
  "result-analysis-verified-wrapper",
);
const trashIcon = document.getElementById("trash-icon");
const trashIconContainer = document.getElementById("trash-icon-container");

const playBackVideo = (videoFile) => {
  if (!videoFile) return;

  videoElement.src = URL.createObjectURL(videoFile);
  videoElement.controls = true;
  videoElement.autoplay = true;
  videoElement.muted = false;

  videoElement.style.width = "100%";
  videoElement.style.height = "34vh";
  videoElement.style.borderRadius = "12px";
  videoElement.style.objectFit = "cover";
  videoElement.style.backgroundColor = "#000";

  videoLabel.style.display = "none";

  const existingVideo = videoForm.querySelector("video");
  if (existingVideo) existingVideo.remove();

  videoForm.appendChild(videoElement);
  videoUploadSectionHeading.textContent = "Processing Video...";
  videoElement.play();
};

const showProcessingOverlay = () => {
  // Reset UI for new analysis
  verifiedWrapper.style.opacity = 0;
  if (confirmBTN) confirmBTN.style.display = "none";

  const container = document.getElementById("video-preview-container");
  const overlay = document.createElement("div");
  overlay.className = "video-processing-overlay";
  overlay.innerHTML = `
    <div class="ai-loader"></div>
    <p class="processing-text">Analyzing Waste...</p>
  `;
  container.appendChild(overlay);
};

const hideProcessingOverlay = (status = "success") => {
  const overlay = document.querySelector(".video-processing-overlay");
  if (overlay) overlay.remove();

  if (status === "error") {
    videoUploadSectionHeading.classList.add("error");
    videoUploadSectionHeading.textContent = `Analysis Failed: Did you show a waste disposal action?`;
  } else if (status === "unexpected-error") {
    videoUploadSectionHeading.classList.add("error");
    videoUploadSectionHeading.textContent = `Analysis Failed: Unexpected Error`;
  } else {
    videoUploadSectionHeading.classList.remove("error");
    videoUploadSectionHeading.textContent = "Analysis Complete";
  }
};

const sendVideoToServer = async (videoFile) => {
  const formData = new FormData();
  formData.append("file", videoFile);
  const response = await fetch("/video/upload", {
    method: "POST",
    body: formData,
  });
  if (!response.ok) throw new Error("Server responded with an error");
  return await response.json();
};

const updateResultAnalysisSection = () => {
  const trashCategory = AIResults.category;

  // Update Icon
  trashIcon.className = "fa-solid";
  trashIcon.classList.add(TrashIconMapping[trashCategory] || "fa-trash");
  trashIconContainer.style.backgroundColor = "rgba(167, 215, 255, 0.3)";

  // Update Text
  document.getElementById("waste-category").textContent = trashCategory;
  document.getElementById("estimated-weight").textContent =
    AIResults.estimatedWeight;
  document.getElementById("total-rewards").textContent =
    `+${AIResults.points} Points`;

  // Update Items List
  const itemsList = document.querySelector(".items-list");
  itemsList.innerHTML = "";
  AIResults.items.forEach((item) => {
    const listItem = document.createElement("li");
    listItem.className = "item";
    listItem.textContent = item;
    itemsList.appendChild(listItem);
  });

  // Fade everything back in
  verifiedWrapper.style.opacity = 1;
  if (confirmBTN) confirmBTN.style.display = "block";
};

videoInput.addEventListener("change", async (e) => {
  const selectedVideo = e.target.files[0];
  if (!selectedVideo) return;

  playBackVideo(selectedVideo);
  showProcessingOverlay();

  try {
    const result = await sendVideoToServer(selectedVideo);
    AIResults = result.result;

    // for Testing
    result.status = "success";
    console.log(result);

    if (!result.status) {
      console.error("Backend Error:");
      hideProcessingOverlay("error");
      return;
    }

    updateResultAnalysisSection();
    hideProcessingOverlay("success");
  } catch (error) {
    console.error("Analysis Error:", error);
    hideProcessingOverlay("unexpected-error");
  }
});

confirmBTN.addEventListener("click", async () => {
  const body = {
    title: `Disposed: ${AIResults.estimatedWeight} of ${AIResults.category}`,
    description: `${AIResults.points} Earned! `,

    // Update Date to 12Hour Format
    timestamp: new Date().toDateString(),
    logo: TrashIconMapping[AIResults.category] || "fa-trash",
    points: AIResults.points,
  };

  try {
    const response = await fetch("/video/submit", {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
      },
    });
    console.log(await response.json());

    statusText.classList.add("status-text-success");
    statusText.textContent = "Collection Added! Reloading Page...";
    setTimeout(() => {
      window.location.reload();
    }, 5000);
  } catch (error) {
    statusText.classList.add("status-text-error");
    statusText.textContent = "Collection Add Failed!";
    console.error("Backend Error:", error);
  }
});
