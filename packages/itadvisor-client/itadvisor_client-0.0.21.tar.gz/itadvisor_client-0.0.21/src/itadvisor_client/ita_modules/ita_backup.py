import os
from hashlib import sha256
from base64 import b64encode
import warnings
import requests
import json
import shutil
from requests.auth import HTTPBasicAuth

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