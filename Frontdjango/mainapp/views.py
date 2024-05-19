from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User
import requests

BACKEND_BASE_URL = "http://18.214.194.0"

# Página principal para seleccionar el tipo de usuario
def index(request):
    return render(request, 'index.html')

# Página de inicio de sesión y registro
def login_register(request, user_type):
    error_message = None
    if request.method == 'POST':
        if 'register' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            payload = {'username': username, 'password': password}
            print(f'Register payload: {payload}')  # Depuración
            response = requests.post(f'{BACKEND_BASE_URL}:5000/register', json=payload)
            print(f'Register response: {response.status_code} - {response.text}')  # Depuración
            if response.status_code == 201:
                return redirect(f'/{user_type}/login')
            else:
                error_message = 'Error al registrar el usuario'
        elif 'login' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            payload = {'username': username, 'password': password}
            print(f'Login payload: {payload}')  # Depuración
            response = requests.post(f'{BACKEND_BASE_URL}:5000/login', json=payload)
            print(f'Login response: {response.status_code} - {response.text}')  # Depuración
            if response.status_code == 200:
                return redirect(f'/{user_type}/dashboard')
            elif response.status_code == 401:
                error_message = 'Credenciales inválidas'
            else:
                error_message = 'Error de conexión con el servidor'

    return render(request, 'login_register.html', {'user_type': user_type, 'error_message': error_message})

# Página del dashboard para pacientes
def patient_dashboard(request):
    response = requests.get(f'{BACKEND_BASE_URL}:8014/cliente')
    pacientes = response.json()
    return render(request, 'patient_dashboard.html', {'pacientes': pacientes})

# Página del dashboard para doctores
def doctor_dashboard(request):
    response = requests.get(f'{BACKEND_BASE_URL}:8016/medicamentos')
    medicamentos = response.json()
    return render(request, 'doctor_dashboard.html', {'medicamentos': medicamentos})
