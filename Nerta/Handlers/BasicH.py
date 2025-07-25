import Nerta.custom_types as nt

from pandas import DataFrame
from streamlit import session_state, markdown

from Nerta.API.GoogleSheetsAPI import GoogleSheetsAPI


class BasicHandler:

    def __init__(self, ws_title: str):
        self.ws_title = ws_title
        self.api = GoogleSheetsAPI(self.ws_title)
        self.gs_data = ...
    
    def to_pandas(self, df: nt.TypeFilledDataFrame) -> DataFrame:
        return DataFrame(df)
    
    def upd_cache(self) -> nt.TypeNothing:
        session_state['Cache'].update(self.api.get_data())
    
    def check_cache(self) -> nt.TypeNothing:
        if self.ws_title not in session_state['Cache']:
            session_state['Cache'].update(self.api.get_data())
    
    def get_data_safe(self) -> list[nt.Any]:
        self.check_cache()
        return session_state['Cache'][self.ws_title]
