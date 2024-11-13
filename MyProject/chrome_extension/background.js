// Figyelmeztetjük a háttérszkriptet, ha egy új URL-t látogatnak meg
chrome.webNavigation.onCompleted.addListener((details) => {
    chrome.tabs.get(details.tabId, (tab) => {
        if (tab.url) {
            saveUrlToStorage(tab.url);
        }
    });
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "uploadHistory") {
        console.log("History upload triggered");
        // A kívánt akciók itt
        sendResponse({ status: "success", message: "History upload initiated" });
    }
});

// URL-ek mentése Chrome tárhelyre
function saveUrlToStorage(url) {
    chrome.storage.local.get({ urls: [] }, (result) => {
        const urls = result.urls;
        urls.push(url);  // Új URL hozzáadása
        chrome.storage.local.set({ urls: urls });
    });
}
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, { action: "collectPageInfo" }, (response) => {
        if (response) {
            saveUrlToStorage(response.url, response.title);
        }
    });
});

// Periodikus mentés a szerverre
setInterval(() => {
    chrome.storage.local.get({ urls: [] }, (result) => {
        if (result.urls.length > 0) {
            fetch('http://127.0.0.1:8000/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ urls: result.urls })
            })
            .then(() => {
                // Sikeres mentés után töröljük a mentett URL-eket
                chrome.storage.local.set({ urls: [] });
            })
            .catch((error) => console.error("Hiba történt az URL-ek mentése közben:", error));
        }
    });
}, 3600000); // Minden órában
