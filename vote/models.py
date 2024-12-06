from enum import unique
from django.db import models
from django.core.validators import ValidationError
from django.contrib.auth.models import User
from rest_framework.schemas.coreapi import serializers

class Award(models.Model):
    name=models.CharField(max_length=100, unique=True)
    description=models.TextField()

    def __str__(self):
        return self.name


class Category(models.Model):
    award=models.ForeignKey(Award, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, unique=True)
    description= models.TextField()
    max_vote_per_user = models.PositiveIntegerField(default=1)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together=["award", "name"]
    def __str__(self):
        return self.name


class Nomination(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='nominations')
    from production.models import Artist
    nominee = models.ForeignKey(
        Artist, on_delete=models.CASCADE, blank=True, null=True)
    # Assuming Artist is in music_production
    nominee_name = models.CharField(max_length=100, null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together=[["category", "nominee"],["category", "nominee_name"]]

    def __str__(self):
        if self.nominee:
             return self.nominee.name
        return self.nominee_name


class Preference(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    points = models.PositiveIntegerField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    
    def clean(self):
        category_preference_count=Preference.objects.filter(category=self.category).count()
        max_category_preferences=self.category.max_vote_per_user
        if not self.pk and  category_preference_count>=max_category_preferences:
          raise ValidationError("Exceede!!!")
    def __str__(self):
        return self.name


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    nomination = models.ForeignKey(Nomination, on_delete=models.CASCADE)
    preference = models.ForeignKey(Preference, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'nomination', 'preference')

    def __str__(self):
        return f"Vote by {self.user.username} for {self.nomination.nominee.name} with preference {self.preference.name}"




# Create your models here.
