from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase

from files.validators import (
    validate_file_extension,
    validate_file_size,
)
from files.serializers import UploadedFileSerializer


class FileValidatorTest(SimpleTestCase):

    def test_valid_file_size(self):
        file = SimpleUploadedFile(
            "report.pdf",
            b"small file"
        )

        try:
            validate_file_size(file)
        except ValidationError:
            self.fail(
                "Valid file size raised ValidationError"
            )

    def test_file_larger_than_10_mb_is_rejected(self):
        file = SimpleUploadedFile(
            "large.pdf",
            b"x" * (10 * 1024 * 1024 + 1)
        )

        with self.assertRaises(ValidationError):
            validate_file_size(file)

    def test_allowed_extension_is_accepted(self):
        file = SimpleUploadedFile(
            "report.pdf",
            b"content"
        )

        try:
            validate_file_extension(file)
        except ValidationError:
            self.fail(
                "Allowed extension raised ValidationError"
            )

    def test_disallowed_extension_is_rejected(self):
        file = SimpleUploadedFile(
            "program.exe",
            b"content"
        )

        with self.assertRaises(ValidationError):
            validate_file_extension(file)

    def test_serializer_rejects_disallowed_file_extension(self):
      invalid_file = SimpleUploadedFile(
        "malware.exe",
        b"fake executable content"
      )

      serializer = UploadedFileSerializer(
        data={
            "file": invalid_file
        }
      ) 

      self.assertFalse(serializer.is_valid())

      self.assertIn(
        "file",
        serializer.errors
      )