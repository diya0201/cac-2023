from django.db import models
from django.utils.crypto import get_random_string
from core.models import CustomUser


class StudyGroup(models.Model):
    name = models.CharField(max_length=100)
    educator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='educator_groups')
    join_code = models.CharField(max_length=6)
    students = models.ManyToManyField(CustomUser, related_name='student_groups', blank=True)
    practice_goal = models.PositiveIntegerField()

    def __str__(self):
        return self.name


def generate_unique_join_code():
    join_code = get_random_string(6).upper()
    while StudyGroup.objects.filter(join_code=join_code).exists():
        join_code = get_random_string(6).upper()
    return join_code
