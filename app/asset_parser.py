import glob
import json
import os
import shutil

from app.model.project_info import ProjectInfo
from app.model.target import Target


class AssetParser:
    @staticmethod
    def update_assets(
            vott_path: str,
            project_info: ProjectInfo) -> None:
        output_path = \
            os.path.join(project_info.target_connection_path, 'output')
        targets, asset_id_mapper = AssetParser._parse(
            vott_path=vott_path,
            new_dir_name=project_info.new_dir_name,
            azure_sas=project_info.azure_sas)
        AssetParser._rename_asset_files(
            vott_path=vott_path,
            target_connection_path=project_info.target_connection_path,
            output_path=output_path,
            asset_id_mapper=asset_id_mapper)
        AssetParser._update_contents(
            output_path=output_path,
            asset_id_mapper=asset_id_mapper,
            targets=targets)

    @staticmethod
    def _parse(
            vott_path: str,
            new_dir_name: str,
            azure_sas: str | None) -> tuple[dict, dict]:
        print('Parsing a vott file...')

        with open(vott_path, 'r') as f:
            vott_dict = json.load(f)

        targets = {}
        asset_id_mapper = {}

        for old_asset_id, asset in vott_dict['assets'].items():
            targets[old_asset_id] = \
                    (Target(asset, new_dir_name, azure_sas))
            if 'parent' in asset:
                targets[asset['parent']['id']] = (
                    Target(asset['parent'], new_dir_name, azure_sas))

        for target in targets.values():
            asset_id_mapper[target.asset_id] = target.new_asset_id
        return targets, asset_id_mapper

    @staticmethod
    def _rename_asset_files(
            vott_path: str,
            target_connection_path: str,
            output_path: str,
            asset_id_mapper: dict) -> None:
        print('Renaming asset json files...')
        asset_paths = \
            glob.glob(os.path.join(
                target_connection_path, '*-asset.json'))

        if os.path.exists(output_path):
            shutil.rmtree(output_path)
        os.makedirs(output_path)
        for old_asset_path in asset_paths:
            old_asset_file = os.path.basename(old_asset_path)
            old_asset_id = old_asset_file.split('-')[0]

            new_asset_id = asset_id_mapper[old_asset_id]
            shutil.copy2(
                old_asset_path,
                os.path.join(output_path, f'{new_asset_id}-asset.json'))

        shutil.copy2(
            vott_path, os.path.join(output_path, os.path.basename(vott_path)))

    @staticmethod
    def _update_contents(
            output_path: str,
            asset_id_mapper: dict, targets: dict) -> None:
        def update_item(asset: dict) -> dict:
            target = targets[asset['id']]
            new_asset = {}
            new_asset.update(asset)

            new_asset['id'] = target.new_asset_id
            new_asset['name'] = target.new_name
            new_asset['path'] = target.new_path

            if 'parent' in asset:
                target = targets[asset['parent']['id']]
                new_asset['parent']['id'] = target.new_asset_id
                new_asset['parent']['name'] = target.new_name
                new_asset['parent']['path'] = target.new_path

            return new_asset

        def update_vott() -> None:
            vott_path_regex = os.path.join(output_path, '*.vott')
            for file_path in glob.glob(vott_path_regex):
                with open(file_path, 'r') as f:
                    info = json.load(f)

                assets: dict = info['assets']
                new_assets = {}
                for v in assets.values():
                    new_asset = update_item(v)
                    new_assets[new_asset['id']] = new_asset

                info['assets'] = new_assets
                info['lastVisitedAssetId'] = \
                    asset_id_mapper[info['lastVisitedAssetId']]
                with open(file_path, 'w') as f:
                    json.dump(info, f, indent=4)

        def update_assets() -> None:
            json_path_regex = os.path.join(output_path, '*.json')
            for file_path in glob.glob(json_path_regex):
                with open(file_path, 'r') as f:
                    info = json.load(f)
                info['asset'] = update_item(info['asset'])
                with open(file_path, 'w') as f:
                    json.dump(info, f, indent=4)

        print('Update assets...')

        update_vott()
        update_assets()
