import logging
import logging.config
NAME_KEY = 'name'
FORMAT_KEY = 'format'
DATE_FORMAT_KEY = 'dateFormat'
DISABLE_EXISTING_LOGGERS_KEY = 'disable_existing_loggers'




class Logger():
    """Class Used to Support Logging Information"""
    # The log level to passed to logging configuration can be decoded from the getattr function
    # getattr(logging, 'DEBUG', None)
    # 10
    # logging.basicConfig(filename='example.log', filemode='w', level=10)
    # assuming loglevel is bound to the string value obtained from the
    # Error checking when loading the logging level from the configuration file
    # numeric_level = getattr(logging, loglevel.upper(), None)
    # if not isinstance(numeric_level, int):
    #    raise ValueError('Invalid log level: %s' % loglevel)
    #logging.basicConfig(level=numeric_level, ...)

    """
    HANDLERS
    
    Handler objects are responsible for dispatching the appropriate log messages (based on the 
    log messages’ severity) to the handler’s specified destination. Logger objects can add zero 
    or more handler objects to themselves with an addHandler() method. As an example scenario, 
    an application may want to send all log messages to a log file, all log messages of error or
     higher to stdout, and all messages of critical to an email address. This scenario requires 
     three individual handlers where each handler is responsible for sending messages of a 
     specific severity to a specific location.
     
     Each handlers should have the setLevel, setFormatter, and addFilter calls when being set
     up for use.
    """
    loggerName = __name__
    def __init__(self, loggerName, config):
        """The config the the dictionary object representing the logger configuration"""
        self.loggerName = loggerName
        if not isinstance(config, dict):
            raise Exception(f'Config must be a dictionary not a {type(config)}')
        #if isinstance(config[DISABLE_EXISTING_LOGGERS_KEY], str):
        #    config[DISABLE_EXISTING_LOGGERS_KEY] = config[DISABLE_EXISTING_LOGGERS_KEY].upper() != 'FALSE'
        logging.config.dictConfig(config)
        self.logger = logging.getLogger(self.loggerName)

    def getLogger(self):
        """returns a reference to a logger instance with the specified name if it is provided, or root if not."""
        return logging.getLogger(self.loggerName)