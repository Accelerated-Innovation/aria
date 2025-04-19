// src/components/ChatBot/ChatInput.jsx
import { Send, Paperclip } from 'lucide-react';

const ChatInput = ({ input, isLoading, onChange, onSubmit }) => {
  return (
    <form onSubmit={onSubmit} className="border-t border-gray-200 p-4">
      <div className="flex items-center bg-white rounded-lg border border-gray-300 focus-within:ring-2 focus-within:ring-blue-500 focus-within:border-blue-500">
        <button 
          type="button" 
          className="flex-shrink-0 text-gray-500 hover:text-gray-700 p-2"
          aria-label="Attach file"
        >
          <Paperclip size={20} />
        </button>
        
        <input
          type="text"
          value={input}
          onChange={onChange}
          placeholder="Type your message..."
          disabled={isLoading}
          className="flex-1 p-2 outline-none bg-transparent"
        />
        
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className={`flex-shrink-0 p-2 rounded-r-lg ${
            isLoading || !input.trim() 
              ? 'text-gray-400' 
              : 'text-blue-500 hover:text-blue-700'
          }`}
          aria-label="Send message"
        >
          <Send size={20} />
        </button>
      </div>
    </form>
  );
};

export default ChatInput;