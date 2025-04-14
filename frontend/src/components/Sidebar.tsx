import { FiPlus } from 'react-icons/fi';
import ConversationItem from './ConversationItem';
import { FaChevronLeft } from 'react-icons/fa';

interface SidebarProps {
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
  setActiveChat: (chat_id: string | null) => void;
  activeChat: string | null;
  chats: { chat_id: string; title: string }[];
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
      className={`md:w-[25%] md:max-w-[20rem] bg-stone-800 p-4 text-stone-100 border-r-1 h-screen flex flex-col border-stone-900 ${
        sidebarOpen ? 'w-[100%]' : 'hidden'
      }`}
    >
      {/* Sidebar Header */}

      <div className='flex justify-center items-center w-full relative'>
        <a href='#'>
          <h2 className='text-xl font-medium font-roboto'>AI-Docs</h2>
        </a>
        <button
          onClick={() => setSidebarOpen(false)}
          className='absolute -right-0 p-1.5 rounded-lg transition-all duration-200 hover:bg-stone-700'
        >
          <FaChevronLeft size={18} />
        </button>
      </div>

      {/* New Chat Button */}
      <button
        onClick={handleNewChat}
        className='w-80 md:w-full md:max-w-80 mt-8 p-2 bg-gray-500 hover:bg-gray-400 transition-all duration-200 rounded flex items-center justify-center self-center gap-2'
      >
        <FiPlus /> New Chat
      </button>

      {/* Chat List */}
      <ul className='mt-4 space-y-2 overflow-y-auto max-h-screen flex flex-col items-center w-full'>
        {chats.map(({ chat_id, title }) => (
          <ConversationItem
            key={chat_id}
            chat_id={chat_id}
            title={title}
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
