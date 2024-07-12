"""Module to establish connect to Vault to fetch config files"""
import logging
import os
import hvac


class Vault:
    """
    This class contains code to establish connect to the vault using environment variables
    """

    def __init__(self, tenant):
        self.tenant = tenant.upper()
        self.path = os.environ.get(f'{self.tenant}_IC_SECRET_PATH')
        self.token = os.environ.get(f'{self.tenant}_VAULT_TOKEN')
        self.mount_point = os.environ.get("SECRET_ENGINE")
        self.data = None
        self.__get_vault_data()

    def __get_vault_data(self):
        """
        Function to fetch data from vault after connecting to it
        args: None
        return: None
        """
        client = hvac.Client(
            token=self.token
        )

        read_response = client.secrets.kv.v2.read_secret_version(
            path=self.path,
            mount_point=self.mount_point
        )

        self.data = read_response["data"]["data"]

    def get_secret_key(self):
        """
        Function to fetch secret key from vault
        args: None
        return: str
        """
        return self.data["secret_key"]

    def get_tenant_data(self):
        """
        Function to fetch tenant config from vault based on Tenant key
        args: None
        return: dict
        """
        try:
            return self.data["tenants"][self.tenant]
        except KeyError as error:
            logging.debug('[FAILURE] Tenant details not found in vault', error)
