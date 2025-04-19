// src/context/ChatContext.jsx
import { createContext, useContext, useState } from 'react';
import useChatSession from '../hooks/useChatSession';

// Create context
const ChatContext = createContext(null);

/**
 * Provider component that wraps your app and makes chat context available to any
 * child component that calls useChatContext().
 */
export const ChatProvider = ({ children }) => {
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [sessions, setSessions] = useState([]);
  
  const chatSession = useChatSession(activeSessionId);
  
  // Create a new chat session
  const createNewSession = () => {
    const newSessionId = `session_${Date.now()}`;
    setActiveSessionId(newSessionId);
    setSessions(prev => [...prev, { id: newSessionId, title: 'New Chat' }]);
    return newSessionId;
  };
  
  // Switch between existing sessions
  const switchSession = (sessionId) => {
    setActiveSessionId(sessionId);
  };
  
  // Update session title
  const updateSessionTitle = (sessionId, title) => {
    setSessions(prev => 
      prev.map(session => 
        session.id === sessionId ? { ...session, title } : session
      )
    );
  };
  
  // Value provided to consumers of this context
  const value = {
    ...chatSession,
    activeSessionId,
    sessions,
    createNewSession,
    switchSession,
    updateSessionTitle
  };
  
  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
};

// Custom hook to use the chat context
export const useChatContext = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChatContext must be used within a ChatProvider');
  }
  return context;
};