
function sendUrlsToServer() {
    chrome.storage.local.get("urls", (result) => {
    if (chrome.runtime.lastError) {
        console.error("Error accessing local storage:", chrome.runtime.lastError);
        return;
    }
    const urls = result.urls || [];
    const filteredUrls = urls.filter(url => url !== "about:blank");
    if (urls.length === 0) {
        console.log("No URLs to send.");
        return;
    }

    // Feltételezzük, hogy a user_id a szerveren ismert (pl. token vagy session)
    const userId = "current_user_id"; // Ezt a szerver adhatja vissza bejelentkezéskor

    fetch("http://127.0.0.1:8000/upload_history/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ urls: urls, user_id: userId }), // Küldjük a user_id-t is
    })
        .then((response) => {
            if (response.ok) {
                console.log("URLs successfully sent to the server.");
                chrome.storage.local.remove("urls", () => {
                    console.log("Local storage cleared.");
                });
            } else {
                console.error("Failed to send URLs. Server responded with status:", response.status);
            }
        })
        .catch((error) => {
            console.error("Error sending URLs to the server:", error);
        });
    });
}

// Időzítő beállítása, hogy percenként fusson a küldés
setInterval(sendUrlsToServer, 60000);

// Első hívás, hogy ne kelljen várni egy percet
sendUrlsToServer();

