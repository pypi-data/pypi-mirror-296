from licensespring.api import APIClient
from licensespring.licensefile import License
from licensespring.licensefile.config import Configuration
from licensespring.licensefile.data_storage import DataStorage
from licensespring.licensefile.error import LicenseFileCorruption


class BaseManager:
    def __init__(self, conf: Configuration):
        self._conf = conf
        self.licensefile_handler = DataStorage(conf)
        self.api_client = APIClient(
            api_key=conf._api_key,
            shared_key=conf._shared_key,
            hardware_id_provider=conf._hardware_id_provider,
            verify_license_signature=conf._verify_license_signature,
            signature_verifier=conf._signature_verifier,
            api_domain=conf._api_domain,
            api_version=conf._api_version,
        )

    def load_license(self) -> License:
        """
        Loads licensefile and sets attributes for LicenseData instance
        Returns:
        License: An instance of the License class reflecting the loaded license.
        """
        self.licensefile_handler.load_licensefile()

        return License(self._conf._product, self.api_client, self.licensefile_handler)

    def current_config(self) -> dict:
        """
        Get current configuration

        Returns:
            dict: configuration
        """
        return self._conf.__dict__

    def reconfigure(self, conf: Configuration) -> None:
        """
        Reconfigure

        Args:
            conf (Configuration): Configuration
        """
        self._conf = conf
        self.licensefile_handler = DataStorage(conf)
        self.api_client = APIClient(
            api_key=conf._api_key,
            shared_key=conf._shared_key,
            hardware_id_provider=conf._hardware_id_provider,
            verify_license_signature=conf._verify_license_signature,
            signature_verifier=conf._signature_verifier,
            api_domain=conf._api_domain,
            api_version=conf._api_version,
        )

    def is_license_file_corrupted(self) -> bool:
        """
        Check if licensefile is corrupted

        Returns:
            bool: True if licensefile is corrupted otherwise False
        """
        try:
            self.licensefile_handler.load_licensefile()
            return False
        except LicenseFileCorruption:
            return True

    def clear_local_storage(self):
        """
        Clear all data from current product
        """
        self.licensefile_handler.clear_storage()

    def data_location(self) -> str:
        """
        Get licensefile location

        Returns:
            str: licensefile location
        """

        return self.licensefile_handler.license_path

    def license_file_name(self) -> str:
        """
        Get licensefile name

        Returns:
            str: licensefile name
        """

        return self.licensefile_handler._filename
