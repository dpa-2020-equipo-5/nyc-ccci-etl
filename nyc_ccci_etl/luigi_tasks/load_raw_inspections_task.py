import json
import luigi
from luigi.contrib.postgres import CopyToTable

from nyc_ccci_etl.etl.extraction_procedure import ExtractionProcedure
from nyc_ccci_etl.commons.configuration import get_database_connection_parameters

class LoadRawInspectionsTask(CopyToTable):
    year = luigi.IntParameter()
    month = luigi.IntParameter()
    day = luigi.IntParameter()

    host, database, user, password = get_database_connection_parameters()
    table = "raw.inspections"
    columns = [("inspection", "json")]

    def rows(self):        
        etl_extraction = ExtractionProcedure(self.year,self.month,self.day)

        #Ejecutamos la extracción y se nos regresa una lista de diccionarios (json)
        inspections_json_data = etl_extraction.execute()


        r = [(json.dumps(d).replace("'", "''"),) for d in inspections_json_data]
        for element in r:
            yield element
        
        with open('tmp/inserted_vars', 'w') as f:
            if len(inspections_json_data) > 0:
                f.write(",".join(inspections_json_data[0].keys()))
            else:
                f.write("")
                
        with open('tmp/inserted_records', 'w') as f:
            f.write(str(len(inspections_json_data)))