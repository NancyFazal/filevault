from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from files.models import UploadedFile
from files.serializers import UploadedFileSerializer


class UploadedFileSerializerTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123"
        )

        self.file = SimpleUploadedFile(
            "report.pdf",
            b"example file content",
            content_type="application/pdf"
        )

        self.uploaded_file = UploadedFile.objects.create(
            owner=self.user,
            file=self.file,
            original_name="report.pdf",
            size=self.file.size
        )

    def test_serializer_contains_expected_fields(self):
        serializer = UploadedFileSerializer(
            instance=self.uploaded_file
        )

        self.assertEqual(
            set(serializer.data.keys()),
            {
                "id",
                "file",
                "original_name",
                "size",
                "uploaded_at",
            }
        )

    def test_serializer_returns_correct_file_metadata(self):
        serializer = UploadedFileSerializer(
            instance=self.uploaded_file
        )

        self.assertEqual(
            serializer.data["original_name"],
            "report.pdf"
        )

        self.assertEqual(
            serializer.data["size"],
            len(b"example file content")
        )