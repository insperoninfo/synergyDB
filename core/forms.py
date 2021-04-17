from .models import Directory, Document, CommonDocument
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