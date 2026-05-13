function getCsrfToken() {
    // Reads Django's CSRF token from the form
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}

function showMessage(text, type) {
    // Updates the account page message area
    const message = document.querySelector("#account-message");
    message.textContent = text;
    message.className = `message ${type}`;
}

document.querySelector("#account-form").addEventListener("submit", function (event) {
    // Sends the account form through AJAX instead of a full page reload
    event.preventDefault();

    const formData = new FormData(event.target);

    fetch("/dbUser/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCsrfToken(),
        },
        body: formData,
    })
        .then(response => response.json().then(data => ({ ok: response.ok, data })))
        .then(result => {
            if (!result.ok) {
                showMessage(result.data.error, "error");
                return;
            }

            showMessage("Account created successfully", "success");
            event.target.reset();
        })
        .catch(() => showMessage("Something went wrong while creating the account", "error"));
});
