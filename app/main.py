import requests
import sys
from db_module import DB
from resquest_retries import requests_retry_session
import logging
import logging.config
from Utils.setup_logging import setup_logging
import os

os.makedirs("log", exist_ok=True)
setup_logging("Utils/logging.yaml")
logger = logging.getLogger(__name__)

if len(sys.argv) < 2:
    print('You need to specify employee ID and db path, for example: python main 1 pythonsqlite.db')
    sys.exit()

employee_id = sys.argv[1]
db_path = sys.argv[2]

api_url = "https://dummy.restapiexample.com/public/api/v1/employee/" + employee_id
headers = {"Accept": "application/json",
           "User-agent": "Mozilla/5.0",
           "Accept-Charset": "utf-8",
           "Accept-Encoding": "gzip, deflate",
           "Accept-Language": "en-US"}

try:
    s = requests_retry_session()
    logger.info("Requesting API... '{}'".format(api_url))
    response = s.get(api_url, headers=headers)
    response.raise_for_status()
except requests.exceptions.HTTPError as err:
    logger.error("Error raised while trying to request api: {}".format(err))
    sys.exit(1)

db_instance = DB(db_path)
db_instance.create_table_if_not_exists(tb_name='EMPLOYEES')
db_instance.upsert_one_in_employees(content=response.json()['data'])

logger.info("Execution was successful. Showing data from employees table:\n {}".format(db_instance.cur.execute('select * from EMPLOYEES').fetchall()))

db_instance.cur.close()
