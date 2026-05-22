function getCsrfToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}

// Updates the account page message area with the given text and type (ex: "error" or "success")
function showMessage(text, type) {
    const message = document.querySelector("#account-message");
    message.textContent = text;
    message.className = `message ${type}`;
}

// Sends the account form through AJAX instead of a full page reload
document.querySelector("#account-form").addEventListener("submit", function (event) {
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
