PYTHONPATH='.' AWS_PROFILE=mathus_itam luigi --log-level=INFO --module nyc_ccci_etl.luigi_tasks.models_creator ModelsCreator --year=$1 --month=$2 --day=$3