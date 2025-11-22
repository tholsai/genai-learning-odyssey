import { useState } from 'react'
import { chat } from '../services/api'

const Chatbot = () => {
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [useRag, setUseRag] = useState(true)

  const handleSend = async () => {
    if (!message.trim()) return

    const userMessage = { role: 'user', content: message }
    setMessages((prev) => [...prev, userMessage])
    setMessage('')
    setLoading(true)

    try {
      const response = await chat(message, useRag)
      const assistantMessage = {
        role: 'assistant',
        content: response.response,
      }
      setMessages((prev) => [...prev, assistantMessage])
    } catch (err) {
      const errorMessage = {
        role: 'assistant',
        content: 'Error: ' + (err.response?.data?.detail || err.message),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chatbot">
      <h2>AI Chatbot Assistant</h2>
      <div className="rag-toggle">
        <label>
          <input
            type="checkbox"
            checked={useRag}
            onChange={(e) => setUseRag(e.target.checked)}
          />
          Use RAG (Retrieval Augmented Generation) - Answers based on uploaded documents
        </label>
      </div>

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="welcome-message">
            Ask me questions about your requirements or the system!
          </div>
        )}
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <strong>{msg.role === 'user' ? 'You' : 'AI'}:</strong>
            <p>{msg.content}</p>
          </div>
        ))}
        {loading && <div className="message assistant">Thinking...</div>}
      </div>

      <div className="chat-input">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Type your message..."
          disabled={loading}
        />
        <button onClick={handleSend} disabled={loading || !message.trim()}>
          Send
        </button>
      </div>
    </div>
  )
}

export default Chatbot

