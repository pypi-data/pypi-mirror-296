import os
from hashlib import sha256
from base64 import b64encode
import warnings
import requests
import json
import shutil
from requests.auth import HTTPBasicAuth

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