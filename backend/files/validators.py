from django.core.exceptions import ValidationError
from pathlib import Path

MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {
  ".pdf",
  ".txt",
  ".csv",
  ".jpg",
  ".jpeg",
  ".png"
}

def validate_file_size(file):
  if file.size > MAX_FILE_SIZE:
    raise ValidationError(
      "File size can not exceed 10MB"
    )

def validate_file_extension(file):
  extension = Path(file.name).suffix.lower()

  if extension not in ALLOWED_EXTENSIONS:
    raise ValidationError(
      "Unsupported file type. "
    )
