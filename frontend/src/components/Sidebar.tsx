import { FiPlus } from 'react-icons/fi';
import { FaChevronLeft } from 'react-icons/fa';

interface SidebarProps {
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ sidebarOpen, setSidebarOpen }) => {
  if (!sidebarOpen) return null;

  return (
    <div className='w-64 bg-stone-800 p-4 text-stone-100 border-r-1 border-stone-900'>
      <div className='flex justify-between items-center'>
        <h2 className='text-lg font-semibold text-center'>AI-Docs</h2>
        <button onClick={() => setSidebarOpen(false)}>
          <FaChevronLeft size={20} />
        </button>
      </div>
      <button className='w-full mt-4 p-2 bg-blue-500 hover:bg-blue-400 transition-all rounded flex items-center justify-center gap-2'>
        <FiPlus /> New Chat
      </button>
    </div>
  );
};

export default Sidebar;
