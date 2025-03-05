import axios from 'axios';
import { useEffect, useState } from 'react';
import { FaBars, FaRegFileAlt } from 'react-icons/fa';
import { FiSettings } from 'react-icons/fi';

import ChatMessages from './components/ChatMessages';
import InputField from './components/InputField';
import PDFModal from './components/PdfModal';
import SettingsModal from './components/SettingsModal';
import Sidebar from './components/Sidebar';

const App: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [FileOpen, setFileOpen] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [settings, setSettings] = useState({
    API_KEY: '',
    MODEL: 'gpt-3.5-turbo',
    SYSTEM_PROMPT: '',
  });
  const [messages, setMessages] = useState<{ text: string; sender: 'user' | 'ai' }[]>([]);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/get-settings/');
      setSettings(response.data);
    } catch (error) {
      console.error('Error fetching settings:', error);
    }
  };

  const handleSendMessage = (message: { text: string; sender: 'user' | 'ai' }) => {
    setMessages(prevMessages => [...prevMessages, message]);
  };

  return (
    <div className='flex h-screen bg-stone-900 text-stone-200'>
      <Sidebar
        sidebarOpen={sidebarOpen}
        setSidebarOpen={setSidebarOpen}
      />
      <div className='flex-1 flex flex-col'>
        {/* Header */}
        <div className='flex justify-between items-center bg-stone-800 p-4 text-stone-200'>
          <button onClick={() => setSidebarOpen(true)}>
            {!sidebarOpen ? <FaBars size={20} /> : ' '}
          </button>
          <h1 className='text-lg font-semibold text-center flex-1 ml-14'>Chat</h1>
          <div className='flex gap-6'>
            <button onClick={() => setFileOpen(true)}>
              <FaRegFileAlt size={20} />
            </button>
            <button onClick={() => setSettingsOpen(true)}>
              <FiSettings size={20} />
            </button>
          </div>
        </div>

        {/* Chat Messages */}
        <ChatMessages messages={messages} />

        {/* Input Field */}
        <InputField onSendMessage={handleSendMessage} />
      </div>

      {/* PDF Modal */}
      {FileOpen && <PDFModal setPdfModalOpen={setFileOpen} />}

      {/* Settings Modal */}
      {settingsOpen && (
        <SettingsModal
          setSettingsOpen={setSettingsOpen}
          fetchSettings={fetchSettings}
          settings={settings}
          setSettings={setSettings}
        />
      )}
    </div>
  );
};

export default App;
