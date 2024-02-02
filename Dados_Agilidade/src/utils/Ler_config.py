import os
import configparser
import base64

class Ler_config(object):
    def __init__(self):
        self.__organization = None
        self.__wi_filter_project = None
        self.__wi_filter_area_path = None
        self.__wi_filter_work_item_type = None
        self.__base64_pat = None
        self.__account_key = None
        self.__account_name = None
        self.__read_config()

    def __read_config(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))

        config = configparser.ConfigParser()

        config.read(os.path.join(script_dir, 'config.ini'))

        pat = os.environ.get('PA_TOKEN')
        self.__account_key = os.environ.get('ACCOUNT_KEY')
        self.__account_name = os.environ.get('ACCOUNT_NAME')
        self.__organization = config.get('Credentials', 'ORGANIZATION')
        self.__wi_filter_project = config.get('Filter', 'PROJECT', fallback=None).split(', ')
        self.__wi_filter_area_path = config.get('Filter', 'AREA_PATH', fallback=None).split(', ')
        self.__wi_filter_work_item_type = config.get('Filter', 'WORK_ITEM_TYPE', fallback=None).split(', ')

        pat_bytes = f":{pat}".encode("ascii")
        self.__base64_pat = base64.b64encode(pat_bytes).decode("ascii")

    def get_pat(self):
        return self.__base64_pat
    
    def get_account_key(self):
        return self.__account_key
    
    def get_account_name(self):
        return self.__account_name
    
    def get_organization(self):
        return self.__organization
    
    def get_wi_filter_project(self):
        return self.__wi_filter_project
    
    def get_wi_filter_area_path(self):
        return self.__wi_filter_area_path
    
    def get_wi_filter_work_item_type(self):
        return self.__wi_filter_work_item_type