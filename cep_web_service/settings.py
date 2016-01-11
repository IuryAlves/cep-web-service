RESTFUL_JSON = {'ensure_ascii': False}
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
ERROR_404_HELP = False
DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(message)s'
        },
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'info': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'api.info': {
            'handlers': ['info'],
            'propagate': True,
            'level': 'INFO'
        },
        'api.error': {
            'handlers': ['error'],
            'propagate': False,
            'level': 'ERROR'
        },
    }
}
