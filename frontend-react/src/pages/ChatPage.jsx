// src/pages/ChatPage.jsx
import { useState, useEffect } from 'react';
import ChatBot from '../components/ChatBot/ChatBot';
import chatService from '../services/chatService';

const ChatPage = () => {
  const [sessionId, setSessionId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Generate or retrieve session ID when component mounts
    const storedSessionId = localStorage.getItem('chatSessionId');
    if (storedSessionId) {
      setSessionId(storedSessionId);
    } else {
      // Generate a new session ID or let backend generate one
      const newSessionId = `session_${Date.now()}`;
      localStorage.setItem('chatSessionId', newSessionId);
      setSessionId(newSessionId);
    }
  }, []);

  const handleStartNewChat = () => {
    const newSessionId = `session_${Date.now()}`;
    localStorage.setItem('chatSessionId', newSessionId);
    setSessionId(newSessionId);
    // You could also reset the ChatBot component state here
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100 p-4">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold text-gray-800">Knowledge Assistant</h1>
        <button
          onClick={handleStartNewChat}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
        >
          Start New Chat
        </button>
      </div>
      
      <div className="flex-1 overflow-hidden">
        {error ? (
          <div className="h-full flex items-center justify-center">
            <div className="bg-red-100 text-red-800 p-4 rounded-lg">
              {error}
              <button 
                onClick={() => setError(null)} 
                className="ml-2 text-red-600 underline"
              >
                Try Again
              </button>
            </div>
          </div>
        ) : (
          <div className="h-full">
            <ChatBot sessionId={sessionId} chatService={chatService} />
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatPage;