import sqlite3
import logging
import sys

logger = logging.getLogger(__name__)


class DB:
    def __init__(self,
                 path=None):

        self.path = path
        self.con = self.db_connect()
        self.cur = self.con.cursor()

    def db_connect(self):
        logger.info("Connecting DB '{}'".format(self.path))
        con = sqlite3.connect(self.path)

        return con

    def create_table_if_not_exists(self, tb_name):
        # Create table
        try:
            self.cur.execute('''CREATE TABLE IF NOT EXISTS EMPLOYEES
                    (id INT PRIMARY KEY,
                    employee_name TEXT,
                    employee_salary INT,
                    employee_age INT,
                    profile_image TEXT)
                    '''
                             )
            self.con.commit()

            logger.info("Creating Employees table")

        except sqlite3.Error as e:
            logger.error(e)
            sys.exit(1)

    def upsert_one_in_employees(self, content:dict):
        # Create table
        try:
            self.cur.execute('''
                INSERT INTO EMPLOYEES (id, employee_name, employee_salary, employee_age, profile_image)
                VALUES (:id, :employee_name, :employee_salary, :employee_age, :profile_image)

                ON CONFLICT (id) DO UPDATE
                SET
                    employee_name = excluded.employee_name,
                    employee_salary = excluded.employee_salary,
                    employee_age = excluded.employee_age,
                    profile_image = excluded.profile_image;
            ''', content)

            self.con.commit()

            logger.info("This data was inserted or updated OK:\n {}".format(self.cur.execute('select * from EMPLOYEES').fetchall()[-1]))

        except sqlite3.Error as e:
            logger.error(e)
            sys.exit(1)