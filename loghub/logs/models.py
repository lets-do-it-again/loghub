from django.db import models
from django.contrib.auth import get_user_model
# from category.models import Category

User = get_user_model()


class Log(models.Model):
    description = models.TextField()
    # category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="logs")
    log_key = models.SlugField(unique=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    is_public = models.BooleanField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="logs")
    deleted_at = models.DateTimeField()


    def __str__(self) -> str:
        return f"{self.user}-{self.category}-{self.start_time}"



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
    json = models.JSONField()


    def __str__(self) -> str:
        return f"{self.log}-{self.is_digital}"

    