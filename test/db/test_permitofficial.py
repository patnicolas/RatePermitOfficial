import unittest
from src.db.databasemanager import DatabaseManager
from typing import NoReturn, List
from src.db.permitofficial import PermitOfficial
import datetime


class PermitOfficialTest(unittest.TestCase):
    database_manager: DatabaseManager = None

    def test_add(self):
        PermitOfficialTest.__create_database_manager()

        count = PermitOfficialTest.database_manager.query_count(PermitOfficial.id)
        print(f'Table PermitOfficial has {count} entries prior insert')
        entries = PermitOfficialTest.__create_permit_officials()
        for entry in entries:
            PermitOfficialTest.database_manager.add(entry)
        new_count = PermitOfficialTest.database_manager.query_count(PermitOfficial.id)
        print(f'Table PermitOfficial has {new_count} entries after insert')
        self.assertEqual(new_count, count + len(entries))

    @unittest.skip('Ignore')
    def test_query(self):
        PermitOfficialTest.__create_database_manager()
        query_result = PermitOfficialTest.database_manager.query(
            DatabaseManager.q_permit_officials,
            PermitOfficial.id < 10000)

        count = 0
        for record in query_result:
            print(f'{str(record)}')
            count += 1
        actual_count = PermitOfficialTest.database_manager.query_count(PermitOfficial.id)
        self.assertEqual(count, actual_count)


    @staticmethod
    def __create_permit_officials() -> List[PermitOfficial]:

        entry1 = PermitOfficial(
            first_name='Lady',
            last_name='Gaga',
            identifier='9123a',
            title='Building Permit Associate',
            department='Construction Permits',
            city='Mountain View'
        )
        entry2 = PermitOfficial(
            first_name='Simone',
            last_name='Bile',
            identifier='A-91233',
            title='Building Permit Manager',
            department='Construction Permits',
            city='Palo Alto'
        )
        entry3 = PermitOfficial(
            first_name='Noah',
            last_name='Lyle',
            identifier='*',
            title='Building Permit Manager',
            department='Building Permits',
            city='Sunnyvale'
        )
        return [entry1, entry2, entry3]


    @staticmethod
    def __create_database_manager() -> NoReturn:
        if PermitOfficialTest.database_manager is None:
            user_name = 'pat_nicolas'
            password = DatabaseManager.default_password
            db_name = 'test_rating'
            PermitOfficialTest.database_manager = DatabaseManager(user_name, password, db_name)

