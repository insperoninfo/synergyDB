from .models import Directory, Document, CommonDocument, DirectoryAccess
from django import forms
from django.forms import ClearableFileInput

class DirectoryCreationForm(forms.ModelForm):

    class Meta:
        model = Directory
        fields = ("name",)


class DocumentUploadForm(forms.ModelForm):
	
	class Meta:
		model = Document 
		fields = ("file",)
		widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }


class CommonDocumentUploadForm(forms.ModelForm):
	
	class Meta:
		model = CommonDocument 
		fields = ("file",)
		widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }


class DirAccessForm(forms.ModelForm):

	class Meta:
		model =DirectoryAccess
		fields = ('user',)
