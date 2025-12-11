import React from 'react';

function Models() {
  const models = [
    {
      name: 'Claude 3.5 Sonnet',
      provider: 'Anthropic',
      description: 'Advanced language model with superior multilingual capabilities and context understanding. Optimized for complex reasoning tasks.',
      strengths: ['Multilingual accuracy', 'Long context handling', 'Consistent quality'],
      bertScore: '0.767',
      bleu: '6.57',
      recommended: true
    },
    {
      name: 'GPT-4',
      provider: 'OpenAI',
      description: 'Powerful general-purpose language model with strong performance across diverse tasks and languages.',
      strengths: ['General versatility', 'Large knowledge base', 'API reliability'],
      bertScore: '0.765',
      bleu: '4.93',
      recommended: false
    },
    {
      name: 'Gemini Pro',
      provider: 'Google',
      description: 'Multimodal AI model with integrated search capabilities and competitive multilingual support.',
      strengths: ['Search integration', 'Multimodal input', 'Fast inference'],
      bertScore: '0.755',
      bleu: '1.55',
      recommended: false
    },
    {
      name: 'Llama 3.1',
      provider: 'Ollama (Local)',
      description: 'Open-source model suitable for local deployment. Good for privacy-sensitive applications with moderate performance.',
      strengths: ['Local deployment', 'No API costs', 'Privacy control'],
      bertScore: '0.818',
      bleu: '1.31',
      recommended: false
    }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-anote-accent mb-2">Model Comparison & Documentation</h1>
      <p className="text-anote-text-secondary mb-8">
        Comprehensive evaluation of multilingual RAG models tested in this project
      </p>

      {/* Tested Models Section */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold text-anote-text-primary mb-6">Tested Models</h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {models.map((model, idx) => (
            <div
              key={idx}
              className={`bg-anote-sidebar rounded-lg p-6 border-2 ${
                model.recommended
                  ? 'border-anote-accent'
                  : 'border-gray-700'
              }`}
            >
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h3 className="text-xl font-bold text-anote-text-primary">
                    {model.name}
                  </h3>
                  <p className="text-sm text-anote-accent">{model.provider}</p>
                </div>
                {model.recommended && (
                  <span className="bg-anote-accent text-anote-primary px-3 py-1 rounded-full text-xs font-semibold">
                    Recommended
                  </span>
                )}
              </div>
              <p className="text-anote-text-secondary mb-4 text-sm">
                {model.description}
              </p>
              <div className="mb-4">
                <p className="text-xs font-semibold text-anote-text-tertiary mb-2">
                  KEY STRENGTHS
                </p>
                <div className="flex flex-wrap gap-2">
                  {model.strengths.map((strength, i) => (
                    <span
                      key={i}
                      className="bg-gray-700 text-anote-text-secondary px-2 py-1 rounded text-xs"
                    >
                      {strength}
                    </span>
                  ))}
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-700">
                <div>
                  <p className="text-xs text-anote-text-tertiary">BERTScore F1</p>
                  <p className="text-lg font-bold text-anote-accent">{model.bertScore}</p>
                </div>
                <div>
                  <p className="text-xs text-anote-text-tertiary">BLEU</p>
                  <p className="text-lg font-bold text-anote-accent">{model.bleu}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Performance Summary Section */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold text-anote-text-primary mb-6">Performance Summary</h2>
        <div className="bg-anote-sidebar rounded-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-700">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-anote-text-primary uppercase tracking-wider">
                    Model
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-anote-text-primary uppercase tracking-wider">
                    Provider
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-semibold text-anote-text-primary uppercase tracking-wider">
                    BERTScore F1
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-semibold text-anote-text-primary uppercase tracking-wider">
                    BLEU
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-semibold text-anote-text-primary uppercase tracking-wider">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-700">
                {models.map((model, idx) => (
                  <tr key={idx} className="hover:bg-gray-700 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-anote-text-primary">
                        {model.name}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-anote-text-secondary">
                        {model.provider}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center">
                      <span className="text-sm font-semibold text-anote-accent">
                        {model.bertScore}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center">
                      <span className="text-sm font-semibold text-anote-accent">
                        {model.bleu}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center">
                      {model.recommended ? (
                        <span className="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-800 text-green-100">
                          Production
                        </span>
                      ) : (
                        <span className="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-700 text-gray-300">
                          Evaluated
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* Production Recommendation Section */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold text-anote-text-primary mb-6">Production Recommendation</h2>
        <div className="bg-anote-sidebar rounded-lg p-6 border-l-4 border-anote-accent">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <svg className="h-6 w-6 text-anote-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-semibold text-anote-text-primary mb-2">
                Claude 3.5 Sonnet - Primary Production Model
              </h3>
              <p className="text-anote-text-secondary mb-4">
                Based on comprehensive evaluation across Spanish, Hebrew, Japanese, and Korean datasets,
                Claude 3.5 Sonnet demonstrates superior performance in multilingual RAG tasks.
              </p>
              <div className="space-y-2">
                <div className="flex items-start">
                  <span className="text-anote-accent mr-2">•</span>
                  <p className="text-sm text-anote-text-secondary">
                    <strong className="text-anote-text-primary">Highest BLEU Score:</strong> Achieved best BLEU score (6.57) across all evaluated models, with strong BERTScore F1 (0.767)
                  </p>
                </div>
                <div className="flex items-start">
                  <span className="text-anote-accent mr-2">•</span>
                  <p className="text-sm text-anote-text-secondary">
                    <strong className="text-anote-text-primary">Multilingual Excellence:</strong> Consistent performance across diverse language families and writing systems
                  </p>
                </div>
                <div className="flex items-start">
                  <span className="text-anote-accent mr-2">•</span>
                  <p className="text-sm text-anote-text-secondary">
                    <strong className="text-anote-text-primary">Context Understanding:</strong> Superior handling of long-context retrieval tasks with accurate source attribution
                  </p>
                </div>
                <div className="flex items-start">
                  <span className="text-anote-accent mr-2">•</span>
                  <p className="text-sm text-anote-text-secondary">
                    <strong className="text-anote-text-primary">Production Ready:</strong> Reliable API, consistent response quality, and excellent documentation
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Documentation Links Section */}
      <section>
        <h2 className="text-2xl font-semibold text-anote-text-primary mb-6">Documentation & Resources</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <a
            href="https://github.com/ShalomDee/btt-anote1a"
            target="_blank"
            rel="noopener noreferrer"
            className="bg-anote-sidebar rounded-lg p-6 hover:bg-gray-700 transition-colors border border-gray-700 hover:border-anote-accent"
          >
            <div className="flex items-center mb-3">
              <svg className="h-8 w-8 text-anote-accent mr-3" fill="currentColor" viewBox="0 0 24 24">
                <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
              </svg>
              <div>
                <h3 className="text-lg font-semibold text-anote-text-primary">GitHub Repository</h3>
                <p className="text-sm text-anote-text-tertiary">Source code and implementation details</p>
              </div>
            </div>
            <p className="text-sm text-anote-text-secondary">
              Complete source code, setup instructions, and technical documentation for the multilingual RAG system.
            </p>
          </a>

          <div className="bg-anote-sidebar rounded-lg p-6 border border-gray-700">
            <div className="flex items-center mb-3">
              <svg className="h-8 w-8 text-anote-accent mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <div>
                <h3 className="text-lg font-semibold text-anote-text-primary">Project Writeup</h3>
                <p className="text-sm text-anote-text-tertiary">Detailed evaluation and findings</p>
              </div>
            </div>
            <p className="text-sm text-anote-text-secondary mb-3">
              Comprehensive analysis of model performance, methodology, and recommendations for multilingual RAG deployment.
            </p>
            <ul className="space-y-1 text-sm text-anote-text-secondary">
              <li className="flex items-center">
                <span className="text-anote-accent mr-2">→</span>
                Evaluation methodology
              </li>
              <li className="flex items-center">
                <span className="text-anote-accent mr-2">→</span>
                Performance metrics analysis
              </li>
              <li className="flex items-center">
                <span className="text-anote-accent mr-2">→</span>
                Architecture decisions
              </li>
            </ul>
          </div>

          <div className="bg-anote-sidebar rounded-lg p-6 border border-gray-700">
            <div className="flex items-center mb-3">
              <svg className="h-8 w-8 text-anote-accent mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              <div>
                <h3 className="text-lg font-semibold text-anote-text-primary">Evaluation Results</h3>
                <p className="text-sm text-anote-text-tertiary">Interactive performance dashboard</p>
              </div>
            </div>
            <p className="text-sm text-anote-text-secondary mb-3">
              Explore detailed evaluation metrics, language-specific performance, and comparative analysis.
            </p>
            <button className="text-sm text-anote-accent hover:text-blue-300 font-semibold">
              View Evaluations →
            </button>
          </div>

          <div className="bg-anote-sidebar rounded-lg p-6 border border-gray-700">
            <div className="flex items-center mb-3">
              <svg className="h-8 w-8 text-anote-accent mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
              <div>
                <h3 className="text-lg font-semibold text-anote-text-primary">Try the Demo</h3>
                <p className="text-sm text-anote-text-tertiary">Test multilingual capabilities live</p>
              </div>
            </div>
            <p className="text-sm text-anote-text-secondary mb-3">
              Experience the multilingual RAG system with real queries in Spanish, Hebrew, Japanese, and Korean.
            </p>
            <button className="text-sm text-anote-accent hover:text-blue-300 font-semibold">
              Go to Languages →
            </button>
          </div>
        </div>
      </section>

      {/* Metrics Legend */}
      <div className="mt-8 bg-anote-sidebar rounded-lg p-4 border border-gray-700">
        <h3 className="text-sm font-semibold text-anote-text-primary mb-3">Metrics Explained</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <p className="font-semibold text-anote-accent mb-1">BERTScore F1</p>
            <p className="text-anote-text-secondary">
              Measures semantic similarity between generated and reference answers using contextual embeddings.
              Range: 0-1, higher is better.
            </p>
          </div>
          <div>
            <p className="font-semibold text-anote-accent mb-1">BLEU Score</p>
            <p className="text-anote-text-secondary">
              Evaluates n-gram overlap between generated and reference text.
              Range: 0-1, higher is better. Commonly used for translation quality.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Models;
