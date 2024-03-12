from django.core.exceptions import ValidationError
import os

def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions_list = [
        'jpg',
        'jpeg',
        'png',
        'gif',
        'bmp',
        'svg',
        'tiff',
        'webp',
        'ico',
    ]
    if ext.lower() not in valid_extensions_list:
        raise ValidationError(f'Unsupported file extension. Allowed extensions are: {valid_extensions_list}')