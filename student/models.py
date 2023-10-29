from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from educator.models import StudyGroup
from django.db.models.signals import post_save
from django.dispatch import receiver


class DayData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = [['user', 'date', 'group']]

    data = models.TextField()
    practice_time = models.PositiveIntegerField(default=0)
    small_claimed = models.BooleanField(default=False)
    big_claimed = models.BooleanField(default=False)


class UploadedText(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)


class UploadedFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    date = models.DateField(default=timezone.now)
    timestamp = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    high_score_met = models.PositiveIntegerField(default=0)
    coins = models.IntegerField(default=0)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class JoinGroup(models.Model):
    join_code = models.CharField(max_length=6, default='000000')
