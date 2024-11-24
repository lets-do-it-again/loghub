from rest_framework import generics
from .models import Log
from .serializers import LogSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import LogSerializer
from django.utils import timezone
from category.api.v1.permissions import IsCategoryUser

class CreateLogView(generics.CreateAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = [IsAuthenticated , IsCategoryUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class UpdateEndTimeIfNullView(generics.UpdateAPIView):
    """API endpoint to update the end_time of a log entry."""
    queryset = Log.objects.all()
    serializer_class = LogSerializer

    def post(self, request, *args, **kwargs):
        log_key = request.data.get('log_key')
        try:
            log = self.queryset.get(log_key=log_key)
        except Log.DoesNotExist:
            return Response({"detail": "Log not found."}, status=status.HTTP_404_NOT_FOUND)

        if log.end_time is None:
            log.end_time = timezone.now()
            log.save()
            serializer = self.get_serializer(log)
            return Response(serializer.data)
        else:
            return Response({"detail": "End time is already set."}, status=status.HTTP_400_BAD_REQUEST)
