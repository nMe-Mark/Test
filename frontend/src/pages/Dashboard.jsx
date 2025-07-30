// src/pages/Dashboard.jsx
import React, { useEffect, useState } from 'react';
import api from '../api';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [dueDate, setDueDate] = useState('');
  const navigate = useNavigate();

  const fetchTasks = async () => {
    try {
      const res = await api.get('/auth/tasks');
      setTasks(res.data);
    } catch (err) {
      console.error(err);
      if (err.response?.status === 401) {
        navigate('/login'); // токенът е невалиден
      }
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await api.post('/auth/tasks', {
        title,
        description,
        due_date: dueDate,
      });
      setTitle('');
      setDescription('');
      setDueDate('');
      fetchTasks(); // презареди списъка
    } catch (err) {
      console.error('Грешка при създаване на задача');
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(`/auth/tasks/${id}`);
      fetchTasks();
    } catch (err) {
      console.error('Грешка при изтриване');
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div>
      <h2>Твоите задачи</h2>
      <form onSubmit={handleCreate}>
        <input
          type="text"
          placeholder="Заглавие"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Описание"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <input
          type="datetime-local"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
          required
        />
        <button type="submit">Създай</button>
      </form>

      <ul>
        {tasks.map(task => (
          <li key={task._id}>
            <strong>{task.title}</strong> – {task.status}
            <button onClick={() => handleDelete(task._id)}>Изтрий</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;
