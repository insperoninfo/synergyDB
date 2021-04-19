from django.db import models
from django.contrib.auth.models import User
import os
from core.storage import OverwriteStorage

BRANCH_CHOICES = (
		("Kathmandu", "KTM"),
		("Bhaktapur", "BTP")
	)


def get_upload_path(instance, filename):
	print(filename)
	upload_path = os.path.join(instance.directory.str(), filename)

	return upload_path

class Directory(models.Model):
	name = models.CharField(max_length=256)
	parent_directory = models.ForeignKey('self', blank=True, null=True,  on_delete = models.CASCADE)
	branch = models.CharField(max_length=64, choices=BRANCH_CHOICES)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	updated_by = models.ForeignKey(User, null=True, on_delete = models.SET_NULL)


	def str(self):
		if self.parent_directory:
			return os.path.join(self.parent_directory.str(), self.name)
		else:
			return os.path.join(self.branch,self.name)

	class Meta:
		ordering = ('-created_at',)

	def __str__(self):
		return self.str()		


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
		return os.path.join(self.directory.str(),self.filename())


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