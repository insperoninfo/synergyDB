from django.db import models
from django.contrib.auth.models import User
import os
from core.storage import OverwriteStorage
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings



BRANCH_CHOICES = (
		("Kathmandu", "KTM"),
		("Bhaktapur", "BTP")
	)


def get_upload_path(instance, filename):
	print(filename)
	upload_path = os.path.join(instance.directory.upload_path(), filename)

	return upload_path

class Directory(models.Model):
	name = models.CharField(max_length=256)
	parent_directory = models.ForeignKey('self', blank=True, null=True,  on_delete = models.CASCADE)
	branch = models.CharField(max_length=64, choices=BRANCH_CHOICES)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	updated_by = models.ForeignKey(User, null=True, on_delete = models.SET_NULL)


	def upload_path(self):
		if self.parent_directory:
			return os.path.join(self.parent_directory.upload_path(), str(self.pk))
		else:
			return os.path.join(self.branch, str(self.pk))

	
	def str_(self):
		if self.parent_directory:
			return os.path.join(self.parent_directory.str_(), self.name)
		else:
			return os.path.join(self.branch, self.name)

	class Meta:
		ordering = ('-created_at',)

	def __str__(self):
		return self.str_()		


class Document(models.Model):
	directory = models.ForeignKey(Directory, on_delete = models.CASCADE)
	file = models.FileField(upload_to = get_upload_path, storage=OverwriteStorage())
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	updated_by = models.ForeignKey(User, null=True, on_delete = models.SET_NULL)

	def filename(self):
		return os.path.basename(self.file.name)

	class Meta:
		ordering = ('-updated_at',)

	def __str__(self):
		return os.path.join(self.directory.str_(),self.filename())


class CommonDocument(models.Model):
	file = models.FileField(upload_to = 'common_documents')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	updated_by = models.ForeignKey(User, null=True, on_delete = models.SET_NULL)

	def filename(self):
		return os.path.basename(self.file.name)

	class Meta:
		ordering = ('-updated_at',)

	def __str__(self):
		return os.path.join(self.filename())


class DirectoryAccess(models.Model):
	directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='assigned_to_user')
	updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='updated_by')
	updated_at = models.DateTimeField(auto_now = True)

	def __str__(self):
		return f'{self.directory.str_()} - {self.user}'


# @receiver(pre_save, sender=Directory)
# def update_dir_name(sender, instance, **kwargs):

# 	# If new instance is being created, do nothing
# 	if instance.pk is None:
# 		print('None')
# 		pass

# 	else:
# 		previous = Directory.objects.filter(pk=instance.pk)

# 		prev_path = os.path.join(settings.MEDIA_ROOT, previous[0].str())

# 		if os.path.exists(prev_path) == True:
# 			if instance.parent_directory:
# 				new_path = os.path.join(settings.MEDIA_ROOT,instance.parent_directory.str(), instance.name)
# 			else:
# 				new_path =  os.path.join(settings.MEDIA_ROOT, instance.branch,instance.name)
			
# 			instance.update(file=new_path)
# 			os.rename(prev_path, new_path)