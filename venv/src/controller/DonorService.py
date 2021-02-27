from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import json
import os
import sys


sys.path.append('..')
import Utilities
import Logging

sys.path.append('../model')
import DonorModel

CONFIG_PATH = '../../config/manageDonors.json'
DEFAULT_PATH = '/usr/src/app/'

logging_config = dict(
    version = 1,
    formatters = {
         "default": {"format": "%(levelname)s: %(asctime)s - %(message)s",
                          "datefmt": "%Y-%m-%d %H:%M:%S"}
        },
    handlers = {
        'console': {"class": 'logging.StreamHandler',
                "level": Logging.DEBUG,
                "formatter": "default",
                "stream": "ext://sys.stdout"},
         'file': {
                "class": 'logging.handlers.RotatingFileHandler',
                "level": Logging.DEBUG,
                "formatter": "default",
                "filename": "../manage_donors.log",
                "maxBytes": 1024,
                "backupCount": 3
              }
        },
    loggers = {
        'manage_donors' : {
            'handlers': ['console', 'file'],
            'level': Logging.DEBUG
        }
    },
    root = {
        'handlers': ['console', 'file'],
        'level': Logging.DEBUG
        }
)

app = (Flask(__name__))
api = Api(app)

utilities = Utilities.Utilities()
utilities.parseConfiguration(CONFIG_PATH)
logger = None
def setupLogging():
    log = Logging.Logger('manage_donors', logging_config)
    logger = log.getLogger()
    logger.info("Logging Initialized")

donors = DonorModel.DonorModel(logger, utilities)
donors.load(utilities.getDonorDataLocation())

@app.route('/Donors')
def get():
    return donors.getDonors()

@app.route('/Donors/eligible/<int:limit>/<int:daysSinceLastDonation>', methods=['GET'])
def eligibleDonors(limit, daysSinceLastDonation):
    return dict(donors=donors.getEligibleDonors(limit, daysSinceLastDonation))

@app.route('/Donors/get_donor/<string:donorId>')
def get_donor(donorId):
    return donors.getDonorById(donorId)

@app.route('/Donors/add/', methods=['Push'])
def addDonor(limit, daysSinceLastDonation):
    return dict(donors=donors.getEligibleDonors(limit, daysSinceLastDonation))

#api.add_resource(DonorsService, '/Donors', methods=['GET'])



if __name__ == '__main__':
    setupLogging()
    app.run(host='0.0.0.0', port=8081, debug=True)