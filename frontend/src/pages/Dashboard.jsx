// src/pages/Dashboard.jsx
import React, { useEffect, useState } from 'react';
import api from '../api';
import { useNavigate } from 'react-router-dom';

function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <nav>
      <button onClick={handleLogout}>Logout</button>
    </nav>
  );
}

const buttonStyle = {
  marginRight: '8px',
  marginTop: '8px',
  padding: '6px 10px',
  backgroundColor: 'white',
  color: 'black',
  border: '1px solid black',
  borderRadius: '4px',
  cursor: 'pointer'
};

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
        completed: null
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

  const handleUpdateStatus = async (taskId, status) => {
    try {
      await api.put(`/auth/tasks/${taskId}`, { completed: status });
      fetchTasks();
    } catch (err) {
      console.error('Грешка при обновяване на задачата:', err);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div>
      <Navbar />
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

      <div>
        {tasks.map((task) => (
          <div
            key={task._id}
            style={{
              border: '1px solid gray',
              padding: '10px',
              marginBottom: '10px',
              backgroundColor:
                task.completed === true
                  ? '#2e7d32'
                  : task.completed === false
                  ? '#c62828'
                  : '#b0bec5',
              color: 'white',
              borderRadius: '6px'
            }}
          >
            <h3>{task.title}</h3>
            <p>{task.description}</p>
            <p>До: {new Date(task.due_date).toLocaleString()}</p>
            <p>
              Статус:{' '}
              {task.completed === true
                ? 'Завършена'
                : task.completed === false
                ? 'Незавършена'
                : 'Няма статус'}
            </p>
            <button
              style={buttonStyle}
              onClick={() => handleUpdateStatus(task._id, true)}
            >
              ✅ Завършено
            </button>
            <button
              style={buttonStyle}
              onClick={() => handleUpdateStatus(task._id, false)}
            >
              ❌ Незавършено
            </button>
            <button
              style={buttonStyle}
              onClick={() => handleDelete(task._id)}
            >
              🗑️ Изтрий
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Dashboard;
