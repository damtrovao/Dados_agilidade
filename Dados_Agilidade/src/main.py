import aiohttp
import asyncio
from get_projects.Get_projects_api import Get_projects_api
from get_work_items.Get_work_items_api import Get_work_items_api
from get_updates.Get_updates_api import Get_updates_api
from upload_csv.Upload_csv import Upload_csv
from gravar_csv.Gravar_csv import Gravar_csv
from datetime import datetime, timedelta


async def main():

    data_mudanca_anterior = None
    revised_date_formatada = None
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    date_format_2 = "%Y-%m-%dT%H:%M:%SZ"
    CHUNK_SIZE = 2000

    updates_reg = {
        "WorkItemId": None,
        "Revision": None,
        "revisedDate": None,
        "OldBoardColumn": None,
        "NewBoardColumn": None,
        "TempoNaColuna": None
        }

    gravar_wi_column_change = Gravar_csv('column_change.csv')
    upload_arquivo = Upload_csv('column_change.csv')

    today = datetime.now()
    periodo = today - timedelta(days=1)
    filter_revised_date = periodo.strftime("%Y-%m-%d")

    projetos = Get_projects_api()
    response_projetos = projetos.ler_projetos()    

    for project in response_projetos:

        work_items = Get_work_items_api()
        response_work_items = work_items.ler_work_items(project)

        if response_work_items:
            updates_api = Get_updates_api()
            
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=20)) as session:
                lista_completa_updates = []
                for chunk_start in range(0, len(response_work_items),CHUNK_SIZE):
                    chunk = response_work_items[chunk_start:chunk_start+CHUNK_SIZE]
                    tasks = [fetch_updates(work_item_id, session, updates_api) for work_item_id in chunk]

                    lista_updates = await asyncio.gather(*tasks)
                    lista_completa_updates.extend(lista_updates)

            for work_item, updates in zip(response_work_items, lista_completa_updates):

                #Limpando o dicionário de possíveis items anteriores
                for key in updates_reg:
                    updates_reg[key] = None
                # --------------------------------------------------
                
                updates_reg['WorkItemId'] = work_item
                
                if isinstance(updates, dict):
                    
                    for work_item_update in updates['value']:

                        updates_reg['Revision'] = work_item_update['rev']
                        updates_reg['revisedDate'] = work_item_update['revisedDate']


                        if not updates_reg['revisedDate'].startswith("9999"):
                            if ("fields" in work_item_update and "System.BoardColumn" in work_item_update['fields'] and "newValue" in work_item_update['fields']['System.BoardColumn']):

                                updates_reg['NewBoardColumn'] = work_item_update['fields']['System.BoardColumn']['newValue']

                                if "oldValue" in work_item_update['fields']['System.BoardColumn']:
                                    updates_reg['OldBoardColumn'] = work_item_update['fields']['System.BoardColumn']['oldValue']

                                    if updates_reg['revisedDate'].startswith("999"):
                                        if 'Microsoft.VSTS.Common.ClosedDate' in work_item_update['fields'] and 'newValue' in work_item_update['fields']['Microsoft.VSTS.Common.ClosedDate']:
                                            data_fechamento = work_item_update['fields']['Microsoft.VSTS.Common.ClosedDate']['newValue']
                                            try:
                                                revised_date_formatada = datetime.strptime(data_fechamento, date_format)
                                            except ValueError:
                                                try:
                                                    revised_date_formatada = datetime.strptime(data_fechamento, date_format_2)
                                                except ValueError:
                                                    print("Erro de formatação da data de fechamento ", work_item_update)    
                                                    continue    
                                        else:
                                            print("Erro de data de fechamento ", work_item_update)
                                    else:
                                        try:
                                            revised_date_formatada = datetime.strptime(updates_reg['revisedDate'], date_format)
                                        except ValueError:
                                            try:
                                                revised_date_formatada = datetime.strptime(updates_reg['revisedDate'], date_format_2)
                                            except ValueError:
                                                print("Erro de formatação da data de revisão ", work_item_update)    
                                                continue    
                                    updates_reg['TempoNaColuna'] = (revised_date_formatada - data_mudanca_anterior).total_seconds()/86400 
                                    
                                    if work_item_update['revisedDate'] >= filter_revised_date and not work_item_update['revisedDate'].startswith("999"):
                                        gravar_wi_column_change.gravar_wi_updates(updates_reg)
                                
                                if updates_reg['revisedDate'].startswith("9999"):
                                    data_mudanca_anterior = revised_date_formatada
                                else: 
                                    try:
                                        data_mudanca_anterior = datetime.strptime(updates_reg['revisedDate'], date_format)
                                    except ValueError:
                                        try:
                                            data_mudanca_anterior = datetime.strptime(updates_reg['revisedDate'], date_format_2)
                                        except ValueError:
                                            print("Erro de formatação da data de revisão ", work_item_update)    
                                            continue    

    upload_arquivo.upload()
                    
async def fetch_updates(work_item_id, session, updates_api):
    for tentativa in range(1, 5):
        try:
            updates = await updates_api.ler_updates(work_item_id, session)
            return updates
        except aiohttp.ClientOSError as e:
            print(f"Erro ao buscar updates do work item {work_item_id}, tentativa {tentativa}/5: {e}")
            await asyncio.sleep(1)
    
    print(f"Falha ao buscar updates do work item {work_item_id} depois de 5 tentativas.")
    return None

if __name__ == "__main__":
    asyncio.run(main())