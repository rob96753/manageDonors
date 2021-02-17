import pytest
import sys

sys.path.insert(1, '../src')
import Utilities
import CommandLine

sys.path.append('../src/model')

import DonorModel

TEST_DB_FILE_PATH = '../data/db.json'
TEST_CONFIG_PATH = '../config/config.json'
SYS_ARGV = 'sys.argv'

cli_values = ["pytest", CommandLine.CONFIG, TEST_CONFIG_PATH,
              CommandLine.DONORS, TEST_DB_FILE_PATH]

class TestClass:
    utilities = None

    @pytest.fixture(autouse=False)
    def setup(self, monkeypatch):
        """Set the collection of command line arguments"""
        self.utilities = Utilities.Utilities()
        monkeypatch.setattr(SYS_ARGV, cli_values)
        self.utilities.parseCommandLine()
        self.donorDataLocation = self.utilities.getDonorDataLocation()

    def test_model_load(self, setup):
        model = DonorModel.DonorModel(None, self.utilities)
        print(self.utilities.getDonorDataLocation())
        model.load(self.utilities.getDonorDataLocation())
        assert(isinstance(model.getDonors(), dict))

