import hashlib
import os


class Target:
    def __init__(
            self,
            asset: dict, new_dir_name: str, azure_sas: str | None):
        self.asset_id = asset['id']
        self.type = asset['type']
        self.name = asset['name'].split('?')[0].split('#')[0]
        self.path = asset['path']
        self.timestamp = asset['timestamp'] if 'timestamp' in asset else None

        if self.type == 1 or self.type == 2:
            self.new_name = self.name
            new_path_basename = self.__finalize_name(self.name, azure_sas)
            self.new_path = os.path.join(new_dir_name, new_path_basename)
        elif self.type == 3:
            self.new_name = self.__finalize_name(self.name, azure_sas)
            self.new_name = f'{self.new_name}#t={self.timestamp}'
            self.new_path = os.path.join(new_dir_name, self.new_name)
        else:
            raise ValueError('Unsupported asset type!')

        self.new_asset_id = \
            hashlib.md5(self.new_path.encode('utf-8')).hexdigest()

    @classmethod
    def __finalize_name(cls, name: str, azure_sas: str | None) -> str:
        if azure_sas:
            return f'{name}{azure_sas}'
        else:
            return name

    def __str__(self):
        return f'{self.asset_id},{self.type},{self.name},{self.path},' \
            + f'{self.new_asset_id},{self.new_name},{self.new_path}'
