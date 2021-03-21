from typing import Optional


class ProjectInfo:
    def __init__(
            self,
            new_local_directory: Optional[str] = None,
            azure_account_name: Optional[str] = None,
            azure_container_name: Optional[str] = None,
            azure_sas: Optional[str] = None):

        self.new_local_directory = new_local_directory

        self.azure_account_name = azure_account_name
        self.azure_container_name = azure_container_name
        self.azure_sas = azure_sas

        self.__validate_params()

    @property
    def is_azure(self):
        return self.azure_account_name \
            or self.azure_container_name \
            or self.azure_sas

    @property
    def new_dir_name(self) -> str:
        if self.is_azure:
            return f"https://{self.azure_account_name}.blob.core.windows.net/"\
                + f"{self.azure_container_name}/"
        else:
            return f"file:{self.new_local_directory}"

    def __validate_params(self):
        if self.is_azure:
            if not self.azure_account_name \
                    or not self.azure_container_name \
                    or not self.azure_sas:
                raise ValueError(
                    'Please specify all params for your azure blob container.')
            if self.new_local_directory:
                raise ValueError(
                    'Plase specify either new_local_directory or azure parameters.')    # noqa: E501
        elif not self.new_local_directory:
            raise ValueError(
                'Please specify a local directory to edit your vott project.')
