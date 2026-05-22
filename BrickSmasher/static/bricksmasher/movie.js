function getCsrfToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}

// Updates the movie page message area with the given text and optional type (e.g. "error")
function showMessage(text, type = "") {
    const message = document.querySelector("#movie-message");
    message.textContent = text;
    message.className = type ? `message ${type}` : "message";
}

// Rebuilds the movie table from the server's data
function renderMovies(movies) {
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
            <td class="clickable" data-action="delete" data-id="${movie.id}" data-title="${movie.title}">Delete</td>
        `;

        tableBody.appendChild(row);
    });
}

// Loads all the movies as soon as the page opens
function loadMovies() {
    fetch("/dbMovie/")
        .then(response => response.json())
        .then(movies => renderMovies(movies))
        .catch(() => showMessage("Could not load movies", "error"));
}

// Sends a movie create, add, or remove request to Django and updates the table on success
function updateMovie(action, id = null, title = null) {
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

// Adds a new movie from the title input
document.querySelector("#movie-form").addEventListener("submit", function (event) {
    event.preventDefault();

    const titleInput = document.querySelector("#movie-title");
    updateMovie("new", null, titleInput.value);
    titleInput.value = "";
});

// Handles the add and remove click functionality from the movie table
document.querySelector("#movie-table-body").addEventListener("click", function (event) {
    if (!event.target.classList.contains("clickable")) {
        return;
    }

    const { action, id, title } = event.target.dataset;

    if (action === "delete") {
        const confirmed = confirm(`Remove "${title}" from the inventory entirely?\n\nThis cannot be undone.`);
        if (!confirmed) return;
    }

    updateMovie(action, id);
});

loadMovies();
