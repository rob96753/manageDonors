import json
import os

class ModelIndexError(Exception):
    """Raised When Model Index Function Violates Rule"""
    pass

class Model:
    """"""
    dataLoaded = False
    _indexes = {}
    modelName = 'default'
    def __init__(self, logger, utilities, modelName = 'Default'):
        self._logger = logger
        self._utilities = utilities
        self._data = None
        self.modelName = modelName

    def load(self, path):
        """Reads the contents of a JASON file into a Dictionary Object."""
        if os.path.exists(path):
            with open(path, "r+") as fp:
                self._data = json.load(fp)
                self.dataLoaded = False
        else:
            self.logger.log(self.logger.ERROR, f'Data Location doesn''t exist at location: {donorDataLocation} ')

    def append(self, record):
        """"""
        recordIds = list(record.keys())
        notAppended = 0
        recordCount = len(recordIds)
        for counter, recordId in enumerate(recordIds):
            if not recordId in self._data:
                self._data[recordId] = record[recordId]
            else:
                notAppended += 1
        return f'{recordCount - notAppended} of {recordCount} Appended to {self.modelName}'

    def upsert(self, record):
        """"""
        recordIds = record.keys()
        for recordId in recordIds:
            self._data[recordId] = record[recordId]


    def _getData(self):
        """"""
        return self._data

    def getIds(self):
        """"""
        return self._data.keys()

    def indexExists(self, indexName):
        """checks that the index exists"""
        return indexName in self._indexes


    def createIndexCompositeKey(self, indexName, compositeKey, filter=None):
        if self.indexExists(indexName):
            raise ModelIndexError(f"Create Index Composite Key: {indexName} Already Exists, Use rebuildIndex to Update Index")

        if not ((filter is None) or callable(filter)):
            raise ModelIndexError(f"Create Index Composite Key: {filter} Must be 'None' or a Callable Function")

        if not callable(compositeKey):
            raise ModelIndexError(f"Create Index Composite Key: {compositeKey} Must be a Callable Function")

        self._indexes[indexName] = {}
        for counter, key in enumerate(self.getIds()):
            item = self._data[key]
            if (filter is None) or (filter(item)):
                self._indexes[indexName][compositeKey(item)] = [key]

        return len(self._indexes[indexName])


    def createIndex(self, indexName, keyName, filter=None):
        """Create Index that Doesn't Already Exist (if it does, raise exception) and Allpied Filter"""
        counter = 0
        if self.indexExists(indexName):
            raise ModelIndexError(f"Create Index: {indexName} Already Exists, Use rebuildIndex to Update Index")

        if not ((filter is None) or callable(filter)):
            raise ModelIndexError(f"Create Index: {filter} Must be 'None' or a Callable Function")
        self._indexes[indexName] = {}
        for counter, key in enumerate(self.getIds()):
            item = self._data[key]
            if not keyName in item:
                raise ModelIndexError(f"Create Index: {keyName} Not In Data Set")


            indexKey = item[keyName]
            if not filter or (filter(indexKey)):
                if indexKey in self._indexes[indexName]:
                    self._indexes[indexName][indexKey].append(key)
                else:
                    self._indexes[indexName][indexKey] = []
                    self._indexes[indexName][indexKey].append(key)
        return counter


    def getIndex(self, indexName):
        """Return Named Index or Raise Exception"""
        if not self.indexExists(indexName):
            raise ModelIndexError(f"Get Index: {indexName} Doesn't Exist")
        return self._indexes[indexName]


    def getItemsIndex(self, filter, indexName, limit):
        """Search an Index for Matching Values, Up to Count"""
        if not callable(filter):
            raise ModelIndexError(f"Get Items Index: {filter} Must be a Callable Function")

        items = []
        if not self.indexExists(indexName):
            raise ModelIndexError(f"Get Items Index: {indexName} Doesn't Exist")
        """
        The list of keys could be collected with list comprehension, but it 
        would process all the keys, regardless of the limit; then the limit
        would have to be applied later. This will actually stop the processing 
        when the limit is reached.
        """

        for key in list(self._indexes[indexName].keys()):
            if filter(key.upper()):
                """only grab enough ids to fullfill the request for number of
                    item requested, then populate the items list with records
                    of donors"""
                ids = self._indexes[indexName][key][:limit - len(items)]
                for id in ids:
                    item = self._data[id]
                    item['_id'] = id
                    items.append(item)
            if len(items) >= limit:
                break
        return items

    def getItems(self, filter, limit):
        """Search an data for Matching Values, Up to Count"""

        if not callable(filter):
            raise ModelIndexError(f"Get Items Index: {filter} Must be a Callable Function")

        items = []
        for key in list(self._data.keys()):
            if len(items) >= limit:
                break
            item = self._data[key]
            item['_id'] = key
            if filter(item):
                items.append(item)
        return items







