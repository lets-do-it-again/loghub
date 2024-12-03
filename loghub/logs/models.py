from django.db import models
from django.contrib.auth import get_user_model
from category.models import CategoryDetail
from django.utils import timezone
from django.core.exceptions import ValidationError
from category.models import *

User = get_user_model()


from django.db import models
from django.db.models import Q

class LogManager(models.Manager):
    def filter_logs(self, request):
        queryset = self.get_queryset()

        accessible_categories = self.get_accessible_categories(request)

        if accessible_categories:
            categories = CategoryDetail.objects.filter(id__in=accessible_categories)
            all_related_categories = categories.get_descendants(include_self=True)
            queryset = queryset.filter(category__in=all_related_categories, is_public=True)

        username = request.query_params.get('username', '').strip()
        if username:
            try:
                user = User.objects.get(username=username)
                queryset = queryset.filter(user=user)
            except User.DoesNotExist:
                pass

        start_time = request.query_params.get('start_time')
        if start_time:
            queryset = queryset.filter(start_time__gte=start_time)

        end_time = request.query_params.get('end_time')
        if end_time:
            queryset = queryset.filter(end_time__lte=end_time)

        log_key = request.query_params.get('log_key')
        if log_key:
            queryset = queryset.filter(log_key=log_key)

        return queryset

    def get_accessible_categories(self, request):
        user = request.user
        keyword = request.query_params.get('keyword')

        conditions = Q()

        if user.is_authenticated:
            conditions |= Q(permission_type="User", user_ids__in=[user.id])
        
        conditions |= Q(permission_type="Anyone")

        if keyword:
            conditions |= Q(permission_type="keyword", keyword=keyword)

        accessible_categories = CategoryPermission.objects.filter(conditions).distinct().values_list('category', flat=True)

        return list(accessible_categories)




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

    
    objects = LogManager()


class SourceLog(models.Model):
    log = models.ForeignKey(Log,on_delete=models.CASCADE,related_name="source")
    url = models.URLField()
    is_digital = models.BooleanField()
    text = models.TextField()
    meta_data = models.JSONField()


    def __str__(self) -> str:
        return f"{self.log}-{self.is_digital}"

    