from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserForm, UserUpdateForm
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from core.decorators import allowed_users
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator


user_admin_required = user_passes_test(lambda user: user.is_superuser, login_url=r'users/accounts/login')

def admin_user_required(view_func):
	decorated_view_func = login_required(user_admin_required(view_func))
	return decorated_view_func


class AdminRequiredMixin(object):
	def dispatch(self, request, *args, **kwargs):
		usr = request.user
		if usr.is_authenticated and usr.is_superuser:
			pass
		else:
			return HttpResponseForbidden('<h1>403 Forbidden</h1>')

		return super().dispatch(request, *args, **kwargs)


@allowed_users(allowed_roles=['admin'])
def createUser(request):
	if request.method == 'POST':
		form = UserForm(request.POST)
		print(form)
		if form.is_valid():
			form.save()
			form.save_m2m()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			
			return redirect('users:update-profile', pk=user.profile.pk)
	else:
		form = UserForm()
	return render(request, r'users/createUser.html', {'form': form})


@method_decorator(allowed_users(allowed_roles=['admin']), name='dispatch')
class ProfileUpdateView(UpdateView):
	model = Profile
	fields = ['designation','branch', 'phone', 'address', 'gender']
	template_name = 'users/update_profile.html'

	success_message =  'User Profile Updated.'   

	def get_success_url(self):
		return reverse('users:user-list')
	

@login_required(login_url='accounts/login')
def changePassword(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Your password was successfully updated!')
			return redirect('core:index')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'users/change_password.html', {
		'form': form
	})
	


@login_required
def userProfile(request):
	user = request.user

	context = {
		'user' : user,
	}
	return render(request, 'users/userProfile.html', context)


@allowed_users(allowed_roles=['admin'])
def userList(request):
	user_list = User.objects.all()
	
	context = {
		'user_list' : user_list,
	}

	return render(request, 'users/userlist.html', context)


@method_decorator(allowed_users(allowed_roles=['admin']), name='dispatch')
class UserUpdateView(UpdateView):
	model = User
	form_class = UserUpdateForm
	template_name = 'users/update_user.html'
	
	def get_success_url(self):
		user = User.objects.get(pk = self.kwargs['pk'])
		print(user, user.profile.pk)
		return reverse('users:update-profile', kwargs = {'pk' : user.profile.pk })


@method_decorator(allowed_users(allowed_roles=['admin']), name='dispatch')
class UserDeleteView(LoginRequiredMixin, DeleteView):
	model = User
	template_name = 'users/user_delete_confirmation.html'
	
	def get_success_url(self):
		return reverse('users:user-list')
