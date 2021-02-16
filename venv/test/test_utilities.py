import pytest
import sys

sys.path.insert(1, '../src')
import Utilities
import CommandLine

TEST_DB_FILE_PATH = '../data/db-test.json'
TEST_CONFIG_PATH = '../config/config-test.json'
NON_EXISTENT_KEY = 'NOKEY'
SYS_ARGV = 'sys.argv'

cli_values = ["pytest", f'{CommandLine.CONFIG}', TEST_CONFIG_PATH,
              f'{CommandLine.DONORS}', TEST_DB_FILE_PATH]

class TestClass:
    utilities = None

    @pytest.fixture()
    def setup(self, monkeypatch):
        self.utilities = Utilities.Utilities()
        """Set the collection of command line arguments"""
        monkeypatch.setattr(SYS_ARGV, cli_values)
        self.utilities.parseCommandLine()

    @pytest.fixture()
    def reset(self, monkeypatch):
        """Set the collection of command line arguments"""
        monkeypatch.setattr(SYS_ARGV, ["pytest"])
git a        self.utilities = None
        self.utilities = Utilities.Utilities()
        self.utilities.parseCommandLine()


    def test_donor_get_donor_location(self, setup):
        assert (self.utilities.getDonorDataLocation().endswith(TEST_DB_FILE_PATH))

    def test_get_config_path(self, setup):
        assert (self.utilities.getConfigFilePath().endswith(TEST_CONFIG_PATH))

    def test_get_command_line_argument_donor_db(self, setup):
        assert (self.utilities.getCommandLineArgument(CommandLine.DONOR_DATA_LOCATION_KEY).endswith(TEST_DB_FILE_PATH))

    def test_get_command_line_argument_undefined(self, reset):
        cliArguement = self.utilities.getCommandLineArgument(NON_EXISTENT_KEY)
        assert (cliArguement is None)
