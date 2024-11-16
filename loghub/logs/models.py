from django.db import models
from django.contrib.auth import get_user_model
from category.models import Category

User = get_user_model()


class Log(models.Model):
    description = models.TextField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="logs")
    log_key = models.SlugField(unique=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    is_public = models.BooleanField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="logs")
    deleted_at = models.DateTimeField()
    duration = models.DurationField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user}-{self.category}-{self.start_time}"
    
    def save(self, *args, **kwargs):
        if self.end_time and self.start_time:
            self.duration = self.end_time - self.start_time
        else:
            self.duration = None
        super().save(*args, **kwargs)


    @property
    def duration(self):
        if self.end_time and self.start_time:
            difference = self.end_time - self.start_time
            return difference
        return None
    


class SourceLog(models.Model):
    log = models.ForeignKey(Log,on_delete=models.CASCADE,related_name="source")
    url = models.URLField()
    is_digital = models.BooleanField()
    text = models.TextField()
    meta_data = models.JSONField()


    def __str__(self) -> str:
        return f"{self.log}-{self.is_digital}"

    