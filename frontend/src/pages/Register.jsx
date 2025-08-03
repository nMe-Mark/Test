// src/pages/Register.jsx
// import React, { useState } from 'react';
// import api from '../api';
// import { useNavigate } from 'react-router-dom';

// function Register() {
//   const [username, setUsername] = useState('');
//   const [email, setEmail] = useState('');
//   const [password, setPassword] = useState('');
//   const [error, setError] = useState('');
//   const navigate = useNavigate();

//   const handleRegister = async (e) => {
//     e.preventDefault();
//     try {
//       await api.post('/auth/register', {
//         username,
//         email,
//         password,
//       });
//       navigate('/login');
//     } catch (err) {
//       setError('Грешка при регистрация');
//     }
//   };

//   return (
//     <div>
//       <h2>Регистрация</h2>
//       {error && <p style={{ color: 'red' }}>{error}</p>}
//       <form onSubmit={handleRegister}>
//         <div>
//           <label>Потребителско име:</label>
//           <input
//             type="text"
//             value={username}
//             onChange={(e) => setUsername(e.target.value)}
//             required
//           />
//         </div>
//         <div>
//           <label>Имейл:</label>
//           <input
//             type="email"
//             value={email}
//             onChange={(e) => setEmail(e.target.value)}
//             required
//           />
//         </div>
//         <div>
//           <label>Парола:</label>
//           <input
//             type="password"
//             value={password}
//             onChange={(e) => setPassword(e.target.value)}
//             required
//           />
//         </div>
//         <button type="submit">Регистрация</button>
//       </form>
//     </div>
//   );
// }

// export default Register;




import React, { useState } from 'react';
import api from '../api';
import { useNavigate } from 'react-router-dom';

function Register() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: ''
  });

  const navigate = useNavigate();
  const [error, setError] = useState('');

  const handleChange = e => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const response = await api.post('/auth/register', formData);
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
        <input type="text" name="username" placeholder="Username" onChange={handleChange} required /><br />
        <input type="email" name="email" placeholder="Email" onChange={handleChange} required /><br />
        <input type="password" name="password" placeholder="Password" onChange={handleChange} required /><br />
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default Register;