import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './components/Home';
import Chat from './components/Chat';
import Evaluations from './components/Evaluations';
import Companies from './components/Companies';
import './colors.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-anote-primary">
        {/* Navbar */}
        <nav className="bg-anote-sidebar border-b border-gray-700">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex items-center justify-between h-16">
              <div className="flex items-center space-x-8">
                <Link to="/" className="text-xl font-bold text-anote-accent">
                  Anote Demo
                </Link>
                <div className="flex space-x-4">
                  <Link
                    to="/"
                    className="text-anote-text-secondary hover:text-anote-hover px-3 py-2 rounded-md text-sm font-medium"
                  >
                    Home
                  </Link>
                  <Link
                    to="/chat"
                    className="text-anote-text-secondary hover:text-anote-hover px-3 py-2 rounded-md text-sm font-medium"
                  >
                    Chat
                  </Link>
                  <Link
                    to="/evaluations"
                    className="text-anote-text-secondary hover:text-anote-hover px-3 py-2 rounded-md text-sm font-medium"
                  >
                    Evaluations
                  </Link>
                  <Link
                    to="/organizations/anote"
                    className="text-anote-text-secondary hover:text-anote-hover px-3 py-2 rounded-md text-sm font-medium"
                  >
                    Companies
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </nav>

        {/* Routes */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/evaluations" element={<Evaluations />} />
          <Route path="/organizations/anote" element={<Companies />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
