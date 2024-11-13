// content.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "collectPageInfo") {
        // Például oldalcím és URL küldése
        const pageInfo = {
            title: document.title,
            url: window.location.href
        };
        sendResponse(pageInfo);
    }
});
