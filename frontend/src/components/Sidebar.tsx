import { FaChevronLeft } from 'react-icons/fa';
import { FiPlus } from 'react-icons/fi';
import ConversationItem from './ConversationItem';

interface SidebarProps {
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
  setActiveChat: (chatId: string | null) => void;
  activeChat: string | null;
  chats: string[];
  fetchChats: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({
  sidebarOpen,
  setSidebarOpen,
  setActiveChat,
  activeChat,
  chats,
  fetchChats,
}) => {
  const handleNewChat = () => {
    setActiveChat(null);
  };

  return (
    <div
      className={`w-64 bg-stone-800 p-4 text-stone-100 border-r-1 border-stone-900 ${
        sidebarOpen ? '' : 'hidden'
      }`}
    >
      {/* Sidebar Header */}
      <div className='flex justify-between items-center'>
        <a href='#'>
          <h2 className='text-lg font-semibold text-center'>AI-Docs</h2>
        </a>
        <button onClick={() => setSidebarOpen(false)}>
          <FaChevronLeft size={18} />
        </button>
      </div>

      {/* New Chat Button */}
      <button
        onClick={handleNewChat}
        className='w-full mt-4 p-2 bg-blue-500 hover:bg-blue-400 transition-all rounded flex items-center justify-center gap-2'
      >
        <FiPlus /> New Chat
      </button>

      {/* Chat List */}
      <ul className='mt-4 space-y-2'>
        {chats.map((chat, i) => (
          <ConversationItem
            key={chat}
            chatId={chat}
            chatNum={i}
            onSelect={setActiveChat}
            activeChat={activeChat}
            refreshChats={fetchChats}
            handleNewChat={handleNewChat}
          />
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;
