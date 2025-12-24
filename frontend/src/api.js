// src/api.js
import axios from 'axios';

/*
  VITE_API_URL трябва да е:
  http://localhost:5000/api/auth
*/
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/* ===== Request interceptor (JWT) ===== */
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

/* ===== Response interceptor (401) ===== */
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('role');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

/* ================= TASKS API ================= */

export const getTasks = () => {
  return api.get('/tasks');
};

export const createTask = (data) => {
  return api.post('/tasks', data);
};

export const updateTask = (taskId, data) => {
  return api.put(`/tasks/${taskId}`, data);
};

export const deleteTask = (taskId) => {
  return api.delete(`/tasks/${taskId}`);
};

/* ================= TEAM API ================= */

export const createTeam = (name) => {
  return api.post('/team/create', { name });
};

export const getAllTeams = () => {
  return api.get('/team/all');
};

export const requestJoinTeam = (team_id) => {
  return api.post('/team/request_join', { team_id });
};

/* ================= AUTH API ================= */

export const login = (data) => {
  return api.post('/login', data);
};

export const register = (data) => {
  return api.post('/register', data);
};

export default api;