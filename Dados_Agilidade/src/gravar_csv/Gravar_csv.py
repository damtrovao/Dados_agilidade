import csv
import os

class Gravar_csv(object):
    def __init__(self, arquivo):
        self.work_item_info = {
            "WorkItemId": None,
            "Title": None,
            "ProjectName": None,
            "CreatedDate": None,
            "InProgressDate": None,
            "ClosedDate": None,
            "LeadTimeDays": None,
            "CycleTimeDays": None,
            "WorkItemType": None,
            "State": None
        }
        self.set_file_path(arquivo)
            
        self.__is_first_row = True

        self.work_item_updates = {
            "WorkItemId": None,
            "Revision": None,
            "revisedDate": None,
            "OldBoardColumn": None,
            "NewBoardColumn": None,
            "TempoNaColuna": None
        }

    def gravar_wi_info(self, dados, projeto):
        if self.__is_first_row:
            self.__gravar_nomes_colunas_wi_info()
            self.__is_first_row = False

        self.work_item_info["WorkItemId"] = dados["WorkItemId"]
        self.work_item_info["Title"] = dados["Title"]
        self.work_item_info["ProjectName"] = projeto
        self.work_item_info["CreatedDate"] = dados["CreatedDate"]
        self.work_item_info["InProgressDate"] = dados["InProgressDate"]
        self.work_item_info["ClosedDate"] = dados["ClosedDate"]
        self.work_item_info["LeadTimeDays"] = dados["LeadTimeDays"]
        self.work_item_info["CycleTimeDays"] = dados["CycleTimeDays"]
        self.work_item_info["WorkItemType"] = dados["WorkItemType"]
        self.work_item_info["State"] = dados["State"]

        decimal_separator = ","
        for key in ["LeadTimeDays", "CycleTimeDays"]:
            if self.work_item_info[key] is not None:
                self.work_item_info[key] = str(self.work_item_info[key]).replace(".", decimal_separator)

        with open(self.__file_path, mode='a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')
            csv_writer.writerow(self.work_item_info.values())

    def __gravar_nomes_colunas_wi_info(self):
        self.work_item_info["WorkItemId"] = "Work Item Id"
        self.work_item_info["Title"] = "Title"
        self.work_item_info["ProjectName"] = "Projeto"
        self.work_item_info["CreatedDate"] = "Created Date"
        self.work_item_info["InProgressDate"] = "In Progress Date"
        self.work_item_info["ClosedDate"] = "Closed Date"
        self.work_item_info["LeadTimeDays"] = "Lead Time Days"
        self.work_item_info["CycleTimeDays"] = "Cycle Time Days"
        self.work_item_info["WorkItemType"] = "Work Item Type"
        self.work_item_info["State"] = "State"

        decimal_separator = ","
        for key in ["LeadTimeDays", "CycleTimeDays"]:
            if self.work_item_info[key] is not None:
                self.work_item_info[key] = str(self.work_item_info[key]).replace(".", decimal_separator)

        with open(self.__file_path, mode='a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')
            csv_writer.writerow(self.work_item_info.values())

    def gravar_wi_updates(self, dados):
        if self.__is_first_row:
            self.__gravar_nomes_colunas_wi_updates()
            self.__is_first_row = False

        self.work_item_updates["WorkItemId"] = dados["WorkItemId"]
        self.work_item_updates["Revision"] = dados["Revision"]
        self.work_item_updates["revisedDate"] = dados["revisedDate"]
        self.work_item_updates["OldBoardColumn"] = dados["OldBoardColumn"]
        self.work_item_updates["NewBoardColumn"] = dados["NewBoardColumn"]
        self.work_item_updates["TempoNaColuna"] = dados["TempoNaColuna"]

        decimal_separator = ","
        for key in ["TempoNaColuna"]:
            if self.work_item_updates[key] is not None:
                self.work_item_updates[key] = str(self.work_item_updates[key]).replace(".", decimal_separator)

        with open(self.__file_path, mode='a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')
            csv_writer.writerow(self.work_item_updates.values())

    def __gravar_nomes_colunas_wi_updates(self):
        self.work_item_updates["WorkItemId"] = "Work Item Id"
        self.work_item_updates["Revision"] = "Revision"
        self.work_item_updates["revisedDate"] = "Revised Date"
        self.work_item_updates["OldBoardColumn"] = "Old Board Column"
        self.work_item_updates["NewBoardColumn"] = "New Board Column"
        self.work_item_updates["TempoNaColuna"] = "Tempo Na Coluna"

        with open(self.__file_path, mode='a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')
            csv_writer.writerow(self.work_item_updates.values())

    def set_file_path(self, arquivo):
        self.__file_path = arquivo