interface ChatMessagesProps {
  messages: { text: string; sender: 'user' | 'ai' }[];
}

const ChatMessages: React.FC<ChatMessagesProps> = ({ messages = [] }) => {
  return (
    <div className='flex-1 flex flex-col overflow-y-auto py-8 px-16 space-y-4 text-stone-100'>
      {messages.length === 0 && <p className='text-center text-stone-400'>No messages yet.</p>}
      {messages.map((msg, index) => (
        <div
          key={index}
          className={`p-3 rounded-lg inline-block max-w-[75%] break-words ${
            msg.sender === 'user' ? 'bg-blue-800 ml-auto text-right' : 'mr-auto text-left'
          }`}
        >
          {msg.text}
        </div>
      ))}
    </div>
  );
};

export default ChatMessages;
