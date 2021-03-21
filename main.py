import glob
import json
import os

from arguments import Arguments
from model.project_info import ProjectInfo
from parser import Parser


def find_vott_path(directory: str):
    candidates = glob.glob(os.path.join(directory, '*.vott'))
    if len(candidates) != 1:
        raise ValueError(
            'Please specify a directory which contains a vott file.')

    return candidates[0]


# Update of azure connections is not supported. Please change them manually.
if __name__ == '__main__':
    arguments = Arguments()
    source_directory = arguments.args.source_directory

    project_info = ProjectInfo(
        new_local_directory=arguments.args.new_local_directory,
        azure_account_name=arguments.args.account_name,
        azure_container_name=arguments.args.container_name,
        azure_sas=arguments.args.sas,
    )
    vott_path = find_vott_path(source_directory)
    with open(vott_path, 'r') as f:
        vott_dict = json.load(f)

    parser = Parser(project_info, source_directory)
    parser.parse(vott_dict)
    parser.rename(vott_path)
    parser.update_contents()

    print(f'Completed! The output is in {parser.output_directory}.')
