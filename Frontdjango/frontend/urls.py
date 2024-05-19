from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from mainapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('<str:user_type>/login', views.login_register, name='login_register'),
    path('<str:user_type>/register', views.login_register, name='register'),
    path('patient/dashboard', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/dashboard', views.doctor_dashboard, name='doctor_dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
