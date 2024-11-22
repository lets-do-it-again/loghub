from django.db import models
from django.contrib.auth import get_user_model
from category.models import CategoryDetail
from django.utils import timezone
from django.core.exceptions import ValidationError

User = get_user_model()


class Log(models.Model):
    description = models.TextField(max_length=200)
    category = models.ForeignKey(CategoryDetail,on_delete=models.CASCADE,related_name="logs")
    log_key = models.SlugField(unique=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    is_public = models.BooleanField(default=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="logs")
    deleted_at = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user}-{self.category}-{self.start_time}"
    
    def save(self, *args, **kwargs):
        if self.end_time and self.start_time:
            self.duration = self.end_time - self.start_time
        # else:
        #     self.duration = None
        super().save(*args, **kwargs)

    


class SourceLog(models.Model):
    log = models.ForeignKey(Log,on_delete=models.CASCADE,related_name="source")
    url = models.URLField()
    is_digital = models.BooleanField()
    text = models.TextField()
    meta_data = models.JSONField()


    def __str__(self) -> str:
        return f"{self.log}-{self.is_digital}"

    