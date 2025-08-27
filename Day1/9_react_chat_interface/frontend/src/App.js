import React, { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [isStreaming, setIsStreaming] = useState(false);
    const [currentThreadId, setCurrentThreadId] = useState('default');
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const sendMessage = async () => {
        if (!inputMessage.trim()) return;

        const userMessage = {
            id: Date.now(),
            role: 'user',
            content: inputMessage,
            timestamp: new Date().toLocaleTimeString()
        };

        // Add user message immediately
        setMessages(prev => [...prev, userMessage]);
        setInputMessage('');
        setIsStreaming(true);

        // Create AI message placeholder
        const aiMessageId = Date.now() + 1;
        const aiMessage = {
            id: aiMessageId,
            role: 'assistant',
            content: '',
            timestamp: new Date().toLocaleTimeString(),
            isStreaming: true
        };

        setMessages(prev => [...prev, aiMessage]);

        try {
            // Start streaming response
            const response = await fetch('/chat/stream', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: inputMessage,
                    thread_id: currentThreadId
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let accumulatedContent = '';

            while (true) {
                const { done, value } = await reader.read();

                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n');

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.slice(6));

                            if (data.type === 'chunk' && data.content) {
                                accumulatedContent += data.content;

                                // Update AI message with accumulated content
                                setMessages(prev => prev.map(msg =>
                                    msg.id === aiMessageId
                                        ? { ...msg, content: accumulatedContent }
                                        : msg
                                ));
                            } else if (data.type === 'complete') {
                                // Mark streaming as complete
                                setMessages(prev => prev.map(msg =>
                                    msg.id === aiMessageId
                                        ? { ...msg, isStreaming: false }
                                        : msg
                                ));
                                setIsStreaming(false);
                                break;
                            } else if (data.type === 'error') {
                                throw new Error(data.message);
                            }
                        } catch (parseError) {
                            console.error('Error parsing SSE data:', parseError);
                        }
                    }
                }
            }

        } catch (error) {
            console.error('Error sending message:', error);

            // Update AI message with error
            setMessages(prev => prev.map(msg =>
                msg.id === aiMessageId
                    ? { ...msg, content: 'Sorry, I encountered an error. Please try again.', isStreaming: false }
                    : msg
            ));

            setIsStreaming(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    const startNewChat = () => {
        setMessages([]);
        setCurrentThreadId(`thread_${Date.now()}`);
    };

    return (
        <div className="App">
            <div className="chat-container">
                {/* Header */}
                <div className="chat-header">
                    <h1>AI Chat Interface</h1>
                    <button
                        className="new-chat-btn"
                        onClick={startNewChat}
                        disabled={isStreaming}
                    >
                        + New Chat
                    </button>
                </div>

                {/* Messages */}
                <div className="messages-container">
                    {messages.length === 0 ? (
                        <div className="welcome-message">
                            <h3>👋 Welcome to AI Chat!</h3>
                            <p>Start a conversation by typing a message below.</p>
                        </div>
                    ) : (
                        messages.map((message) => (
                            <div
                                key={message.id}
                                className={`message ${message.role === 'user' ? 'user-message' : 'ai-message'}`}
                            >
                                <div className="message-content">
                                    {message.content}
                                    {message.isStreaming && (
                                        <span className="typing-indicator">▌</span>
                                    )}
                                </div>
                                <div className="message-timestamp">
                                    {message.timestamp}
                                </div>
                            </div>
                        ))
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input */}
                <div className="input-container">
                    <div className="input-wrapper">
                        <textarea
                            value={inputMessage}
                            onChange={(e) => setInputMessage(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder="Type your message here..."
                            disabled={isStreaming}
                            rows={1}
                        />
                        <button
                            onClick={sendMessage}
                            disabled={!inputMessage.trim() || isStreaming}
                            className="send-button"
                        >
                            {isStreaming ? '⏳' : '📤'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;
