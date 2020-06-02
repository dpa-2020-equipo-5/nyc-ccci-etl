import json
import luigi
from luigi.contrib.postgres import CopyToTable

from nyc_ccci_etl.commons.configuration import get_database_connection_parameters
from nyc_ccci_etl.orchestrator_tasks.fit_random_forest_and_create_pickle import FitRandomForestAndCreatePickle

from nyc_ccci_etl.ccci_aequitas.fairness_metrics import FairnessMetrics


class LoadAequitasFairness(CopyToTable):
    year = luigi.IntParameter()
    month = luigi.IntParameter()
    day = luigi.IntParameter()
    def requires(self):
        return FitRandomForestAndCreatePickle(self.year, self.month, self.day)
        
    host, database, user, password = get_database_connection_parameters()
    table = "aequitas.fairness"
    schema = "aequitas"
    def run(self):
        f = FairnessMetrics(self.year, self.month, self.day)
        self._rows, self.columns = f.execeute()
        super().run()
    

    def rows(self):
        for element in self._rows:
            yield element