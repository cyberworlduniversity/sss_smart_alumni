(function () {
    const STORAGE_KEY = "smartAlumniTheme";

    function getTheme() {
        return localStorage.getItem(STORAGE_KEY) || "light";
    }

    function applyTheme(theme) {
        document.documentElement.classList.toggle("dark-mode", theme === "dark");
        updateButtons(theme);
    }

    function updateButtons(theme) {
        document.querySelectorAll(".dark-mode-toggle").forEach(function (button) {
            const icon = button.querySelector(".theme-icon");
            const text = button.querySelector(".theme-text");

            if (theme === "dark") {
                if (icon) icon.textContent = "☀️";
                if (text) text.textContent = "Light Mode";
                button.setAttribute("aria-label", "Switch to light mode");
                button.setAttribute("title", "Switch to light mode");
            } else {
                if (icon) icon.textContent = "🌙";
                if (text) text.textContent = "Dark Mode";
                button.setAttribute("aria-label", "Switch to dark mode");
                button.setAttribute("title", "Switch to dark mode");
            }
        });
    }

    // Apply before page rendering where possible.
    applyTheme(getTheme());

    document.addEventListener("DOMContentLoaded", function () {
        updateButtons(getTheme());

        document.querySelectorAll(".dark-mode-toggle").forEach(function (button) {
            button.addEventListener("click", function () {
                const newTheme = document.documentElement.classList.contains("dark-mode")
                    ? "light"
                    : "dark";

                localStorage.setItem(STORAGE_KEY, newTheme);
                applyTheme(newTheme);
            });
        });
    });
})();
