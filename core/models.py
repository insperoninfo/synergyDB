from django.db import models
from django.contrib.auth.models import User

BRANCH_CHOICES = (
		("Kathmandu", "KTM"),
		("Bhaktapur", "BTP")
	)

class Directory(models.Model):
	name = models.CharField(max_length=256)
	parent_directory = models.ForeignKey('self', blank=True, null=True,  on_delete = models.CASCADE)
	branch = models.CharField(max_length=64, choices=BRANCH_CHOICES)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	updated_by = models.ForeignKey(User, null=True, on_delete = models.SET_NULL)


	def str(self):
		if self.parent_directory:
			return f'{self.branch}-{self.parent_directory.str()}/{self.name}'
		else:
			return f'{self.branch}-/{self.name}'

	def __str__(self):
		return self.str()		


class Document(models.Model):
	directory = models.ForeignKey(Directory, on_delete = models.CASCADE)
	file = models.FileField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	updated_by = models.ForeignKey(User, null=True, on_delete = models.SET_NULL)

	def __str__(self):
		return f'{self.directory.str()}/{self.file.name}'