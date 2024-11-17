from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Category(models.Model):
    parent = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='children'
    )
    image = models.ImageField(upload_to='media/categories',blank=True, null=True)
    name = models.CharField(max_length=30,
        # validators = [
        #     RegexValidator(
        #         regex=r'^[a-zA-Z]+$',
        #         message="Please use only alphabetic English characters."
        #         )
        # ]
    )
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


    def __str__(self):
        return f"title is {self.title}"


class UserAccessCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='user_access_categories'
    )

    ROLE_TYPE_CHOICES = [
        ("N", "None"),
        ("A", "Anyone"),
        ("U", "User"),
        ("M", "Mix"),
    ]
    role_type = models.CharField(
        max_length=10,
        choices=ROLE_TYPE_CHOICES,
        default="N",
    )

    def __str__(self):
        return f"{self.user} - {self.category} - {self.role_type}"

    @classmethod
    def include_template_access(cls, user, category, role_type="U"):
        """Include access for a user to a specific category."""
        return cls.objects.get_or_create(
            user=user,
            category=category,
            defaults={'role_type': role_type}
        )

    @classmethod
    def exclude_template_access(cls, user, category):
        """Exclude access for a user from a specific category."""
        cls.objects.filter(user=user, category=category).delete()

    @classmethod
    def has_access_to_template(cls, user, category):
        """Check if a user has access to a specific category."""
        return cls.objects.filter(user=user, category=category).exists()