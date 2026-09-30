from rest_framework import serializers

from files.models import UploadedFile


class UploadedFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadedFile
        fields = [
            "id",
            "file",
            "original_name",
            "size",
            "uploaded_at",
        ]

        read_only_fields = [
            "id",
            "original_name",
            "size",
            "uploaded_at",
        ]