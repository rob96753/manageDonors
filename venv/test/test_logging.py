import pytest
import sys
import logging

sys.path.insert(1, '../src')
import CommandLine
import Utilities
import Logging

CONFIG_FILE_PATH = '../config/manageDonors.json'
cli_config_values = ['pytest', f'{CommandLine.CONFIG}', CommandLine.DEFAULT_CONFIG_PATH]
SYS_ARGV = 'sys.argv'

logging_config = dict(
            version = 1,
            formatters = {
              "default": {"format": "%(asctime)s - %(levelname)s - %(message)s",
                          "datefmt": "%Y-%m-%d %H:%M:%S"}
            },
            handlers = {
              "console": {
                "class": 'logging.StreamHandler',
                "level": logging.DEBUG,
                "formatter": "default",
                "stream": "ext://sys.stdout"
              },
              "file": {
                "class": 'logging.handlers.RotatingFileHandler',
                "level": logging.DEBUG,
                "formatter": "default",
                "filename": "../manage_donors.log",
                "maxBytes": 1024,
                "backupCount": 3
              }
            },
            root = {
                    "level": logging.DEBUG,
                    "handlers": ["console", "file"]
            }
)

logging_config = dict(
    version = 1,
    formatters = {
         "default": {"format": "%(levelname)s: %(asctime)s - %(message)s",
                          "datefmt": "%Y-%m-%d %H:%M:%S"}
        },
    handlers = {
        'console': {"class": 'logging.StreamHandler',
                "level": logging.DEBUG,
                "formatter": "default",
                "stream": "ext://sys.stdout"},
         'file': {
                "class": 'logging.handlers.RotatingFileHandler',
                "level": logging.DEBUG,
                "formatter": "default",
                "filename": "../manage_donors.log",
                "maxBytes": 1024,
                "backupCount": 3
              }
        },
    loggers = {
        'manage_donors' : {
            'handlers': ['console', 'file'],
            'level': logging.DEBUG
        }
    },
    root = {
        'handlers': ['console', 'file'],
        'level': logging.DEBUG
        }
)

class TestClass:
    utilities = None

    @pytest.fixture(autouse=False)
    def setup(self, monkeypatch):
        """Set the collection of command line arguments"""
        self.utilities = Utilities.Utilities()
        monkeypatch.setattr(SYS_ARGV, cli_config_values)
        self.utilities.parseCommandLine()

    def test_logger_config(self, setup):
        self.utilities.parseConfiguration(self.utilities.getConfigFilePath())
        #config = self.utilities.getConfigurationValue(Utilities.LOGGER_KEY)
        log = Logging.Logger('manage_donors', logging_config)
        logger = log.getLogger()
        logger.error("Test Message")
        assert(logger.isEnabledFor(logging.DEBUG))




