import { useState, useEffect } from 'react';
import axios from 'axios';

function Evaluations() {
  const [evaluations, setEvaluations] = useState([]);
  const [filteredEvals, setFilteredEvals] = useState([]);
  const [selectedLang, setSelectedLang] = useState('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedRow, setExpandedRow] = useState(null);
  const [summaryStats, setSummaryStats] = useState({
    gptAvgFaith: 0,
    gptAvgRel: 0,
    claudeAvgFaith: 0,
    claudeAvgRel: 0,
    gptCombined: 0,
    claudeCombined: 0,
    winner: 'N/A'
  });

  useEffect(() => {
    fetchEvaluations();
  }, []);

  useEffect(() => {
    if (selectedLang === 'all') {
      setFilteredEvals(evaluations);
    } else {
      setFilteredEvals(evaluations.filter(e => e.lang === selectedLang));
    }
  }, [selectedLang, evaluations]);

  useEffect(() => {
    if (evaluations.length > 0) {
      calculateSummaryStats();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [evaluations]);

  const fetchEvaluations = async () => {
    try {
      const response = await axios.get('http://localhost:8001/model-comparison');
      setEvaluations(response.data);
      setFilteredEvals(response.data);
      setLoading(false);
    } catch (err) {
      setError('Error loading model comparison. Make sure model_comparison.csv exists and API is running.');
      setLoading(false);
    }
  };

  const calculateSummaryStats = () => {
    const gptFaith = evaluations.map(e => parseFloat(e.gpt_faithfulness) || 0);
    const gptRel = evaluations.map(e => parseFloat(e.gpt_relevancy) || 0);
    const claudeFaith = evaluations.map(e => parseFloat(e.claude_faithfulness) || 0);
    const claudeRel = evaluations.map(e => parseFloat(e.claude_relevancy) || 0);

    const gptAvgFaith = gptFaith.reduce((a, b) => a + b, 0) / gptFaith.length;
    const gptAvgRel = gptRel.reduce((a, b) => a + b, 0) / gptRel.length;
    const claudeAvgFaith = claudeFaith.reduce((a, b) => a + b, 0) / claudeFaith.length;
    const claudeAvgRel = claudeRel.reduce((a, b) => a + b, 0) / claudeRel.length;

    const gptCombined = (gptAvgFaith + gptAvgRel) / 2;
    const claudeCombined = (claudeAvgFaith + claudeAvgRel) / 2;
    const winner = gptCombined > claudeCombined ? 'GPT-4' : 'Claude';

    setSummaryStats({
      gptAvgFaith,
      gptAvgRel,
      claudeAvgFaith,
      claudeAvgRel,
      gptCombined,
      claudeCombined,
      winner
    });
  };

  const getScoreColor = (score) => {
    const numScore = parseFloat(score) || 0;
    if (numScore >= 0.85) return 'text-green-400';
    if (numScore >= 0.70) return 'text-yellow-400';
    return 'text-red-400';
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex flex-col items-center justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-anote-accent mb-4"></div>
          <p className="text-anote-text-secondary text-center">Loading evaluations...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-red-600 text-white p-4 rounded-lg">
          {error}
        </div>
      </div>
    );
  }

  if (evaluations.length === 0) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-anote-accent mb-6">Evaluation Results</h1>
        <div className="bg-anote-sidebar rounded-lg p-8 text-center">
          <div className="text-5xl mb-4">⏳</div>
          <h2 className="text-xl font-semibold mb-2 text-anote-text-primary">Evaluation in progress...</h2>
          <p className="text-anote-text-secondary mb-6">Results will appear here once processing completes.</p>
          <button
            onClick={fetchEvaluations}
            className="bg-anote-accent text-anote-primary px-6 py-2 rounded-md font-semibold hover:bg-blue-400"
          >
            Refresh
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-anote-accent mb-6">Model Comparison: GPT-4 vs Claude</h1>

      {/* Summary Stats */}
      {evaluations.length > 0 && (
        <div className="mb-8 bg-[#374151] p-6 rounded-lg">
          <h2 className="text-2xl font-bold mb-4 text-anote-text-primary">Model Performance Summary</h2>
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-[#111827] p-4 rounded">
              <h3 className="text-lg font-semibold text-[#40C0FF] mb-2">GPT-4</h3>
              <p className="text-anote-text-secondary">Avg Faithfulness: <span className="font-semibold text-anote-text-primary">{summaryStats.gptAvgFaith.toFixed(3)}</span></p>
              <p className="text-anote-text-secondary">Avg Relevancy: <span className="font-semibold text-anote-text-primary">{summaryStats.gptAvgRel.toFixed(3)}</span></p>
              <p className="text-xl font-bold text-anote-text-primary mt-2">Combined: {summaryStats.gptCombined.toFixed(3)}</p>
            </div>
            <div className="bg-[#111827] p-4 rounded">
              <h3 className="text-lg font-semibold text-[#40C0FF] mb-2">Claude</h3>
              <p className="text-anote-text-secondary">Avg Faithfulness: <span className="font-semibold text-anote-text-primary">{summaryStats.claudeAvgFaith.toFixed(3)}</span></p>
              <p className="text-anote-text-secondary">Avg Relevancy: <span className="font-semibold text-anote-text-primary">{summaryStats.claudeAvgRel.toFixed(3)}</span></p>
              <p className="text-xl font-bold text-anote-text-primary mt-2">Combined: {summaryStats.claudeCombined.toFixed(3)}</p>
            </div>
          </div>
          <div className="mt-4 text-center">
            <p className="text-2xl text-anote-text-primary">
              Winner: <span className="text-[#40C0FF] font-bold">{summaryStats.winner}</span>
            </p>
          </div>
        </div>
      )}

      {/* Filter */}
      <div className="mb-6">
        <label className="block text-anote-text-secondary mb-2">Filter by Language:</label>
        <select
          value={selectedLang}
          onChange={(e) => setSelectedLang(e.target.value)}
          className="bg-anote-sidebar text-anote-text-primary px-4 py-2 rounded-md border border-gray-700 focus:outline-none focus:border-anote-accent"
        >
          <option value="all">All Languages</option>
          <option value="es">Spanish</option>
          <option value="he">Hebrew</option>
          <option value="ja">Japanese</option>
          <option value="ko">Korean</option>
        </select>
        <span className="ml-4 text-anote-text-tertiary">
          Showing {filteredEvals.length} of {evaluations.length} results
        </span>
      </div>

      {/* Table */}
      <div className="bg-anote-sidebar rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-700">
              <tr>
                <th className="px-4 py-3 text-left text-anote-text-primary font-semibold">Lang</th>
                <th className="px-4 py-3 text-left text-anote-text-primary font-semibold">Question</th>
                <th className="px-4 py-3 text-center text-anote-text-primary font-semibold">GPT Faith</th>
                <th className="px-4 py-3 text-center text-anote-text-primary font-semibold">GPT Rel</th>
                <th className="px-4 py-3 text-center text-anote-text-primary font-semibold">Claude Faith</th>
                <th className="px-4 py-3 text-center text-anote-text-primary font-semibold">Claude Rel</th>
                <th className="px-4 py-3 text-center text-anote-text-primary font-semibold">Difficulty</th>
                <th className="px-4 py-3 text-center text-anote-text-primary font-semibold">Details</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {filteredEvals.map((evaluation, idx) => (
                <>
                  <tr key={idx} className="hover:bg-gray-600">
                    <td className="px-4 py-3 text-anote-text-secondary">
                      <span className="inline-block bg-anote-accent text-anote-primary px-2 py-1 rounded text-xs font-semibold">
                        {evaluation.lang.toUpperCase()}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-anote-text-secondary max-w-xs truncate">
                      {evaluation.question}
                    </td>
                    <td className={`px-4 py-3 text-center font-semibold ${getScoreColor(evaluation.gpt_faithfulness)}`}>
                      {parseFloat(evaluation.gpt_faithfulness).toFixed(2)}
                    </td>
                    <td className={`px-4 py-3 text-center font-semibold ${getScoreColor(evaluation.gpt_relevancy)}`}>
                      {parseFloat(evaluation.gpt_relevancy).toFixed(2)}
                    </td>
                    <td className={`px-4 py-3 text-center font-semibold ${getScoreColor(evaluation.claude_faithfulness)}`}>
                      {parseFloat(evaluation.claude_faithfulness).toFixed(2)}
                    </td>
                    <td className={`px-4 py-3 text-center font-semibold ${getScoreColor(evaluation.claude_relevancy)}`}>
                      {parseFloat(evaluation.claude_relevancy).toFixed(2)}
                    </td>
                    <td className="px-4 py-3 text-center">
                      <span className={`inline-block px-2 py-1 rounded text-xs font-semibold ${
                        evaluation.difficulty === 'easy' ? 'bg-green-600 text-white' :
                        evaluation.difficulty === 'medium' ? 'bg-yellow-600 text-white' :
                        'bg-red-600 text-white'
                      }`}>
                        {evaluation.difficulty}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-center">
                      <button
                        onClick={() => setExpandedRow(expandedRow === idx ? null : idx)}
                        className="bg-anote-accent text-anote-primary px-3 py-1 rounded text-sm font-semibold hover:bg-blue-400"
                      >
                        {expandedRow === idx ? 'Hide' : 'Show'}
                      </button>
                    </td>
                  </tr>
                  {expandedRow === idx && (
                    <tr key={`${idx}-expanded`} className="bg-gray-700">
                      <td colSpan="8" className="px-4 py-4">
                        <div className="space-y-3">
                          <div>
                            <p className="text-anote-accent font-semibold">Full Question:</p>
                            <p className="text-anote-text-secondary">{evaluation.question}</p>
                          </div>
                          <div>
                            <p className="text-anote-accent font-semibold">Citation:</p>
                            <p className="text-anote-text-secondary">{evaluation.citation}</p>
                          </div>
                          <div className="grid grid-cols-2 gap-4">
                            <div>
                              <p className="text-anote-accent font-semibold">GPT Answer:</p>
                              <p className="text-anote-text-secondary">{evaluation.gpt_answer}</p>
                            </div>
                            <div>
                              <p className="text-anote-accent font-semibold">Claude Answer:</p>
                              <p className="text-anote-text-secondary">{evaluation.claude_answer}</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                  )}
                </>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Evaluations;
