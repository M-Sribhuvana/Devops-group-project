import React, { useState, useRef, useEffect } from 'react';
import { Bot, MessageSquare, Send, X, Sparkles, Sprout } from 'lucide-react';

export default function ChatWidget({ activeDiagnosis }) {
  const [isOpen, setIsOpen] = useState(false);
  const [inputMessage, setInputMessage] = useState('');
  const [isSending, setIsSending] = useState(false);
  const chatBodyRef = useRef(null);

  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'assistant',
      text: "Hello! I am **Crop Doctor AI**, your botanical diagnostic expert. Ask me anything about crop diseases, organic remedies, fungicide schedules, or soil management!"
    }
  ]);

  useEffect(() => {
    if (chatBodyRef.current) {
      chatBodyRef.current.scrollTop = chatBodyRef.current.scrollHeight;
    }
  }, [messages, isOpen]);

  const handleSendMessage = async (textToSend) => {
    const text = textToSend || inputMessage;
    if (!text.trim() || isSending) return;

    const userMsg = { id: Date.now(), sender: 'user', text };
    setMessages((prev) => [...prev, userMsg]);
    if (!textToSend) setInputMessage('');
    setIsSending(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: text,
          disease_context: activeDiagnosis ? activeDiagnosis.prediction : null
        })
      });

      if (!response.ok) throw new Error("Chat request failed");
      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, sender: 'assistant', text: data.response }
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          sender: 'assistant',
          text: "I am having trouble reaching the chat server right now. Please verify if your FastAPI backend is running on port 8000."
        }
      ]);
    } finally {
      setIsSending(false);
    }
  };

  return (
    <>
      {/* Floating 3D Tactile Trigger Button */}
      <button
        className="chatbot-trigger"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle Crop Doctor Assistant"
      >
        {isOpen ? <X size={26} /> : <Bot size={28} />}
      </button>

      {/* Chat Window Modal */}
      {isOpen && (
        <div className="chat-modal">
          <div className="chat-header">
            <h3>
              <Sprout size={20} color="#FFFFFF" />
              <span>Crop Doctor AI Assistant</span>
            </h3>
            <button className="chat-close-btn" onClick={() => setIsOpen(false)} aria-label="Close chat">
              <X size={18} />
            </button>
          </div>

          <div className="chat-body" ref={chatBodyRef}>
            {messages.map((msg) => (
              <div key={msg.id} className={`chat-msg ${msg.sender}`}>
                <div style={{ fontWeight: 700, fontSize: '0.74rem', opacity: 0.85, marginBottom: '0.2rem' }}>
                  {msg.sender === 'user' ? 'You' : 'Crop Doctor AI'}
                </div>
                <div style={{ whiteSpace: 'pre-line' }}>{msg.text}</div>
              </div>
            ))}
            {isSending && (
              <div className="chat-msg assistant" style={{ fontStyle: 'italic', color: 'var(--text-muted)' }}>
                Crop Doctor is researching...
              </div>
            )}
          </div>

          {/* Quick Preset Buttons */}
          <div style={{
            padding: '0.5rem 0.8rem',
            background: 'var(--bg-canvas-subtle)',
            borderTop: '1px solid var(--border-subtle)',
            display: 'flex',
            gap: '0.4rem',
            overflowX: 'auto'
          }}>
            <button
              onClick={() => handleSendMessage("How do I treat Wheat Rust organically?")}
              className="crop-tag"
              style={{ fontSize: '0.72rem', cursor: 'pointer', padding: '0.25rem 0.65rem' }}
            >
              🌾 Organic Wheat Rust
            </button>
            <button
              onClick={() => handleSendMessage("How to prevent Corn Blight?")}
              className="crop-tag"
              style={{ fontSize: '0.72rem', cursor: 'pointer', padding: '0.25rem 0.65rem' }}
            >
              🌽 Prevent Blight
            </button>
            <button
              onClick={() => handleSendMessage("How to treat Tomato Curl Virus?")}
              className="crop-tag"
              style={{ fontSize: '0.72rem', cursor: 'pointer', padding: '0.25rem 0.65rem' }}
            >
              🍅 Tomato Curl
            </button>
          </div>

          <div className="chat-input-area">
            <input
              type="text"
              className="chat-input"
              placeholder="Ask about plant pathology, remedies..."
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
            />
            <button
              className="chat-send-btn"
              onClick={() => handleSendMessage()}
              disabled={isSending}
              aria-label="Send message"
            >
              <Send size={18} />
            </button>
          </div>
        </div>
      )}
    </>
  );
}
