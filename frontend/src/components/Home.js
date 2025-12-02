import { Languages, Library, BotMessageSquare } from 'lucide-react';

function Home() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="text-center">
        <h1 className="text-5xl font-bold text-anote-accent mb-4">
          Anote RAG Demo
        </h1>
        <p className="text-xl text-anote-text-secondary mb-8">
          Multilingual AI Chatbot with RAG Evaluation
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-12">
          <div className="bg-anote-sidebar p-6 rounded-lg border border-gray-700">
            <h2 className="text-2xl font-bold text-anote-accent mb-3">Chat</h2>
            <p className="text-anote-text-secondary mb-4">
              Ask questions in Spanish, Hebrew, Japanese, or Korean. Our RAG system retrieves relevant context and provides accurate answers.
            </p>
            <a href="/chat" className="inline-block bg-anote-accent text-anote-primary px-6 py-2 rounded-md font-semibold hover:bg-blue-400">
              Try Chat
            </a>
          </div>

          <div className="bg-anote-sidebar p-6 rounded-lg border border-gray-700">
            <h2 className="text-2xl font-bold text-anote-accent mb-3">Evaluations</h2>
            <p className="text-anote-text-secondary mb-4">
              View evaluation results from 400 multilingual test cases across different models and difficulty levels.
            </p>
            <a href="/evaluations" className="inline-block bg-anote-accent text-anote-primary px-6 py-2 rounded-md font-semibold hover:bg-blue-400">
              View Results
            </a>
          </div>
        </div>

        <div className="mt-16">
          <h2 className="text-3xl font-bold text-center mb-8">Our Datasets</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Card 1: Translation Dataset */}
            <div className="bg-[#374151] border border-gray-600 rounded-lg p-6 text-center">
              <Languages className="w-12 h-12 mx-auto mb-4 text-[#40C6FF]" />
              <h3 className="text-xl font-semibold mb-2">Translation Testing</h3>
              <div className="text-4xl font-bold text-[#DEFE47] mb-2">400</div>
              <p className="text-gray-300 text-sm">QA pairs across 4 languages</p>
              <p className="text-gray-400 text-xs mt-2">Balanced difficulty & register</p>
            </div>

            {/* Card 2: Benchmark Chunks */}
            <div className="bg-[#374151] border border-gray-600 rounded-lg p-6 text-center">
              <Library className="w-12 h-12 mx-auto mb-4 text-[#40C6FF]" />
              <h3 className="text-xl font-semibold mb-2">Benchmark Corpus</h3>
              <div className="text-4xl font-bold text-[#DEFE47] mb-2">9,322</div>
              <p className="text-gray-300 text-sm">Multilingual Wikipedia chunks</p>
              <p className="text-gray-400 text-xs mt-2">Spanish • Hebrew • Korean • Japanese</p>
            </div>

            {/* Card 3: RAG System */}
            <div className="bg-[#374151] border border-gray-600 rounded-lg p-6 text-center">
              <BotMessageSquare className="w-12 h-12 mx-auto mb-4 text-[#40C6FF]" />
              <h3 className="text-xl font-semibold mb-2">RAG System</h3>
              <div className="text-4xl font-bold text-[#DEFE47] mb-2">135</div>
              <p className="text-gray-300 text-sm">Anote documentation chunks</p>
              <p className="text-gray-400 text-xs mt-2">Claude • OpenAI • Ollama support</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;
