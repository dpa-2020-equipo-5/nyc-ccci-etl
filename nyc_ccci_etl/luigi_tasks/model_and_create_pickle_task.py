import luigi
import luigi.contrib.s3
from nyc_ccci_etl.luigi_tasks.load_transformed_inspections_task import LoadTransformedInspectionsTask
import pickle
class ModelAndCreatePickleTask(luigi.Task):
    year = luigi.IntParameter()
    month = luigi.IntParameter()
    day = luigi.IntParameter()

    def requires(self):
        return LoadTransformedInspectionsTask(self.year, self.month, self.day)

    def output(self):
        output_path = "s3://nyc-ccci/random_forest_{}_{}_{}.pckl".\
        format(
            str(self.year),
            str(self.month),
            str(self.day),
        )
        return luigi.contrib.s3.S3Target(path=output_path, format=luigi.format.Nop)

    def run(self):
        #Aquí va todo el código del modelo
        words = ['apple', 'banana', 'grapefruit']

        with self.output().open('w') as output_file:
            pickle.dump(words, output_file)