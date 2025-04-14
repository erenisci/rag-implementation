import { useEffect, useRef } from 'react';

interface ChatMessagesProps {
  messages: { text: string; sender: 'user' | 'ai' }[];
  chatId: string | null;
}

const ChatMessages: React.FC<ChatMessagesProps> = ({ messages = [] }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className='flex-1 flex flex-col overflow-y-auto px-[6%] sm:px-[8%] md:px-[6%] lg:px-[10%] xl:px-[14%] 2xl:px-[18%] my-8 space-y-4 text-gray-200 items-center w-full self-center'>
      {messages.length === 0 && <p className='text-center text-stone-400'>No messages yet.</p>}
      {messages.map((msg, index) => (
        <div
          key={index}
          className={`p-3 rounded-lg inline-block max-w-[75%] break-words ${
            msg.sender === 'user'
              ? 'bg-gray-700 ml-auto text-right'
              : 'bg-gray-800 mr-auto text-left'
          }`}
        >
          {msg.text}
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatMessages;
