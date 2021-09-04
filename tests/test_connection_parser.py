import unittest

from app.connection_parser import ConnectionParser


class ParserTests(unittest.TestCase):
    def test_decrypt_connection_local1(self):
        key = "VqVIBjp5p6ZRnqzKYB1Oql0dvrK0TkCtNXPiqjace2A="
        encrypted = "eyJjaXBoZXJ0ZXh0IjoiOWRmNDZhNGMwNDM5ODIxZDg3MWUyMjQwMzQ3NTFjNDc0OTM5MjRjZGUwZTkxNDRlOTQ4ZDBiYjMyY2E0ZmU0N2U2OTQ1NjVjZmNhNDM4ODlkZjNkMjYwOWViNGY0MDczMzNmNDBjNjQ3ZjFiZGRiMWExOWQzZmY5YTYyNDc4NzMiLCJpdiI6ImM2NDVlOTA5YzJkYmIwZDViZDA0MmE4NmM0YWVjMDU2YmI1NTEzN2M1NDA2YWQyYyJ9"  # noqa: E501

        decoded_json = ConnectionParser.decrypt_connection(key, encrypted)
        self.assertEqual(
            decoded_json,
            {"folderPath": "/Users/niccari/Downloads/test/video"})

    def test_decrypt_connection_local2(self):
        key = "VqVIBjp5p6ZRnqzKYB1Oql0dvrK0TkCtNXPiqjace2A="
        encrypted = "eyJjaXBoZXJ0ZXh0IjoiMmM1ODdkMWQwNzU0MTg3MDJlOWNlMjZmOTI5YzliMjM5ODFiYjE5ZDg4MjhhODk4ODZkMzE4ZGUyZmJhNDhkY2U1YmYxMDUzYjdiNWNhYTY5YmFjNTliMDdmOWFlZTFmIiwiaXYiOiIzNDFkOTY3MzVkZWZiZmJlMzM3NGE2NjJiYTc4YWVhNjZkOGQ5MzM5ZDAyYWE5ZWMifQ=="  # noqa: E501

        decoded_json = ConnectionParser.decrypt_connection(key, encrypted)
        self.assertEqual(
            decoded_json,
            {"folderPath": "/Users/niccari/Downloads/test"})

    def test_decrypt_connection_azure(self):
        key = "VqVIBjp5p6ZRnqzKYB1Oql0dvrK0TkCtNXPiqjace2A="
        encrypted = "eyJjaXBoZXJ0ZXh0IjogIjRlZDM3MmQzYTg1YzU5YzE3NTIyN2MyZmEwNzg5ZDFjYjk0OWJiZGFmN2YzYTY3MjMyMmJlYjc5NWM0NjkwZmI2N2NjYWM1ODM5NjU2OGY4ODg0ZjQxZmU5OWNmNzAzYjRiYjgwOWI2ZWIwZDYyNjU0ZDliZjQ0MjdhNGU4ZGQ3NDhmOTY0OTM2NTM5NmU5ODEwNmM1M2Y3NTA0ZDcxYTU3YzMzMTk4NzBkYzEzOWY0ZThiMWNmMTM3ZDU1MzY4NmIyNmMxODc2NjVkNGViMWYzMDViYjhhOTY0MzkzM2Q3IiwgIml2IjogIjM4OWU0ZThjMWYxMTdiMTQ3MmY1NTNiN2Q2ZmEzMGU3NDkyN2M1NmE0NWJkYjFhZCJ9"  # noqa: E501

        decoded_json = ConnectionParser.decrypt_connection(key, encrypted)
        self.assertEqual(
            decoded_json,
            {
                'accountName': 'some_account',
                'containerName': 'some_container',
                'sas': '?sv=some_sas_string...'
            })
