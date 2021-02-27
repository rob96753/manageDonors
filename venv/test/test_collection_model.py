import pytest
import sys
from datetime import datetime
import uuid

sys.path.insert(1, '../src')
import Utilities
import CommandLine

sys.path.append('../src/model')

import DonorModel
import Model

TEST_DB_FILE_PATH = '../data/db.json'
TEST_CONFIG_PATH = '../config/config.json'
SYS_ARGV = 'sys.argv'

INDEX_NAME = "last_donation"
INDEX_KEY_NAME = "last_donation"
INDEX_UNKNOWN_NAME = "foo"
FILTERED_INDEX_NAME = "filtered_index"
COMPOSITE_INDEX_NAME = 'golden_demographics'
COMPOSITE_INDEX_NAME_FILTERED = 'golden_demographics_filtered'

cli_values = ["pytest", CommandLine.CONFIG, TEST_CONFIG_PATH,
              CommandLine.DONORS, TEST_DB_FILE_PATH]

class TestClass:

    @pytest.fixture(autouse=False)
    def setup(self, monkeypatch):
        """Set the collection of command line arguments"""
        utilities = Utilities.Utilities()
        monkeypatch.setattr(SYS_ARGV, cli_values)
        utilities.parseCommandLine()
        return(utilities)

    @pytest.fixture(autouse=False)
    def donorLocation(self, setup):
        donorDataLocation = setup.getDonorDataLocation()
        return(donorDataLocation)

    @pytest.fixture(autouse=False)
    def loadData(self, monkeypatch, setup, donorLocation):
        model = DonorModel.DonorModel(None, setup)
        model.load(donorLocation)
        return(model)

    @pytest.fixture(autouse=False)
    def addMockRecord(self, monkeypatch, loadData):
        """Create a Mock Record With a Date of Today for last_donation"""
        """This will be used for testing the filter function of create index"""
        mockRecord = {
            "36e5ad04-9067-42bd-8ad2-7923eb8102fd": {
                "first_name": "JUDIE",
                "middle_name": "J",
                "surname": "MORROW",
                "ssn": "921-02-1700",
                "issn": "921021700",
                "donor_id": "MORRJ1998010115006",
                "blood_type": "O POSITIVE",
                "nationality": "United States of America",
                "home_donation_site": "WAIANAE",
                "ltowb": "n",
                "gender": "F",
                "race": "CAUCASIAN",
                "dob": "01 JAN 1988",
                "last_donation": f"{datetime.strftime(datetime.now(), '%d %b %Y')}",
                "donor_original_index": 610
            }
        }
        loadData.append(mockRecord)
        return(loadData)


    def test_model_load(self, loadData):
        """Test Loading the Donor Content and Verify It's a Dictionary Using getDonors"""
        model = loadData
        assert(isinstance(model.getDonors(), dict))

    def test_model_get_ids(self, loadData):
        """Test the getIds Method to Verify it Returns All Ids from Data"""
        ids = loadData.getIds()
        assert(len(ids) >= 610)

    def test_get_index_exception(self, loadData):
        """Test the Get Index for Index that Doesn't Exist"""
        with pytest.raises(Model.ModelIndexError):
            loadData.getIndex(INDEX_UNKNOWN_NAME)

    def test_model_create_index(self, loadData):
        """Test the Indexes Should Map Keys to Ids with No Filter"""
        count = loadData.createIndex(INDEX_NAME, INDEX_KEY_NAME)
        assert(loadData.getIndex(INDEX_NAME))
        assert(count + 1 == len(list(loadData.getIds())))

    def test_model_create_index_filtered(self, addMockRecord):
        """Test the Indexes Should Map Keys to Ids with No Filter"""
        filter = lambda x: (datetime.now() - datetime.strptime(x, '%d %b %Y')).days < 2
        count = addMockRecord.createIndex(FILTERED_INDEX_NAME, INDEX_KEY_NAME, filter)
        assert(len(list(addMockRecord.getIndex(FILTERED_INDEX_NAME).keys())) == 1)

    def test_model_create_index_exception(self, loadData):
        """Test the Indexes Should Map Keys to Ids"""
        with pytest.raises(Model.ModelIndexError):
            loadData.createIndex(INDEX_NAME, INDEX_KEY_NAME)

    def test_get_items_filtered(self, loadData):
        """Test Get Items from Model Using Filter"""
        limit = 10
        filter = lambda x: ((datetime.now() - datetime.strptime(x['last_donation'], '%d %b %Y')).days > 56) and (x['gender'].upper() == 'F') and (x['blood_type'].upper().startswith('O POS'))
        results = loadData.getItems(filter, limit)
        assert(len(results) == limit)


    def test_get_items_filtered_from_index(self, loadData):
        """Test Get Items Index from Model Using Filter"""
        limit = 300
        filter = lambda x: (datetime.now() - datetime.strptime(x, '%d %b %Y')).days > 56
        results = loadData.getItemsIndex(filter, INDEX_NAME, limit)
        assert(len(results) == limit)

    def test_create_index_non_callable_filter(self, loadData):
        """Test Passing Filter That's Not Callable"""
        with pytest.raises(Model.ModelIndexError):
            loadData.createIndex(INDEX_NAME, INDEX_KEY_NAME, "not callable")

    def test_get_items_index_non_callable_filter(self, loadData):
        """Test Passing Filter That's Not Callable to Get Items Index"""
        limit = 10
        filter = "not callable "
        with pytest.raises(Model.ModelIndexError):
            results = loadData.getItemsIndex(filter, INDEX_NAME, limit)

    def test_get_items_non_callable_filter(self, loadData):
        """Test Passing Filter That's Not Callable to Get Items"""
        limit = 10
        filter = "not callable "
        with pytest.raises(Model.ModelIndexError):
            results = loadData.getItems(filter, limit)

    def test_create_index_composite_key(self, loadData):
        """Create an Index of Domgraphics to Record Id for Faster Searching"""
        compositeKey = lambda x: f"{x['surname']}|{x['issn']}|{x['dob']}"
        count = loadData.createIndexCompositeKey(COMPOSITE_INDEX_NAME, compositeKey, None)
        assert(count > 0)

    def test_create_index_composite_key_name_repeat(self, loadData):
        """Index Name is Repeated and will Throw an Exception"""
        compositeKey = lambda x: f"{x['surname']}|{x['issn']}|{x['dob']}"
        with pytest.raises(Model.ModelIndexError):
            count = loadData.createIndexCompositeKey(COMPOSITE_INDEX_NAME, compositeKey, None)

    def test_create_index_composite_key_filter_not_callable(self, loadData):
        """Index Name is Repeated and will Throw an Exception"""
        compositeKey = lambda x: f"{x['surname']}|{x['issn']}|{x['dob']}"
        filter = 'test'
        with pytest.raises(Model.ModelIndexError):
            count = loadData.createIndexCompositeKey(COMPOSITE_INDEX_NAME, compositeKey, None)


    def test_create_index_composite_key_filter(self, loadData):
        """Create a Composite Key Index Represented as a Filter"""
        compositeKey = lambda x: f"{x['surname']}|{x['issn']}|{x['dob']}"
        filter = lambda x: True if x['blood_type'].upper().startswith('B') else False
        count = loadData.createIndexCompositeKey(COMPOSITE_INDEX_NAME_FILTERED, compositeKey, filter)
        assert(count > 0)

    def test_retreive_patient_from_index(self, loadData):
        """Search for a Donor based on the Demographics for the Donor"""
        """GEIER|945200815|28 Oct 2020"""
        surname = 'GEIER'
        ssn = '945200815'
        dob = "12 JUL 1995"

        compositeKey = lambda x: x == f"{surname}|{ssn}|{dob}".upper()
        items = loadData.getItemsIndex(compositeKey, COMPOSITE_INDEX_NAME_FILTERED, 10)

        assert(len(items) == 1)






