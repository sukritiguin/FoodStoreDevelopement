from django.core.exceptions import ValidationError
import os

def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1]
    print(f"File name: {value.name}")
    print(f"Extracted extension: {ext}")
    valid_extensions_list = [
        '.jpg',
        '.jpeg',
        '.png',
        '.gif',
        '.bmp',
        '.svg',
        '.tiff',
        '.webp',
        '.ico',
    ]
    if not ext.lower() in valid_extensions_list:
        raise ValidationError(f'Unsupported file extension. Allowed extensions are: {valid_extensions_list}')
