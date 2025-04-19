// src/components/ChatBot/ChatMessage.jsx
import { format } from 'date-fns';
import { User, Bot } from 'lucide-react';

const ChatMessage = ({ message }) => {
  const { text, sender, timestamp, isError } = message;
  const isUser = sender === 'user';
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`flex max-w-3/4 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        <div className={`flex-shrink-0 h-8 w-8 rounded-full flex items-center justify-center 
          ${isUser ? 'bg-blue-500 ml-2' : 'bg-gray-200 mr-2'}`}>
          {isUser ? <User size={16} className="text-white" /> : <Bot size={16} />}
        </div>
        
        <div className={`px-4 py-2 rounded-lg ${
          isUser 
            ? 'bg-blue-500 text-white' 
            : isError 
              ? 'bg-red-100 text-red-800' 
              : 'bg-gray-200 text-gray-800'
        }`}>
          <div className="text-sm">{text}</div>
          <div className={`text-xs mt-1 ${isUser ? 'text-blue-100' : 'text-gray-500'}`}>
            {format(new Date(timestamp), 'HH:mm')}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;