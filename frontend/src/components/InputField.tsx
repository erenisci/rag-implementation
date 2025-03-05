import { useState } from 'react';
import { LuSendHorizontal } from 'react-icons/lu';

const InputField: React.FC = () => {
  const [input, setInput] = useState('');

  const sendMessage = () => {
    if (!input.trim()) return;
    console.log('Message sent:', input);
    setInput('');
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
      />
      <button
        onClick={sendMessage}
        className='ml-2 py-2 px-4 bg-blue-500 rounded hover:bg-blue-400 transition-all'
      >
        <LuSendHorizontal size={20} />
      </button>
    </div>
  );
};

export default InputField;
