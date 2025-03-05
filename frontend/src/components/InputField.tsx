import axios from 'axios';
import { useState } from 'react';
import { LuSendHorizontal } from 'react-icons/lu';

interface InputFieldProps {
  onSendMessage: (message: { text: string; sender: 'user' | 'ai' }) => void;
}

const InputField: React.FC<InputFieldProps> = ({ onSendMessage }) => {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { text: input, sender: 'user' } as const;
    onSendMessage(userMessage);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post('http://127.0.0.1:8000/ask/', {
        question: input,
      });

      const answer = response.data.answer;
      const aiMessage = { text: answer, sender: 'ai' } as const;
      onSendMessage(aiMessage);
    } catch (error) {
      console.error('Error sending message:', error);
      onSendMessage({ text: 'Error getting response from AI.', sender: 'ai' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className='p-4 bg-stone-800 flex items-center text-stone-100 mb-10 mx-10 rounded w-[50rem] self-center'>
      <input
        type='text'
        placeholder='Type a message...'
        className='flex-1 p-2 bg-stone-700 text-stone-200 rounded'
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && sendMessage()}
        disabled={loading}
      />
      <button
        onClick={sendMessage}
        className={`ml-2 py-2 px-4 rounded transition-all ${
          loading ? 'bg-gray-500 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-400'
        }`}
        disabled={loading}
      >
        <LuSendHorizontal size={20} />
      </button>
    </div>
  );
};

export default InputField;
