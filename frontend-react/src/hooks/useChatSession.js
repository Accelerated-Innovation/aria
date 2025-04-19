// src/hooks/useChatSession.js
import { useState, useEffect, useCallback } from 'react';
import chatService from '../services/chatService';

/**
 * Custom hook to manage chat session state and logic
 * @param {string} initialSessionId - Optional initial session ID
 * @returns {Object} Chat session methods and state
 */
export const useChatSession = (initialSessionId = null) => {
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(initialSessionId);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Initialize or restore session
  useEffect(() => {
    const initSession = async () => {
      // Use stored session or create new one
      const storedSessionId = localStorage.getItem('chatSessionId') || initialSessionId;
      
      if (storedSessionId) {
        setSessionId(storedSessionId);
        try {
          // Load existing chat history if available
          setIsLoading(true);
          const history = await chatService.getChatHistory(storedSessionId);
          if (history?.messages?.length) {
            const formattedMessages = history.messages.map(msg => ({
              text: msg.content,
              sender: msg.role,
              timestamp: new Date(msg.timestamp),
              id: msg.id
            }));
            setMessages(formattedMessages);
          }
        } catch (err) {
          console.warn('Could not fetch chat history:', err);
          // Continue with empty history
        } finally {
          setIsLoading(false);
        }
      } else {
        // Create new session
        const newSessionId = `session_${Date.now()}`;
        localStorage.setItem('chatSessionId', newSessionId);
        setSessionId(newSessionId);
      }
    };

    initSession();
  }, [initialSessionId]);

  // Send a message to the API
  const sendMessage = useCallback(async (messageText) => {
    if (!messageText.trim()) return;

    try {
      setIsLoading(true);
      setError(null);

      // Add user message to UI immediately
      const userMessage = { 
        text: messageText, 
        sender: 'user', 
        timestamp: new Date(),
        id: `temp_${Date.now()}`
      };
      setMessages(prev => [...prev, userMessage]);

      // Send to API
      const response = await chatService.sendMessage(messageText, sessionId);
      
      // Add bot response
      const botMessage = {
        text: response.response,
        sender: 'bot',
        timestamp: new Date(),
        id: response.message_id
      };
      
      setMessages(prev => [...prev, botMessage]);
      
      // Update session ID if it changed (e.g. first message)
      if (response.session_id !== sessionId) {
        setSessionId(response.session_id);
        localStorage.setItem('chatSessionId', response.session_id);
      }
      
      return botMessage;
    } catch (err) {
      setError('Failed to send message. Please try again.');
      console.error('Error sending message:', err);
      
      // Add error message to chat
      const errorMessage = {
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot',
        isError: true,
        timestamp: new Date(),
        id: `error_${Date.now()}`
      };
      setMessages(prev => [...prev, errorMessage]);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, [sessionId]);

  // Clear the current chat
  const clearChat = useCallback(() => {
    setMessages([]);
    // Optionally start a new session
    const newSessionId = `session_${Date.now()}`;
    localStorage.setItem('chatSessionId', newSessionId);
    setSessionId(newSessionId);
  }, []);

  return {
    messages,
    isLoading,
    error,
    sessionId,
    sendMessage,
    clearChat
  };
};

export default useChatSession;