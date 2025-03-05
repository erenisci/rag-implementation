import { useState } from 'react';

const ChatMessages: React.FC = () => {
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);

  return (
    <div className='flex-1 overflow-y-auto p-4 space-y-4 text-stone-100'>
      {messages.length === 0 && <p className='text-center text-stone-400'>No messages yet.</p>}
      {messages.map((msg, index) => (
        <div
          key={index}
          className={`p-3 rounded max-w-2xl ${
            msg.role === 'user' ? 'bg-stone-700 ml-auto' : 'bg-stone-700 mr-auto'
          }`}
        >
          {msg.content}
        </div>
      ))}
    </div>
  );
};

export default ChatMessages;
