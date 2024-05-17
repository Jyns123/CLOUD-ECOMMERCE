import React, { useState, useEffect } from 'react';
import { getDoctors } from './api';
import DoctorCard from './components/DoctorCard';
import Signup from './components/Signup';
import Login from './components/Login';
import Header from './components/Header';

const App = () => {
    const [doctors, setDoctors] = useState([]);
    const [user, setUser] = useState(null);
    const [view, setView] = useState('home');

    useEffect(() => {
        const fetchDoctors = async () => {
            const response = await getDoctors();
            setDoctors(response.data);
        };
        fetchDoctors();
    }, []);

    return (
        <div className="App">
            <Header user={user} setUser={setUser} />
            {view === 'home' && (
                <div>
                    {doctors.map(doctor => (
                        <DoctorCard key={doctor.id} doctor={doctor} user={user} />
                    ))}
                </div>
            )}
            {view === 'signup' && <Signup setUser={setUser} />}
            {view === 'login' && <Login setUser={setUser} />}
        </div>
    );
};

export default App;
