import unittest

from parser import Parser


class ParserTests(unittest.TestCase):
    def test_decrypt_connection_1(self):
        key = "VqVIBjp5p6ZRnqzKYB1Oql0dvrK0TkCtNXPiqjace2A="
        encrypted = "eyJjaXBoZXJ0ZXh0IjoiOWRmNDZhNGMwNDM5ODIxZDg3MWUyMjQwMzQ3NTFjNDc0OTM5MjRjZGUwZTkxNDRlOTQ4ZDBiYjMyY2E0ZmU0N2U2OTQ1NjVjZmNhNDM4ODlkZjNkMjYwOWViNGY0MDczMzNmNDBjNjQ3ZjFiZGRiMWExOWQzZmY5YTYyNDc4NzMiLCJpdiI6ImM2NDVlOTA5YzJkYmIwZDViZDA0MmE4NmM0YWVjMDU2YmI1NTEzN2M1NDA2YWQyYyJ9"  # noqa: E501

        decoded_json = Parser.decrypt_connection(key, encrypted)
        self.assertEqual(
            decoded_json,
            {"folderPath": "/Users/niccari/Downloads/test/video"})

    def test_decrypt_connection_2(self):
        key = "VqVIBjp5p6ZRnqzKYB1Oql0dvrK0TkCtNXPiqjace2A="
        encrypted = "eyJjaXBoZXJ0ZXh0IjoiMmM1ODdkMWQwNzU0MTg3MDJlOWNlMjZmOTI5YzliMjM5ODFiYjE5ZDg4MjhhODk4ODZkMzE4ZGUyZmJhNDhkY2U1YmYxMDUzYjdiNWNhYTY5YmFjNTliMDdmOWFlZTFmIiwiaXYiOiIzNDFkOTY3MzVkZWZiZmJlMzM3NGE2NjJiYTc4YWVhNjZkOGQ5MzM5ZDAyYWE5ZWMifQ=="  # noqa: E501

        decoded_json = Parser.decrypt_connection(key, encrypted)
        self.assertEqual(
            decoded_json,
            {"folderPath": "/Users/niccari/Downloads/test"})

    def test_decrypt_connection_3(self):
        key = "VqVIBjp5p6ZRnqzKYB1Oql0dvrK0TkCtNXPiqjace2A="
        encrypted = "eyJjaXBoZXJ0ZXh0IjoiZWUwYTU3YjM3NjU1ODMzODczMGM3YjZlY2M1ZjQ4NDg3MzQ4MzRhMDY5MmY0ZWY3NDg4MjNiOTU4MTdiMmE0ODA2OGFhNTQyZjI2NDYzYTQ0YzMzY2ZiMTA1YmI3OTNmIiwiaXYiOiI2MTIyOTNhNjcwMDAzMTEyOTM0MzMzMTE1MjQyMGJkMjQ4NTNjM2M5YzI3NTViYTgifQ=="  # noqa: E501

        decoded_json = Parser.decrypt_connection(key, encrypted)
        self.assertEqual(
            decoded_json,
            {'assetState': 'visited', 'includeImages': True})
