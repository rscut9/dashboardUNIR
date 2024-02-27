from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('ver/', views.coleccion_view, name='ver_coleccion'),
    path('mostrar/', views.mostrar_coleccion_view, name='mostrar_coleccion'),
]