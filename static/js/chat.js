const chatForm = document.getElementById('chat-form');
const questionInput = document.getElementById('question-input');
const chatMessages = document.getElementById('chat-messages');
const sendButton = document.getElementById('send-button');

function addUserMessage(question) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = question;
    
    messageDiv.appendChild(bubble);
    chatMessages.appendChild(messageDiv);
    
    const welcomeMessage = chatMessages.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }
    
    scrollToBottom();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function typeText(element, text, speed = 15) {
    return new Promise((resolve) => {
        let index = 0;
        let currentHTML = '';
        
        function typeChar() {
            if (index < text.length) {
                const char = text[index];
                
                if (char === '\n') {
                    currentHTML += '<br>';
                } else {
                    const escapedChar = escapeHtml(char);
                    currentHTML += escapedChar;
                }
                
                element.innerHTML = currentHTML;
                index++;
                scrollToBottom();
                
                let delay = speed;
                if (char === ' ' || char === '\n') {
                    delay = speed * 0.5;
                } else if (char === '.' || char === '!' || char === '?') {
                    delay = speed * 2;
                } else if (char === ',' || char === ';' || char === ':') {
                    delay = speed * 1.5;
                }
                
                setTimeout(typeChar, delay);
            } else {
                resolve();
            }
        }
        typeChar();
    });
}

async function addAssistantMessage(answer, articles) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    
    const answerText = document.createElement('div');
    bubble.appendChild(answerText);
    
    messageDiv.appendChild(bubble);
    chatMessages.appendChild(messageDiv);
    
    await typeText(answerText, answer, 15);
    
    if (articles && articles.length > 0) {
        for (const article of articles) {
            await new Promise(resolve => setTimeout(resolve, 300));
            
            const citation = document.createElement('div');
            citation.className = 'article-citation';
            
            const title = document.createElement('strong');
            title.textContent = `Artikulli ${article.article_number}`;
            citation.appendChild(title);
            
            const text = document.createElement('p');
            citation.appendChild(text);
            
            bubble.appendChild(citation);
            
            const articleContent = article.full_text || article.article_text || '';
            
            await typeText(text, articleContent, 15);
            scrollToBottom();
        }
    }
    
    scrollToBottom();
}

function addLoadingMessage() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    messageDiv.id = 'loading-message';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble loading';
    
    const dots = document.createElement('div');
    dots.className = 'loading-dots';
    for (let i = 0; i < 3; i++) {
        const span = document.createElement('span');
        dots.appendChild(span);
    }
    
    bubble.appendChild(dots);
    messageDiv.appendChild(bubble);
    chatMessages.appendChild(messageDiv);
    
    scrollToBottom();
}

function removeLoadingMessage() {
    const loadingMessage = document.getElementById('loading-message');
    if (loadingMessage) {
        loadingMessage.remove();
    }
}

function addErrorMessage(error) {
    removeLoadingMessage();
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = `Gabim: ${error}`;
    chatMessages.appendChild(errorDiv);
    
    scrollToBottom();
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const question = questionInput.value.trim();
    
    if (!question) {
        return;
    }
    
    questionInput.disabled = true;
    sendButton.disabled = true;
    
    addUserMessage(question);
    
    questionInput.value = '';
    
    addLoadingMessage();
    
    try {
        const response = await fetch('/api/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question }),
        });
        
        const data = await response.json();
        
        removeLoadingMessage();
        
        if (!response.ok) {
            addErrorMessage(data.error || 'Një gabim ka ndodhur');
        } else {
            addAssistantMessage(data.answer, data.articles);
        }
    } catch (error) {
        removeLoadingMessage();
        addErrorMessage('Nuk mund të lidhem me serverin. Ju lutem provoni përsëri.');
        console.error('Error:', error);
    } finally {
        questionInput.disabled = false;
        sendButton.disabled = false;
        questionInput.focus();
    }
});

questionInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});

questionInput.focus();
