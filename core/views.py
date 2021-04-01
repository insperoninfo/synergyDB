from django.shortcuts import render
from .decorators import allowed_users
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
	return render(request, 'core/index.html')