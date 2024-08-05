import unittest
from src.db.databasemanager import DatabaseManager
from src.db.user import User
from typing import NoReturn
from src.util.keyencryption import KeyEncryption
import datetime

class UserTest(unittest.TestCase):
    database_manager: DatabaseManager = None

    @unittest.skip('Ignore')
    def test_add_super_admin(self):
        key_encryption = KeyEncryption()
        UserTest.__create_database_manager()
        test_key = "Yge_1908"

        user = User(
            first_name='Patrick',
            last_name='Nicolas',
            created = datetime.datetime.now(),
            role_id=2,
            is_anonymous=0,
            credential=key_encryption.encrypt(test_key))

        UserTest.database_manager.add(user)
        count = UserTest.database_manager.query_count(User.id)
        self.assertEqual(count, 1)

    def test_query_all(self):
        key_encryption = KeyEncryption()
        UserTest.__create_database_manager()
        users = UserTest.database_manager.query(DatabaseManager.q_users, User.id < 100)
        for user in users:
            print(f'User: {user.first_name} {user.last_name} {user.credential} Pwd: {key_encryption.decrypt(user.credential)}')



    @staticmethod
    def __create_database_manager() -> NoReturn:
        if UserTest.database_manager is None:
            user_name = 'pat_nicolas'
            password = DatabaseManager.default_password
            db_name = 'test_rating'
            UserTest.database_manager = DatabaseManager(user_name, password, db_name)