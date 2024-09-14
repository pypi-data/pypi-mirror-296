# ITAdvisor Client
![image](https://img.shields.io/badge/pypi-3775A9?style=for-the-badge&logo=pypi&logoColor=white)<br>
An unoffical ITAdvisor API Client.<br> 
<br>
All capabilities available in the API are supported by this module.<br>
<br>
<u><b>Supported IT Advisor Versions:</b></u><br>
- 9.4.4

## Installation
```
pip install itadvisor-client
```

## Documentation
Example:
```
import itadvisor_client

# Mr. Robot Inspired Connection Details
ita_client = ITAdvisor(
    host = "itadvisor.evilcorp.com"
    username = "ealderson"
    password = "fS0c13tY"
)

my_genome = ita_client.genomes.get_genomes_by_id(genome_id="9ecca877-7b9f-45e8-ac69-929b5ff87b7e")

```
## Classes and Functions
**assets**
- in-progress

**audit_trail**
- in-progress

**authentication**
- in-progress

**autentication_servers**
- in-progress

**backup**
- list_backup_files()
- download_backup_file(file_name:str, download_directory:str)
- upload_backup_file(backup_file:str)
- get_backup_settings()
- update_backup_settings(backup_retention_days:int, backup_location:str, fail_if_not_mounted:bool, backup_cleanup_enabled:bool)
- trigger_restore(backup_file_name:str)
- trigger_backup(backup_prefix:str="custom_")

**certificates**
- get_certificates()
- add_certificate(certificate:str)
- delete_certificate(certificate:str)

**change_request**
- in-progress

**change_request_template**
- in-progress

**configuration**
- in-progress

**custom_properties**
- get_definitions()
- get_templates()
- check_usage(cp_name:str, cp_value:str)
- get_item_cp(item_id:str)

**customers**
- in-progress

**customers_count**
- get_customers_count(root_location_id, only_active:bool=None, only_with_users:bool=None)

**equipment_browser**
- in-progress

**etl_configuration**
- in-progress

**genomes**
- get_genomes(query:str=None, query_types:list=[], genomes:list=[], genome_source:str=None)
- get_genome_by_id(genome_id:str, genome_library:str=None)

**kpis**
- in-progress

**licenses**
- get_licenses()
- add_license(license_key:str)
- delete_license(license_key:str)

**mail**
- in-progress

**platform_status**
- get_job_queue()
- get_job_status()

**power_capacity**
- in-progress

**power_path**
- in-progress

**routing**
- in-progress

**sensor_mapping**
- in-progress

**struxure_on**
- in-progress

**svg**
- Schneider Electric states DO NOT USE.

**user_groups**
- in-progress

**user_message**
- in-progress

**users**
- in-progress

**work_orders**
- in-progress
