from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

GENDER_CHOICES = (
		("male", "M"),
		("Female", "F"),
		("Other", "O")
	)

BRANCH_CHOICES = (
		("Kathmandu", "KTM"),
		("Bhaktapur", "BTP")
	)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=256, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES)
    branch = models.CharField(max_length=50, choices=BRANCH_CHOICES)
    phone = models.BigIntegerField(null= True, blank=True)


    def __str__(self):
    	return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()