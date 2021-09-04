# vott-replace-paths
Updates VoTT directory and asset ids in assets.

You will be able to move files(\*.vott, \*-asset.json, movies and pictures) to a specified directory or your azure blob container.

## Notes
Source/Target connection updates are not supported - Please fix them manually.

## Installation
It runs in a Python 3.x environment.

No additional libraries need to be installed.

## Usage
The converted file will be output to "output/" under the directory where the vott file is located.

In below examples, it will be "path/to/vott_file_directory/output/".

### To local
```
python main.py \
    -t security_token \
    -s path/to/vott_file_directory \
    -n path/to/new_local_directory
```

### To cloud(Azure Blob Container)
```
python main.py \
    -t security_token \
    -s path/to/vott_file_directory \
    -a your_azure_storage_account_name
    -c your_azure_container_name
    -sas sas_for_reading_your_container
```

## Acknowledgements
This code is based on the [update-vott-assets](https://github.com/cnrmck/update-vott-assets), Thanks!
