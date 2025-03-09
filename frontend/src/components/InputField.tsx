import { useRef, useState } from 'react';
import { LuSendHorizontal } from 'react-icons/lu';

interface InputFieldProps {
  onSendMessage: (message: { text: string; sender: 'user' | 'ai' }) => void;
}

const InputField: React.FC<InputFieldProps> = ({ onSendMessage }) => {
  const [input, setInput] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    if (!input.trim()) return;

    onSendMessage({ text: input, sender: 'user' });
    setInput('');

    requestAnimationFrame(() => {
      if (textareaRef.current) {
        textareaRef.current.focus();
      }
    });
  };

  return (
    <div className='p-4 bg-stone-800 flex items-center text-stone-100 mb-10 mx-10 rounded w-[50rem] self-center'>
      <textarea
        ref={textareaRef}
        placeholder='Type a message...'
        className='flex-1 p-2 bg-stone-700 text-stone-200 rounded resize-none overflow-hidden min-h-[40px] max-h-40'
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => {
          if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
          }
        }}
        rows={1}
      />
      <button
        onClick={handleSend}
        className='ml-2 py-2 px-4 rounded transition-all bg-blue-500 hover:bg-blue-400'
      >
        <LuSendHorizontal size={18} />
      </button>
    </div>
  );
};

export default InputField;
