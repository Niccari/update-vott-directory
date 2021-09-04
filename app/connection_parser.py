import base64
import glob
import json
import os

from app.libs.cipher import Cipher
from app.model.project_info import ProjectInfo


class ConnectionParser:
    @staticmethod
    def decrypt_connection(key_security_token: str, encrypted: str) -> dict:
        decoded_json = json.loads(base64.b64decode(encrypted))
        ciphertext = bytes.fromhex(decoded_json["ciphertext"])
        iv = bytes.fromhex(decoded_json["iv"])
        key = base64.b64decode(key_security_token)
        return json.loads(Cipher.aes_decrypt_to_plain(ciphertext, iv, key))

    @staticmethod
    def encrypt_connection(key_security_token: str, decrypted: dict) -> str:
        iv = os.urandom(16) + os.urandom(8)
        key = base64.b64decode(key_security_token)
        ciphertext_hex: str = Cipher.aes_encrypt_to_hex(
            json.dumps(decrypted).encode('utf-8'), iv, key)
        return base64.b64encode(json.dumps({
            "ciphertext": ciphertext_hex,
            "iv": iv.hex(),
        }).encode()).decode()

    @staticmethod
    def _update_connection_local(
            key_security_token: str, encrypted: str, dst_dir: str) -> str:
        connection = ConnectionParser.decrypt_connection(
            key_security_token, encrypted)
        connection_new = {"folderPath": dst_dir}
        print("change connection: " + str(connection)
              + " => " + str(connection_new))
        return ConnectionParser.encrypt_connection(
            key_security_token, connection_new)

    @staticmethod
    def _update_connection_azure(
            key_security_token: str, encrypted: str,
            account_name: str, countainer_name: str, sas: str) -> str:
        connection = ConnectionParser.decrypt_connection(
            key_security_token, encrypted)
        connection_new = {
            "accountName": account_name,
            "containerName": countainer_name,
            "sas": sas,
        }
        print("change connection: " + str(connection)
              + " => " + str(connection_new))
        return ConnectionParser.encrypt_connection(
            key_security_token, connection_new)

    @staticmethod
    def update_connections(project_info: ProjectInfo):
        print('Update connections...')

        output_directory = \
            os.path.join(project_info.target_connection_path, 'output')
        vott_path_regex = os.path.join(output_directory, '*.vott')

        for file_path in glob.glob(vott_path_regex):
            with open(file_path, 'r') as f:
                info = json.loads(f.read())

            if project_info.is_azure:
                info['sourceConnection']['providerOptions']['encrypted'] = \
                    ConnectionParser._update_connection_azure(
                        project_info.key_security_token,
                        info['sourceConnection']['providerOptions']['encrypted'],  # noqa: E501
                        project_info.azure_account_name,
                        project_info.azure_container_name,
                        project_info.azure_sas)
                info['targetConnection']['providerOptions']['encrypted'] = \
                    ConnectionParser._update_connection_azure(
                        project_info.key_security_token,
                        info['targetConnection']['providerOptions']['encrypted'],  # noqa: E501
                        project_info.azure_account_name,
                        project_info.azure_container_name,
                        project_info.azure_sas)
            else:
                info['sourceConnection']['providerOptions']['encrypted'] = \
                    ConnectionParser._update_connection_local(
                        project_info.key_security_token,
                        info['sourceConnection']['providerOptions']['encrypted'],  # noqa: E501
                        project_info.source_connection_path)
                info['targetConnection']['providerOptions']['encrypted'] = \
                    ConnectionParser._update_connection_local(
                        project_info.key_security_token,
                        info['targetConnection']['providerOptions']['encrypted'],  # noqa: E501
                        project_info.target_connection_path)

            providerType = "azureBlobStorage" \
                if project_info.is_azure else "localFileSystemProxy"
            info['sourceConnection']['providerType'] = providerType
            info['targetConnection']['providerType'] = providerType
            with open(file_path, 'w') as f:
                f.write(json.dumps(info, indent=4))
