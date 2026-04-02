document.addEventListener("DOMContentLoaded", () => {
  const signupForm = document.getElementById("signup-form");

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

    if (response.ok) {
      console.log("User Successfully Created, Redirecting to Login");
      window.location.href = "/auth/login";
    } else {
      const errorData = await response.json();
      console.log("Signup Failed, Please Try Again: ", errorData);
    }
  });
});
