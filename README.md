# vott-replace-paths
[![unittest](https://github.com/Niccari/vott-replace-paths/actions/workflows/unittests.yaml/badge.svg)](https://github.com/Niccari/vott-replace-paths/actions/workflows/unittests.yaml)

Converts your VoTT projects portable to an other local file path or an Azure Blob Storage container.

## Installation
### Requirements
- Python 3.10.x
- pycryptodome

### pipenv
```bash
$ pipenv sync
$ pipenv shell    # To enter your virtual environment
```

### pip
```bash
$ python -m pip install -r requirements.txt
```

## Usage
Converted files will be output to "output/" under the directory where the vott file is located.

### To local
Please specify below parameters.

- -k: The security token to load/store your vott project.
- -s: The new video path (= Source connection)
- -t: The vott/assets file path (= Target connection)

```bash
$ python main.py \
    -k security_key_security_token \
    -s path/to/video_source_path \
    -t path/to/vott_file_directory
```

### To cloud(Azure Blob Container)
Please specify below parameters.

- -k: Security token to load/store your vott project.
- -t: VoTT/Assets file path
- -a: Azure blob storage account name
- -c: Azure blob storage container name
- -sas: SAS string for your Azure blob storage

```bash
$ python main.py \
    -k security_key_security_token \
    -t path/to/vott_file_directory \
    -a your_azure_storage_account_name
    -c your_azure_container_name
    -sas sas_for_reading_your_container
```

## Notice
If you find some bug, feel free to create an Issue or PR!

## Acknowledgements
This code is based on the [update-vott-assets](https://github.com/cnrmck/update-vott-assets), Thanks!

