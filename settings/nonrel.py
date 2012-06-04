from common import *

INSTALLED_APPS += [
    'django_mongodb_engine',
    'djangotoolbox',
    'permission_backend_nonrel',
]

AUTHENTICATION_BACKENDS += (
    'permission_backend_nonrel.backends.NonrelPermissionBackend',
)
