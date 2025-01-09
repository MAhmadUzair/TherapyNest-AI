import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import ChatConsultation from './pages/ChatConsultation';
import VoiceConsultation from './pages/VoiceConsultation';

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-slate-50">
        <Navbar />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/chat" element={<ChatConsultation />} />
            <Route path="/voice" element={<VoiceConsultation />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;