from django.urls import path
from .views import index, createDirectory, uploadDocument

app_name = 'core'

urlpatterns = [
	path('', index, name='index'),
	path('create-dir/<int:pk>', createDirectory, name='create-dir'),
	path('upload-document/<int:pk>', uploadDocument, name='upload-document'),

]
