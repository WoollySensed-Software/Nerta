import Nerta.custom_types as nt

from Nerta.Handlers.BasicH import BasicHandler


class KpiHandler(BasicHandler):

    def __init__(self, ws_title):
        super().__init__(ws_title)
    
    def get_df_sample(self) -> nt.TypeSampleDataFrame:
        df = {'Знание.Лекторий': {'aim': None, 'aim_new': None, 
                                  'check_in': None,'validity': None}, 
              'Знание.Государство': {'aim': None, 'aim_new': None, 
                                     'check_in': None,'validity': None}, 
              'ЦА Школьники': {'aim': None, 'aim_new': None, 
                               'check_in': None,'validity': None}, 
              'ЦА Студенты': {'aim': None, 'aim_new': None, 
                              'check_in': None,'validity': None}, 
              'ЦА Ветераны СВО': {'aim': None, 'aim_new': None, 
                                  'check_in': None,'validity': None}, 
              'ЦА Работающая молодежь': {'aim': None, 'aim_new': None, 
                                         'check_in': None,'validity': None}, 
              'ЦА Родители': {'aim': None, 'aim_new': None, 
                              'check_in': None,'validity': None}, 
              'ЦА Пожилые': {'aim': None, 'aim_new': None, 
                             'check_in': None,'validity': None}}
        return df
    
    def fill_df(self) -> nt.TypeFilledDataFrame:
        df = self.get_df_sample()
        unfiltered_data = self.gs_data
        elems_gen = unfiltered_data[0]
        elems_row = [v for v in unfiltered_data[1][0] if v]

        df['Знание.Лекторий']['aim'] = elems_gen[0][0]
        df['Знание.Лекторий']['aim_new'] = elems_gen[0][1]
        df['Знание.Лекторий']['check_in'] = elems_gen[0][2]
        df['Знание.Лекторий']['validity'] = elems_gen[0][3]
        df['Знание.Государство']['aim'] = elems_gen[1][0]
        df['Знание.Государство']['aim_new'] = elems_gen[1][1]
        df['Знание.Государство']['check_in'] = elems_gen[1][2]
        df['Знание.Государство']['validity'] = elems_gen[1][3]

        df['ЦА Школьники']['aim'] = elems_row[0]
        df['ЦА Школьники']['aim_new'] = elems_row[1]
        df['ЦА Школьники']['check_in'] = elems_row[2]
        df['ЦА Школьники']['validity'] = elems_row[3]

        df['ЦА Студенты']['aim'] = elems_row[4]
        df['ЦА Студенты']['aim_new'] = elems_row[5]
        df['ЦА Студенты']['check_in'] = elems_row[6]
        df['ЦА Студенты']['validity'] = elems_row[7]

        df['ЦА Ветераны СВО']['aim'] = elems_row[8]
        df['ЦА Ветераны СВО']['aim_new'] = elems_row[9]
        df['ЦА Ветераны СВО']['check_in'] = elems_row[10]
        df['ЦА Ветераны СВО']['validity'] = elems_row[11]
        
        df['ЦА Работающая молодежь']['aim'] = elems_row[12]
        df['ЦА Работающая молодежь']['aim_new'] = elems_row[13]
        df['ЦА Работающая молодежь']['check_in'] = elems_row[14]
        df['ЦА Работающая молодежь']['validity'] = elems_row[15]

        df['ЦА Родители']['aim'] = elems_row[16]
        df['ЦА Родители']['aim_new'] = elems_row[17]
        df['ЦА Родители']['check_in'] = elems_row[18]
        df['ЦА Родители']['validity'] = elems_row[19]

        df['ЦА Пожилые']['aim'] = elems_row[20]
        df['ЦА Пожилые']['aim_new'] = elems_row[21]
        df['ЦА Пожилые']['check_in'] = elems_row[22]
        df['ЦА Пожилые']['validity'] = elems_row[23]

        return df
    
    def get_last_row(self, col: int) -> int:
        return len(self.api.worksheet.col_values(col)[3:]) + 3
    
    def upd_kpi_data(self, updates: list) -> nt.TypeNothing:
        self.api.worksheet.batch_update(updates)
