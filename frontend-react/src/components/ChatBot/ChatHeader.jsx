// src/components/ChatBot/ChatHeader.jsx
import { Trash } from 'lucide-react';

const ChatHeader = ({ onClearChat }) => {
  return (
    <div className="bg-white border-b border-gray-200 p-4 flex justify-between items-center">
      <h3 className="font-medium text-lg">Knowledge Assistant</h3>
      <button
        onClick={onClearChat}
        className="text-gray-500 hover:text-red-500 transition-colors"
        aria-label="Clear chat"
      >
        <Trash size={18} />
      </button>
    </div>
  );
};

export default ChatHeader;