document.addEventListener("DOMContentLoaded", () => {
    const saveButton = document.getElementById("save-history");
    if (saveButton) {
        saveButton.addEventListener("click", () => {
            chrome.runtime.sendMessage({ action: "uploadHistory" }, (response) => {
                console.log(response);  // Ellenőrizze a választ a konzolon
            });
        });
    }
});
