let currentUser = null;

function getCsrfToken() {
    // Reads Django's CSRF token from the hidden form
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}

function showMessage(text, type = "") {
    // Updates the rental page message area
    const message = document.querySelector("#rent-message");
    message.textContent = text;
    message.className = type ? `message ${type}` : "message";
}

function renderCheckedOut(checkouts) {
    // Displays the selected member's checked out movies
    const tableBody = document.querySelector("#checked-out-body");
    tableBody.innerHTML = "";

    checkouts.forEach(item => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${item.title}</td>
            <td class="clickable" data-action="return" data-movie="${item.movie}">Return</td>
        `;

        tableBody.appendChild(row);
    });
}

function renderAvailableMovies(movies) {
    // Displays only movies with at least one copy in stock
    const tableBody = document.querySelector("#available-movies-body");
    tableBody.innerHTML = "";

    movies
        .filter(movie => movie.in_stock > 0)
        .forEach(movie => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${movie.title}</td>
                <td>${movie.in_stock}</td>
                <td class="clickable" data-action="rent" data-movie="${movie.id}">Rent</td>
            `;

            tableBody.appendChild(row);
        });
}

function refreshRentalTables() {
    // Reloads both rental tables for the current member
    if (!currentUser) {
        return;
    }

    Promise.all([
        fetch(`/dbRent/?user=${currentUser.id}`).then(response => response.json()),
        fetch("/dbMovie/").then(response => response.json()),
    ])
        .then(([checkouts, movies]) => {
            renderCheckedOut(checkouts);
            renderAvailableMovies(movies);
        })
        .catch(() => showMessage("Could not refresh rental data", "error"));
}

function findMember(email) {
    // Finds a member by email and then loads their rental tables
    fetch(`/dbUser/?email=${encodeURIComponent(email)}`)
        .then(response => response.json().then(data => ({ ok: response.ok, data })))
        .then(result => {
            if (!result.ok) {
                currentUser = null;
                document.querySelector("#member-section").classList.add("hidden");
                showMessage(result.data.error, "error");
                return;
            }

            currentUser = result.data;
            document.querySelector("#member-name").textContent = `${currentUser.first_name} ${currentUser.last_name}`;
            document.querySelector("#member-section").classList.remove("hidden");
            showMessage("");
            refreshRentalTables();
        })
        .catch(() => showMessage("Could not find member", "error"));
}

function updateRental(action, movieId) {
    // Sends a rent or return request for the selected movie
    if (!currentUser) {
        showMessage("Search for a member first", "error");
        return;
    }

    const formData = new FormData();
    formData.append("action", action);
    formData.append("user", currentUser.id);
    formData.append("movie", movieId);

    fetch("/dbRent/", {
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

            showMessage("");
            refreshRentalTables();
        })
        .catch(() => showMessage("Could not update rental data", "error"));
}

document.querySelector("#user-search-form").addEventListener("submit", function (event) {
    // Searches for the member entered in the email field
    event.preventDefault();
    findMember(document.querySelector("#member-email").value.trim());
});

document.querySelector("#checked-out-body").addEventListener("click", function (event) {
    // Returns a checked out movie when its row is clicked
    if (event.target.classList.contains("clickable")) {
        updateRental("return", event.target.dataset.movie);
    }
});

document.querySelector("#available-movies-body").addEventListener("click", function (event) {
    // Rents an available movie when its row is clicked
    if (event.target.classList.contains("clickable")) {
        updateRental("rent", event.target.dataset.movie);
    }
});
