import unittest
from src.db.databasemanager import DatabaseManager
from typing import Any, NoReturn
from src.db.kpi import KPI


class KPITest(unittest.TestCase):
    database_manager: DatabaseManager = None

    def test_add(self):
        import random
        try:
            KPITest.__create_database_manager()
            count = KPITest.database_manager.query_count(KPI.id)
            print(f'Table KPI has {count} entries prior insert')
            entry = KPI(
                helpfulness=random.randint(1, 5),
                consistency=random.randint(1, 5),
                responsiveness=random.randint(1, 5),
                cost=random.randint(0, 5))
            KPITest.database_manager.add(entry)

            new_count = KPITest.database_manager.query_count(KPI.id)
            print(f'Table KPI has {new_count} entries after insert')
            self.assertEqual(new_count, count + 1)
        except Exception as e:
            self.assertTrue(False, {str(e)})

    @unittest.skip('Ignore')
    def test_delete(self):
        try:
            KPITest.__create_database_manager()
            count = KPITest.database_manager.query_count(KPI.id)

            print(f'Table KPI has {count} entries prior deletion')
            KPITest.database_manager.delete_entry(KPI, count)
            new_count = KPITest.database_manager.query_count(KPI.id)
            print(f'Table KPI has {new_count} entries after deletion')
            self.assertEqual(new_count, count-1)
        except Exception as e:
            self.assertTrue(False, {str(e)})

    @staticmethod
    def __create_database_manager() -> NoReturn:
        if KPITest.database_manager is None:
            user_name = 'pat_nicolas'
            password = DatabaseManager.default_password
            db_name = 'test_rating'
            KPITest.database_manager = DatabaseManager(user_name, password, db_name)

    @staticmethod
    def __get_random_id(field: Any) -> int:
        import random

        max_id = KPITest.database_manager.query_count(field)-1
        return random.randint(1, max_id)


if __name__ == '__main__':
    unittest.main()

