import Nerta.custom_types as nt

from Nerta.Handlers.BasicH import BasicHandler


class BudgetHandler(BasicHandler):

    def __init__(self, ws_title):
        super().__init__(ws_title)
    
    def get_df_sample(self) -> nt.TypeSampleDataFrame:
        df = {'Знание.Лекторий': None, 
              'Знание.Государство': None, 
              'ЦА Школьники': None, 
              'ЦА Студенты': None, 
              'ЦА Ветераны СВО': None, 
              'ЦА Работающая молодежь': None, 
              'ЦА Родители школьников': None, 
              'ЦА Пожилые': None}
        return df
    
    def fill_df(self) -> nt.TypeFilledDataFrame:
        df = self.get_df_sample()

        for v in self.gs_data:
            df[v[0]] = (v[1], v[2])
        
        return df
