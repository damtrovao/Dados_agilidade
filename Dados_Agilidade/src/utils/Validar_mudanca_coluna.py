from datetime import datetime
from utils.Ler_config import Ler_config as Ler_config

class Validar_mudanca_coluna(object):
    def __init__(self):
        self.updates_reg = {
        "WorkItemId": None,
        "Revision": None,
        "revisedDate": None,
        "OldBoardColumn": None,
        "NewBoardColumn": None,
        "TempoNaColuna": None
        }
        self.date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        self.date_format_2 = "%Y-%m-%dT%H:%M:%SZ"
        
    def processar_mudanca(self, updates):
        self.updates_reg['Revision'] = updates['rev']
        self.updates_reg['revisedDate'] = updates['revisedDate']

        if not self.updates_reg['revisedDate'].startswith("9999"):
            if ("fields" in updates and "System.BoardColumn" in updates['fields'] and "newValue" in updates['fields']['System.BoardColumn']):
                self.updates_reg['NewBoardColumn'] = updates['fields']['System.BoardColumn']['newValue']

                if "oldValue" in updates['fields']['System.BoardColumn']:
                    self.updates_reg['OldBoardColumn'] = updates['fields']['System.BoardColumn']['oldValue']

                    if self.updates_reg['revisedDate'].startswith("999"):
                        if 'Microsoft.VSTS.Common.ClosedDate' in updates['fields'] and 'newValue' in updates['fields']['Microsoft.VSTS.Common.ClosedDate']:
                            data_fechamento = updates['fields']['Microsoft.VSTS.Common.ClosedDate']['newValue']
                            try:
                                revised_date_formatada = datetime.strptime(data_fechamento, self.date_format)
                            except ValueError:
                                try:
                                    revised_date_formatada = datetime.strptime(data_fechamento, self.date_format_2)
                                except ValueError:
                                    print("Erro de formatação da data de fechamento ", updates)    
                                    #continue    
                        else:
                            print("Erro de data de fechamento ", updates)
                    else:
                        try:
                            revised_date_formatada = datetime.strptime(self.updates_reg['revisedDate'], self.date_format)
                        except ValueError:
                            try:
                                revised_date_formatada = datetime.strptime(self.updates_reg['revisedDate'], self.date_format_2)
                            except ValueError:
                                print("Erro de formatação da data de revisão ", updates)    
                                #continue    
                    
                    self.updates_reg['TempoNaColuna'] = (revised_date_formatada - data_mudanca_anterior).total_seconds()/86400 
                    
                    gravar_wi_column_change.gravar_wi_updates(self.updates_reg)
                
                if self.updates_reg['revisedDate'].startswith("9999"):
                    data_mudanca_anterior = revised_date_formatada
                else: 
                    try:
                        data_mudanca_anterior = datetime.strptime(self.updates_reg['revisedDate'], self.date_format)
                    except ValueError:
                        try:
                            data_mudanca_anterior = datetime.strptime(self.updates_reg['revisedDate'], self.date_format_2)
                        except ValueError:
                            print("Erro de formatação da data de revisão ", updates)    
                            #continue