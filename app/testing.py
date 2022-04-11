import unittest
import db_module
import logging

logger = logging.getLogger(__name__)

class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.info('Setting up environment for testing: Creating and populating sqlite test database')
        cls.test_db_instance = db_module.DB(':memory:')   # creates an in memory sqlite database

        with open("insert_testing_data.sql") as sql_file:
            sql_as_string = sql_file.read()
            cls.test_db_instance.cur.executescript(sql_as_string)  # executes external script to populate test database. Only one row with id 2

    @classmethod
    def tearDownClass(cls):
        logger.info('Closing sqlite test database connection')
        cls.test_db_instance.con.close()

    def test_insert_duplicated_data(self):
        self.test_db_instance.upsert_one_in_employees({'id': 2, 'employee_name': 'Inventado', 'employee_salary': 170750, 'employee_age': 63, 'profile_image': ''})
        self.test_db_instance.cur.execute("SELECT * FROM EMPLOYEES")
        rows = self.test_db_instance.cur.fetchall()

        expected = (2, 'Inventado',  170750,  63,  '')
        expected_number_of_rows = 1
        expected_types = (int,str, int, int, str)
        with self.subTest():
            self.assertEqual(rows[0], expected)
            self.assertEqual(len(rows), expected_number_of_rows)
            for my_type, expected_type in zip(tuple(rows[0]), expected_types):
                self.assertIsInstance(my_type, expected_type, f'Actual output has not expected data type')

    def test_insert_new_data(self):
        self.test_db_instance.upsert_one_in_employees({'id': 99, 'employee_name': 'Carlos Valiente', 'employee_salary': 170750, 'employee_age': 63, 'profile_image': ''})
        self.test_db_instance.cur.execute("SELECT * FROM EMPLOYEES")
        rows = self.test_db_instance.cur.fetchall()

        expected = (99, 'Carlos Valiente', 170750, 63, '')
        expected_number_of_rows = 2
        with self.subTest():
            self.assertTrue(rows[0] == expected or rows[1] == expected)
            self.assertEqual(rows[1], expected) # todo: assertequal any
            self.assertEqual(len(rows), expected_number_of_rows)


if __name__ == '__main__':
    unittest.main()