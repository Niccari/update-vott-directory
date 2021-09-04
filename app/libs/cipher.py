from Crypto.Cipher import AES


class Cipher:
    @staticmethod
    def _aes(key: bytes, iv: bytes):
        return AES.new(key, AES.MODE_CBC, iv)

    @staticmethod
    def _pad(plaintext: bytes) -> bytes:
        padding_length = 16 - len(plaintext) % 16
        return plaintext + chr(padding_length).encode('utf-8') * padding_length

    @staticmethod
    def _unpad(plaintext: bytes) -> bytes:
        return plaintext[:-plaintext[-1]]

    @staticmethod
    def aes_encrypt_to_hex(plaintext: bytes, iv: bytes, key: bytes) -> str:
        return Cipher._aes(key, iv[:16]) \
            .encrypt(Cipher._pad(plaintext)).hex()

    @staticmethod
    def aes_decrypt_to_plain(ciphertext: bytes, iv: bytes, key: bytes) -> str:
        return Cipher._unpad(Cipher._aes(key, iv[:16]).decrypt(ciphertext)) \
            .decode()
