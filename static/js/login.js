document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");

  if (!loginForm) {
    console.log("login-form not found");
    return;
  }

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(loginForm);
    const username = formData.get("username");
    const password = formData.get("password");

    const response = await fetch("/auth/token", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
      console.log("User Successfully Authenticated, Redirecting to Home Page");
      window.location.href = "/";
    } else {
      const errorData = await response.json();
      console.log("Authentication Failed, Please Try Again: ", errorData);
    }
  });
});
