# @brief
# Performs file upload validation for django. The original version implemented
# by dokterbob had some problems with determining the correct mimetype and
# determining the size of the file uploaded (at least within my Django application
# that is).

# @author dokterbob
# @author jrosebr1

import mimetypes
from os.path import splitext

from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat


extension_message = "Extension '%(extension)s' not allowed. Allowed extensions are: '%(allowed_extensions)s.'"
video_extension_message = "Extension '%(extension)s' not allowed. Allowed extensions are: '%(allowed_extensions)s.'"
image_extension_message = "Extension '%(extension)s' not allowed. Allowed extensions are: '%(allowed_extensions)s.'"
mime_message = "MIME type '%(mimetype)s' is not valid. Allowed types are: %(allowed_mimetypes)s."
min_size_message = 'The current file %(size)s, is too small. The minumum file size is %(allowed_size)s.'
max_size_message = 'The current file %(size)s, is too large. The maximum file size is %(allowed_size)s.'

allowed_extensions = ['mp3', 'wav']
allowed_video_extensions = ['mp4', 'webm', 'mov', 'wmv', 'avi', 'wav']
allowed_image_extensions = ['jpg', 'jpeg', 'png']
allowed_mimetypes = ['audio/mpeg', 'audio/vnd.wav']
min_size = 100
max_size = 52428800

def check_extension(value):
    # Check the extension
    ext = splitext(value.name)[1][1:].lower()
    if allowed_extensions and not ext in allowed_extensions:
        message = extension_message % {
            'extension' : ext,
            'allowed_extensions': ', '.join(allowed_extensions)
        }

        raise ValidationError(message)

def check_video_extension(value):
    # Check the extension
    ext = splitext(value.name)[1][1:].lower()
    if allowed_video_extensions and not ext in allowed_video_extensions:
        message = video_extension_message % {
            'extension' : ext,
            'allowed_extensions': ', '.join(allowed_video_extensions)
        }

        raise ValidationError(message)
    
def check_image_extension(value):
    # Check the extension
    ext = splitext(value.name)[1][1:].lower()
    if allowed_image_extensions and not ext in allowed_image_extensions:
        message = image_extension_message % {
            'extension' : ext,
            'allowed_extensions': ', '.join(allowed_image_extensions)
        }

        raise ValidationError(message)
    
def check_mime_type(value):
    # Check the content type
    mimetype = mimetypes.guess_type(value.name)[0]
    if allowed_mimetypes and not mimetype in allowed_mimetypes:
        message = mime_message % {
            'mimetype': mimetype,
            'allowed_mimetypes': ', '.join(allowed_mimetypes)
        }

        raise ValidationError(message)

def check_file_size(value):
    # Check the file size
    filesize = len(value)
    if max_size and filesize > max_size:
        message = max_size_message % {
            'size': filesizeformat(filesize),
            'allowed_size': filesizeformat(max_size)
        }

        raise ValidationError(message)

    elif filesize < min_size:
        message = min_size_message % {
            'size': filesizeformat(filesize),
            'allowed_size': filesizeformat(min_size)
        }

        raise ValidationError(message)

        