from django.shortcuts import render, redirect, HttpResponse
from .decorators import allowed_users
from django.contrib.auth.decorators import login_required
from .models import Directory, Document
from .forms import DirectoryCreationForm, DocumentUploadForm
from django.contrib import messages


@login_required
def index(request):
	current_user = request.user
	current_user_branch = current_user.profile.branch

	root_dir = Directory.objects.filter(name='root').filter(branch = current_user_branch)
	root_dir_documents = Document.objects.filter(directory = root_dir[0])
	root_dir_folders = Directory.objects.filter(parent_directory = root_dir[0])

	create_dir_form = DirectoryCreationForm()

	context = {
		'current_user' : current_user,
		'current_user_branch' : current_user_branch,
		'root_dir' : root_dir[0],
		'root_dir_documents' : root_dir_documents,
		'root_dir_folders' : root_dir_folders,
		'parent_dir_pk' : root_dir[0].pk,
		'create_dir_form' : create_dir_form,

	}

	return render(request, 'core/index.html', context)



def createDirectory(request,pk):
	form = DirectoryCreationForm()
	if request.method == 'POST':
		created_by = request.user
		parent_directory = Directory.objects.get(pk = pk)
		branch = parent_directory.branch

		if created_by.profile.branch != branch:
			messages.warning(request, 'You are not authorized to perform the action.')
			return redirect('core:index')

		else:
			try:	
			
				form = DirectoryCreationForm(request.POST or None)
				if form.is_valid():
					
					form.instance.parent_directory = parent_directory
					form.instance.branch = branch
					
					form.save()
					return redirect('core:index')
			except:
				return HttpResponse('Some error occured!!')

	# For development process only. Change to error msg on production.
	return render(request, 'core/create_dir_form.html', {'create_dir_form': form, "parent_dir_pk":pk})


			

	



