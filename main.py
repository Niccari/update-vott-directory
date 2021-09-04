import glob, os

import json

from app.arguments import Arguments
from app.model.project_info import ProjectInfo
from app.asset_parser import AssetParser
from app.connection_parser import ConnectionParser


def find_vott_path(directory: str):
    print(directory)
    candidates = glob.glob(os.path.join(directory, '*.vott'))
    if len(candidates) != 1:
        raise ValueError('Please specify a directory which contains a vott file.')

    return candidates[0]

if (__name__ == '__main__'):
    arguments = Arguments()
    project_info = ProjectInfo(
        key_security_token=arguments.args.key_security_token,
            target_connection_path=arguments.args.target_connection_path,
        source_connection_path=arguments.args.source_connection_path,
        azure_account_name=arguments.args.account_name,
        azure_container_name=arguments.args.container_name,# comment
        azure_sas = arguments.args.sas,
    )
    vott_path=find_vott_path(project_info.target_connection_path)

    AssetParser.update_assets(vott_path, project_info)
    ConnectionParser.update_connections(project_info)

    print(f"Completed! The output is in "
            +f"{project_info.target_connection_path}/output.")