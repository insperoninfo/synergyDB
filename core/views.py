from django.shortcuts import render
from .decorators import allowed_users
from django.contrib.auth.decorators import login_required
from .models import Directory, Document


@login_required
def index(request):
	current_user = request.user
	current_user_branch = current_user.profile.branch

	root_dir = Directory.objects.filter(name='root').filter(branch = current_user_branch)
	root_dir_documents = Document.objects.filter(directory = root_dir[0])
	root_dir_folders = Directory.objects.filter(parent_directory = root_dir[0])

	context = {
		'current_user' : current_user,
		'current_user_branch' : current_user_branch,
		'root_dir' : root_dir[0],
		'root_dir_documents' : root_dir_documents,
		'root_dir_folders' : root_dir_folders,

	}

	return render(request, 'core/index.html', context)