from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenBlacklistView)
from app import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),

    path('users/', views.UserListView.as_view(), name='users_list'),
    path('users/<uuid:pk>/chat/',
         views.UserChatView.as_view(),
         name='user_chat'),
]
