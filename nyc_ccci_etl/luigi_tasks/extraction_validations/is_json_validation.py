import luigi
from luigi.contrib.postgres import CopyToTable
from nyc_ccci_etl.tests.test_inspections_extraction import TestInspectionsExtractor
from nyc_ccci_etl.utils.print_with_format import print_test_failed, print_test_passed
import sys
from nyc_ccci_etl.commons.configuration import get_database_connection_parameters
class IsJsonValidation(CopyToTable):
    year = luigi.IntParameter()
    month = luigi.IntParameter()
    day = luigi.IntParameter()
    
    
    host, database, user, password = get_database_connection_parameters()
    table = "testing.extractions"
    schema = "testing"

    columns = [
        ('ran_at', 'timestamp'),
        ('test', 'varchar'),
        ('params', 'varchar'),
        ('status', 'varchar')
    ]
    
    def run(self):
        test_inspections_extractor = TestInspectionsExtractor()
        self.test_result = test_inspections_extractor.test_extraction_date_is_valid(self.year, self.month, self.day)
        if self.test_result['status'] == 'failed':
            print_test_failed(self.test_result['test'], self.test_result['note'])
        else:
            print_test_passed(self.test_result['test'])
        super().run()
        if self.test_result['status'] == 'failed':
            sys.exit()
    
    def rows(self):
        params = "year={} month={} day={}".format(self.year, self.month, self.day)
        yield (self.test_result['ran_at'], self.test_result['test'], params, self.test_result['status'])
