import CommandLine
import json

LOGGER_KEY = "logger"

class Utilities:
    def __init__(self):
        self.commandLineArguments = {}
        self.configuration = {}

    def getDonorDataLocation(self):
        """ Get the Location of the Donor Database File, Check Config File First Override """
        if CommandLine.DONOR_DATA_LOCATION_KEY in self.configuration:
            return self.getConfigurationValue(CommandLine.DONOR_DATA_LOCATION_KEY)
        else:
            return self.getCommandLineArgument(CommandLine.DONOR_DATA_LOCATION_KEY)

    def getConfigFilePath(self):
        """Returns the Configuration File Path From The Arguments"""
        return self.getCommandLineArgument(CommandLine.CONFIGURATION_PATH_KEY)

    def getCommandLineArguments(self):
        """Returns the Contents of the Command Line Arguments: Should be used for testing only"""
        return self.commandLineArguments


    def parseCommandLine(self):
        """ Calls The Command Line Parser, Loading Arguments into a Dictionary """
        self.commandLineArguments = CommandLine.parse_command_line()

    def getCommandLineArgument(self, argumentName):
        """ Returns the Named Argument from the Command Line """
        return self.commandLineArguments.get(argumentName, None)

    def parseConfiguration(self, configFilePath):
        """Load the Contents of the Configuration File into a Dictionary"""
        try:
            with open(configFilePath, "r+") as fp:
                self.configuration = json.load(fp)
        except Exception as ex:
            raise Exception(f'Utilities: Parse Configuration Exception {ex}')

    def getConfigurationValue(self, valueKey):
        """Get a Value from the Configuration Dictionary Based on Value Key: None if the Key Doesn't Exist"""
        return self.configuration.get(valueKey, None)
