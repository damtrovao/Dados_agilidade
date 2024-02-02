import requests
import json
from utils.Ler_config import Ler_config as Ler_config

class Get_projects_api(object):
    def __init__(self):
        self.__url = None
        self.__organization = None
        self.__pat = None
        self.__headers = None

    def __buscar_config(self):
        configuracoes = Ler_config()
        self.__pat = configuracoes.get_pat()
        self.__organization = configuracoes.get_organization()

    def ler_projetos(self):
        self.__buscar_config()
        self.__url = f"https://dev.azure.com/{self.__organization}/_apis/projects?api-version=7.1-preview.4"
        self.__headers = { "Authorization": f"Basic {self.__pat}" }

        response = requests.get(self.__url, headers=self.__headers)

        if response.status_code == 200:
            projects_response = json.loads(response.text)
            return [item["name"] for item in projects_response["value"]]
        else:
            return "Erro ao obter a lista de Projetos:", response.status_code, response.reason