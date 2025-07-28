import Nerta.custom_types as nt

from Nerta.Handlers.BasicH import BasicHandler


class ContractsHandler(BasicHandler):

    def __init__(self, ws_title):
        super().__init__(ws_title)
    
    def get_df_sample(self) -> nt.TypeSampleDataFrame:
        df = {'Номер договора': [], 
              'Тип': [], 
              'Спикер': [], 
              'Дата': [], 
              'Проект': [], 
              'Кол-во': [], 
              'Этап согласования': [], 
              'ПЭП: Договор': [], 
              'ПЭП: Акт': [], 
              'ПЭП: Расторжение': [], 
              'Статус: Отчет': [], 
              'Статус: Оплата': [], 
              'Комментарий': [], 
              '-': [], 
              'Название': [], 
              'Старт': [], 
              'Конец': [], 
              'Площадка': [], 
              'Адрес': [], 
              'Уровень слушателей': []}
        return df
    
    def fill_df(self, count: int = 0) -> nt.TypeFilledDataFrame:
        df = self.get_df_sample()

        for v in self.gs_data[-count:]:
            for k, inx in zip(df.keys(), range(len(df.keys()))):
                df[k].append(v[inx])
        
        return df
