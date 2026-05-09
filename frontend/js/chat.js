const sendBtn = document.getElementById("sendBtn");
const messageInput = document.getElementById("messageInput");
const chatMessages = document.getElementById("chatMessages");

const phone = localStorage.getItem("phone");

async function loadHistory(){
    try {
        const response = await fetch(
            `http://127.0.0.1:8000/history/${phone}`
        );
        const data = await response.json();

        const history = data.history;

        history.forEach(msg => {
            if(msg.role === "user"){
                addMessage(msg.content, "user-message");
            }
            else if(msg.role === "assistant"){
                addMessage(msg.content, "bot-message");
            }
        });

            
    } catch (error){
        console.error(error);
    }
}

// --- Add message bubble ---
function addMessage(text, className){
    const messageDiv = document.createElement("div");

    messageDiv.classList.add("message");
    messageDiv.classList.add(className);

    messageDiv.textContent = text;

    chatMessages.appendChild(messageDiv)
    
    // Auto-scroll
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// --- Send message ---
async function sendMessage() {
    const message = messageInput.value.trim();

    if (!message) return;

    // User bubble
    addMessage(message, "user-message")
    messageInput.value = "";

    // Thinking bubble
    addMessage("Thinking...","bot-message");

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                phone: phone,
                message: message
            })
        });

        const data = await response.json();

        // Remove "Thinking..."
        chatMessages.lastChild.remove();

        // Bot bubble
        addMessage(data.response, "bot-message");

    } catch (error) {
        console.error(error);

        chatMessages.lastChild.remove();

        addMessage("Error contacting server.", "bot-message");
    }
}

// --- Button click ---
sendBtn.addEventListener("click", sendMessage);

// --- Enter key ---
messageInput.addEventListener("keypress", function(event) {
    if(event.key === "Enter") {
        sendMessage();
    }
});

// --- Load old chats on page open ---
loadHistory();