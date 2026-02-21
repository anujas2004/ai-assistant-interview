// Send message function
async function sendMessage() {
    const userId = document.getElementById("user_id").value;
    const messageInput = document.getElementById("message");
    const message = messageInput.value;
    const mode = document.getElementById("mode").value;
    const chatBox = document.getElementById("chat-box");

    if (!message.trim()) return;

    // Show user message
    chatBox.innerHTML += `<div class="user-msg">${message}</div>`;

    // Show loading indicator
    const loadingId = "loading-" + Date.now();
    chatBox.innerHTML += `<div class="bot-msg" id="${loadingId}">Typing...</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: userId,
                question: message,
                mode: mode
            })
        });

        const data = await response.json();

        // Remove loading
        document.getElementById(loadingId).remove();

        // Show bot response
        chatBox.innerHTML += `<div class="bot-msg">${data.response}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;

    } catch (error) {
        document.getElementById(loadingId).remove();
        chatBox.innerHTML += `<div class="bot-msg">Error connecting to server.</div>`;
    }

    messageInput.value = "";
}


// Clear chat function
function clearChat() {
    document.getElementById("chat-box").innerHTML = "";
}


// ✅ Enable Enter key (IMPORTANT: Outside sendMessage)
document.addEventListener("DOMContentLoaded", function () {
    const messageInput = document.getElementById("message");

    messageInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });
});