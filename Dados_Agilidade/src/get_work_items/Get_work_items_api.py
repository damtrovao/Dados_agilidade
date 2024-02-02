import requests
import json
from urllib.parse import quote
from utils.Ler_config import Ler_config as Ler_config

class Get_work_items_api(object):
    def __init__(self):
        self.__url = None
        self.__organization = None
        self.__pat = None
        self.__headers = None
        self.__filter_project = None
        self.__filter_area_path = None
        self.__filter_work_item_type = None
        self.__lista_wi = []

    def __buscar_config(self):
        configuracoes = Ler_config()
        self.__pat = configuracoes.get_pat()
        self.__organization = configuracoes.get_organization()
        self.__filter_project = configuracoes.get_wi_filter_project()
        self.__filter_area_path = configuracoes.get_wi_filter_area_path()
        self.__filter_work_item_type = configuracoes.get_wi_filter_work_item_type()

    def ler_work_items(self, project):
        self.__buscar_config()

        if self.__filter_project[0] == "*" or project in self.__filter_project:
            self.__url = f"https://analytics.dev.azure.com/{self.__organization}/{project}/_odata/v3.0-preview/WorkItems?%24select=WorkItemId"

            self.__url += f"&%24filter=%28ClosedDate+ge+2024-01-31Z+or+State+ne+%27Closed%27%29"

            if self.__filter_area_path[0]:
                self.__url += f"+and+%28"
                
                for area_path in self.__filter_area_path:
                    self.__url += f"startswith%28Area%2FAreaPath%2C%27{area_path}%27%29+or+"
                
                #Retirando o operador lógico "or" do final da URL
                self.__url = self.__url[:-4]
                self.__url += f"%29"

            if self.__filter_work_item_type[0]:
                self.__url += f"+and+%28"
                
                for wi_type in self.__filter_work_item_type:
                    self.__url += f"WorkItemType+eq+%27{quote(wi_type)}%27+or+"
                
                #Retirando o operador lógico "or" do final da URL
                self.__url = self.__url[:-4]
                self.__url += f"%29"

            self.__headers = { "Authorization": f"Basic {self.__pat}" }

            while True:
                response = requests.get(self.__url, headers=self.__headers)

                if response.status_code == 200:
                    response_texto = json.loads(response.text)

                    for work_item in response_texto['value']:
                        self.__lista_wi.append(work_item['WorkItemId'])

                    if "@odata.nextLink" not in response_texto:
                        break
                    else:
                        self.__url = response_texto['@odata.nextLink']
                else:
                    return "Erro ao obter a lista de Work Items:", response.status_code, response.reason
            
            return self.__lista_wi
        else:
            return None