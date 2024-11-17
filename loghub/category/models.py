from django.db import models
from loghub.accounts.models import User

class Category(models.Model):
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )
    image = models.ImageField(upload_to='media/categories', blank=True, null=True)
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Template(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='templates'
    )
    title = models.CharField(max_length=30)

    def __str__(self):
        return f"title is {self.title}"


class UserAccessCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(
        Category,
        related_name='user_access_categories',
        blank=True,
    )

    ROLE_TYPE_CHOICES = [
        ("None", "None"),
        ("Anyone", "Anyone"),
        ("User", "User"),
        ("mix", "mix"),
    ]

    role_type = models.CharField(
        max_length=10,
        choices=ROLE_TYPE_CHOICES,
        default="None",
    )

    include_categories = models.ManyToManyField(
        Category,
        related_name='included_in_user_access',
        blank=True,
    )

    exclude_categories = models.ManyToManyField(
        Category,
        related_name='excluded_from_user_access',
        blank=True,
    )

    def update_categories(self):
        """
        Update categories based on role_type:
        - Exclude categories if listed in exclude_categories.
        - Include categories if listed in include_categories.
        """
        if self.role_type == "mix":
            # Get current categories
            current_categories = self.categories.all()

            # Exclude categories
            for category in self.exclude_categories.all():
                if category in current_categories:
                    self.categories.remove(category)

            # Include categories
            for category in self.include_categories.all():
                if category not in current_categories:
                    self.categories.add(category)


class Keyword(models.Model):
    user_access_category = models.ForeignKey(
        UserAccessCategory,
        on_delete=models.CASCADE,
        related_name='keywords'
    )
    created_date = models.DateTimeField(auto_now_add=True)
    expired_date = models.DateTimeField(null=True, blank=True)
    value = models.TextField()
