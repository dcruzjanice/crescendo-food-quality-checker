src-> settings.py-> 'add these changes'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_FROM = 'from_whom_u_want_mail'
EMAIL_HOST_USER = 'ur_email'
EMAIL_HOST_PASSWORD = 'ur_app_password'
