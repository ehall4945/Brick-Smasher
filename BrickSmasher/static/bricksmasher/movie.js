function getCsrfToken() {
    // Reads Django's CSRF token from the form
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}

function showMessage(text, type = "") {
    // Updates the movie page message area
    const message = document.querySelector("#movie-message");
    message.textContent = text;
    message.className = type ? `message ${type}` : "message";
}

function renderMovies(movies) {
    // Rebuilds the movie table from server data
    const tableBody = document.querySelector("#movie-table-body");
    tableBody.innerHTML = "";

    movies.forEach(movie => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${movie.title}</td>
            <td>${movie.in_stock}</td>
            <td>${movie.checked_out}</td>
            <td class="clickable" data-action="add" data-id="${movie.id}">+</td>
            <td class="clickable" data-action="remove" data-id="${movie.id}">-</td>
        `;

        tableBody.appendChild(row);
    });
}

function loadMovies() {
    // Loads all movies when the page opens
    fetch("/dbMovie/")
        .then(response => response.json())
        .then(movies => renderMovies(movies))
        .catch(() => showMessage("Could not load movies", "error"));
}

function updateMovie(action, id = null, title = null) {
    // Sends a movie create, add, or remove request to Django
    const formData = new FormData();
    formData.append("action", action);

    if (id !== null) {
        formData.append("id", id);
    }

    if (title !== null) {
        formData.append("title", title);
    }

    fetch("/dbMovie/", {
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

            renderMovies(result.data);
            showMessage("");
        })
        .catch(() => showMessage("Could not update movie data", "error"));
}

document.querySelector("#movie-form").addEventListener("submit", function (event) {
    // Adds a new movie from the title input
    event.preventDefault();

    const titleInput = document.querySelector("#movie-title");
    updateMovie("new", null, titleInput.value);
    titleInput.value = "";
});

document.querySelector("#movie-table-body").addEventListener("click", function (event) {
    // Handles add and remove clicks from the movie table
    if (!event.target.classList.contains("clickable")) {
        return;
    }

    updateMovie(event.target.dataset.action, event.target.dataset.id);
});

loadMovies();
