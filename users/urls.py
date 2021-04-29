from django.urls import path, include
from .views import (
			createUser, 
			ProfileUpdateView, 
			changePassword, 
			userProfile, 
			userList,
			UserUpdateView,
			UserDeleteView,
	)

app_name = 'users'

urlpatterns = [
	path('create-user', createUser, name='create-user'),
	path('update-profile/<int:pk>', ProfileUpdateView.as_view(), name='update-profile'),
	path('change-password', changePassword, name='change-password'),
	path('profile', userProfile, name='profile'),
	path('user-list', userList, name='user-list'),
	path('update-user/<int:pk>', UserUpdateView.as_view(), name='update-user'),
	path('delete-user/<int:pk>', UserDeleteView.as_view(), name='delete-user'),

	path('accounts/', include('django.contrib.auth.urls')),
]
