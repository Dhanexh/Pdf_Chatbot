import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
// import Register from './Register';
import Register from './components/Register';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import FileUpload from './components/FileUpload';
import BotManagement from './components/BotManagement';
import ChatHistory from './components/ChatHistory';
import ChatPage from './components/ChatPage';
import LandingPage from './components/LandingPage';
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/Register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/Chat/:botName" element={<ChatPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/upload" element={<FileUpload />} />
        <Route path="/bots" element={<BotManagement />} />
        <Route path="/" element={<LandingPage />} />
        <Route path="/chat-history" element={<ChatHistory />} />
      </Routes>
    </Router>
  );
}

export default App;
