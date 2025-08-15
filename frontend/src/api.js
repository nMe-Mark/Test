


// src/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});


api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Засича 401 Unauthorized и пренасочва към login
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login'; // Автоматично пренасочване
    }
    return Promise.reject(error);
  }
);

export default api;



// frontend/src/api.js

// const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

// export async function login(username, password) {
//   const res = await fetch(`${API_URL}/login`, {
//     method: 'POST',
//     headers: {'Content-Type': 'application/json'},
//     body: JSON.stringify({ username, password }),
//   });
//   if (!res.ok) throw new Error('Login failed');
//   return res.json();
// }