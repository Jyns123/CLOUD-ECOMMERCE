import React, { useState } from 'react';
import { createAppointment } from '../api';

const AppointmentForm = ({ doctorId, user }) => {
    const [duration, setDuration] = useState('');

    const handleAppointment = async () => {
        if (!user) {
            alert('Por favor inicie sesión para pedir una cita');
            return;
        }
        try {
            await createAppointment(doctorId, user.username, duration);
            alert('Cita creada correctamente');
            setDuration('');
        } catch (error) {
            alert('Error al crear la cita');
        }
    };

    return (
        <div className="appointment-form">
            <input 
                type="text" 
                placeholder="Duración de la cita" 
                value={duration} 
                onChange={(e) => setDuration(e.target.value)} 
            />
            <button onClick={handleAppointment}>Pedir Cita</button>
        </div>
    );
};

export default AppointmentForm;
