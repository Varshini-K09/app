from django.urls import path

from api.views import (
    UserProfile,
    ProfileView,
    LoginView
)

urlpatterns = [

    path(
        'register/',
        UserProfile.as_view(),
        name='register-user'
    ),

    path(
        'login/',
        LoginView.as_view(),
        name='user-login'
    ),

    path(
        'profile/',
        ProfileView.as_view(),
        name='user-profile'
    ),
]