import React from 'react';
import AppointmentForm from './AppointmentForm';

const DoctorCard = ({ doctor, user }) => {
    return (
        <div className="doctor-card">
            <h3>{doctor.first_name} {doctor.last_name}</h3>
            <p>Edad: {doctor.age}</p>
            <p>Sexo: {doctor.gender}</p>
            <p>Años de experiencia: {doctor.years_of_experience}</p>
            <AppointmentForm doctorId={doctor.id} user={user} />
        </div>
    );
};

export default DoctorCard;
