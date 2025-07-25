import Nerta.custom_types as nt

from Nerta.Handlers.BasicH import BasicHandler


class SpeakersHandler(BasicHandler):

    def __init__(self, ws_title):
        super().__init__(ws_title)
        self.speakers_data: nt.TypeSpeakersData = ...
    
    def get_speakers_data(self) -> nt.TypeSpeakersData:
        data = []

        for v in self.gs_data:
            data.append({v[0]: {'Анкета': v[1], 
                                'Карточка': v[2], 
                                'Паспорт': v[3], 
                                'Прописка': v[4], 
                                'ИНН': v[5], 
                                'СНИЛС': v[6], 
                                'Реквизиты': v[7], 
                                'Соглашение': v[8]}})
        
        return data
    
    def get_df_sample(self) -> nt.TypeSampleDataFrame:
        df = {'Спикер': [], 
              'Анкета': [], 
              'Карточка': [], 
              'Паспорт': [], 
              'Прописка': [], 
              'ИНН': [], 
              'СНИЛС': [], 
              'Реквизиты': [], 
              'Соглашение': []}
        return df
    
    def fill_df(self) -> nt.TypeFilledDataFrame:
        df = self.get_df_sample()

        for speaker in self.speakers_data:
            for k, v in speaker.items():
                df['Спикер'].append(k)
                df['Анкета'].append(v['Анкета'])
                df['Карточка'].append(v['Карточка'])
                df['Паспорт'].append(v['Паспорт'])
                df['Прописка'].append(v['Прописка'])
                df['ИНН'].append(v['ИНН'])
                df['СНИЛС'].append(v['СНИЛС'])
                df['Реквизиты'].append(v['Реквизиты'])
                df['Соглашение'].append(v['Соглашение'])
        
        return df
    
    def get_count_no_form(self, deep_scan: bool, df: nt.TypeFilledDataFrame) -> int:
        if not deep_scan:
            return df['Анкета'].count('Нет')
        else:
            count = 0

            for speaker in self.speakers_data:
                for v in speaker.values():
                    if (v['Анкета'] == 'Нет' and 
                        v['Карточка'] != 'Нет' and 
                        v['Паспорт'] != 'Нет' and 
                        v['Прописка'] != 'Нет' and 
                        v['ИНН'] != 'Нет' and 
                        v['СНИЛС'] != 'Нет' and 
                        v['Реквизиты'] != 'Нет' and 
                        v['Соглашение'] != 'Нет'):
                        count += 1
            
            return count

    def get_count_no_card(self, deep_scan: bool, df: nt.TypeFilledDataFrame) -> int:
        if not deep_scan:
            return df['Карточка'].count('Нет')
        else:
            count = 0

            for speaker in self.speakers_data:
                for v in speaker.values():
                    if (v['Анкета'] != 'Нет' and 
                        v['Карточка'] == 'Нет' and 
                        v['Паспорт'] != 'Нет' and 
                        v['Прописка'] != 'Нет' and 
                        v['ИНН'] != 'Нет' and 
                        v['СНИЛС'] != 'Нет' and 
                        v['Реквизиты'] != 'Нет' and 
                        v['Соглашение'] != 'Нет'):
                        count += 1
            
            return count

    def get_count_no_agree(self, deep_scan: bool, df: nt.TypeFilledDataFrame) -> int:
        if not deep_scan:
            return df['Соглашение'].count('Нет')
        else:
            count = 0

            for speaker in self.speakers_data:
                for v in speaker.values():
                    if (v['Анкета'] != 'Нет' and 
                        v['Карточка'] != 'Нет' and 
                        v['Паспорт'] != 'Нет' and 
                        v['Прописка'] != 'Нет' and 
                        v['ИНН'] != 'Нет' and 
                        v['СНИЛС'] != 'Нет' and 
                        v['Реквизиты'] != 'Нет' and 
                        v['Соглашение'] == 'Нет'):
                        count += 1
            
            return count

    def add_speaker(self, name: str) -> nt.TypeNothing:
        self.api.worksheet.append_row([name, *['Нет' for _ in range(8)]])
    
    def validate_speaker(self, name: str, df: nt.TypeFilledDataFrame) -> bool:
        return name in df['Спикер']
    
    def find_name(self, name: str):
        return self.api.worksheet.find(name, in_column=1)
    
    def upd_speaker_data(self, updates: list) -> nt.TypeNothing:
        self.api.worksheet.batch_update(updates)
