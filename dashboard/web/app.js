async function loadIncidents() {
    try {
        const response = await fetch("/events/latest");
        const data = await response.json();

        const table = document.querySelector("#incident-table tbody");
        table.innerHTML = "";

        data.forEach(row => {
            const tr = document.createElement("tr");

            const [id, timestamp, message, risk] = row;

            tr.innerHTML = `
                <td>${id}</td>
                <td>${timestamp}</td>
                <td>${message}</td>
                <td class="risk-${risk}">
                    ${risk.toUpperCase()}
                </td>
            `;

            table.appendChild(tr);
        });

    } catch (err) {
        console.error("Error loading incidents:", err);
    }
}

// Ladda direkt
loadIncidents();

// Auto-refresh varannan sekund
setInterval(loadIncidents, 2000);
