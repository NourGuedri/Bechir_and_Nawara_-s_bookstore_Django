from django.urls import path 
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('password_change_step1/', views.password_change_step1, name='password_change_step1'),
    path('password_change_step2/', views.password_change_step2, name='password_change_step2'),
    path('password_change_step3/', views.password_change_step3, name='password_change_step3'),
    
]