// src/components/Layout/Sidebar.jsx
import { useNavigate } from 'react-router-dom';
import { useChatContext } from '../../context/ChatContext';
import { MessageSquare, Plus, Trash, Settings } from 'lucide-react';

const Sidebar = ({ onClose }) => {
  const navigate = useNavigate();
  const { sessions, createNewSession, switchSession, activeSessionId } = useChatContext();
  
  const handleNewChat = () => {
    const sessionId = createNewSession();
    navigate(`/chat/${sessionId}`);
    if (onClose) onClose();
  };
  
  const handleSessionClick = (sessionId) => {
    switchSession(sessionId);
    navigate(`/chat/${sessionId}`);
    if (onClose) onClose();
  };
  
  return (
    <div className="flex flex-col h-full">
      <div className="p-4 border-b">
        <h1 className="text-xl font-bold">Knowledge Assistant</h1>
      </div>
      
      <div className="p-4">
        <button
          onClick={handleNewChat}
          className="w-full py-2 px-4 bg-blue-500 text-white rounded-lg flex items-center justify-center"
        >
          <Plus size={18} className="mr-2" />
          New Chat
        </button>
      </div>
      
      <div className="flex-1 overflow-y-auto p-2">
        <h2 className="text-xs uppercase text-gray-500 font-semibold px-2 mb-2">Recent Chats</h2>
        
        {sessions.length === 0 ? (
          <div className="text-center text-gray-500 p-4">
            No recent chats
          </div>
        ) : (
          <ul className="space-y-1">
            {sessions.map(session => (
              <li key={session.id}>
                <button
                  onClick={() => handleSessionClick(session.id)}
                  className={`w-full flex items-center px-3 py-2 rounded-md text-left ${
                    session.id === activeSessionId 
                      ? 'bg-blue-100 text-blue-700' 
                      : 'hover:bg-gray-100'
                  }`}
                >
                  <MessageSquare size={16} className="mr-2 flex-shrink-0" />
                  <span className="truncate">{session.title}</span>
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
      
      <div className="p-4 border-t">
        <button className="flex items-center justify-center w-full px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md">
          <Settings size={16} className="mr-2" />
          Settings
        </button>
      </div>
    </div>
  );
};

export default Sidebar;