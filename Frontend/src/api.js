import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export const signup = (username, password) => axios.post(`${API_URL}/clientes/signup`, { username, password });
export const login = (username, password) => axios.post(`${API_URL}/clientes/login`, { username, password });
export const getDoctors = () => axios.get(`${API_URL}/doctores`);
export const createAppointment = (doctor_id, user_name, duration) => axios.post(`${API_URL}/citas`, { doctor_id, user_name, duration });
