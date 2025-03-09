import axios from 'axios';
import { useEffect, useState } from 'react';
import { FaChevronLeft } from 'react-icons/fa';
import { FiPlus } from 'react-icons/fi';
import ConversationItem from './ConversationItem';

interface SidebarProps {
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
  setActiveChat: (chatId: string | null) => void;
  activeChat: string | null;
}

const Sidebar: React.FC<SidebarProps> = ({
  sidebarOpen,
  setSidebarOpen,
  setActiveChat,
  activeChat,
}) => {
  const [chats, setChats] = useState<string[]>([]);

  useEffect(() => {
    fetchChats();
  }, []);

  const fetchChats = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/get-chats/');
      setChats(response.data.chats);
    } catch (error) {
      console.error('Error fetching chats:', error);
    }
  };

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
        <h2 className='text-lg font-semibold text-center'>AI-Docs</h2>
        <button onClick={() => setSidebarOpen(false)}>
          <FaChevronLeft size={20} />
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
        {chats.map(chat => (
          <ConversationItem
            key={chat}
            chatId={chat}
            onSelect={setActiveChat}
            activeChat={activeChat}
            refreshChats={fetchChats}
          />
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;
