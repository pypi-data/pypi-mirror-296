import os
from hashlib import sha256
from base64 import b64encode
import warnings
import requests
import json
import shutil
from requests.auth import HTTPBasicAuth

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