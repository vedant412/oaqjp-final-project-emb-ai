const form = document.querySelector("#emotion-form");
const button = form.querySelector("button");
const result = document.querySelector("#system_response");

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const url = new URL(form.action);
    url.search = new URLSearchParams(new FormData(form)).toString();

    button.disabled = true;
    result.textContent = "Analyzing…";
    try {
        const response = await fetch(url);
        result.textContent = await response.text();
    } catch {
        result.textContent = "Could not reach the app. Please try again.";
    } finally {
        button.disabled = false;
    }
});
