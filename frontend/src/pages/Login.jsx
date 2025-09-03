
import React, { useState } from 'react';
import api from '../api.js'; // Това е правилно, ако 'api.js' е в 'src/'
import { useNavigate } from 'react-router-dom';


function Login() {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = e => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

const handleSubmit = async e => {
  e.preventDefault();
  console.log(formData);  // добави това за дебъг
  try {
    const response = await api.post('/auth/login', formData);
    localStorage.setItem('token', response.data.token);
    navigate('/dashboard');
  } catch (err) {
    console.error(err);
    setError(err.response?.data?.msg || 'Грешка при вход');
  }
};


  return (
    <div>
      <h2>Login</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <input type="email" name="email" placeholder="Email" onChange={handleChange} required /><br />
        <input type="password" name="password" placeholder="Password" onChange={handleChange} required /><br />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;
