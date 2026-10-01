from rest_framework import serializers

from files.models import UploadedFile
from files.validators import validate_file_extension, validate_file_size


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

    def validate_file(self, file):
        validate_file_size(file)
        validate_file_extension(file)
        return file