import argparse   #pip3 install argparse
DONOR_DATA_LOCATION_KEY = 'donorDataLocation'
CONFIGURATION_PATH_KEY = 'configPath'
DONATION_DATA_LOCATION_KEY = 'donationDataLocation'
CONFIG = '--config'
DONORS = '--donors'
DONATIONS = '--donations'

DEFAULT_CONFIG_PATH = '../config/manageDonors.json'
DEFAULT_DONOR_DATA_LOCATION_PATH = '../data/db.json'
DEFAULT_DONATION_DATA_LOCATION_PATH = '../data/donations/'


#--config /Users/rob/config/msg2json.json --dirs andrew_jones;amanda_hammerschmidt
def parse_command_line():
    """Parse Command Line Arguments and Return a Dictionary Object Derrived from a NameSpace Object"""
    try:

        parser = argparse.ArgumentParser(description='Process command line arguments.')

        parser.add_argument(CONFIG, dest=CONFIGURATION_PATH_KEY, action='store', default=DEFAULT_CONFIG_PATH,
                            help='Represents the path to the configuration file')

        parser.add_argument(DONORS, dest=DONOR_DATA_LOCATION_KEY, action='store', default=DEFAULT_DONOR_DATA_LOCATION_PATH,
                            help='Location of the Donors Database File')

        parser.add_argument(DONATIONS, dest=DONATION_DATA_LOCATION_KEY, action='store', default=DEFAULT_DONATION_DATA_LOCATION_PATH,
                            help='Location of the Donations Database File(s)')

        arguments = parser.parse_args()
        return vars(arguments)
    except Exception as ex:
        raise Exception(f'Parse Command Line {ex}')