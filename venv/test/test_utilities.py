import pytest
import sys

sys.path.insert(1, '../src')
import Utilities
import CommandLine

TEST_DB_FILE_PATH = '../data/db-test.json'
TEST_CONFIG_PATH = '../config/config-test.json'
TEST_DONATION_DATA_LOCATION_FROM_CONFIG = '/venv/data/db.json'
NON_EXISTENT_KEY = 'NOKEY'
SYS_ARGV = 'sys.argv'
CONFIG_FILE_PATH = '../config/manageDonors.json'

cli_values = ["pytest", f'{CommandLine.CONFIG}', TEST_CONFIG_PATH,
              f'{CommandLine.DONORS}', TEST_DB_FILE_PATH]

cli_config_values = ['pytest', f'{CommandLine.CONFIG}', CommandLine.DEFAULT_CONFIG_PATH]


class TestClass:
    utilities = None

    @pytest.fixture(autouse=True, scope="function")
    def setup(self, monkeypatch):
        """Set the collection of command line arguments"""
        self.utilities = Utilities.Utilities()
        monkeypatch.setattr(SYS_ARGV, cli_values)
        self.utilities.parseCommandLine()

    @pytest.fixture(autouse=False)
    def clear(self):
        self.utilities = None
        self.utilities = Utilities.Utilities()

    @pytest.fixture(autouse=False)
    def reset(self, monkeypatch, clear):
        """Reset the collection of command line arguments to test default values"""
        monkeypatch.setattr(SYS_ARGV, ['pytest'])
        self.utilities.parseCommandLine()

    @pytest.fixture(autouse=False)
    def config(self, monkeypatch, clear):
        """Reset the collection of command line arguments to test default values"""
        monkeypatch.setattr(SYS_ARGV, ['pytest',CommandLine.CONFIG, CommandLine.DEFAULT_CONFIG_PATH])
        self.utilities.parseCommandLine()
        self.utilities.parseConfiguration(self.utilities.getConfigFilePath())

    def test_donor_get_donor_location(self):
        """Test the Value for The Get Donor DB File Path Location"""
        assert (self.utilities.getDonorDataLocation().endswith(TEST_DB_FILE_PATH))

    def test_get_config_path(self):
        """Test the Value for The Config File Path Location"""
        assert (self.utilities.getConfigFilePath().endswith(TEST_CONFIG_PATH))

    def test_get_command_line_argument_donor_db(self):
        """Test the Value Return for Get A Command Line Argumetn Using Valid Key"""
        assert (self.utilities.getCommandLineArgument(CommandLine.DONOR_DATA_LOCATION_KEY).endswith(TEST_DB_FILE_PATH))

    def test_get_command_line_argument_undefined(self, reset):
        """Test the Value Return for Get A Command Line Argument Using Non Existent Key"""
        cliArguement = self.utilities.getCommandLineArgument(NON_EXISTENT_KEY)
        assert (cliArguement is None)

    def test_get_command_line_argument_default_config(self, reset):
        """Test the Value Return for Get Config File Path for Situation Where Command Line Omits Key: Default Value Should Be Returned"""
        assert (self.utilities.getConfigFilePath().endswith(CommandLine.DEFAULT_CONFIG_PATH))

    def test_get_command_line_argument_default_donor(self, reset):
        """Test the Value Return for Get Donor File Path for Situation Where Command Line Omits Key: Default Value Should Be Returned"""
        assert (self.utilities.getDonorDataLocation().endswith(CommandLine.DEFAULT_DONOR_DATA_LOCATION_PATH))

    def test_get_config_value_donor_data_location(self, config):
        """Test the Reading of Config File For the Data Donor Path"""
        assert(self.utilities.getConfigurationValue(CommandLine.DONOR_DATA_LOCATION_KEY).endswith(TEST_DONATION_DATA_LOCATION_FROM_CONFIG))

    def test_get_config_value_donor_data_loc_from_config(self, config):
        """Test the Reading of Config File For the Data Donor Path By Calling getDonorDataLocation"""
        assert(self.utilities.getDonorDataLocation().endswith(TEST_DONATION_DATA_LOCATION_FROM_CONFIG))

    def test_get_config_non_exist_key(self, config):
        """Test the Reading of Config File For Requesting a Config Value that Doesn't Exist"""
        assert(self.utilities.getConfigurationValue(NON_EXISTENT_KEY) is None)