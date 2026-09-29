from django.contrib.auth import get_user_model
from django.test import TestCase

from files.models import UploadedFile


class UploadedFileModelTest(TestCase):

    def test_uploaded_file_string_representation(self):
        user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123"
        )

        uploaded_file = UploadedFile.objects.create(
            owner=user,
            file="uploads/report.pdf",
            original_name="report.pdf",
            size=1024
        )

        self.assertEqual(
            str(uploaded_file),
            "report.pdf"
        )