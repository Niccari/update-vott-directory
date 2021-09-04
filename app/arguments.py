import argparse


class Arguments:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Updates VoTT directory.')
        parser.add_argument('-k', '--key_security_token', required=True)
        parser.add_argument('-t', '--target_connection_path', required=True)
        parser.add_argument('-s', '--source_connection_path')
        parser.add_argument('-a', '--account_name')
        parser.add_argument('-c', '--container_name')
        parser.add_argument('-sas')

        self.args = parser.parse_args()
