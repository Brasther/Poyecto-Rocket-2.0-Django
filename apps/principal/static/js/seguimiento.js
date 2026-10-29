(() => {
    const form = document.getElementById("tracking-form");
    if (!form) return;

    const input = document.getElementById("tracking-code");
    const result = document.getElementById("tracking-result");

    function showMessage(message, kind = "info") {
        const alert = document.createElement("div");
        alert.className = `alert alert-${kind}`;
        alert.setAttribute("role", "status");
        alert.textContent = message;
        result.replaceChildren(alert);
    }

    function addDetail(list, label, value) {
        const row = document.createElement("div");
        row.className = "d-flex justify-content-between gap-3 py-2 border-bottom";
        const term = document.createElement("dt");
        const detail = document.createElement("dd");
        term.className = "mb-0 text-secondary";
        detail.className = "mb-0 fw-medium text-end";
        term.textContent = label;
        detail.textContent = value;
        row.append(term, detail);
        list.append(row);
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        if (!form.reportValidity()) return;

        const button = form.querySelector("button[type='submit']");
        button.disabled = true;
        showMessage("Buscando envío…");

        try {
            const endpoint = new URL(form.dataset.endpoint, window.location.origin);
            endpoint.searchParams.set("numero_seguimiento", input.value.trim());
            const response = await fetch(endpoint, { headers: { Accept: "application/json" } });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || "No se encontró el envío.");

            const card = document.createElement("article");
            card.className = "card shadow-sm";
            const body = document.createElement("div");
            body.className = "card-body";
            const heading = document.createElement("h3");
            heading.className = "h5 card-title";
            heading.textContent = "Estado del envío";
            const details = document.createElement("dl");
            details.className = "mb-0";
            addDetail(details, "Código", data.codigo_seguimiento);
            addDetail(details, "Estado", data.estado_envio);
            addDetail(details, "Paquete", data.tipo_paquete);
            addDetail(details, "Servicio", data.tipo_envio);
            body.append(heading, details);
            card.append(body);
            result.replaceChildren(card);
        } catch (error) {
            showMessage(error.message || "No fue posible consultar el envío.", "warning");
        } finally {
            button.disabled = false;
        }
    });
})();
