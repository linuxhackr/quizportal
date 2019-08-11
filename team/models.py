from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=64)
    id = models.IntegerField(default=0, primary_key=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    participants = models.ManyToManyField(User)
    name = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_rank(self, round):
        pass

    def is_eligible_for_round(self, round):
        pass

    def get_leader(self):
        return self.participants.first()

