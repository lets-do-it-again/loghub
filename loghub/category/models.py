from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from accounts.models import User
from mptt.models import MPTTModel, TreeForeignKey


class CategoryDetail(MPTTModel):
    parent = TreeForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )
    image = models.ImageField(upload_to="media/categories", blank=True, null=True)
    title = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z]+$",
                message="Please use only alphabetic English characters.",
            )
        ],
    )
    slug = models.SlugField(unique=True)
    description = models.TextField()
    is_root = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Category(models.Model):
    category_detail = models.ForeignKey(
        CategoryDetail, on_delete=models.CASCADE, related_name="category"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="UserAccessCategory"
    )
    title = models.CharField(max_length=30, blank=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"title is {self.title}"


class CategoryTemplate(models.Model):
    category_detail = models.ForeignKey(
        CategoryDetail, on_delete=models.CASCADE, related_name="templates"
    )

    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)

    def __str__(self):
        return f"title is {self.title}"


class CategoryPermission(models.Model):
    user_ids = models.JSONField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="User_access_category"
    )
    included_childs = models.JSONField(null=True, blank=True)
    excluded_childs = models.JSONField(null=True, blank=True)
    PERMISSION_TYPE_CHOICES = [
        ("None", "None"),
        ("Anyone", "Anyone"),
        ("User", "User"),
        ("Keyword", "Keyword"),
        ("Mix", "Mix"),
    ]
    keyword = models.UUIDField(unique=True, null=True, blank=True)
    permission_type = models.CharField(
        max_length=10,
        choices=PERMISSION_TYPE_CHOICES,
        default="None",
    )
