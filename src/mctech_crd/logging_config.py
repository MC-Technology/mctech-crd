# import logging

# logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)
# console = logging.StreamHandler()
# console.setLevel(logging.WARN)
# logging.getLogger().addHandler(console)

# console = logging.StreamHandler()
# console.setLevel(logging.ERROR)
# formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
# console.setFormatter(formatter)
# logging.getLogger("").addHandler(console)

import logging
import logging.config
import sys

class _ExcludeErrorsFilter(logging.Filter):
    def filter(self, record):
        """Filters out log messages with log level ERROR (numeric value: 40) or higher."""
        return record.levelno < 40


config = {
    'version': 1,
    'filters': {
        'exclude_errors': {
            '()': _ExcludeErrorsFilter
        }
    },
    'formatters': {
        # Modify log message format here or replace with your custom formatter class
        'my_formatter': {
            'format': '(%(process)d) %(asctime)s %(name)s (line %(lineno)s) | %(levelname)s %(message)s'
        }
    },
    'handlers': {
        'console_stderr': {
            # Sends log messages with log level ERROR or higher to stderr
            'class': 'logging.StreamHandler',
            'level': 'ERROR',
            'formatter': 'my_formatter',
            'stream': sys.stderr
        },
        'console_stdout': {
            # Sends log messages with log level lower than ERROR to stdout
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'my_formatter',
            'filters': ['exclude_errors'],
            'stream': sys.stdout
        },
        'file': {
            # Sends all log messages to a file
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': 'my_formatter',
            'filename': 'app.log',
            'encoding': 'utf8'
        }
    },
    'root': {
        # In general, this should be kept at 'NOTSET'.
        # Otherwise it would interfere with the log levels set for each handler.
        'level': 'NOTSET',
        'handlers': ['console_stderr', 'console_stdout', 'file']
    },
}

logging.config.dictConfig(config)
logging.getLogger('googleapiclient').setLevel(logging.CRITICAL)
logging.getLogger('omxplayer').setLevel(logging.CRITICAL)