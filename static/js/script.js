flatpickr("#date-picker", {
    dateFormat: "Y-m-d",
    monthSelectorType: "dropdown",
    yearSelectorType: "input",
    allowInput: true,
    // Remove the onchange handler!
});

document.addEventListener("DOMContentLoaded", function () {
    // Wait for Flatpickr to render
    const fp = document.querySelector("#date-picker")._flatpickr;

    // Listen for change events on the month dropdown
    document.body.addEventListener("change", function (e) {
        if (e.target.classList.contains("flatpickr-monthDropdown-months")) {
            var select = e.target;
            var newMonth = select.selectedIndex;
            // Get the current selected date or today
            let date = fp.selectedDates[0] || new Date();
            // Set the new month, keep the day and year
            let newDate = new Date(date);
            newDate.setMonth(newMonth);
            // If the day is invalid for the new month (e.g., 31 in Feb), set to last day of month
            if (newDate.getMonth() !== newMonth) {
                newDate.setDate(0);
            }
            // Update Flatpickr and input field
            fp.setDate(newDate, true);
        }
    });
    // --- Month transactions pagination ---
    // --- Dashboard-specific JS ---

    // Show/hide reset and upload buttons
    const settingsCog = document.getElementById("settings-cog");
    if (settingsCog) {
        settingsCog.addEventListener("click", function () {
            const resetConfirm = document.getElementById("show-reset-confirm");
            const showUpload = document.getElementById("show-upload");
            if (resetConfirm) resetConfirm.classList.toggle("d-none");
            if (showUpload) showUpload.classList.toggle("d-none");
        });
    }

    // Show CSV help in modal if error tag present
    if (window.showCsvHelp) {
        const uploadModalElem = document.getElementById("uploadModal");
        if (uploadModalElem) {
            var uploadModal = new bootstrap.Modal(uploadModalElem);
            uploadModal.show();
            const csvHelp = document.getElementById("csv-help");
            if (csvHelp) csvHelp.classList.remove("d-none");
        }
    }

    // Show dashboard toasts if present
    if (window.dashboardMessages) {
        window.dashboardMessages.forEach(function (msg) {
            showDashboardToast(msg.text, msg.type);
        });
    }

    // Show month view toasts if present
    if (window.monthToasts) {
        window.monthToasts.forEach(function (msg) {
            showMonthToast(msg.text, msg.type);
        });
    }
});

function showDashboardToast(message, type = "info") {
    const icons = {
        success: "bi-check-circle-fill",
        warning: "bi-exclamation-triangle-fill",
        info: "bi-info-circle-fill",
        error: "bi-x-circle-fill",
        danger: "bi-x-circle-fill",
    };
    const toastDiv = document.getElementById("dashboard-toast");
    if (!toastDiv) return;
    toastDiv.innerHTML = `
        <div class="alert alert-${type} d-flex align-items-center gap-2 mb-0 py-2 px-3 rounded-3 shadow">
            <i class="bi ${icons[type] || icons.info} toast-icon"></i>
            <span>${message}</span>
        </div>
    `;
    toastDiv.style.display = "block";
    toastDiv.style.opacity = "1";
    toastDiv.style.transition = "opacity 0.5s";
    setTimeout(() => {
        toastDiv.style.opacity = "1";
    }, 10);
    setTimeout(() => {
        toastDiv.style.opacity = "0";
        setTimeout(() => {
            toastDiv.style.display = "none";
            toastDiv.innerHTML = "";
            toastDiv.style.opacity = "1";
        }, 500);
    }, 3000);
}
function showMonthToast(message, type = "info") {
    const icons = {
        success: "bi-check-circle-fill",
        warning: "bi-exclamation-triangle-fill",
        info: "bi-info-circle-fill",
        error: "bi-x-circle-fill",
    };

    const toastDiv = document.getElementById("month-toast");
    if (!toastDiv) return;

    toastDiv.innerHTML = `
        <div class="ww-toast alert-${type} d-flex align-items-center gap-2 mb-0 py-2 px-3 rounded-3 shadow">
            <i class="bi ${icons[type] || icons.info} toast-icon"></i>
            <span>${message}</span>
        </div>
    `;

    toastDiv.style.display = "block";
    toastDiv.style.opacity = "1";
    toastDiv.style.transition = "opacity 0.5s";

    setTimeout(() => {
        toastDiv.style.opacity = "1";
    }, 10);

    setTimeout(() => {
        toastDiv.style.opacity = "0";
        setTimeout(() => {
            toastDiv.style.display = "none";
            toastDiv.innerHTML = "";
            toastDiv.style.opacity = "1";
        }, 500);
    }, 3000);
}
