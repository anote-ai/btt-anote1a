function KeyFindings({ bestResult }) {
  return (
    <div className="bg-gradient-to-r from-blue-900/30 to-anote-sidebar rounded-lg border-l-4 border-anote-accent p-6 mb-6">
      <div className="flex items-start mb-4">
        <svg
          className="h-6 w-6 text-anote-accent mr-3 mt-1 flex-shrink-0"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
          />
        </svg>
        <div>
          <h3 className="text-xl font-bold text-anote-text-primary mb-2">Key Findings</h3>
          <p className="text-sm text-anote-text-secondary">
            Important context for interpreting these results
          </p>
        </div>
      </div>

      <div className="space-y-4">
        {/* Finding 1: Best Score */}
        <div className="flex items-start">
          <div className="bg-anote-accent rounded-full p-1 mr-3 mt-0.5 flex-shrink-0">
            <svg className="h-4 w-4 text-anote-primary" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clipRule="evenodd"
              />
            </svg>
          </div>
          <div>
            <p className="text-anote-text-primary">
              <strong className="text-anote-accent">{bestResult?.model || 'Ollama'}</strong> achieved the highest
              BERTScore F1 of <strong className="text-anote-accent">{bestResult?.bertscore_f1?.toFixed(3) || '0.833'}</strong> in{' '}
              <strong className="text-anote-accent">{bestResult?.language || 'Hebrew'}</strong>, demonstrating strong
              semantic similarity to reference translations.
            </p>
          </div>
        </div>

        {/* Finding 2: Production Recommendation */}
        <div className="flex items-start">
          <div className="bg-anote-accent rounded-full p-1 mr-3 mt-0.5 flex-shrink-0">
            <svg className="h-4 w-4 text-anote-primary" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                clipRule="evenodd"
              />
            </svg>
          </div>
          <div>
            <p className="text-anote-text-primary">
              However, <strong className="text-anote-accent">qualitative analysis recommends Claude 3.5 Sonnet for production</strong>.
              While Ollama scores well on automated metrics, manual review revealed issues with response quality and consistency.
            </p>
          </div>
        </div>

        {/* Finding 3: Metrics Limitations */}
        <div className="flex items-start">
          <div className="bg-yellow-500 rounded-full p-1 mr-3 mt-0.5 flex-shrink-0">
            <svg className="h-4 w-4 text-anote-primary" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                clipRule="evenodd"
              />
            </svg>
          </div>
          <div>
            <p className="text-anote-text-primary">
              <strong className="text-yellow-400">Automated metrics don't capture everything.</strong> They cannot
              measure hallucination rates, factual accuracy, or response coherence. Human evaluation remains essential
              for production model selection.
            </p>
          </div>
        </div>

        {/* Finding 4: Full Analysis Link */}
        <div className="flex items-start bg-anote-primary rounded-lg p-4 border border-gray-700">
          <div className="bg-anote-accent rounded-full p-1 mr-3 mt-0.5 flex-shrink-0">
            <svg className="h-4 w-4 text-anote-primary" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z"
                clipRule="evenodd"
              />
            </svg>
          </div>
          <div>
            <p className="text-anote-text-secondary mb-2">
              For a comprehensive analysis including qualitative evaluation, methodology details, and production recommendations:
            </p>
            <a
              href="https://github.com/ShalomDee/btt-anote1a/blob/main/FINAL_WRITEUP.md"
              className="text-anote-accent hover:text-blue-300 font-semibold inline-flex items-center"
              target="_blank"
              rel="noopener noreferrer"
            >
              Read Full Project Writeup
              <svg className="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default KeyFindings;
