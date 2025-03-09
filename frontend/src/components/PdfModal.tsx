import { useState, useEffect } from 'react';
import axios from 'axios';
import { FiTrash, FiUploadCloud, FiRefreshCw, FiFile } from 'react-icons/fi';

interface PDFModalProps {
  setPdfModalOpen: (open: boolean) => void;
}

const PDFModal: React.FC<PDFModalProps> = ({ setPdfModalOpen }) => {
  const [pdfList, setPdfList] = useState<{ name: string; size_mb: number }[]>([]);
  const [loading, setLoading] = useState(true);
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [processing, setProcessing] = useState(false);

  useEffect(() => {
    fetchPDFs();
  }, []);

  const fetchPDFs = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/list-pdfs/');
      setPdfList(response.data.pdfs);
    } catch (error) {
      console.error('Error fetching PDFs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async () => {
    if (!file) {
      alert('Please select a file first.');
      return;
    }
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      await axios.post('http://127.0.0.1:8000/upload-pdf/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      alert('File uploaded successfully!');
      fetchPDFs();
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Failed to upload file.');
    } finally {
      setUploading(false);
    }
  };

  const handleProcessPDFs = async () => {
    setProcessing(true);
    try {
      await axios.post('http://127.0.0.1:8000/process-pdfs/');
      alert('All PDFs processed successfully!');
      fetchPDFs();
    } catch (error) {
      console.error('Error processing PDFs:', error);
      alert('Failed to process PDFs.');
    } finally {
      setProcessing(false);
    }
  };

  const deletePDF = async (fileName: string) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/delete-pdf/?file_name=${fileName}`);
      alert('File deleted successfully!');
      fetchPDFs();
    } catch (error) {
      console.error('Error deleting file:', error);
      alert('Failed to delete file.');
    }
  };

  return (
    <div className='fixed inset-0 bg-stone-900 bg-opacity-50 flex justify-center items-center'>
      <div className='bg-stone-800 p-6 rounded-lg w-96 text-white relative'>
        <h2 className='text-xl font-semibold mb-4'>PDF Files</h2>
        {loading ? (
          <p>Loading...</p>
        ) : pdfList.length === 0 ? (
          <p>No PDFs yet.</p>
        ) : (
          <ul className='space-y-2 max-h-[14.5rem] overflow-y-scroll'>
            {pdfList.map((pdf, index) => (
              <li
                key={index}
                className='flex justify-between items-center bg-stone-700 p-2 rounded'
              >
                <span className='flex items-center gap-2'>
                  <FiUploadCloud size={16} /> {pdf.name} ({pdf.size_mb} MB)
                </span>
                <button
                  onClick={() => deletePDF(pdf.name)}
                  className='bg-red-500 hover:bg-red-400 p-1 rounded'
                >
                  <FiTrash size={16} />
                </button>
              </li>
            ))}
          </ul>
        )}

        <div className='mt-4 flex gap-2'>
          <label className='w-1/2 flex items-center gap-2 px-4 py-2 bg-stone-700 text-white rounded-lg shadow-md tracking-wide border border-blue cursor-pointer hover:bg-stone-600 justify-center'>
            <FiFile size={18} />
            <span className='text-sm'>Select PDF</span>
            <input
              type='file'
              accept='.pdf'
              onChange={e => setFile(e.target.files ? e.target.files[0] : null)}
              className='hidden'
            />
          </label>
          <button
            onClick={handleFileUpload}
            className='w-1/2 bg-blue-500 hover:bg-blue-400 p-2 rounded flex items-center justify-center gap-2'
            disabled={uploading}
          >
            <FiUploadCloud size={18} />
            {uploading ? 'Uploading...' : 'Upload'}
          </button>
        </div>

        <button
          onClick={handleProcessPDFs}
          className='w-full bg-purple-600 hover:bg-purple-500 mt-2 p-2 rounded flex items-center justify-center gap-2'
          disabled={processing}
        >
          <FiRefreshCw size={18} /> {processing ? 'Synchronizing...' : 'Process PDFs'}
        </button>

        <div className='flex justify-end mt-4'>
          <button
            onClick={() => setPdfModalOpen(false)}
            className='bg-red-500 hover:bg-red-400 p-2 rounded'
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default PDFModal;
