import json
import os
import CollectionModel

class DonorModel(CollectionModel):

    def __init__(self):
        donorDataLocation = self.utilities.getDonorDataLocation()
        if os.path.exists(donorDataLocation):
            with open(donorDataLocation, "r+") as fp:
                self.donors = json.load(fp)
        else:
            self.logger.log(self.logger.ERROR, f'Donor Data Location doesn''t exist at location: {donorDataLocation} ')
            

    def getDonors(self):
        return self.donors