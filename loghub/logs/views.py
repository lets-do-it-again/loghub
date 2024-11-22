from rest_framework import generics
from .models import Log
from .serializers import LogSerializer
from rest_framework.permissions import IsAuthenticated

class CreateLogView(generics.CreateAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
