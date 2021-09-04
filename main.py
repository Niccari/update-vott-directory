import glob
import json
import os

from app.arguments import Arguments
from app.model.project_info import ProjectInfo
from app.asset_parser import AssetParser
from app.connection_parser import ConnectionParser


def find_vott_path(directory: str):
    candidates = glob.glob(os.path.join(directory, '*.vott'))
    if len(candidates) != 1:
        raise ValueError(
            'Please specify a directory which contains a vott file.')

    return candidates[0]


if __name__ == '__main__':
    arguments = Arguments()
    target_connection_path = arguments.args.target_connection_path

    project_info = ProjectInfo(
        key_security_token=arguments.args.key_security_token,
        source_connection_path=arguments.args.source_connection_path,
        azure_account_name=arguments.args.account_name,
        azure_container_name=arguments.args.container_name,
        azure_sas=arguments.args.sas,
    )
    vott_path = find_vott_path(target_connection_path)
    with open(vott_path, 'r') as f:
        vott_dict = json.load(f)

    asset_parser = AssetParser(project_info, target_connection_path)
    asset_parser.parse(vott_dict)
    asset_parser.rename(vott_path)
    asset_parser.update_contents()

    connection_parser = ConnectionParser(project_info, target_connection_path)
    connection_parser.update_connections()

    print(f'Completed! The output is in {asset_parser.output_directory}.')
