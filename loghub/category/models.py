from django.core.validators import RegexValidator
from django.db import models
from accounts.models import User

class CategoryDetail(models.Model):
    parent = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='children'
    )
    image = models.ImageField(upload_to='media/categories',blank=True, null=True)
    title = models.CharField(max_length=30,
        validators = [
            RegexValidator(
                regex=r'^[a-zA-Z]+$',
                message="Please use only alphabetic English characters."
                )
        ]
    )
    slug = models.SlugField(unique=True)
    description = models.TextField()
    is_root = models.BooleanField(default=False)

    
    def __str__(self) :
        return self.title

class Category(models.Model):
    category_detail = models.ForeignKey(
        CategoryDetail,
        on_delete=models.CASCADE,
        related_name='templates'
        )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='categories'
        )
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)

    def __str__(self):
        return f"title is {self.title}"

class CategoryTemplate(models.Model):
    category_detail = models.ForeignKey(
        CategoryDetail,
        on_delete=models.CASCADE,
        related_name='header'
        )

    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)

    def __str__(self):
        return f"title is {self.title}"

class CategoryPermission(models.Model):
    user_ids = models.JSONField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='user_access_categories'
        )
    included_childs = models.JSONField()
    excluded_childs = models.JSONField()
    PERMISSION_TYPE_CHOICES = [
    ("None", "None"),
    ("Anyone", "Anyone"),
    ("User", "User"),
    ("Keyword", "Keyword"),
    ("Mix", "Mix")
    ]
    keyword = models.SlugField(blank=True, null=True, unique=True)
    permission_type = models.CharField(
        max_length= 10,
        choices=PERMISSION_TYPE_CHOICES,
        default="None",
    )
