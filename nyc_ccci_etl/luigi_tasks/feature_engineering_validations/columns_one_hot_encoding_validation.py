import luigi
from luigi.contrib.postgres import CopyToTable
from nyc_ccci_etl.tests.test_feature_engineering import TestFeatureEngineering
from nyc_ccci_etl.utils.print_with_format import print_test_failed, print_test_passed
import sys
from nyc_ccci_etl.commons.configuration import get_database_connection_parameters
class ColumnsOneHotEncodingValidation(CopyToTable):
    year = luigi.IntParameter()
    month = luigi.IntParameter()
    day = luigi.IntParameter()
    
    
    host, database, user, password = get_database_connection_parameters()
    table = "testing.feature_engineering"
    schema = "testing"

    columns = [
        ('test', 'varchar'),
        ('ran_at', 'timestamp'),
        ('params', 'varchar'),
        ('status', 'varchar'),
        ('note', 'varchar')
    ]

    def run(self):
        test_feature_engineering = TestFeatureEngineering()
        self.test_result = test_feature_engineering.test_columns_one_hot_encoding(self.year, self.month, self.day)
        if self.test_result['status'] == 'failed':
            print_test_failed(self.test_result['test'], self.test_result['note'])
        else:
            print_test_passed(self.test_result['test'])
        super().run()
        if self.test_result['status'] == 'failed':
            sys.exit()
    
    def rows(self):
        params = "year={} month={} day={}".format(self.year, self.month, self.day)
        yield (self.test_result['test'], self.test_result['ran_at'], params, self.test_result['status'], self.test_result['note'])
        