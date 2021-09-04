import json
import unittest

from app.libs.cipher import Cipher


class CipherTests(unittest.TestCase):
    def test_aes_1(self):
        key = b"Svko-azkv@kqe@ogqko@qoASOdKGojqe"
        iv = b"Spoakgoppagkpgpc"

        plaintext = "Some test text"
        ciphertext_hex = Cipher.aes_encrypt_to_hex(
            plaintext.encode('utf-8'), iv, key)
        self.assertEqual(ciphertext_hex, "1bb8cab5126c695a48d8fc6d2374d311")
        decrypted = Cipher.aes_decrypt_to_plain(
            bytes.fromhex(ciphertext_hex), iv, key)
        self.assertEqual(decrypted, plaintext)

    def test_aes_2(self):
        key = b"AFAfkOFPAKFoaigjgoiajvaomgo$iega"
        iv = b"aZ{@;v@pKt0#=bjeSODjkfoig"

        ciphertext_hex = \
            "9b8f35ad7599eecc857582bddbe24367f90d6f00d08b52dcf8f3e4d2e73cac66"
        decrypted = Cipher.aes_decrypt_to_plain(
            bytes.fromhex(ciphertext_hex), iv, key)
        value = json.loads(decrypted)
        self.assertEqual(value["test"], 123456789)
        ciphertext_hex_actual = Cipher.aes_encrypt_to_hex(
            decrypted.encode('utf-8'), iv, key)
        self.assertEqual(ciphertext_hex_actual, ciphertext_hex)
