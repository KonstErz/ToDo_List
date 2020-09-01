from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    """
    The Model is a Company with a name and a list of its members (users).
    """

    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, blank=True, related_name='members')

    def __str__(self):
        return f'{self.name}'


class ToDo(models.Model):
    """
    The Model is a ToDo with a description and creation date.
    This is company-specific.
    """

    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE,
                                related_name='todos')
