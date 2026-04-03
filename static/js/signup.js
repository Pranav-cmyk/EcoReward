document.addEventListener("DOMContentLoaded", () => {
  const signupForm = document.getElementById("signup-form");
  const errorMessage = document.getElementById("error-message-div");

  if (!signupForm) {
    console.log("signup-form not found");
    return;
  }

  signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(signupForm);
    const username = formData.get("username");
    const password = formData.get("password");

    const response = await fetch("/auth/createUser", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    const data = await response.json();

    if (response.ok && data.status === "success") {
      console.log("User Successfully Created, Redirecting to Login");
      window.location.href = "/auth/login";
    } else {
      console.log("Signup Failed, Please Try Again: ", data.message);
      errorMessage.classList.add("error-message-show");
    }
  });
});
