import axios from 'axios';
import { FiTrash } from 'react-icons/fi';

interface ConversationItemProps {
  chatId: string;
  onSelect: (chatId: string) => void;
  activeChat: string | null;
  refreshChats: () => void;
}

const ConversationItem: React.FC<ConversationItemProps> = ({
  chatId,
  onSelect,
  activeChat,
  refreshChats,
}) => {
  const deleteChat = async () => {
    try {
      await axios.delete(`http://127.0.0.1:8000/delete-chat/${chatId}`);
      refreshChats();
    } catch (error) {
      console.error('Error deleting chat:', error);
    }
  };

  return (
    <li
      className={`flex justify-between items-center p-2 rounded cursor-pointer transition-all ${
        activeChat === chatId ? 'bg-stone-700' : 'hover:bg-stone-700'
      }`}
    >
      <span
        onClick={() => onSelect(chatId)}
        className='cursor-pointer'
      >
        Chat {chatId.slice(0, 8)}...
      </span>
      <button
        onClick={deleteChat}
        className='p-1 text-red-500 hover:text-red-300'
      >
        <FiTrash size={18} />
      </button>
    </li>
  );
};

export default ConversationItem;
