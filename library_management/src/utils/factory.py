from logging.config import dictConfig
from flask import Flask


def create_app(package_name, config, extensions=None):
    app = Flask(package_name)
    app.config.from_object(config)
    config.init_app(app)

    if extensions:
        for extension in extensions:
            extension.init_app(app)

        dictConfig({
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'verbose': {
                    'format': '{"loggerName":"%(name)s", "functionName":"%(funcName)s", "lineNo":"%(lineno)d",'
                              ' "levelName":"%(levelname)s", "msg":"%(message)s"}'
                },
                'json': {
                    'format': '{"loggerName":"%(name)s", "functionName":"%(funcName)s", "lineNo":"%(lineno)d",'
                              ' "levelName":"%(levelname)s", "msg":"%(message)s"}'
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'DEBUG',
                    'formatter': 'verbose',
                    'stream': 'ext://sys.stderr'
                },
                'file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'formatter': 'json',
                    'filename': 'library.log',
                    'maxBytes': 2048 * 1024 * 1024,
                    'backupCount': 0,
                    'level': 'DEBUG'
                },
            },
            'loggers': {
                'tasks': {
                    'handlers': ['file'],
                    'level': 'DEBUG'
                },
                'tasks2': {
                    'handlers': ['console'],
                    'level': 'DEBUG'
                }

            }
        })

    return app
