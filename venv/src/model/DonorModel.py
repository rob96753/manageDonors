import json
import os
import Model

class DonorModel(Model.Model):

    def __init__(self, logger, utilities):

       super().__init__(logger, utilities)

    def getDonors(self):
        return self._getData()
