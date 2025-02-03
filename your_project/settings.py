MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Add this to ensure proper mime types
MIME_TYPES = {
    'video/mp4': '.mp4',
    'video/webm': '.webm',
} 