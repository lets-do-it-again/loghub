from rest_framework import generics
from .models import Log
from .serializers import LogSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import LogSerializer
from django.utils import timezone
from category.permissions import IsCategoryUser
from django.contrib.auth import get_user_model
from category.models import Category,CategoryPermission

User = get_user_model()

class CreateLogView(generics.CreateAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = [IsAuthenticated , IsCategoryUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# about Apiview and generics
class UpdateEndTimeView(generics.UpdateAPIView):
    """API endpoint to update the end_time of a log entry."""
    queryset = Log.objects.all()
    serializer_class = LogSerializer

    def post(self, request):
        log_key = request.data.get('log_key')
        try:
            log = self.queryset.get(log_key=log_key)
        except Log.DoesNotExist:
            return Response({"detail": "Log not found."}, status=status.HTTP_404_NOT_FOUND)

        if log.end_time is None:
            log.end_time = timezone.now()
            log.save()
            serializer = self.serializer_class(log)
            return Response(serializer.data)
        else:
            return Response({"detail": "End time is already set."}, status=status.HTTP_400_BAD_REQUEST)

class LogSearchView(generics.ListAPIView):
    serializer_class = LogSerializer

    def get_queryset(self):
        queryset = Log.objects.all()
        
        username = self.request.query_params.get('username')
        if username:
            try:
                user = User.objects.get(username=username)
            except:
                # talk about this
                pass
            queryset = queryset.filter(user=user)

        # talk about problem
        start_time = self.request.query_params.get('start_time')
        if start_time:
            queryset = queryset.filter(start_time__gte=start_time)

        end_time = self.request.query_params.get('end_time')
        if end_time:
            queryset = queryset.filter(end_time__lte=end_time)

        log_key = self.request.query_params.get('log_key')
        if log_key:
            queryset = queryset.filter(log_key=log_key)

        
        queryset = queryset.filter(is_public=True)


        
        allowed_log_ids = self.get_allowed_logs(queryset)
        queryset = queryset.filter(id__in=allowed_log_ids)

        return queryset

    def get_allowed_logs(self, queryset):
        allowed_log_ids = set()
        keyword = self.request.query_params.get('keyword')


        for log in queryset:
            category = log.category
            permission = CategoryPermission.objects.get(category_id=category.id)


            if permission.permission_type == "None":
                continue

            elif keyword:
                if permission.permission_type == "keyword" and keyword == permission.keyword:
                    allowed_log_ids.add(log.id)

            elif self.request.user.is_authenticated:
                if permission.permission_type == "User" and self.request.user.id in permission.user_ids:
                    allowed_log_ids.add(log.id)

            elif permission.permission_type == "Anyone":
                allowed_log_ids.add(log.id)
            
            #logic MIX

        return allowed_log_ids

