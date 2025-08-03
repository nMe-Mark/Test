import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';

import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <>
      <nav style={{ padding: '1rem', background: '#eee' }}>
        <Link to="/login" style={{ marginRight: '1rem' }}>Login</Link>
        <Link to="/register" style={{ marginRight: '1rem' }}>Register</Link>
        <Link to="/dashboard">Dashboard</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </>
  );
}

export default App;
