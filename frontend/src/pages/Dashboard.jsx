import React, { useEffect, useState } from 'react';
import api, { createTeam, getAllTeams, requestJoinTeam } from '../api';
import { useNavigate } from 'react-router-dom';

/* ================= NAVBAR ================= */

function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    navigate('/login');
  };

  return (
    <nav style={{ marginBottom: '1rem' }}>
      <button onClick={handleLogout}>Logout</button>
    </nav>
  );
}

/* ================= STYLES ================= */

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

/* ================= DASHBOARD ================= */

function Dashboard() {
  const navigate = useNavigate();

  /* -------- TASKS -------- */
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [dueDate, setDueDate] = useState('');

  /* -------- TEAMS -------- */
  const [teamName, setTeamName] = useState('');
  const [allTeams, setAllTeams] = useState([]);
  const [joinTeamId, setJoinTeamId] = useState('');

  /* ================= API CALLS ================= */

  const fetchTasks = async () => {
    try {
      const res = await api.get('/tasks');
      setTasks(res.data);
    } catch (err) {
      if (err.response?.status === 401) {
        navigate('/login'); // токенът е невалиден
      }
    }
  };

  const fetchTeams = async () => {
    try {
      const res = await getAllTeams();
      setAllTeams(res.data);
    } catch (err) {
      console.error('Error fetching teams', err);
    }
  };

  useEffect(() => {
    fetchTasks();
    fetchTeams();
  }, []);

  /* ================= TASK ACTIONS ================= */

  const handleCreateTask = async (e) => {
    e.preventDefault();
    try {
      await api.post('/tasks', {
        title,
        description,
        due_date: dueDate,
        completed: null
      });

      setTitle('');
      setDescription('');
      setDueDate('');
      fetchTasks();
    } catch (err) {
      alert('Грешка при създаване на задача');
    }
  };

    const handleDelete = async (id) => {
    try {
      await api.delete(`/tasks/${id}`);
      fetchTasks();
    } catch (err) {
      console.error('Грешка при изтриване');
    }
  };

  const updateTaskStatus = async (taskId, completed) => {
    await api.put(`/tasks/${taskId}`, { completed });
    fetchTasks();
  };

  /* ================= TEAM ACTIONS ================= */

  const handleCreateTeam = async (e) => {
    e.preventDefault();
    try {
      await createTeam(teamName);
      alert('Екипът е създаден успешно');
      setTeamName('');
      fetchTeams();
    } catch (err) {
      console.error(err);
      alert('Грешка при създаване на екипа');
    }
  };

  const handleJoinTeam = async () => {
    try {
      await requestJoinTeam(joinTeamId);
      alert('Заявката за присъединяване е изпратена');
      setJoinTeamId('');
    } catch (err) {
      alert(err.response?.data?.msg || 'Грешка при join');
    }
  };

  /* ================= RENDER ================= */

  return (
    <div>
      <Navbar />

      {/* ---------- TASKS ---------- */}
      <h2>Твоите задачи</h2>

      <form onSubmit={handleCreateTask}>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Заглавие"
          required
        />
        <input
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Описание"
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
        {tasks.map(task => (
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
              onClick={() => updateTaskStatus(task._id, true)}
            >
              ✅ Завършено
            </button>

            <button
              style={buttonStyle}
              onClick={() => updateTaskStatus(task._id, false)}
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

      <hr />

      {/* ---------- TEAMS ---------- */}
      <h3>Всички екипи</h3>
      {allTeams.map(t => (
        <p key={t._id}>
          {t.name} – <small>{t._id}</small>
        </p>
      ))}

      <h3>Създай екип</h3>
      <form onSubmit={handleCreateTeam}>
        <input
          value={teamName}
          onChange={(e) => setTeamName(e.target.value)}
          placeholder="Име на екипа"
          required
        />
        <button type="submit">Създай</button>
      </form>

      <h3>Присъедини се към екип</h3>
      <input
        value={joinTeamId}
        onChange={(e) => setJoinTeamId(e.target.value)}
        placeholder="Team ID"
      />
      <button onClick={handleJoinTeam}>
        Join
      </button>
    </div>
  );
}

export default Dashboard;


// import React, { useEffect, useState } from 'react';
// import api, { createTeam, getAllTeams, requestJoinTeam } from '../api';
// import { useNavigate } from 'react-router-dom';

// function Navbar() {
//   const navigate = useNavigate();
//   const handleLogout = () => {
//     localStorage.removeItem('token');
//     localStorage.removeItem('role');
//     navigate('/login');
//   };
//   return (
//     <nav style={{ marginBottom: '1rem' }}>
//       <button onClick={handleLogout}>Logout</button>
//     </nav>
//   );
// }

// const buttonStyle = {
//   marginRight: '8px',
//   marginTop: '8px',
//   padding: '6px 10px',
//   backgroundColor: 'white',
//   color: 'black',
//   border: '1px solid black',
//   borderRadius: '4px',
//   cursor: 'pointer'
// };

// function Dashboard() {
//   const navigate = useNavigate();
//   const [tasks, setTasks] = useState([]);
//   const [title, setTitle] = useState('');
//   const [description, setDescription] = useState('');
//   const [dueDate, setDueDate] = useState('');
//   const [teamName, setTeamName] = useState('');
//   const [allTeams, setAllTeams] = useState([]);
//   const [joinTeamId, setJoinTeamId] = useState('');

//   const fetchTasks = async () => {
//     try {
//       const res = await api.get('/tasks');
//       setTasks(res.data);
//     } catch (err) {
//       if (err.response?.status === 401) navigate('/login');
//     }
//   };

//   const fetchTeams = async () => {
//     try {
//       const res = await getAllTeams();
//       setAllTeams(res.data);
//     } catch (err) {
//       console.error('Error fetching teams', err);
//     }
//   };

//   useEffect(() => { fetchTasks(); fetchTeams(); }, []);

//   const handleCreateTask = async (e) => {
//     e.preventDefault();
//     try {
//       await api.post('/tasks', { title, description, due_date: dueDate });
//       setTitle(''); setDescription(''); setDueDate('');
//       fetchTasks();
//     } catch { alert('Грешка при създаване на задача'); }
//   };

//   const updateTaskStatus = async (taskId, completed) => {
//     try { await api.put(`/tasks/${taskId}`, { completed }); fetchTasks(); }
//     catch { alert('Грешка при актуализация на задачата'); }
//   };

//   const handleCreateTeam = async (e) => {
//     e.preventDefault();
//     try { await createTeam(teamName); alert('Екипът е създаден успешно'); setTeamName(''); fetchTeams(); }
//     catch (err) { console.error(err); alert('Грешка при създаване на екипа'); }
//   };

//   const handleJoinTeam = async () => {
//     try { await requestJoinTeam(joinTeamId); alert('Заявката за присъединяване е изпратена'); setJoinTeamId(''); }
//     catch (err) { alert(err.response?.data?.msg || 'Грешка при join'); }
//   };

//   return (
//     <div>
//       <Navbar />
//       <h2>Твоите задачи</h2>
//       <form onSubmit={handleCreateTask}>
//         <input value={title} onChange={e=>setTitle(e.target.value)} placeholder="Заглавие" required />
//         <input value={description} onChange={e=>setDescription(e.target.value)} placeholder="Описание" />
//         <input type="datetime-local" value={dueDate} onChange={e=>setDueDate(e.target.value)} required />
//         <button type="submit">Създай</button>
//       </form>
//       {tasks.map(task => (
//         <div key={task._id} style={{border:'1px solid gray',padding:'10px',marginBottom:'10px'}}>
//           <h3>{task.title}</h3>
//           <p>{task.description}</p>
//           <p>{task.due_date ? new Date(task.due_date).toLocaleString() : '-'}</p>
//           <button style={buttonStyle} onClick={()=>updateTaskStatus(task._id,true)}>✅</button>
//           <button style={buttonStyle} onClick={()=>updateTaskStatus(task._id,false)}>❌</button>
//         </div>
//       ))}

//       <hr />
//       <h3>Всички екипи</h3>
//       {allTeams.map(t => <p key={t._id}>{t.name} – <small>{t._id}</small></p>)}

//       <h3>Създай екип</h3>
//       <form onSubmit={handleCreateTeam}>
//         <input value={teamName} onChange={e=>setTeamName(e.target.value)} placeholder="Име на екипа" required />
//         <button type="submit">Създай</button>
//       </form>

//       <h3>Присъедини се към екип</h3>
//       <input value={joinTeamId} onChange={e=>setJoinTeamId(e.target.value)} placeholder="Team ID" />
//       <button onClick={handleJoinTeam}>Join</button>
//     </div>
//   );
// }

// export default Dashboard;
