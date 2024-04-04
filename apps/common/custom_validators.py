from math import ceil
import mimetypes
from django.core.exceptions import ValidationError
from core.settings.base import FILE_UPLOAD_MAX_MEMORY_SIZE
from django.core.files.storage import FileSystemStorage


def convert_to_megabyte(file_size):
    file_size_in_mb = round(file_size / (1000 * 1000))
    return ceil(file_size_in_mb)


def custom_file_validator(file):

    file_types = ["image/png", "image/jpeg", "image/jpg", "application/pdf"]

    if not file:
        raise ValidationError("No file selected.....")

    if file.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
        raise ValidationError(f"File shouldn't be larger than {convert_to_megabyte(FILE_UPLOAD_MAX_MEMORY_SIZE)}MB.")

    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    file_type = mimetypes.guess_type(filename)[0]
    if file_type not in file_types:
        raise ValidationError("Invalid file, please upload an image file with extensions (png, jpg or jpeg).")
    return file
