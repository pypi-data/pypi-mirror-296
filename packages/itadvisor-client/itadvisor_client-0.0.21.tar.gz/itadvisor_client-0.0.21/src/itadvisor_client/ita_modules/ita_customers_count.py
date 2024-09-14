import os
from hashlib import sha256
from base64 import b64encode
import warnings
import requests
import json
import shutil
from requests.auth import HTTPBasicAuth

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