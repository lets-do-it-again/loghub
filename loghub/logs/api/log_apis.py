from rest_framework import generics
from ..models import Log
from ..serializers import LogSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..serializers import LogSerializer,SourceLogSerializer
from django.utils import timezone
from category.api.v1.permissions import IsCategoryUser
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateLogView(generics.CreateAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = [IsAuthenticated , IsCategoryUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
        return Log.objects.filter_logs(self.request)


class AddSourceToLogView(generics.GenericAPIView):
    serializer_class = SourceLogSerializer
    permission_classes = [IsAuthenticated, IsCategoryUser]

    def post(self, request, log_id):
        try:
            log_instance = Log.objects.get(pk=log_id)
        except Log.DoesNotExist:
            return Response({"detail": "Log not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(log=log_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)