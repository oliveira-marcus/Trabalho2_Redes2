/**
 * Participantes:
 *   Caio Bruno Gonzaga Liboreiro
 *   Kayky Nery Alcantara Vieira
 *   Marcus Vinícius de Oliveira Pinto
 */

// Variáveis globais
let ws = null;
let username = '';
let typingTimeout = null;

/**
 * Conecta ao servidor WebSocket
 */
function connect() {
    username = document.getElementById('usernameInput').value.trim();
    
    if (!username) {
        alert('Por favor, digite um nome de usuário!');
        return;
    }

    // Esconde modal e mostra chat
    document.getElementById('loginModal').classList.add('hidden');
    document.getElementById('chatContainer').classList.remove('hidden');

    // Cria conexão WebSocket
    ws = new WebSocket('ws://localhost:9000');

    ws.onopen = handleOpen;
    ws.onmessage = handleIncomingMessage;
    ws.onclose = handleClose;
    ws.onerror = handleError;
}

/**
 * Handler para conexão aberta
 */
function handleOpen() {
    console.log('Conectado ao servidor');
    document.getElementById('status').textContent = '🟢 Conectado';
    
    // Registra username no servidor
    ws.send(JSON.stringify({
        type: 'register',
        username: username
    }));
}

/**
 * Handler para mensagens recebidas
 */
function handleIncomingMessage(event) {
    const data = JSON.parse(event.data);
    handleMessage(data);
}

/**
 * Handler para conexão fechada
 */
function handleClose() {
    console.log('Desconectado do servidor');
    document.getElementById('status').textContent = '🔴 Desconectado';
    addSystemMessage('Conexão perdida com o servidor');
}

/**
 * Handler para erros
 */
function handleError(error) {
    console.error('Erro WebSocket:', error);
    addSystemMessage('Erro na conexão');
}

/**
 * Processa mensagens recebidas do servidor
 */
function handleMessage(data) {
    switch(data.type) {
        case 'message':
            addChatMessage(
                data.username, 
                data.message, 
                data.timestamp, 
                data.username === username
            );
            break;
        case 'system':
            addSystemMessage(data.message);
            break;
        case 'user_list':
            updateUsersList(data.users);
            break;
        case 'typing':
            showTypingIndicator(data.username);
            break;
    }
}

/**
 * Adiciona mensagem de chat à área de mensagens
 */
function addChatMessage(user, message, timestamp, isOwn) {
    const chatArea = document.getElementById('chatArea');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isOwn ? 'own' : 'other'}`;
    
    messageDiv.innerHTML = `
        ${!isOwn ? `<div class="message-header">${escapeHtml(user)}</div>` : ''}
        <div class="message-content">${escapeHtml(message)}</div>
        <div class="message-time">${escapeHtml(timestamp)}</div>
    `;
    
    chatArea.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Adiciona mensagem do sistema
 */
function addSystemMessage(message) {
    const chatArea = document.getElementById('chatArea');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message system';
    messageDiv.textContent = message;
    
    chatArea.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Atualiza lista de usuários online
 */
function updateUsersList(users) {
    document.getElementById('usersList').textContent = users.join(', ');
}

/**
 * Mostra indicador de digitação
 */
function showTypingIndicator(user) {
    const indicator = document.getElementById('typingIndicator');
    indicator.textContent = `${user} está digitando...`;
    
    setTimeout(() => {
        indicator.textContent = '';
    }, 2000);
}

/**
 * Envia mensagem para o servidor
 */
function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message || !ws) return;
    
    ws.send(JSON.stringify({
        type: 'message',
        message: message
    }));
    
    input.value = '';
    input.focus();
}

/**
 * Handler para evento de digitação
 */
function handleTyping() {
    if (!ws) return;
    
    clearTimeout(typingTimeout);
    
    typingTimeout = setTimeout(() => {
        ws.send(JSON.stringify({
            type: 'typing'
        }));
    }, 500);
}

/**
 * Handler para tecla pressionada
 */
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

/**
 * Escapa HTML para prevenir XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Rola área de chat para o final
 */
function scrollToBottom() {
    const chatArea = document.getElementById('chatArea');
    chatArea.scrollTop = chatArea.scrollHeight;
}

/**
 * Inicialização quando a página carrega
 */
window.onload = () => {
    // Foca no input de username
    document.getElementById('usernameInput').focus();
    
    // Permite Enter no input de username
    document.getElementById('usernameInput').onkeypress = (e) => {
        if (e.key === 'Enter') connect();
    };
};