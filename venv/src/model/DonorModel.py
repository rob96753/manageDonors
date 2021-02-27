import json
import os
from datetime import datetime
import Model

class DonorModel(Model.Model):

    def __init__(self, logger, utilities):
       super().__init__(logger, utilities)

    def getDonors(self):
        return self._getData()

    def getEligibleDonors(self, limit, daysSinceLastDonation):
        filter = lambda x: ((datetime.now() - datetime.strptime(x['last_donation'], '%d %b %Y')).days > daysSinceLastDonation)
        return self.getItems(filter, limit)

    def getDonorById(self, id):
        return self._data[id]

    def getDonorByDemographics(self, surname, ssn, dob):
        """Use a Composite Key Index to Search for a Donor by Identifiers"""
        compositeKey = lambda x: x == f"{surname}|{ssn}|{dob}"
        items = self.getItemsIndex(compositeKey, 'golden_demographics', 10)



