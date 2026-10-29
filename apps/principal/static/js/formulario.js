(() => {
    const form = document.getElementById("formulario");
    if (!form) return;

    const packagePrices = { xs: 3000, s: 3900, m: 4800, l: 5700, xl: 6800 };
    const regionFees = {
        "1": 2450, "2": 2000, "3": 1600, "4": 1250,
        "5": 950, "6": 700, "7": 500, "8": 700,
        "9": 950, "10": 1250, "11": 1600, "12": 2000,
        "13": 2500, "14": 3000, "15": 3550, "16": 4150,
    };

    const region = document.getElementById("id_region");
    const packageType = document.getElementById("id_tipoPaquete");
    const deliveryType = document.getElementById("id_tipoEnvio");
    const total = document.getElementById("totalAmount");
    const formatter = new Intl.NumberFormat("es-CL");

    function updateEstimate() {
        const base = packagePrices[packageType.value];
        const regionFee = regionFees[region.value];
        if (base === undefined || regionFee === undefined) {
            total.value = "Selecciona región y envío";
            return;
        }

        const expressFee = deliveryType.value === "express" ? 500 : 0;
        total.value = formatter.format(base + regionFee + expressFee);
    }

    [region, packageType, deliveryType].forEach((field) => {
        field.addEventListener("change", updateEstimate);
    });

    updateEstimate();
})();
