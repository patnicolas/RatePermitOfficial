__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2024. All rights reserved."

from cryptography.fernet import Fernet
from typing import AnyStr

"""
      Encrypt and decrypt a key through a Fernet generator. The encrypted key is encoded
      as an array of bytes.
      - Encryption/Decryption of keys
      - Encryption/Decryption of bytes
      - Encryption/Decryption of file content
      AssertError is thrown in case of undefined argument for methods
"""


class KeyEncryption(object):

    key = b'EfKZgsKKTo0fgvMEkMPmVUgoUysbcbPyGIf7J5vHXaQ='
    # key = Fernet.generate_key()
    fernet = Fernet(key)

    def encrypt(self, key: AnyStr) -> bytes:
        assert(len(key) > 0, 'Cannot encrypt undefined key')
        return self.encrypt_bytes(key.encode())

    def decrypt(self, encrypted_key: bytes) -> AnyStr:
        assert (len(encrypted_key) > 0, 'Cannot decrypt undefined key')
        return self.decrypt_bytes(encrypted_key).decode()

    def encrypt_bytes(self, key: bytes) -> bytes:
        assert (len(key) > 0, 'Cannot encrypt undefined bytes')
        return self.fernet.encrypt(key)

    def decrypt_bytes(self, encrypted_key: bytes) -> bytes:
        assert (len(encrypted_key) > 0, 'Cannot decrypt undefined bytes')
        output = self.fernet.decrypt(encrypted_key)
        return output

    def encrypt_file(self, src_file_name: AnyStr, dest_file_name: AnyStr) -> None:
        assert (len(src_file_name) > 0 and len(dest_file_name), 'Cannot encrypted undefined file')

        with open(src_file_name, 'rb') as f:
            clear_content = f.read()
            encrypted_content = self.encrypt_bytes(clear_content)
            with open(dest_file_name, 'wb') as g:
                g.write(encrypted_content)

    def decrypt_file(self, src_file_name: AnyStr, dest_file_name: AnyStr) -> None:
        assert (len(src_file_name) > 0 and len(dest_file_name), 'Cannot decrypted undefined file')

        with open(src_file_name, 'rb') as f:
            clear_content = f.read()
            decrypted_content = self.decrypt_bytes(clear_content)
            with open(dest_file_name, 'wb') as g:
                g.write(decrypted_content)

