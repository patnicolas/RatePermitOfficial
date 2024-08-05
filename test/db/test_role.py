import unittest
from src.db.databasemanager import DatabaseManager
from src.db.role import Role
from typing import NoReturn

class RoleTest(unittest.TestCase):
    database_manager: DatabaseManager = None

    @unittest.skip('Ignored')
    def test_role_add(self):
        RoleTest.__create_database_manager()
        _role = Role(role='admin', is_active=1)
        RoleTest.database_manager.add(_role)
        _role = Role(role='super_admin', is_active=1)
        RoleTest.database_manager.add(_role)
        _role = Role(role='user', is_active=1)
        RoleTest.database_manager.add(_role)
        count = RoleTest.database_manager.query_count(Role.id)
        self.assertEqual(count, 3)

    def test_role_query(self):
        RoleTest.__create_database_manager()

        count = RoleTest.database_manager.query_count(Role.id)
        self.assertEqual(count, 3)
        results = RoleTest.database_manager.query(DatabaseManager.q_roles, Role.id < 10)
        for result in results:
            print(f'\nRole: {result.role}, Is active: {result.is_active}')

    """ -----------------  Supporting helper methods ----------------- """

    @staticmethod
    def __create_database_manager() -> NoReturn:
        if RoleTest.database_manager is None:
            user_name = 'pat_nicolas'
            password = DatabaseManager.default_password
            db_name = 'test_rating'
            RoleTest.database_manager = DatabaseManager(user_name, password, db_name)

