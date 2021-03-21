import argparse


class Arguments:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Updates VoTT directory.')
        parser.add_argument('-s', '--source_directory', required=True)
        parser.add_argument('-n', '--new_local_directory')
        parser.add_argument('-a', '--account_name')
        parser.add_argument('-c', '--container_name')
        parser.add_argument('-sas')

        self.args = parser.parse_args()
