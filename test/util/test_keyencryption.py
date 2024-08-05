import unittest
from src.util.keyencryption import KeyEncryption
from src.db.databasemanager import DatabaseManager


class KeyEncryptionTest(unittest.TestCase):

    def test_encrypt_decrypt_key(self):
        key_encryption = KeyEncryption()

        test_key = "Yge_1908"
        encrypted = key_encryption.encrypt(test_key)
        print(f'\nEncrypted: {encrypted}')
        decrypted_key = key_encryption.decrypt(encrypted)
        print(f'\nDecrypted {decrypted_key}')
        self.assertEqual(test_key, decrypted_key)

    def test_decrypt_key(self):
        key_encryption = KeyEncryption()
        k = DatabaseManager.default_password
        decrypted_key = key_encryption.decrypt(k)
        self.assertEqual(decrypted_key,  "Yge_1908")
