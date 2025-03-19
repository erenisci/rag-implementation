import axios from 'axios';
import { useEffect, useState } from 'react';
import { FiEye, FiEyeOff } from 'react-icons/fi';

interface Settings {
  OPENAI_API_KEY: string;
  MODEL: string;
  SYSTEM_PROMPT: string;
}

interface SettingsModalProps {
  settings: Settings;
  setSettings: (settings: { OPENAI_API_KEY: string; MODEL: string; SYSTEM_PROMPT: string }) => void;
  setSettingsOpen: (open: boolean) => void;
  fetchSettings: () => Promise<void>;
}

const SettingsModal: React.FC<SettingsModalProps> = ({
  settings,
  setSettings,
  setSettingsOpen,
  fetchSettings,
}) => {
  const [localSettings, setLocalSettings] = useState<Settings>(settings);
  const [showApiKey, setShowApiKey] = useState(false);

  useEffect(() => {
    setLocalSettings(settings);
  }, [settings]);

  const updateSettings = async () => {
    try {
      const trimmedSettings = {
        OPENAI_API_KEY: localSettings.OPENAI_API_KEY.replace(/^\s+|\s+$/g, ''),
        MODEL: localSettings.MODEL.replace(/^\s+|\s+$/g, ''),
        SYSTEM_PROMPT: localSettings.SYSTEM_PROMPT.replace(/^\s+|\s+$/g, ''),
      };
      setLocalSettings(trimmedSettings);
      setSettings(trimmedSettings);

      await axios.post('http://127.0.0.1:8000/update-settings/', localSettings, {
        headers: { 'Content-Type': 'application/json' },
      });

      alert('Settings updated successfully!');
      await fetchSettings();

      setSettingsOpen(false);
    } catch (error) {
      console.error('Error updating settings:', error);
      alert('Failed to update settings.');
    }
  };

  return (
    <div className='fixed inset-0 bg-stone-900 bg-opacity-50 flex justify-center items-center'>
      <div className='bg-stone-800 p-6 rounded-lg w-[30rem]'>
        <h2 className='text-xl font-medium mb-4'>Settings</h2>
        <label className='block mb-2 relative'>
          API Key:
          <div className='flex items-center bg-stone-700 rounded mt-1 p-2'>
            <input
              type={showApiKey ? 'text' : 'password'}
              className='w-full bg-transparent outline-none'
              value={localSettings.OPENAI_API_KEY}
              onChange={e => setLocalSettings({ ...localSettings, OPENAI_API_KEY: e.target.value })}
            />
            <button
              onClick={() => setShowApiKey(!showApiKey)}
              className='ml-2 px-1 text-gray-400 hover:text-gray-200'
            >
              {showApiKey ? <FiEyeOff /> : <FiEye />}
            </button>
          </div>
        </label>
        <label className='block mb-2'>
          Model:
          <select
            className='w-full p-2 bg-stone-700 rounded mt-1'
            value={localSettings.MODEL}
            onChange={e => setLocalSettings({ ...localSettings, MODEL: e.target.value })}
          >
            <option value='gpt-3.5-turbo'>GPT-3.5 Turbo</option>
            <option value='gpt-4'>GPT-4</option>
          </select>
        </label>
        <label className='block mb-2'>
          System Prompt:
          <textarea
            className='w-full p-3 bg-stone-700 rounded mt-1 h-39 resize-none overflow-y-auto'
            value={localSettings.SYSTEM_PROMPT}
            onChange={e => setLocalSettings({ ...localSettings, SYSTEM_PROMPT: e.target.value })}
          />
        </label>
        <div className='flex justify-end mt-4'>
          <button
            onClick={() => setSettingsOpen(false)}
            className='mr-2 w-18 bg-red-500 hover:bg-red-400 transition-all duration-300 p-2 rounded'
          >
            Cancel
          </button>
          <button
            onClick={updateSettings}
            className='w-18 bg-green-500 hover:bg-green-400 transition-all duration-300 p-2 rounded'
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
};

export default SettingsModal;
