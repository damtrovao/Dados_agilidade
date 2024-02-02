import asyncio
import aiohttp
from utils.Ler_config import Ler_config as Ler_config

class Get_updates_api(object):
    def __init__(self):
        self.__url = None
        self.__organization = None
        self.__pat = None
        self.__headers = None

    def __buscar_config(self):
        configuracoes = Ler_config()
        self.__pat = configuracoes.get_pat()
        self.__organization = configuracoes.get_organization()

    async def ler_updates(self, work_item_id,session):
        self.__buscar_config()
        self.__url = f"https://dev.azure.com/{self.__organization}/_apis/wit/workItems/{work_item_id}/updates"
        self.__headers = { "Authorization": f"Basic {self.__pat}" }

        for tentativa in range(1,5):
            try:
                async with session.get(self.__url, headers=self.__headers) as response:

                    return await response.json()
            except (asyncio.TimeoutError, aiohttp.ClientError) as e:
                print(f"Erro ao obter a lista de updates para o Work Item {work_item_id}, tentativa {tentativa}/5: {e}")
            
                await asyncio.sleep(1)

        print(f"Falha ao obter a lista de updates para o Work Item {work_item_id} em 5 tentativas")
        return None
