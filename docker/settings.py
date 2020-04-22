from .base_settings import *

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'django_user_agents',
    'compressor',
    'django_client_logger',
    'userservice',
    'rc_django',
    'supporttools',
    'blti',
    'hx_toolkit',
    'myuw.apps.MyUWConfig'
]

MIDDLEWARE += [
    'django.middleware.locale.LocaleMiddleware',
    'userservice.user.UserServiceMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'rc_django.middleware.EnableServiceDegradationMiddleware'
]

if os.getenv('AUTH', 'NONE') == 'SAML_MOCK':
    MOCK_SAML_ATTRIBUTES = {
        'uwnetid': ['javerage'],
        'affiliations': ['student', 'member', 'alum', 'staff', 'employee'],
        'eppn': ['javerage@washington.edu'],
        'scopedAffiliations': ['student@washington.edu',
                               'member@washington.edu'],
        'isMemberOf': ['u_test_group', 'u_test_another_group',
                       'u_astratest_myuw_test-support-admin'],
    }

# MYUW_PREFETCH_THREADING = True
MYUW_ENABLED_FEATURES = []

EMAIL_BACKEND = "saferecipient.EmailBackend"
MAILMAN_COURSEREQUEST_RECIPIENT = ""


# Thrive required settings
MEDIA_ROOT = "/statics/hx_images"
MEDIA_URL = "/uploaded_images/"
THRIVE_OUTPUT = "/hx_toolkit_output"

USERSERVICE_VALIDATION_MODULE = "myuw.authorization.validate_netid"
USERSERVICE_OVERRIDE_AUTH_MODULE = "myuw.authorization.can_override_user"
RESTCLIENTS_ADMIN_AUTH_MODULE = "myuw.authorization.can_proxy_restclient"
MYUW_ADMIN_GROUP = 'u_astratst_myuw_test-support-admin'
MYUW_OVERRIDE_GROUP = 'u_astratst_myuw_test-support-impersonate'
MYUW_ASTRA_GROUP_STEM = "u_astratst_myuw"
MYUW_DISABLE_ACTIONS_WHEN_OVERRIDE = False

# Support Tools settings
SUPPORTTOOLS_PARENT_APP = "MyUW"
SUPPORTTOOLS_PARENT_APP_URL = "/"

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

if os.getenv("COMPRESSOR_ENABLED", "True") == "False":
    COMPRESS_ENABLED = False

COMPRESS_ROOT = "/static"
STATICFILES_FINDERS += (
    'compressor.finders.CompressorFinder',
)

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

TEMPLATES[0]['DIRS'] = ['/app/myuw/templates']
TEMPLATES[0]['OPTIONS']['context_processors'] += [
    'django.template.context_processors.i18n',
    'django.template.context_processors.media',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    'supporttools.context_processors.supportools_globals',
    'supporttools.context_processors.has_less_compiled',
    'supporttools.context_processors.has_google_analytics',
    'myuw.context_processors.is_hybrid',
]

# RESTCLIENTS overrides
RESTCLIENTS_SWS_TIMEOUT = 5
RESTCLIENTS_SWS_POOL_SIZE = 15

RESTCLIENTS_PWS_TIMEOUT = 5
RESTCLIENTS_PWS_POOL_SIZE = 15

RESTCLIENTS_GWS_TIMEOUT = 5
RESTCLIENTS_GWS_POOL_SIZE = 15

RESTCLIENTS_UWNETID_TIMEOUT = 2
RESTCLIENTS_UWNETID_POOL_SIZE = 15

RESTCLIENTS_CANVAS_POOL_SIZE = 10

RESTCLIENTS_CODA_TIMEOUT = 5
RESTCLIENTS_CODA_POOL_SIZE = 10

RESTCLIENTS_BOOK_TIMEOUT = 5
RESTCLIENTS_BOOK_POOL_SIZE = 10

RESTCLIENTS_IASYSTEM_UW_TIMEOUT = 5
RESTCLIENTS_IASYSTEM_UW_POOL_SIZE = 10

RESTCLIENTS_IASYSTEM_UWB_TIMEOUT = 5
RESTCLIENTS_IASYSTEM_UWB_POOL_SIZE = 10

RESTCLIENTS_IASYSTEM_UWT_TIMEOUT = 5
RESTCLIENTS_IASYSTEM_UWT_POOL_SIZE = 10

RESTCLIENTS_IASYSTEM_UWEO_AP_TIMEOUT = 5
RESTCLIENTS_IASYSTEM_UWEO_AP_POOL_SIZE = 10

RESTCLIENTS_IASYSTEM_UWEO_IELP_TIMEOUT = 5
RESTCLIENTS_IASYSTEM_UWEO_IELP_POOL_SIZE = 5

RESTCLIENTS_LIBCURRICS_TIMEOUT = 5
RESTCLIENTS_LIBCURRICS_POOL_SIZE = 10

RESTCLIENTS_LIBRARIES_TIMEOUT = 5
RESTCLIENTS_LIBRARIES_POOL_SIZE = 10

RESTCLIENTS_CALENDAR_TIMEOUT = 5
RESTCLIENTS_CALENDAR_POOL_SIZE = 10

RESTCLIENTS_MAILMAN_TIMEOUT = 5
RESTCLIENTS_MAILMAN_POOL_SIZE = 5

RESTCLIENTS_HFS_TIMEOUT = 60
RESTCLIENTS_HFS_POOL_SIZE = 10

RESTCLIENTS_GRAD_TIMEOUT = 5
RESTCLIENTS_GRAD_POOL_SIZE = 10

RESTCLIENTS_GRADEPAGE_TIMEOUT = 5
RESTCLIENTS_GRADEPAGE_POOL_SIZE = 5

RESTCLIENTS_MYPLAN_TIMEOUT = 5
RESTCLIENTS_MYPLAN_POOL_SIZE = 10

RESTCLIENTS_UPASS_TIMEOUT = 60
RESTCLIENTS_UPASS_POOL_SIZE = 10

if os.getenv("ENV", '') == "localdev":
    DEBUG = True
else:
    RESTCLIENTS_DAO_CACHE_CLASS = 'myuw.util.cache_implementation.MyUWMemcachedCache'
