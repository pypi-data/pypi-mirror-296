import os
from hashlib import sha256
from base64 import b64encode
import warnings
import requests
import json
import shutil
from requests.auth import HTTPBasicAuth


class ITAdvisor:
    def __init__(self, host_name:str, username:str, password:str, protocol:str="https", cookies:dict={}, verify=None, cert=None, timeout:int=60):
        """
        Initializes the `itadvisor-client` object with the provided parameters.
        Args:
            host_name (str): The host name of the API server.
            username (str): The username for authentication.
            password (str): The password for authentication.
            protocol (str ('http', 'https'), optional): The protocol to use for communication. Defaults to "https".
            cookies (dict, optional): Cookies to include in the Request. Helpful when Zero Trust is implemented. 
            verify ((None, False, "/path/to/certificate"), optional): Whether to verify SSL certificates. Defaults to None.
            cert ((None, tuple, "/path/to/certificate"), optional): Client-side SSL certificate and key. Defaults to None
            timeout (int, optional): The timeout value for API requests in seconds. Defaults to 60.
        """

        if verify not in [None, False]:
            if not os.path.isfile(cert):
                raise ValueError(f"The specified certificate file `{cert}` does not exist.")
        else:
            warnings.filterwarnings("ignore")
            
        if cert is not None:
            if type(cert) is str:
                if not os.path.isfile(cert):
                    raise ValueError(f"The specified certificate file `{cert}` does not exist.")
            if type(cert) is tuple:
                for cert_itme in cert:
                    if not os.path.isfile(cert_itme):
                        raise ValueError(f"The specified certificate file `{cert_itme}` does not exist.")

        if protocol not in ["http", "https"]:
            raise ValueError("The protocol must be either 'http' or 'https'.")
            
        self.username = username
        self.password = password
        self.verify = verify
        self.cookies = cookies
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = f"{protocol}://{host_name}/api/current"

        self.assets = _Assets(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.audit_trail = _AuditTrail(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.authentication = _Authentication(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.autentication_servers = _AuthenticationServers(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.backup = _Backup(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.certificates = _Certificates(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.change_request = _ChangeRequest(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.change_request_template = _ChangeRequestTemplate(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.configuration = _Configuration(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.custom_properties = _CustomProperties(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.customers = _Customers(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.customers_count = _CustomersCount(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.equipment_browser = _EquipmentBrowser(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.etl_configuration = _ETLConfiguration(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.genomes = _Genomes(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.kpis = _KPIS(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.licenses = _Licenses(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.mail = _Mail(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.platform_status = _PlatformStatus(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.power_capacity = _PowerCapacity(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.power_path = _PowerPath(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.routing = _Routing(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.sensor_mapping = _SensorMapping(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.struxure_on = _StruxureOn(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.svg = _SVG(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.user_groups = _UserGroups(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.user_message = _UserMessage(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.users = _Users(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.work_orders = _WorkOrders(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)

class _Assets:
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

    def get_assets(self, customer_id:str=None, recursive:bool=None):
        """
        
        """
        session = requests.Session()
        api_resource = f"{self.base_api_url}/assets?"
        if customer_id != None:
            api_resource += f"customer-id={customer_id}"
        if customer_id != None and recursive!=None:
            api_resource += "&"
        if recursive != None:
            api_resource += f"recursive={str(recursive).lower()}"
        if self.verify not in [None, False]:
            session.verify = self.verify
            session.cert
        if self.cert != None:
            session.cert = self.cert
        headers = {"Content-Type": "application/json"}
        session.cookies.update(self.cookies)
        session.verify = self.verify
        api_auth = HTTPBasicAuth(self.username, self.password)
        response = session.get(api_resource, headers=headers, auth=api_auth, verify=self.verify, timeout=self.timeout)
        return response
    
    def update_assets(self):
        pass

    def search_assets(self):
        pass

    def get_asset_types(self):
        pass

    def upload_asset_visual(self):
        """DO NOT USE"""
        pass
    
    def get_asset_visual(self):
        """DO NOT USE"""
        pass

    def get_asset_by_id(self):
        pass

    def update_asset_by_id(self):
        pass

    def delete_asset_by_id(self):
        pass
    
    def create_child_asset(self):
        pass

    def set_custom_property_by_id(self):
        pass

    def delete_custom_property_by_id(self):
        pass

    def get_customer_relation_by_id(self):
        pass

    def set_customer_relation_by_id(self):
        pass

    def delete_custom_property_by_id(self):
        pass

    def get_associated_devices_by_id(self):
        pass

    def get_metrics_by_id(self):
        pass

    def set_asset_visual_by_id(self):
        """DO NOT USE"""

    def delete_asset_visual_by_id(self):
        """DO NOT USE"""

class _AuditTrail:
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

class _Authentication:
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

class _AuthenticationServers:
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

class _Backup: # Done
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

    def list_backup_files(self):
        """
        Returns a list of certificates
        """
        session = requests.Session()
        api_resource = f"{self.base_api_url}/backup"
        if self.verify not in [None, False]:
            session.verify = self.verify
            session.cert
        if self.cert != None:
            session.cert = self.cert
        headers = {"Content-Type": "application/json"}
        session.cookies.update(self.cookies)
        session.verify = self.verify
        api_auth = HTTPBasicAuth(self.username, self.password)
        response = session.get(api_resource, headers=headers, auth=api_auth, verify=self.verify, timeout=self.timeout)
        return response
    
    def download_backup_file(self, file_name:str, download_directory:str):
        """
        Downloads specified backup file
        """
        session = requests.Session()
        if os.path.isdir(download_directory) != True:
            raise ValueError(f"The path specified `{download_directory}` does not exist.")
        api_resource = f"{self.base_api_url}/backup/backup-file/{file_name}"
        if self.verify not in [None, False]:
            session.verify = self.verify
            session.cert
        if self.cert != None:
            session.cert = self.cert
        headers = {"Content-Type": "application/octet-stream"}
        session.cookies.update(self.cookies)
        session.verify = self.verify
        api_auth = HTTPBasicAuth(self.username, self.password)
        with session.get(api_resource, headers=headers, stream=True, auth=api_auth, verify=self.verify, timeout=None) as response:
            with open(f"{download_directory}/{file_name}", 'wb') as download_file:
                shutil.copyfileobj(response.raw, download_file)
        return response

    def upload_backup_file(self, backup_file:str):
        """
        Uploads backup file
        curl -X 'POST' \
        f'http://{self.base_url}/backup/backup-file' \
        -H 'accept: application/json' \
        -H 'Content-Type: multipart/form-data' \
        -F 'backupFile=@{file_name};type=application/x-gzip'

        """
        session = requests.Session()
        if os.path.isfile(backup_file) != True:
            raise ValueError(f"The file specified `{backup_file}` does not exist.")
        upload_data = {"backupFile": open(backup_file, "rb"),
                       "type": "application/x-gzip"
                       }
        api_resource = f"{self.base_api_url}/backup/backup-file"
        if self.verify not in [None, False]:
            session.verify = self.verify
            session.cert
        if self.cert != None:
            session.cert = self.cert
        headers = {"Content-Type": "multipart/form-data",
                   "accept": "application/json"}
        session.cookies.update(self.cookies)
        session.verify = self.verify
        api_auth = HTTPBasicAuth(self.username, self.password)
        response = session.post(api_resource, headers=headers, files=upload_data, auth=api_auth, verify=self.verify, timeout=None)
        return response
    
    def get_backup_settings(self):
        """
        Returns backup settings
        """
        session = requests.Session()
        api_resource = f"{self.base_api_url}/backup/settings"
        if self.verify not in [None, False]:
            session.verify = self.verify
            session.cert
        if self.cert != None:
            session.cert = self.cert
        headers = {"Content-Type": "application/json"}
        session.cookies.update(self.cookies)
        session.verify = self.verify
        api_auth = HTTPBasicAuth(self.username, self.password)
        response = session.get(api_resource, headers=headers, auth=api_auth, verify=self.verify, timeout=self.timeout)
        return response
    
    def update_backup_settings(self,backup_retention_days:int, backup_location:str, fail_if_not_mounted:bool, backup_cleanup_enabled:bool):
        """
        Updates backup settings
        """
        session = requests.Session()
        settings = {
        "numberOfDaysToKeepBackups": backup_retention_days,
        "backupLocation": backup_location,
        "failIfNotMountedRemotely": fail_if_not_mounted,
        "backupCleanupEnabled": backup_cleanup_enabled
        }
        api_resource = f"{self.base_api_url}/backup/settings"
        if self.verify not in [None, False]:
            session.verify = self.verify
            session.cert
        if self.cert != None:
            session.cert = self.cert
        headers = {"Content-Type": "application/json"}
        session.cookies.update(self.cookies)
        session.verify = self.verify
        api_auth = HTTPBasicAuth(self.username, self.password)
        response = session.put(api_resource, headers=headers, data=json.dumps(settings), auth=api_auth, verify=self.verify, timeout=self.timeout)
        return response
    
    def trigger_restore(self,backup_file_name:str):
        """
        Updates backup settings
        """
        session = requests.Session()
        api_resource = f"{self.base_api_url}/backup/restore?file={backup_file_name}"
        if self.verify not in [None, False]:
            session.verify = self.verify
            session.cert
        if self.cert != None:
            session.cert = self.cert
        headers = {"Content-Type": "application/json"}
        session.cookies.update(self.cookies)
        session.verify = self.verify
        api_auth = HTTPBasicAuth(self.username, self.password)
        response = session.put(api_resource, headers=headers, auth=api_auth, verify=self.verify, timeout=self.timeout)
        return response
    
    def trigger_backup(self,backup_prefix:str="custom_"):
        """
        Updates backup settings
        """
        session = requests.Session()
        api_resource = f"{self.base_api_url}/backup/backup?backupPrefix={backup_prefix}"
        if self.verify not in [None, False]:
            session.verify = self.verify
            session.cert
        if self.cert != None:
            session.cert = self.cert
        headers = {"Content-Type": "application/json"}
        session.cookies.update(self.cookies)
        session.verify = self.verify
        api_auth = HTTPBasicAuth(self.username, self.password)
        response = session.put(api_resource, headers=headers, auth=api_auth, verify=self.verify, timeout=self.timeout)
        return response

class _Certificates: # Done
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

    def get_certificates(self):
        """
        Returns a list of certificates
        """
        session = requests.Session()
        api_resource = f"{self.base_api_url}/certificates"
        if self.verify not in [None, False]:
            session.verify = self.verify
            session.cert
        if self.cert != None:
            session.cert = self.cert
        headers = {"Content-Type": "application/json"}
        session.cookies.update(self.cookies)
        session.verify = self.verify
        api_auth = HTTPBasicAuth(self.username, self.password)
        response = session.get(api_resource, headers=headers, auth=api_auth, verify=self.verify, timeout=self.timeout)
        return response

    def add_certificate(self, certificate:str):
        """
        Adds certificate to the keystore
        """
        session = requests.Session()
        api_resource = f"{self.base_api_url}/certificates"
        if self.verify not in [None, False]:
            session.verify = self.verify
            session.cert
        if self.cert != None:
            session.cert = self.cert
        headers = {"Content-Type": "application/json"}
        session.cookies.update(self.cookies)
        session.verify = self.verify
        api_auth = HTTPBasicAuth(self.username, self.password)
        response = session.post(api_resource, data=certificate ,headers=headers, auth=api_auth, verify=self.verify, timeout=self.timeout)
        return response

    def delete_certificate(self, certificate:str):
        """
        Deletes a certificate.
        """
        session = requests.Session()
        api_resource = f"{self.base_api_url}/certificates/{certificate}"
        if self.verify not in [None, False]:
            session.verify = self.verify
            session.cert
        if self.cert != None:
            session.cert = self.cert
        headers = {"Content-Type": "application/json"}
        session.cookies.update(self.cookies)
        session.verify = self.verify
        api_auth = HTTPBasicAuth(self.username, self.password)
        response = session.delete(api_resource, data=certificate ,headers=headers, auth=api_auth, verify=self.verify, timeout=self.timeout)
        return response

class _ChangeRequest:
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

class _ChangeRequestTemplate:
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

class _Configuration:
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

class _CustomProperties: # Done
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

    def get_definitions(self):
        """
        Returns a list of dictionaries. Dictionaries are custom property definitions.
        """
        session = requests.Session()
        api_resource = f"{self.base_api_url}/custom-properties/definitions"
        if self.verify not in [None, False]:
            session.verify = self.verify
            session.cert
        if self.cert != None:
            session.cert = self.cert
        headers = {"Content-Type": "application/json"}
        session.cookies.update(self.cookies)
        session.verify = self.verify
        api_auth = HTTPBasicAuth(self.username, self.password)
        response = session.get(api_resource, headers=headers, auth=api_auth, verify=self.verify, timeout=self.timeout)
        return response
    
    def get_templates(self):
        """
        Returns list of custom property templates
        """
        session = requests.Session()
        api_resource = f"{self.base_api_url}/custom-properties/templates"
        if self.verify not in [None, False]:
            session.verify = self.verify
            session.cert
        if self.cert != None:
            session.cert = self.cert
        headers = {"Content-Type": "application/json"}
        session.cookies.update(self.cookies)
        session.verify = self.verify
        api_auth = HTTPBasicAuth(self.username, self.password)
        response = session.get(api_resource, headers=headers, auth=api_auth, verify=self.verify, timeout=self.timeout)
        return response
    
    def check_usage(self, cp_name:str, cp_value:str):
        """
        checks to see if a cp_name and cp_value combo is in use. 
        Returns boolian.
        """
        session = requests.Session()
        api_resource = f"{self.base_api_url}/custom-properties/value-used?property-name={cp_name}"
        if self.verify not in [None, False]:
            session.verify = self.verify
            session.cert
        if self.cert != None:
            session.cert = self.cert
        headers = {"Content-Type": "application/json"}
        session.cookies.update(self.cookies)
        session.verify = self.verify
        api_auth = HTTPBasicAuth(self.username, self.password)
        response = session.get(api_resource, headers=headers, data = cp_value, auth=api_auth, verify=self.verify, timeout=self.timeout)
        return response
    
    def get_item_cp(self, item_id:str):
        """
        item_id must be GUID string.
        Output is a list of dictionaries with custom property details defined for the item.
        """
        session = requests.Session()
        api_resource = f"{self.base_api_url}/custom-properties/{item_id}/definitions"
        if self.verify not in [None, False]:
            session.verify = self.verify
            session.cert
        if self.cert != None:
            session.cert = self.cert
        headers = {"Content-Type": "application/json"}
        session.cookies.update(self.cookies)
        session.verify = self.verify
        api_auth = HTTPBasicAuth(self.username, self.password)
        response = session.get(api_resource, headers=headers, auth=api_auth, verify=self.verify, timeout=self.timeout)
        return response

class _Customers:
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

class _CustomersCount: # Done
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

    def get_customers_count(self, root_location_id, only_active:bool=None, only_with_users:bool=None):
        """
        Get number of customers in child locations and rooms of specified root location matching the given filtering options
        """
        session = requests.Session()
        api_resource = f"{self.base_api_url}/customers-count?q={root_location_id}"
        if only_active != None:
            only_active = str(only_active).lower()
            api_resource += f"&only-active={only_active}"
        if only_with_users != None:
            only_with_users = str(only_with_users).lower()
            api_resource += f"&only-with-users={only_with_users}"

        if self.verify not in [None, False]:
            session.verify = self.verify
            session.cert
        if self.cert != None:
            session.cert = self.cert
        headers = {"Content-Type": "application/json"}
        session.cookies.update(self.cookies)
        session.verify = self.verify
        api_auth = HTTPBasicAuth(self.username, self.password)
        response = session.get(api_resource, headers=headers, auth=api_auth, verify=self.verify, timeout=self.timeout)
        return response

class _EquipmentBrowser:
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

class _ETLConfiguration:
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

class _Genomes: # Done
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

    def get_genomes(self, query:str=None, query_types:list=[], genomes:list=[], genome_source:str=None):
        """
        query option is string that will be filtered with wild cards on both ends.
        genome_source options ["LIBRARY", "USER"]
        query_types options ["FLOOR_MOUNTABLE", "RACK_MOUNTABLE", "BLADE_ENCLOSURE_MOUNTABLE", "SWITCH_ENCLOSURE_MOUNTABLE", "SHELF_MOUNTABLE"]
        genomes [
        AIR_COOLED_CHILLER
        ATS
        BATTERY
        BLADE
        BLADE_ENCLOSURE
        BLOCK
        BREAKER
        BREAKER_MODULE
        BUNDLE_FLOOR
        CACS
        CAMERA
        CDU
        CHILLER
        CONDENSER
        COOLINGTOWER
        CRAC
        CRACFAN
        CRAH
        DOOR
        DRIVE_ARRAY
        DRYCOOLER
        ENVIRONMENTAL_EQUIPMENT
        ENVIRONMENTAL_POWER_EQUIPMENT
        EPO
        FIRE_SUPPRESSION
        GAP
        GENERATOR
        GENERIC_POWERED_FLOORMOUNTABLE
        HACS
        INROOM
        ISX_MANAGER
        LADDER
        LAYER1_NETWORK_GEAR
        LAYER2_NETWORK_GEAR
        LAYER3_NETWORK_GEAR
        NETBOTZ_CENTRAL
        NETWORK
        NETWORK_CABLE
        NONEPOWERED_FLOORMOUNTABLE
        NONEPOWERED_RACKMOUNTABLE
        OVERHEAD_COOLING_UNIT
        PAC
        PDU
        RECTIFIER
        PERFORATED_CEILING_TILE
        PERFORATED_TILE
        PERFORATED_TILES_4X
        PERFORATED_TILES_8X
        PERSON
        POWER_PANEL
        POWER_RECEPTACLE
        PUMP
        RACK
        RACS
        RDP
        ROW
        SERVER
        SHELF
        SWITCHGEAR
        SWITCH_ENCLOSURE
        SWITCH_MODULE
        TELECOM
        UPS
        VERTICAL_GRILLE
        WATER_TANK
        WALL
        WINDOW]
        """
        session = requests.Session()
        api_resource = f"{self.base_api_url}/genomes?"
        if query != None:
            api_resource += f"&query={query}"
        if len(query_types) > 0:
            for query_type in query_types:
                api_resource += f"&type={query_type}"
        if len(genomes) > 0:
            for genome in genomes:
                api_resource += f"&genomes={genome}"
        if genome_source != None:
            genome_source = (genome_source).upper()
            api_resource += f"&source={genome_source}"

        if self.verify not in [None, False]:
            session.verify = self.verify
            session.cert
        if self.cert != None:
            session.cert = self.cert
        headers = {"Content-Type": "application/json"}
        session.cookies.update(self.cookies)
        session.verify = self.verify
        api_auth = HTTPBasicAuth(self.username, self.password)
        response = session.get(api_resource, headers=headers, auth=api_auth, verify=self.verify, timeout=self.timeout)
        return response
    
    def get_genome_by_id(self, genome_id:str, genome_library:str=None):
        """
        returns Genome data. Default library is both.
        Genome library option = LIBRARY or USER
        """
        session = requests.Session()
        api_resource = f"{self.base_api_url}/genomes/{genome_id}"
        if genome_library != None:
            genome_library = (genome_library).upper()
            api_resource += f"?source={genome_library}"
        if self.verify not in [None, False]:
            session.verify = self.verify
            session.cert
        if self.cert != None:
            session.cert = self.cert
        headers = {"Content-Type": "application/json"}
        session.cookies.update(self.cookies)
        session.verify = self.verify
        api_auth = HTTPBasicAuth(self.username, self.password)
        response = session.get(api_resource, headers=headers, auth=api_auth, verify=self.verify, timeout=self.timeout)
        return response

class _KPIS:
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

class _Licenses: # Done
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

    def get_licenses(self):
        """
        Returns licenses
        This operation requires the enabling-permission SYSTEM_CONFIGURATION_ADMINISTRATOR.
        """
        session = requests.Session()
        api_resource = f"{self.base_api_url}/licenses"
        if self.verify not in [None, False]:
            session.verify = self.verify
            session.cert
        if self.cert != None:
            session.cert = self.cert
        headers = {"Content-Type": "application/json"}
        session.cookies.update(self.cookies)
        session.verify = self.verify
        api_auth = HTTPBasicAuth(self.username, self.password)
        response = session.get(api_resource, headers=headers, auth=api_auth, verify=self.verify, timeout=self.timeout)
        return response
    
    def add_license(self, license_key:str):
        """
        Adds license key
        This operation requires the enabling-permission SYSTEM_CONFIGURATION_ADMINISTRATOR.
        """
        session = requests.Session()
        api_resource = f"{self.base_api_url}/licenses"
        if self.verify not in [None, False]:
            session.verify = self.verify
            session.cert
        if self.cert != None:
            session.cert = self.cert
        headers = {"Content-Type": "application/json"}
        session.cookies.update(self.cookies)
        session.verify = self.verify
        api_auth = HTTPBasicAuth(self.username, self.password)
        response = session.post(api_resource, headers=headers, auth=api_auth, data=license_key, verify=self.verify, timeout=self.timeout)
        return response
    
    def delete_license(self, license_key:str):
        """
        deletes license key
        This operation requires the enabling-permission SYSTEM_CONFIGURATION_ADMINISTRATOR.
        Encoded sha256+base64 automatically
        """
        session = requests.Session()
        api_resource = f"{self.base_api_url}/licenses/"
        if self.verify not in [None, False]:
            session.verify = self.verify
            session.cert
        if self.cert != None:
            session.cert = self.cert

        sha = sha256()
        sha.update(license_key.encode('utf-8'))
        hex_string = sha.digest().hex()
        digest_again = bytes.fromhex(hex_string)
        b64bytes = b64encode(digest_again)
        encrypted_license_key = b64bytes.decode('ascii')

        api_resource += encrypted_license_key

        headers = {"Content-Type": "application/json"}
        session.cookies.update(self.cookies)
        session.verify = self.verify
        api_auth = HTTPBasicAuth(self.username, self.password)
        response = session.post(api_resource, headers=headers, auth=api_auth, data=encrypted_license_key, verify=self.verify, timeout=self.timeout)
        return response

class _Mail:
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

class _PlatformStatus: # Done
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

    def get_job_queue(self):
        """
        Returns a list of jobs
        """
        session = requests.Session()
        api_resource = f"{self.base_api_url}/platform-status/job-queue"
        if self.verify not in [None, False]:
            session.verify = self.verify
            session.cert
        if self.cert != None:
            session.cert = self.cert
        headers = {"Content-Type": "application/json"}
        session.cookies.update(self.cookies)
        session.verify = self.verify
        api_auth = HTTPBasicAuth(self.username, self.password)
        response = session.get(api_resource, headers=headers, auth=api_auth, verify=self.verify, timeout=self.timeout)
        return response
    
    def get_job_status(self):
        """
        Returns job status
        """
        session = requests.Session()
        api_resource = f"{self.base_api_url}/platform-status/job-status"
        if self.verify not in [None, False]:
            session.verify = self.verify
            session.cert
        if self.cert != None:
            session.cert = self.cert
        headers = {"Content-Type": "application/json"}
        session.cookies.update(self.cookies)
        session.verify = self.verify
        api_auth = HTTPBasicAuth(self.username, self.password)
        response = session.get(api_resource, headers=headers, auth=api_auth, verify=self.verify, timeout=self.timeout)
        return response

class _PowerCapacity:
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

class _PowerPath:
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

class _Routing:
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

class _SensorMapping:
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

class _StruxureOn:
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

class _SVG:
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

class _UserGroups:
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

class _UserMessage:
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

class _Users:
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

class _WorkOrders:
    def __init__(self, base_api_url, username, password, cookies, verify, cert, timeout):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.base_api_url = base_api_url

if __name__ == "__main__":
    pass
