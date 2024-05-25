from django.urls import path
from app import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
]
