import json
import os

class Model:
    dataLoaded = False
    def __init__(self, logger, utilities):
        self._logger = logger
        self._utilities = utilities
        self._data = None

    def load(self, path):
        if os.path.exists(path):
            with open(path, "r+") as fp:
                self._data = json.load(fp)
                self.dataLoaded = False
        else:
            self.logger.log(self.logger.ERROR, f'Data Location doesn''t exist at location: {donorDataLocation} ')

    def _getData(self):
        return self._data



