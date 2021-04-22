from django.shortcuts import render, redirect, HttpResponse, reverse
from .decorators import allowed_users
import os
from django.contrib.auth.decorators import login_required
from .models import Directory, Document, CommonDocument
from .forms import DirectoryCreationForm, DocumentUploadForm, CommonDocumentUploadForm
from django.contrib import messages
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from users.views import AdminRequiredMixin
from .check_file import check_if_file_exists


@login_required
def index(request):
	try:
		current_user = request.user
		current_user_branch = current_user.profile.branch

		common_documnts = CommonDocument.objects.filter()

		root_dir = Directory.objects.filter(name='root').filter(branch = current_user_branch)

		context = {
			'current_user' : current_user,
			'current_user_branch' : current_user_branch,
			'root_dir' : root_dir[0],
			'common_documnts' : common_documnts,

		}

	except (IndexError) as e:
            return HttpResponse('/404')


	return render(request, 'core/index.html', context)


@login_required
def createDirectory(request,pk):
	form = DirectoryCreationForm()
	if request.method == 'POST':
		created_by = request.user
		parent_directory = Directory.objects.get(pk = pk)
		branch = parent_directory.branch

		if created_by.profile.branch != branch or created_by.is_superuser == False:
			return HttpResponseForbidden('<h1>403 Forbidden</h1>') 

		else:
			try:	
			
				form = DirectoryCreationForm(request.POST or None)
				if form.is_valid():
					
					form.instance.parent_directory = parent_directory
					form.instance.branch = branch
					
					form.save()
					return redirect('core:directory', pk=pk)
			except:
				return HttpResponse('Some error occured!!')

	# For development process only. Change to error msg on production.
	return render(request, 'core/create_dir_form.html', {'create_dir_form': form, "parent_dir_pk":pk})


@login_required
def uploadDocument(request, pk):
	form = DocumentUploadForm()

	if request.method == 'POST':
		created_by = request.user
		parent_directory = Directory.objects.get(pk = pk)
		branch = parent_directory.branch

		if created_by.profile.branch != branch:
			messages.warning(request, 'You are not authorized to perform the action.')
			return redirect('core:index')

		else:
			try:
				form = DocumentUploadForm(request.POST, request.FILES)
				if form.is_valid():
					filelist = request.FILES.getlist('file')
					for file in filelist:
						# check if file already exists
						if (check_if_file_exists(parent_directory, file)) == True:
							file_path = os.path.join(parent_directory.upload_path(), file.name)


							doc = Document.objects.get(directory=parent_directory, file = file_path)
							doc.file = file
							doc.updated_by = created_by
							doc.save()
						else:
							document_instance = Document(directory=parent_directory, file = file, updated_by=created_by)
					
							document_instance.save()

					return redirect('core:directory', pk=pk)

			except:
				return HttpResponse('Some error occured!!')


	# For development process only. Change to error msg on production.
	context = {
		'document_upload_form' :form,
		'parent_dir_pk' : pk,

	}

	return render(request, 'core/document_upload_form.html', context)

	
@login_required
def directoryContent(request, pk):
	current_directory = Directory.objects.get(pk=pk)
	current_user = request.user

	print(current_user.get_full_name())

	if current_directory.branch != current_user.profile.branch:
		return HttpResponseForbidden('<h1>403 Forbidden</h1>')

	else:
		child_directories = Directory.objects.filter(parent_directory=current_directory)
		documents = Document.objects.filter(directory = current_directory)

		current_path = current_directory.str_()


		create_dir_form = DirectoryCreationForm()
		document_upload_form = DocumentUploadForm()

		context = {
			'current_directory' : current_directory,
			'child_directories' : child_directories,
			'documents' : documents,
			'parent_dir_pk' : current_directory.pk,
			'create_dir_form' : create_dir_form,
			'document_upload_form' : document_upload_form,
			'current_path' : current_path,
			'dir_update_form' : DirectoryCreationForm,
		}	

		return render(request, 'core/directory.html', context)	


class DirectoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Directory
	form_class = DirectoryCreationForm
	template_name = 'core/update_dir_form.html'
	success_message = "Updated successfully"

	def test_func(self):
		usr = self.request.user
		if usr.is_authenticated and usr.is_superuser:
			directory = Directory.objects.get(pk = self.kwargs['pk'])
			print(directory)
			if usr.profile.branch == directory.branch and directory.name != 'root':
				return True
		else:
			return False

	def get_success_url(self):
		return reverse('core:directory', kwargs = {'pk' : self.kwargs['pk']})


class DirectoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Directory
	template_name = 'core/dir_delete_confirmation.html'
	success_url = '/'

	def test_func(self):
		usr = self.request.user
		if usr.is_authenticated and usr.is_superuser:
			directory = Directory.objects.get(pk = self.kwargs['pk'])
			
			if usr.profile.branch == directory.branch and directory.name != 'root':
				return True
		else:
			return False

	def get_success_url(self):
		current_directory = Directory.objects.get(pk = self.kwargs['pk'])
		parent_dir_pk = current_directory.parent_directory.pk
		return reverse('core:directory', kwargs = {'pk' : parent_dir_pk})


class DocumentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Document
	template_name = 'core/document_delete_confirmation.html'
	success_url = '/'

	def test_func(self):
		usr = self.request.user
		if usr.is_authenticated:
			document = Document.objects.get(pk = self.kwargs['pk'])
			
			if usr.profile.branch == document.directory.branch:
				return True
		else:
			return False

	def get_success_url(self):
		document = Document.objects.get(pk = self.kwargs['pk'])
		parent_dir_pk = document.directory.pk
		return reverse('core:directory', kwargs = {'pk' : parent_dir_pk})



@allowed_users(allowed_roles=['admin'])
def uploadCommonDocuments(request):
	form = CommonDocumentUploadForm()

	if request.method == 'POST':
		created_by = request.user

		try:
			form = CommonDocumentUploadForm(request.POST, request.FILES)
			if form.is_valid():
				filelist = request.FILES.getlist('file')
				for file in filelist:
					document_instance = CommonDocument(file = file, updated_by=created_by)
				
					document_instance.save()

				return redirect('core:index')

		except:
			return HttpResponse('Some error occured!!')

	# For development process only. Change to error msg on production.
	context = {
		'document_upload_form' :form,

	}

	return render(request, 'core/common_document_upload_form.html', context)



class CommonDocumentDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
	model = CommonDocument
	template_name = 'core/document_delete_confirmation.html'
	success_url = '/'