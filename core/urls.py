from django.urls import path
from .views import (
				index, 
				createDirectory, 
				uploadDocument, 
				directoryContent, 
				DirectoryUpdateView, 
				DirectoryDeleteView,
				DocumentDeleteView,
				uploadCommonDocuments,
				CommonDocumentDeleteView,
				commonDocumentView
			)

app_name = 'core'

urlpatterns = [
	path('', index, name='index'),
	path('create-dir/<int:pk>', createDirectory, name='create-dir'),
	path('upload-document/<int:pk>', uploadDocument, name='upload-document'),
	path('directory/<int:pk>', directoryContent, name='directory'),
	path('update-directory/<int:pk>', DirectoryUpdateView.as_view(), name='update-directory'),
	path('delete-directory/<int:pk>', DirectoryDeleteView.as_view(), name='delete-directory'),
	path('delete-document/<int:pk>', DocumentDeleteView.as_view(), name='delete-document'),
	path('upload-common-document', uploadCommonDocuments, name='upload-common-document'),
	path('delete-common-document/<int:pk>', CommonDocumentDeleteView.as_view(), name='delete-common-document'),
	path('common-documents', commonDocumentView, name='common-documents'),

]
