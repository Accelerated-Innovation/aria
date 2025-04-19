// src/components/ChatBot/ChatBot.jsx
import { useState, useEffect, useRef } from 'react';
import { Send, Paperclip, Trash, User, Bot } from 'lucide-react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import ChatHeader from './ChatHeader';

const ChatBot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message to chat
    const userMessage = { text: input, sender: 'user', timestamp: new Date() };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Call to your FastAPI backend
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      
      // Add bot response to chat
      const botMessage = { 
        text: data.response, 
        sender: 'bot', 
        timestamp: new Date() 
      };
      
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Error:', error);
      // Add error message
      const errorMessage = { 
        text: 'Sorry, I encountered an error. Please try again.', 
        sender: 'bot', 
        isError: true,
        timestamp: new Date() 
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className="flex flex-col h-full bg-gray-50 rounded-lg shadow-lg overflow-hidden">
      <ChatHeader onClearChat={clearChat} />
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-gray-500">
            <Bot size={48} className="mb-2" />
            <p>How can I help you today?</p>
          </div>
        ) : (
          messages.map((msg, index) => (
            <ChatMessage key={index} message={msg} />
          ))
        )}
        {isLoading && (
          <div className="flex items-center space-x-2 text-gray-500">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <p>Thinking...</p>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <ChatInput 
        input={input}
        isLoading={isLoading}
        onChange={handleInputChange}
        onSubmit={handleSubmit}
      />
    </div>
  );
};

export default ChatBot;