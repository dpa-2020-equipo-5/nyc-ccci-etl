from sodapy import Socrata
from etl_dpa.commons.configuration import get_app_token

class Extraction():
    def __init__(self, year, month, day):
        self.date_param = "{}-{}-{}T00:00:00.000".format(year, month,day)
        self.socrataClient = Socrata("data.cityofnewyork.us", get_app_token()) 

    def execute(self):
        return self.socrataClient.get("dsg6-ifza", inspectiondate=self.date_param)