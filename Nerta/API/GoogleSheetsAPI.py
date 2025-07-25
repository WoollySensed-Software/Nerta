import gspread as gsp
import Nerta.custom_types as nt

from Nerta.settings import TABLE_NAME, temp_path


class GoogleSheetsAPI:

    def __init__(self, ws_title: str):
        self.service_acc = gsp.service_account(temp_path)
        self.open = self.service_acc.open(TABLE_NAME)
        self.ws_title = ws_title
        self.worksheet = self.open.worksheet(self.ws_title)
 
    def get_data(self) -> nt.TypeGoogleSheetsData:
        if 'КПЭ' in self.ws_title:
            return {self.ws_title: self.worksheet.batch_get(['B4:E5', 'G3:AO3'])}
        elif 'Бюджет' in self.ws_title:
            return {self.ws_title: self.worksheet.get('A2:C9')}
        else:
            return {self.ws_title: self.worksheet.get_all_values()[1:]}
