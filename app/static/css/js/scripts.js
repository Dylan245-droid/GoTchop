document.addEventListener("DOMContentLoaded", function() {
    const themeButton = document.getElementById("toggleTheme");
    const isDarkMode = localStorage.getItem("darkMode") === "enabled";

    if (isDarkMode) {
        document.body.classList.add("dark-mode");
        themeButton.textContent = "☀️ Mode Clair";
    }

    themeButton.addEventListener("click", function() {
        document.body.classList.toggle("dark-mode");
        const isDark = document.body.classList.contains("dark-mode");
        localStorage.setItem("darkMode", isDark ? "enabled" : "disabled");
        themeButton.textContent = isDark ? "☀️ Mode Clair" : "🌙 Mode Sombre";
    });
});
