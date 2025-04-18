import axios from 'axios';
import { useState } from 'react';
import { FiEdit, FiSave, FiTrash } from 'react-icons/fi';
import useWindowWidth from '../hooks/useWindowWidth';

interface ConversationItemProps {
  chat_id: string;
  title: string;
  onSelect: (chat_id: string) => void;
  activeChat: string | null;
  refreshChats: () => void;
  handleNewChat: () => void;
}

const ConversationItem: React.FC<ConversationItemProps> = ({
  chat_id,
  title,
  onSelect,
  activeChat,
  refreshChats,
  handleNewChat,
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [newTitle, setNewTitle] = useState(title || chat_id);

  const width = useWindowWidth();

  let maxTitleLength = 21;
  if (width < 1400) maxTitleLength = 19;
  if (width < 1300) maxTitleLength = 17;
  if (width < 1200) maxTitleLength = 15;
  if (width < 1100) maxTitleLength = 13;
  if (width < 1010) maxTitleLength = 11;
  if (width < 920) maxTitleLength = 9;
  if (width < 830) maxTitleLength = 7;

  if (width < 768) maxTitleLength = 21;

  const displayTitle =
    newTitle.length > maxTitleLength ? newTitle.slice(0, maxTitleLength).trim() + '...' : newTitle;

  const deleteChat = async (e: React.MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation();

    try {
      await axios.delete(`http://127.0.0.1:8000/delete-chat/${chat_id}`);

      if (activeChat === chat_id) {
        handleNewChat();
      }

      refreshChats();
    } catch (error) {
      console.error('Error deleting chat:', error);
    }
  };

  const updateTitle = async () => {
    if (!newTitle.trim()) return;

    try {
      await axios.post(
        `http://127.0.0.1:8000/update-chat-title/${chat_id}/${encodeURIComponent(newTitle)}`
      );
      setIsEditing(false);
      refreshChats();
    } catch (error) {
      console.error('Error updating chat title:', error);
    }
  };

  return (
    <li
      className={`flex justify-between items-center p-2 rounded cursor-pointer transition-all w-[28rem] md:max-w-[28rem] md:w-full ${
        activeChat === chat_id ? 'bg-stone-700' : 'hover:bg-stone-700'
      }`}
      onClick={() => !isEditing && onSelect(chat_id)}
    >
      {isEditing ? (
        <input
          type='text'
          value={newTitle}
          onChange={e => setNewTitle(e.target.value)}
          onBlur={updateTitle}
          onKeyDown={e => e.key === 'Enter' && updateTitle()}
          className='bg-transparent border-b border-stone-500 focus:outline-none w-full'
          autoFocus
        />
      ) : (
        <span
          className='cursor-pointer flex-grow'
          onDoubleClick={() => setIsEditing(true)}
        >
          {displayTitle}
        </span>
      )}

      <div className='flex'>
        {isEditing ? (
          <button
            onClick={updateTitle}
            className='p-1 mr-1 text-green-500 hover:text-green-400'
          >
            <FiSave size={18} />
          </button>
        ) : (
          <button
            onClick={e => {
              e.stopPropagation();
              setIsEditing(true);
            }}
            className='p-1 mr-1 text-stone-400 hover:text-stone-300'
          >
            <FiEdit size={18} />
          </button>
        )}

        <button
          onClick={deleteChat}
          className='p-1 text-red-500 hover:text-red-400'
        >
          <FiTrash size={18} />
        </button>
      </div>
    </li>
  );
};

export default ConversationItem;
