import base64
import glob
import json
import os
import shutil

from app.libs.cipher import Cipher
from app.model.project_info import ProjectInfo
from app.model.target import Target

from typing import Optional


class Parser:
    def __init__(self, project_info: ProjectInfo, source_directory: str):
        self.project_info = project_info
        self.targets = {}
        self.asset_id_mapper = {}
        self.source_directory = source_directory
        self.output_directory = os.path.join(self.source_directory, 'output')

    def parse(self, vott_dict: dict):
        print('Parsing a vott file...')

        for old_asset_id, asset in vott_dict['assets'].items():
            self.targets[old_asset_id] = (
                Target(
                    asset,
                    self.project_info.new_dir_name,
                    self.project_info.azure_sas
                ))
            if 'parent' in asset:
                self.targets[asset['parent']['id']] = (
                    Target(
                        asset['parent'],
                        self.project_info.new_dir_name,
                        self.project_info.azure_sas
                    ))

        for target in self.targets.values():
            self.asset_id_mapper[target.asset_id] = target.new_asset_id

    def rename(self, vott_path: str):
        print('Renaming asset json files...')
        asset_paths = \
            glob.glob(os.path.join(self.source_directory, '*-asset.json'))
        output_path = self.output_directory

        if os.path.exists(output_path):
            shutil.rmtree(output_path)
        os.makedirs(output_path)
        for old_asset_path in asset_paths:
            old_asset_file = os.path.basename(old_asset_path)
            old_asset_id = old_asset_file.split('-')[0]

            new_asset_id = self.asset_id_mapper[old_asset_id]
            shutil.copy2(
                old_asset_path,
                os.path.join(output_path, f'{new_asset_id}-asset.json'))

        shutil.copy2(
            vott_path, os.path.join(output_path, os.path.basename(vott_path)))

    @staticmethod
    def decrypt_connection(token: str, encrypted: str) -> dict:
        decoded_json = json.loads(base64.b64decode(encrypted))
        ciphertext = bytes.fromhex(decoded_json["ciphertext"])
        iv = bytes.fromhex(decoded_json["iv"])
        key = base64.b64decode(token)
        return json.loads(Cipher.aes_decrypt_to_plain(ciphertext, iv, key))

    @staticmethod
    def update_connection(token: str, encrypted: str,
                          src_dir: str, dst_dir: str) -> str:
        connection = Parser.decrypt_connection(token, encrypted)
        folder_path: Optional[str] = connection.get("folderPath")
        connection["folderPath"] = folder_path.replace(src_dir, dst_dir)

        iv = os.urandom(16) + os.urandom(8)
        ciphertext_hex: str = Cipher.aes_encrypt_to_hex(
            json.dumps(connection), iv)
        return base64.b64encode({
            "ciphertext": ciphertext_hex,
            "iv": iv.hex(),
        }.decode())

    def update_connections(self):
        print('Update connections...')

        vott_path_regex = os.path.join(self.output_directory, '*.vott')

        for file_path in glob.glob(vott_path_regex):
            with open(file_path, 'w+') as f:
                info = json.load(f)

            info['sourceConnection']['providerOptions']['encrypted'] = \
                Parser.update_connection(
                    self.project_info.token,
                    info['sourceConnection']['providerOptions']['encrypted'],
                    self.source_directory,
                    self.project_info.new_dir_name)
            info['tagretConnection']['providerOptions']['encrypted'] = \
                Parser.update_connection(
                    self.project_info.token,
                    info['tagretConnection']['providerOptions']['encrypted'],
                    self.source_directory,
                    self.project_info.new_dir_name)

    def update_contents(self):
        def update_item(asset: dict):
            target = self.targets[asset['id']]
            new_asset = {}
            new_asset.update(asset)

            new_asset['id'] = target.new_asset_id
            new_asset['name'] = target.new_name
            new_asset['path'] = target.new_path

            if 'parent' in asset:
                target = self.targets[asset['parent']['id']]
                new_asset['parent']['id'] = target.new_asset_id
                new_asset['parent']['name'] = target.new_name
                new_asset['parent']['path'] = target.new_path

            return new_asset

        print('Update assets...')

        vott_path_regex = os.path.join(self.output_directory, '*.vott')
        json_path_regex = os.path.join(self.output_directory, '*.json')

        for file_path in glob.glob(vott_path_regex):
            with open(file_path, 'r') as f:
                info = json.load(f)

            assets = info['assets']
            new_assets = {}
            for k, v in assets.items():
                new_asset = update_item(v)
                new_assets[new_asset['id']] = new_asset

            info['assets'] = new_assets
            info['lastVisitedAssetId'] = \
                self.asset_id_mapper[info['lastVisitedAssetId']]
            with open(file_path, 'w') as f:
                json.dump(info, f, indent=4)

        for file_path in glob.glob(json_path_regex):
            with open(file_path, 'r') as f:
                info = json.load(f)

            new_asset = update_item(info['asset'])
            assets[new_asset['id']] = new_asset
            info['asset'] = new_asset

            with open(file_path, 'w') as f:
                json.dump(info, f, indent=4)
