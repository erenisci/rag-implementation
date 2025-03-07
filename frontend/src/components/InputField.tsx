import axios from 'axios';
import { useRef, useState } from 'react';
import { LuSendHorizontal } from 'react-icons/lu';

interface InputFieldProps {
  onSendMessage: (message: { text: string; sender: 'user' | 'ai' }) => void;
}

const InputField: React.FC<InputFieldProps> = ({ onSendMessage }) => {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

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
      <textarea
        ref={textareaRef}
        placeholder='Type a message...'
        className='flex-1 p-2 bg-stone-700 text-stone-200 rounded resize-none overflow-hidden min-h-[40px] max-h-40'
        value={input}
        onChange={e => {
          setInput(e.target.value);
          if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
            textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
          }
        }}
        onKeyDown={e => {
          if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
          }
        }}
        rows={1}
        disabled={loading}
      />
      <button
        onClick={sendMessage}
        className={`ml-2 py-2 px-4 rounded transition-all self-end ${
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
