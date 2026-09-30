from django.conf import settings
from django.db import models


class UploadedFile(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_files"
    )

    file = models.FileField(
        upload_to="uploads/"
    )

    original_name = models.CharField(
        max_length=255
    )

    size = models.PositiveBigIntegerField()

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.original_name