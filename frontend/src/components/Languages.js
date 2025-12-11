import { useState } from 'react';
import axios from 'axios';
import { stripMarkdown } from '../utils/markdownUtils';

function Chat() {
  const [language, setLanguage] = useState('spanish');
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    const userMessage = { type: 'user', text: question };
    setMessages([...messages, userMessage]);

    try {
      const response = await axios.post('http://localhost:8001/chat', {
        question: question,
        language: language
      });

      const botMessage = {
        type: 'bot',
        text: stripMarkdown(response.data.answer),
        sources: response.data.sources
      };

      setMessages([...messages, userMessage, botMessage]);
      setQuestion('');
    } catch (error) {
      const errorMessage = {
        type: 'error',
        text: 'Error connecting to API. Make sure the backend is running on port 8001.'
      };
      setMessages([...messages, userMessage, errorMessage]);
    }

    setLoading(false);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-anote-accent mb-6">Languages</h1>

      {/* Language Selector */}
      <div className="mb-6">
        <label className="block text-anote-text-secondary mb-2">Select Language:</label>
        <div className="flex space-x-4">
          <button
            onClick={() => setLanguage('spanish')}
            className={`px-6 py-2 rounded-md font-semibold ${
              language === 'spanish'
                ? 'bg-anote-accent text-anote-primary'
                : 'bg-anote-sidebar text-anote-text-secondary hover:bg-gray-600'
            }`}
          >
            Spanish
          </button>
          <button
            onClick={() => setLanguage('hebrew')}
            className={`px-6 py-2 rounded-md font-semibold ${
              language === 'hebrew'
                ? 'bg-anote-accent text-anote-primary'
                : 'bg-anote-sidebar text-anote-text-secondary hover:bg-gray-600'
            }`}
          >
            Hebrew
          </button>
          <button
            onClick={() => setLanguage('japanese')}
            className={`px-6 py-2 rounded-md font-semibold ${
              language === 'japanese'
                ? 'bg-anote-accent text-anote-primary'
                : 'bg-anote-sidebar text-anote-text-secondary hover:bg-gray-600'
            }`}
          >
            Japanese
          </button>
          <button
            onClick={() => setLanguage('korean')}
            className={`px-6 py-2 rounded-md font-semibold ${
              language === 'korean'
                ? 'bg-anote-accent text-anote-primary'
                : 'bg-anote-sidebar text-anote-text-secondary hover:bg-gray-600'
            }`}
          >
            Korean
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="bg-anote-sidebar rounded-lg p-4 mb-6 min-h-[400px] max-h-[500px] overflow-y-auto">
        {messages.length === 0 ? (
          <p className="text-anote-text-tertiary text-center py-8">
            Ask a question to get started...
          </p>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} className="mb-4">
              {msg.type === 'user' && (
                <div className="flex justify-end">
                  <div className="bg-gray-600 text-anote-text-primary px-4 py-2 rounded-lg max-w-lg">
                    {msg.text}
                  </div>
                </div>
              )}
              {msg.type === 'bot' && (
                <div className="flex justify-start">
                  <div className="bg-anote-accent text-anote-primary px-4 py-2 rounded-lg max-w-lg">
                    <p className="mb-2">{msg.text}</p>
                    {msg.sources && msg.sources.length > 0 && (
                      <div className="text-sm mt-2 pt-2 border-t border-blue-600">
                        <p className="font-semibold">Sources:</p>
                        <ul className="list-disc list-inside">
                          {msg.sources.map((src, i) => (
                            <li key={i}>{src}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              )}
              {msg.type === 'error' && (
                <div className="flex justify-center">
                  <div className="bg-red-600 text-white px-4 py-2 rounded-lg">
                    {msg.text}
                  </div>
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="flex space-x-4">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Type your question..."
          className="flex-1 bg-anote-sidebar text-anote-text-primary px-4 py-2 rounded-md border border-gray-700 focus:outline-none focus:border-anote-accent"
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-anote-accent text-anote-primary px-8 py-2 rounded-md font-semibold hover:bg-blue-400 disabled:opacity-50"
        >
          {loading ? 'Asking...' : 'Ask'}
        </button>
      </form>
    </div>
  );
}

export default Chat;
