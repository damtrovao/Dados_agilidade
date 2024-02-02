from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from utils.Ler_config import Ler_config as Ler_config

class Upload_csv(object):
    def __init__(self, arquivo):
        
        self.set_file_path(arquivo)

    def __buscar_config(self):
        configuracoes = Ler_config()
        self.__account_name = configuracoes.get_account_name()
        self.__account_key = configuracoes.get_account_key()
            
    def upload(self):
        self.__buscar_config()

        blob_service_client = BlobServiceClient(account_url=f"https://{self.__account_name}.blob.core.windows.net", credential=self.__account_key)

        container_name = "scripts"
        blob_name = "column_change.csv"
        
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)

        if blob_client.exists():
            arquivo_historico = blob_client.download_blob().readall()
            with open(self.__file_path, "rb") as arquivo_novo:
                arquivos_combinados = arquivo_historico + arquivo_novo.read()
            blob_client.upload_blob(arquivos_combinados, overwrite=True)
        else:
            with open(self.__file_path, "rb") as data:
                blob_client.upload_blob(data)


    def set_file_path(self, arquivo):
        self.__file_path = arquivo