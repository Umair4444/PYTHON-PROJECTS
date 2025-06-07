'use client';
import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [quote, setQuote] = useState('');

  const fetchQuote = async () => {
    const res = await axios.get('http://localhost:8000/quote');
    setQuote(res.data.quote);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-10">
      <h1 className="text-3xl font-bold mb-4">Random Quote Generator</h1>
      <button
        onClick={fetchQuote}
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        Get Quote
      </button>
      {quote && (
        <p className="mt-6 text-xl max-w-xl text-center">"{quote}"</p>
      )}
    </main>
  );
}
