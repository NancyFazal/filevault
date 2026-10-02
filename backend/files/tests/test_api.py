from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from files.models import UploadedFile


class UploadedFileAPITest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
        )

        self.client.force_authenticate(
            user=self.user
        )

    def test_user_can_upload_file(self):
        file = SimpleUploadedFile(
            "report.pdf",
            b"example PDF content",
            content_type="application/pdf",
        )

        response = self.client.post(
            "/api/files/",
            {"file": file},
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            UploadedFile.objects.count(),
            1,
        )

        uploaded_file = UploadedFile.objects.first()

        self.assertEqual(
            uploaded_file.owner,
            self.user,
        )

        self.assertEqual(
            uploaded_file.original_name,
            "report.pdf",
        )

    def test_unauthenticated_user_cannot_list_files(self):
      self.client.force_authenticate(user=None)

      response = self.client.get(
        "/api/files/"
      )

      self.assertIn(
        response.status_code,
        [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        ],
      )

    def test_user_only_sees_own_files(self):
      other_user = get_user_model().objects.create_user(
        username="otheruser",
        password="testpassword123",
      )

      UploadedFile.objects.create(
        owner=self.user,
        file="uploads/my-file.pdf",
        original_name="my-file.pdf",
        size=100,
      )

      UploadedFile.objects.create(
        owner=other_user,
        file="uploads/private.pdf",
        original_name="private.pdf",
        size=200,
      )

      response = self.client.get(
        "/api/files/"
      )

      self.assertEqual(
        response.status_code,
        status.HTTP_200_OK,
      )

      self.assertEqual(
        len(response.data),
        1,
      )

      self.assertEqual(
        response.data[0]["original_name"],
        "my-file.pdf",
      )