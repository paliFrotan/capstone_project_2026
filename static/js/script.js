flatpickr("#date-picker", {
    dateFormat: "Y-m-d",
    monthSelectorType: "dropdown",
    yearSelectorType: "input", // ← THIS is the key
    allowInput: true, // ← REQUIRED for the arrows to appear
    onchange: function (selectedDates, dateStr, instance) {
        // When the date changes, submit the form
        instance.input.form.submit();
    },
});

document.addEventListener("DOMContentLoaded", function () {
    const rowsPerPage = 3; // change to 10 or 15 if you prefer
    let currentPage = 1;

    const tbody = document.getElementById("transactions-body");
    const rows = Array.from(tbody.querySelectorAll("tr"));
    const pagination = document.getElementById("pagination");

    function showPage(page) {
        const totalPages = Math.ceil(rows.length / rowsPerPage);

        if (page < 1) page = 1;
        if (page > totalPages) page = totalPages;

        currentPage = page;

        rows.forEach((row) => (row.style.display = "none"));

        const start = (page - 1) * rowsPerPage;
        const end = start + rowsPerPage;

        rows.slice(start, end).forEach((row) => {
            row.style.display = "";
        });

        renderPagination(totalPages);
    }

    function renderPagination(totalPages) {
        pagination.innerHTML = "";

        if (currentPage > 1) {
            const prev = document.createElement("button");
            prev.textContent = "Previous";
            prev.onclick = () => showPage(currentPage - 1);
            pagination.appendChild(prev);
        }

        for (let i = 1; i <= totalPages; i++) {
            const btn = document.createElement("button");
            btn.textContent = i;
            if (i === currentPage) btn.classList.add("active");
            btn.onclick = () => showPage(i);
            pagination.appendChild(btn);
        }

        if (currentPage < totalPages) {
            const next = document.createElement("button");
            next.textContent = "Next";
            next.onclick = () => showPage(currentPage + 1);
            pagination.appendChild(next);
        }
    }

    showPage(1);
});
