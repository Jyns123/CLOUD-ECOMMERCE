import React, { useState } from 'react';
import { signup } from '../api';

const Signup = ({ setUser }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await signup(username, password);
            setUser({ username });
            alert('Usuario creado correctamente');
        } catch (error) {
            alert('Error al crear el usuario');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input 
                type="text" 
                placeholder="Usuario" 
                value={username} 
                onChange={(e) => setUsername(e.target.value)} 
            />
            <input 
                type="password" 
                placeholder="Contraseña" 
                value={password} 
                onChange={(e) => setPassword(e.target.value)} 
            />
            <button type="submit">Sign Up</button>
        </form>
    );
};

export default Signup;
