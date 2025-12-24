import React, { useState } from 'react';
import api from '../api';
import { useNavigate } from 'react-router-dom';

function Register() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    role: 'personal' 
  });

  const navigate = useNavigate();
  const [error, setError] = useState('');

  const handleChange = e => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const response = await api.post('/register', formData);
      console.log('Регистрация успешна:', response.data);
      navigate('/login');
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.msg || 'Грешка при регистрация');
    }
  };

  return (
    <div>
      <h2>Register</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          placeholder="Username"
          onChange={handleChange}
          required
        /><br />
        <input
          type="email"
          name="email"
          placeholder="Email"
          onChange={handleChange}
          required
        /><br />
        <input
          type="password"
          name="password"
          placeholder="Password"
          onChange={handleChange}
          required
        /><br />

        <label>
          <input
            type="radio"
            name="role"
            value="personal"
            checked={formData.role === 'personal'}
            onChange={handleChange}
          />
          Личен акаунт
        </label>
        <label style={{ marginLeft: '1rem' }}>
          <input
            type="radio"
            name="role"
            value="team"
            checked={formData.role === 'team'}
            onChange={handleChange}
          />
          Екипен акаунт
        </label><br />

        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default Register;
