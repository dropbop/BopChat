document.addEventListener('DOMContentLoaded', function() {
    const promptInput = document.getElementById('prompt');
    const conversationHistory = document.getElementById('conversationHistory');
    const llmForm = document.getElementById('llmForm');
    const modelSelect = document.getElementById('model');

    const modelNames = {
        'anthropic': 'Claude Sonnet 3.6',
        'openai_chatgpt-4o-latest': 'GPT-4o',
        'openai_o3-mini': 'o3-mini',
        'google_gemini-2.0-flash-thinking-exp-01-21': 'Gemini 2.0 FT',
        'google_gemini-2.0-flash-exp': 'Gemini 2.0',
        'google_gemini-exp-1206': 'Gemini 1206',
        'deepseek': 'DeepSeek R1'
    };

    // Configure Marked to enable GitHub-Flavored Markdown
    marked.setOptions({
        gfm: true,
        breaks: true,
        headerIds: false,
        smartLists: true,
        smartypants: false,
    });

    // --- Markdown Rendering Function ---
    function renderMarkdown(text) {
        return marked.parse(text);
    }

    // --- Function to Display a New Message ---
    function displayNewMessage(modelName, messageText, isUserMessage = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'markdown-content'); // Use 'message' base class and 'markdown-content'

        let fullHTML = "";
        if (!isUserMessage) {
            // Create the label HTML for LLM messages.
            fullHTML += `<strong class="mono small">${modelName}: </strong>`;
            messageDiv.classList.add('llm-message');
        } else {
            fullHTML += `<strong class="mono small">You: </strong>`; // Or just "You" if modelName is not needed for user
            messageDiv.classList.add('user-message');
        }

        // Append the rendered markdown content.
        fullHTML += renderMarkdown(messageText);
        messageDiv.innerHTML = fullHTML;

        console.log("--- messageText (HTML from server-side Markdown): ---"); // ADDED LOGGING
        console.log(messageText);
        conversationHistory.appendChild(messageDiv);
        messageDiv.scrollIntoView({ behavior: 'smooth', block: 'end' });
        Prism.highlightAllUnder(messageDiv);
    }

    // --- Shift+Enter to Send ---
    promptInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter' && event.ctrlKey) {
            event.preventDefault();
            llmForm.dispatchEvent(new Event('submit'));
        }
    });

    // --- Check for existing conversation UUID in URL ---
    let conversationUuid = null;
    const pathSegments = window.location.pathname.split('/');
    if (pathSegments[1] === 'chat' && pathSegments[2]) {
        conversationUuid = pathSegments[2]; // Extract UUID from URL like /chat/your-uuid
    }

    // --- Form Submission Handler ---
    llmForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const form = event.target;
        const promptValue = form.prompt.value;
        const modelValue = form.model.value;
        const modelName = modelNames[modelValue];

        if (!conversationUuid) {
            // --- New Conversation Logic ---
            fetch('/new_conversation', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams({ model: modelValue })
            })
            .then(response => response.json())
            .then(data => {
                conversationUuid = data.conversation_uuid; // Get UUID from backend
                window.history.pushState({}, '', `/chat/${conversationUuid}`); // Update URL

                // Now send the message to llm_query_stream, including the conversationUuid
                sendChatMessage(promptValue, modelValue, conversationUuid, modelName);
            });
        } else {
            // --- Existing Conversation Logic ---
            sendChatMessage(promptValue, modelValue, conversationUuid, modelName);
        }

        // Display user message immediately
        displayNewMessage('You', promptValue, true);
        form.prompt.value = ""; // Clear input
    });


    function sendChatMessage(prompt, model, uuid, modelDisplayName) {
        const formData = new URLSearchParams({
            prompt: prompt,
            conversation_uuid: uuid, // Include conversationUuid in formData
            model: model
        });

        fetch('/llm_query_stream', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        })
        .then(response => {
            const reader = response.body.getReader();
            const decoder = new TextDecoder("utf-8");
            let accumulatedResponse = '';

            function readStream() {
                reader.read().then(({ done, value }) => {
                    if (done) {
                        displayNewMessage(modelDisplayName, accumulatedResponse);
                        return;
                    }
                    const textChunk = decoder.decode(value);
                    accumulatedResponse += textChunk;
                    readStream();
                }).catch(error => {
                    const message = document.createElement('div');
                    message.className = 'message error';
                    message.textContent = 'Error: Could not connect to the model.';
                    conversationHistory.appendChild(message);
                });
            }
            readStream();
        });
    }


}); // End of DOMContentLoaded