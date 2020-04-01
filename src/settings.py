import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY') or 'SuperSecretKeys'
PROMQL_HOSTNAME = os.environ.get('PROMQL_HOSTNAME') or '10.244.0.64'
PROMQL_USERNAME = os.environ.get('PROMQL_USERNAME') or 'postgres'
PROMQL_DB_NAME = os.environ.get('PROMQL_DB_NAME') or 'postgres'
PROMQLDB_PASSWORD = os.environ.get('PROMQLDB_PASSWORD') or 'mypass'
PROMQL_PORT = int(os.environ.get('PROMQL_PORT','5432'))

ML_LR_MODEL = os.environ.get('ML_LR_MODEL') or basedir+'/../models/linear_regression.model'
DEBUG = True

if not PROMQL_HOSTNAME:
    logger.error("No MySQL Hostname specified! Exiting!")
    sys.exit()
if not PROMQL_USERNAME:
    logger.error("No MYSQL_USERNAME specified! Exiting!")
    sys.exit()
if not PROMQL_DB_NAME:
    logger.error("No MYSQL_DB_NAME specified! Exiting!")
    sys.exit()
if not PROMQLDB_PASSWORD:
    logger.error("No MYSQLDB_PASSWORD specified! Exiting!")
    sys.exit()
