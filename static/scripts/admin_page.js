let users = [];

window.onload = function() {
    getTotalusers();
    populateTable();
};

function getTotalusers() {
    const totalusers = document.getElementById("totalusers");
    totalusers.textContent = users.length;
}

function populateTable() {
    const tableBody = document.querySelector("tbody");

    fetch('/admin')
        .then(response => response.json())
        .then(data => {
            users = data;
            users.forEach(user => {
                const row = document.createElement("tr");
                const IDcell = document.createElement("td");
                const nameCell = document.createElement("td");
                const emailCell = document.createElement("td");
                const usernameCell = document.createElement("td");

                IDcell.textContent = user.ID;
                nameCell.textContent = user.Name;
                emailCell.textContent = user.email;
                usernameCell.textContent = user.username;

                row.appendChild(IDcell);
                row.appendChild(nameCell);
                row.appendChild(emailCell);
                row.appendChild(usernameCell);

                tableBody.appendChild(row);
            });
            getTotalusers();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    populateTable();
    getTotalusers();
};

// let users = [
//     {ID: 1,Name:"Hardik", email: "user1@example.com", username: "user1" },
//     {ID: 2,Name:"Arnav", email: "user2@example.com", username: "user2" },
//     {ID: 3,Name:"Sudheera", email: "user3@example.com", username: "user3" }
// ];

function getTotalusers() {
    const totalusers = document.getElementById("totalusers");
    totalusers.textContent = users.length;
}

function populateTable() {
    const tableBody = document.querySelector("tbody");

    users.forEach(user => {
        const row = document.createElement("tr");
        const IDcell=document.createElement("td");
        const nameCell = document.createElement("td");
        const emailCell = document.createElement("td");
        const usernameCell = document.createElement("td");

        IDcell.textContent=user.ID;
        nameCell.textContent = user.Name;
        emailCell.textContent = user.email;
        usernameCell.textContent = user.username;

        row.appendChild(IDcell);
        row.appendChild(nameCell);
        row.appendChild(emailCell);
        row.appendChild(usernameCell);

        tableBody.appendChild(row);
    });
}