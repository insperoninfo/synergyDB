from django.shortcuts import render, redirect, HttpResponse, reverse
from .decorators import allowed_users
import os
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Directory, Document, CommonDocument, DirectoryAccess
from .forms import DirectoryCreationForm, DocumentUploadForm, CommonDocumentUploadForm, DirAccessForm
from django.contrib import messages
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from users.views import AdminRequiredMixin
from .check_file import check_if_file_exists
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator


@login_required
def index(request):
	try:
		current_user = request.user
		current_user_branch = current_user.profile.branch


		common_documnts = CommonDocument.objects.filter()

		root_dirs = Directory.objects.filter(name='root').filter(parent_directory=None)

		context = {
			'current_user' : current_user,
			'current_user_branch' : current_user_branch,
			'root_dirs' : root_dirs,
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

		if created_by.groups.filter(name='admin').exists() != True:
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
		dirAccess = DirectoryAccess.objects.filter(directory=parent_directory).filter(user=created_by).exists()

		if (parent_directory.name == 'root' and parent_directory.parent_directory == None):
			return HttpResponseForbidden('<h1>403 Forbidden</h1>')

		elif dirAccess == True or created_by.groups.filter(name='admin').exists() == True:
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

		else:
			return HttpResponseForbidden('<h1>403 Forbidden</h1>')


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
	dirAccess = DirectoryAccess.objects.filter(directory=current_directory).filter(user=current_user).exists()


	if (current_user.groups.filter(name='admin').exists() == True) or current_user.is_superuser:
		child_directories = Directory.objects.filter(parent_directory=current_directory)
		documents = Document.objects.filter(directory = current_directory)

		current_path = current_directory.str_()


		create_dir_form = DirectoryCreationForm()
		document_upload_form = DocumentUploadForm()
		dir_access_form = DirAccessForm()

		context = {
			'current_directory' : current_directory,
			'child_directories' : child_directories,
			'documents' : documents,
			'parent_dir_pk' : current_directory.pk,
			'create_dir_form' : create_dir_form,
			'document_upload_form' : document_upload_form,
			'current_path' : current_path,
			'dir_update_form' : DirectoryCreationForm,
			'dir_access_form' : dir_access_form,
		}	

		return render(request, 'core/directory.html', context)


	

	elif (dirAccess == True or (current_directory.name == 'root' and current_directory.parent_directory == None)):
		child_directories = Directory.objects.filter(parent_directory=current_directory).filter(directoryaccess__user=current_user)
		documents = Document.objects.filter(directory = current_directory)

		current_path = current_directory.str_()


		create_dir_form = DirectoryCreationForm()
		document_upload_form = DocumentUploadForm()
		dir_access_form = DirAccessForm()

		context = {
			'current_directory' : current_directory,
			'child_directories' : child_directories,
			'documents' : documents,
			'parent_dir_pk' : current_directory.pk,
			'create_dir_form' : create_dir_form,
			'document_upload_form' : document_upload_form,
			'current_path' : current_path,
			'dir_update_form' : DirectoryCreationForm,
			'dir_access_form' : dir_access_form,
		}	

		return render(request, 'core/directory.html', context)	

	else:
		return HttpResponseForbidden('<h1>403 Forbidden</h1>')


@method_decorator(allowed_users(allowed_roles=['admin']), name='dispatch')
class DirectoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Directory
	form_class = DirectoryCreationForm
	template_name = 'core/update_dir_form.html'
	success_message = "Updated successfully"

	def test_func(self):
		directory = Directory.objects.get(pk = self.kwargs['pk'])
		if directory.name == 'root' and directory.parent_directory == None:
			return False
		else:
			return True

	def get_success_url(self):
		return reverse('core:directory', kwargs = {'pk' : self.kwargs['pk']})


@method_decorator(allowed_users(allowed_roles=['admin']), name='dispatch')
class DirectoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Directory
	template_name = 'core/dir_delete_confirmation.html'
	success_url = '/'

	def test_func(self):
		directory = Directory.objects.get(pk = self.kwargs['pk'])
		if directory.name == 'root' and directory.parent_directory == None:
			return False
		else:
			return True

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
		document = Document.objects.get(pk = self.kwargs['pk'])
		dirAccess = DirectoryAccess.objects.filter(directory=document.directory).filter(user=usr).exists()
		if usr.groups.filter(name='admin').exists() == True:
			return True
		elif dirAccess == True:
				return True
		else:
			return False

	def get_success_url(self):
		document = Document.objects.get(pk = self.kwargs['pk'])
		parent_dir_pk = document.directory.pk
		return reverse('core:directory', kwargs = {'pk' : parent_dir_pk})


def commonDocumentView(request):
	common_documnts_list = CommonDocument.objects.filter()

	form = CommonDocumentUploadForm()

	paginator = Paginator(common_documnts_list, 4)

	page = request.GET.get('page', 1)

	try:
		common_documnts = paginator.page(page)
	except PageNotAnInteger:
		common_documnts = paginator.page(1)
	except EmptyPage:
		common_documnts = paginator.page(paginator.num_pages)

	context = {
		'common_documnts' : common_documnts,
		'document_upload_form' : form,
	}

	return render(request, 'core/common_documnts.html', context)


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

				return redirect('core:common-documents')

		except:
			return HttpResponse('Some error occured!!')

	# For development process only. Change to error msg on production.
	context = {
		'document_upload_form' :form,

	}

	return render(request, 'core/common_document_upload_form.html', context)



@method_decorator(allowed_users(allowed_roles=['admin']), name='dispatch')
class CommonDocumentDeleteView(LoginRequiredMixin, DeleteView):
	model = CommonDocument
	template_name = 'core/document_delete_confirmation.html'
	success_url = '/'


@allowed_users(allowed_roles=['admin'])
def dirAccess(request, pk):
	if request.method == 'POST':
		try:
			usr = User.objects.get(pk = request.POST['user'])
			directory = Directory.objects.get(pk = pk)

			if (DirectoryAccess.objects.filter(user=usr).filter(directory=directory)).exists():
				messages.success(request, f'User already have access to {directory.name} folder.')
				return redirect('core:directory', pk=pk)

			else:
				form = DirAccessForm(request.POST or None)
				if form.is_valid():
					
					
					form.instance.directory = directory
					form.instance.updated_by = request.user
					
					form.save()
					return redirect('core:directory', pk=pk)
		except:
			return HttpResponse('Some error occured!!')

	else:

		dir_access_form = DirAccessForm()

		context = {
			'dir_access_form' : dir_access_form
		}

		return render(request, 'core/dir_access.html', context)


@method_decorator(allowed_users(allowed_roles=['admin']), name='dispatch')
class DirAccessDeleteView(LoginRequiredMixin, DeleteView):
	model = DirectoryAccess
	template_name = 'core/dir_access_delete_confirmation.html'
	
	def get_success_url(self):
		dir_access = DirectoryAccess.objects.get(pk = self.kwargs['pk'])
		return reverse('core:directory', kwargs = {'pk' : dir_access.directory.pk})

