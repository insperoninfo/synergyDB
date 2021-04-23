from django.urls import path, include
from .views import createUser, ProfileUpdateView, changePassword, userProfile

app_name = 'users'

urlpatterns = [
	path('create-user', createUser, name='create-user'),
	path('update-profile/<int:pk>', ProfileUpdateView.as_view(), name='update-profile'),
	path('change-password', changePassword, name='change-password'),
	path('profile', userProfile, name='profile'),
	path('accounts/', include('django.contrib.auth.urls')),
]
