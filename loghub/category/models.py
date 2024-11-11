from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    parent = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='children'
    )
    image = models.ImageField(upload_to='media/categories',blank=True, null=True)
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    def __str__(self) :
        return self.name

class Template(models.Model):
    category_id = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='templates'
        )

    title = models.CharField(max_length=30)


class UserAccessCategory(models.Model):
    user_id = models.ForeignKey(User)
    category_id = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='UserAccessCategory'
        )
    
    ROLE_TYPE_CHOICES = [
    ("None", "None"),
    ("Anyone", "Anyone"),
    ("User", "User"),
    ("mix", "mix"),
    ]
    role_type = models.CharField(
        max_length= 10,
        choices=ROLE_TYPE_CHOICES,
        default="None",
    )