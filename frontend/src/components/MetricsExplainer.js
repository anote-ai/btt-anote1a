import { useState } from 'react';

function MetricsExplainer() {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="bg-anote-sidebar rounded-lg border border-gray-700 mb-6">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-700 transition-colors"
      >
        <div className="flex items-center">
          <svg
            className="h-6 w-6 text-anote-accent mr-3"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <h3 className="text-lg font-semibold text-anote-text-primary">
            Understanding the Metrics
          </h3>
        </div>
        <svg
          className={`h-5 w-5 text-anote-text-secondary transition-transform ${
            isExpanded ? 'transform rotate-180' : ''
          }`}
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {isExpanded && (
        <div className="px-6 pb-6 pt-2 border-t border-gray-700">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* BLEU Score */}
            <div className="bg-gray-700 rounded-lg p-4">
              <div className="flex items-center mb-3">
                <div className="bg-anote-accent rounded-full p-2 mr-3">
                  <svg className="h-5 w-5 text-anote-primary" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                    <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" />
                  </svg>
                </div>
                <h4 className="text-base font-bold text-anote-accent">BLEU Score</h4>
              </div>
              <p className="text-sm text-anote-text-secondary mb-2">
                <span className="font-semibold text-anote-text-primary">Bilingual Evaluation Understudy</span>
              </p>
              <p className="text-sm text-anote-text-secondary mb-3">
                Measures word-level and phrase-level overlap between generated text and reference translations.
              </p>
              <ul className="space-y-1 text-sm text-anote-text-secondary">
                <li className="flex items-start">
                  <span className="text-anote-accent mr-2">•</span>
                  <span><strong className="text-anote-text-primary">Range:</strong> 0-100 (higher is better)</span>
                </li>
                <li className="flex items-start">
                  <span className="text-anote-accent mr-2">•</span>
                  <span><strong className="text-anote-text-primary">Focus:</strong> N-gram precision (exact word matches)</span>
                </li>
                <li className="flex items-start">
                  <span className="text-anote-accent mr-2">•</span>
                  <span><strong className="text-anote-text-primary">Best for:</strong> Translation quality, surface-level accuracy</span>
                </li>
              </ul>
            </div>

            {/* BERTScore */}
            <div className="bg-gray-700 rounded-lg p-4">
              <div className="flex items-center mb-3">
                <div className="bg-anote-accent rounded-full p-2 mr-3">
                  <svg className="h-5 w-5 text-anote-primary" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                </div>
                <h4 className="text-base font-bold text-anote-accent">BERTScore F1</h4>
              </div>
              <p className="text-sm text-anote-text-secondary mb-2">
                <span className="font-semibold text-anote-text-primary">Contextual Embedding Similarity</span>
              </p>
              <p className="text-sm text-anote-text-secondary mb-3">
                Uses BERT embeddings to measure semantic similarity, capturing meaning even when exact words differ.
              </p>
              <ul className="space-y-1 text-sm text-anote-text-secondary">
                <li className="flex items-start">
                  <span className="text-anote-accent mr-2">•</span>
                  <span><strong className="text-anote-text-primary">Range:</strong> 0-1 (higher is better)</span>
                </li>
                <li className="flex items-start">
                  <span className="text-anote-accent mr-2">•</span>
                  <span><strong className="text-anote-text-primary">Focus:</strong> Semantic meaning and context</span>
                </li>
                <li className="flex items-start">
                  <span className="text-anote-accent mr-2">•</span>
                  <span><strong className="text-anote-text-primary">Best for:</strong> Paraphrase quality, multilingual tasks</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Why Both Matter */}
          <div className="mt-4 bg-anote-primary rounded-lg p-4 border border-gray-700">
            <h5 className="text-sm font-semibold text-anote-accent mb-2">Why Both Metrics Matter</h5>
            <p className="text-sm text-anote-text-secondary">
              <strong className="text-anote-text-primary">BLEU</strong> ensures literal accuracy and word choice,
              while <strong className="text-anote-text-primary">BERTScore</strong> captures whether the meaning is preserved.
              High scores in both indicate quality translations that are both accurate and semantically correct.
              However, automated metrics have limitations and should be combined with qualitative analysis.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default MetricsExplainer;
