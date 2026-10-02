from rest_framework import permissions, viewsets

from files.models import UploadedFile
from files.serializers import UploadedFileSerializer


class UploadedFileViewSet(viewsets.ModelViewSet):
    serializer_class = UploadedFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UploadedFile.objects.filter(
            owner=self.request.user
        ).order_by("-uploaded_at")

    def perform_create(self, serializer):
        uploaded_file = self.request.FILES["file"]

        serializer.save(
            owner=self.request.user,
            original_name=uploaded_file.name,
            size=uploaded_file.size,
        )