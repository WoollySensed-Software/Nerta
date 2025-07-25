import Nerta.custom_types as nt

from Nerta.Handlers.BasicH import BasicHandler


class AuditLogHandler(BasicHandler):

    def __init__(self, ws_title):
        super().__init__(ws_title)
    
    def get_df_sample(self) -> nt.TypeSampleDataFrame:
        df = {'Спикер': [], 
              'Дата': [], 
              'Проект': [], 
              'Название': [], 
              'Кол-во': [], 
              'Комментарий': [], 
              'Статус: Ссылка': [], 
              'Статус: Договор': [], 
              'Номер договора': [], 
              'Гонорар': []}
        return df
    
    def fill_df(self) -> nt.TypeFilledDataFrame:
        df = self.get_df_sample()

        for v in self.gs_data:
            for k, inx in zip(df.keys(), range(len(df.keys()))):
                df[k].append(v[inx])
        
        return df
