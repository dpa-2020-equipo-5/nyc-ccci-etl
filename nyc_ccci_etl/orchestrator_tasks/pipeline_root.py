import luigi
from luigi.contrib.postgres import CopyToTable

from nyc_ccci_etl.orchestrator_tasks.fit_random_forest_and_create_pickle import FitRandomForestAndCreatePickle
from nyc_ccci_etl.orchestrator_tasks.create_predictions import CreatePredictions
from nyc_ccci_etl.commons.configuration import get_database_connection_parameters
from datetime import datetime

class PipelineRoot(CopyToTable):
    year = luigi.IntParameter()
    month = luigi.IntParameter()
    day = luigi.IntParameter()
    pipeline_type = luigi.Parameter()

    def requires(self):
        if str(self.pipeline_type) == 'train':
            return  FitRandomForestAndCreatePickle(self.year, self.month, self.day)
        elif str(self.pipeline_type) == 'predict':
            return CreatePredictions(self.year, self.month, self.day)

    columns = [
        ('update_id', 'text'),
        ('target_table', 'text'),
        ('inserted', 'timestamp'),
    ]
    host, database, user, password = get_database_connection_parameters()
    table = "table_updates"

    def rows(self):
        update_id = "{}_{}{}{}".format(str(self.pipeline_type),str(self.year), str(self.month), str(self.day))
        yield (update_id, "table_updates" ,datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    