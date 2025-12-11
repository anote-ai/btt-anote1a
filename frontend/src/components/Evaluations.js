import { useState, useEffect } from 'react';
import MetricsExplainer from './MetricsExplainer';
import KeyFindings from './KeyFindings';

function Evaluations() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8001/evaluations')
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        return res.json();
      })
      .then(data => {
        console.log('Loaded evaluation data:', data);
        setResults(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error loading evaluations:', err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="bg-gray-800 rounded-lg p-8 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#40C0FF] mx-auto mb-4"></div>
          <p className="text-gray-400">Loading evaluation results...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="bg-red-900/20 border-2 border-red-500 rounded-lg p-8">
          <h2 className="text-xl font-bold text-red-400 mb-2">Error Loading Data</h2>
          <p className="text-gray-300 mb-4">{error}</p>
          <p className="text-gray-400 text-sm">
            Make sure the backend is running and leaderboard_by_language.csv exists in data/processed/
          </p>
        </div>
      </div>
    );
  }

  // Calculate summary stats from real data
  const totalQuestions = results.reduce((sum, r) => sum + r.count, 0);
  const uniqueLanguages = [...new Set(results.map(r => r.language))].length;
  const uniqueModels = [...new Set(results.map(r => r.model))].length;

  // Find best model (highest BERTScore F1)
  const bestResult = results.reduce((best, current) =>
    current.bertscore_f1 > best.bertscore_f1 ? current : best
  , results[0] || {});

  return (
    <div className="max-w-6xl mx-auto">
      <div className="bg-gray-800 rounded-lg p-8 mb-6">
        <h2 className="text-3xl font-bold text-white mb-2">Model Evaluation Results</h2>
        <p className="text-gray-400">
          Translation Quality Assessment across {uniqueModels} AI models and {uniqueLanguages} languages ({Math.floor(totalQuestions / uniqueModels)} translation pairs)
        </p>
      </div>

      {/* Summary Stats - Calculated from REAL data */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-gray-800 rounded-lg p-6">
          <h3 className="text-gray-400 text-sm mb-2">Highest BERTScore</h3>
          <p className="text-2xl font-bold text-[#40C0FF]">{bestResult.model}</p>
          <p className="text-gray-500 text-sm">{bestResult.bertscore_f1?.toFixed(3)} F1 ({bestResult.language})</p>
        </div>
        <div className="bg-gray-800 rounded-lg p-6">
          <h3 className="text-gray-400 text-sm mb-2">Total Questions</h3>
          <p className="text-2xl font-bold text-white">{totalQuestions}</p>
          <p className="text-gray-500 text-sm">{totalQuestions / uniqueLanguages} per language</p>
        </div>
        <div className="bg-gray-800 rounded-lg p-6">
          <h3 className="text-gray-400 text-sm mb-2">Languages</h3>
          <p className="text-2xl font-bold text-white">{uniqueLanguages}</p>
          <p className="text-gray-500 text-sm">{[...new Set(results.map(r => r.language))].join(', ')}</p>
        </div>
        <div className="bg-gray-800 rounded-lg p-6">
          <h3 className="text-gray-400 text-sm mb-2">Models Tested</h3>
          <p className="text-2xl font-bold text-white">{uniqueModels}</p>
          <p className="text-gray-500 text-sm">{[...new Set(results.map(r => r.model))].slice(0, 2).join(', ')}...</p>
        </div>
      </div>

      {/* Metrics Explainer */}
      <MetricsExplainer />

      {/* Key Findings */}
      <KeyFindings bestResult={bestResult} />

      {/* Results Table - All REAL data */}
      <div className="bg-gray-800 rounded-lg overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-900">
            <tr>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">Model</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">Language</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">BLEU</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">BERTScore F1</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-400">Questions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-700">
            {results.map((result, idx) => (
              <tr key={idx} className="hover:bg-gray-700 transition">
                <td className="px-6 py-4 text-white font-medium">{result.model}</td>
                <td className="px-6 py-4 text-gray-400">{result.language}</td>
                <td className="px-6 py-4 text-gray-400">{result.bleu.toFixed(2)}</td>
                <td className="px-6 py-4">
                  <span className={`font-semibold ${
                    result.bertscore_f1 >= 0.8 ? 'text-green-400' :
                    result.bertscore_f1 >= 0.7 ? 'text-[#40C0FF]' :
                    'text-yellow-400'
                  }`}>
                    {result.bertscore_f1.toFixed(3)}
                  </span>
                </td>
                <td className="px-6 py-4 text-gray-400">{result.count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Footer Note */}
      <div className="mt-6 bg-gray-800 rounded-lg p-6 border border-gray-700">
        <div className="flex items-start">
          <svg className="h-5 w-5 text-[#40C0FF] mr-3 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div>
            <p className="text-gray-300 text-sm mb-2">
              <strong className="text-white">About This Evaluation:</strong> This evaluation uses our translation testing dataset
              ({Math.floor(totalQuestions / uniqueModels)} translation pairs per language). The results measure how well each model translates
              text across {uniqueLanguages} languages using automated metrics.
            </p>
            <p className="text-gray-400 text-sm">
              <strong className="text-gray-300">Future Work:</strong> Multilingual QA evaluation using 9,322 Wikipedia chunks
              is available for comprehensive RAG system testing. See our documentation for methodology details.
            </p>
            <p className="text-gray-500 text-xs mt-3">
              Data source: <code className="text-[#40C0FF] bg-gray-900 px-2 py-0.5 rounded">data/processed/leaderboard_by_language.csv</code>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Evaluations;
