
import os
import warnings
from .ita_modules import ita_assets
from .ita_modules import ita_audit_trail
from .ita_modules import ita_authentication
from .ita_modules import ita_authentication_servers
from .ita_modules import ita_backup
from .ita_modules import ita_certificates
from .ita_modules import ita_change_request_template
from .ita_modules import ita_change_request
from .ita_modules import ita_configuration
from .ita_modules import ita_custom_properties
from .ita_modules import ita_customers_count
from .ita_modules import ita_customers
from .ita_modules import ita_equipment_browser
from .ita_modules import ita_etl_configuration
from .ita_modules import ita_genomes
from .ita_modules import ita_kpis
from .ita_modules import ita_licenses
from .ita_modules import ita_mail
from .ita_modules import ita_platform_status
from .ita_modules import ita_power_capacity
from .ita_modules import ita_power_path
from .ita_modules import ita_routing
from .ita_modules import ita_sensor_mapping
from .ita_modules import ita_struxure_on
from .ita_modules import ita_svg
from .ita_modules import ita_user_groups
from .ita_modules import ita_user_message
from .ita_modules import ita_users
from .ita_modules import ita_work_orders

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

        self.assets = ita_assets._Assets(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.audit_trail = ita_audit_trail._AuditTrail(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.authentication = ita_authentication._Authentication(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.autentication_servers = ita_authentication_servers._AuthenticationServers(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.backup = ita_backup._Backup(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.certificates = ita_certificates._Certificates(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.change_request = ita_change_request._ChangeRequest(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.change_request_template = ita_change_request_template._ChangeRequestTemplate(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.configuration = ita_configuration._Configuration(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.custom_properties = ita_custom_properties._CustomProperties(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.customers = ita_customers._Customers(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.customers_count = ita_customers_count._CustomersCount(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.equipment_browser = ita_equipment_browser._EquipmentBrowser(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.etl_configuration = ita_etl_configuration._ETLConfiguration(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.genomes = ita_genomes._Genomes(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.kpis = ita_kpis._KPIS(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.licenses = ita_licenses._Licenses(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.mail = ita_mail._Mail(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.platform_status = ita_platform_status._PlatformStatus(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.power_capacity = ita_power_capacity._PowerCapacity(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.power_path = ita_power_path._PowerPath(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.routing = ita_routing._Routing(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.sensor_mapping = ita_sensor_mapping._SensorMapping(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.struxure_on = ita_struxure_on._StruxureOn(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.svg = ita_svg._SVG(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.user_groups = ita_user_groups._UserGroups(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.user_message = ita_user_message._UserMessage(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.users = ita_users._Users(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)
        self.work_orders = ita_work_orders._WorkOrders(base_api_url = self.base_api_url, username = self.username, password = self.password, cookies = self.cookies, verify=self.verify, cert=self.cert, timeout = self.timeout)

if __name__ == "__main__":
    pass
