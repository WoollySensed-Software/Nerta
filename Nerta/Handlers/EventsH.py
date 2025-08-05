import Nerta.custom_types as nt

from datetime import datetime, timedelta
from pytz import timezone

from Nerta.Handlers.BasicH import BasicHandler


class EventsHandler(BasicHandler):

    def __init__(self, ws_title: str = 'Договоры'):
        super().__init__(ws_title)
    
    def dt_now(self) -> datetime:
        now = datetime.now(timezone('Europe/Moscow')).strftime('%d.%m.%Y')
        return datetime.strptime(now, '%d.%m.%Y')
    
    def get_event_status(self, 
        event: nt.Literal['Статус договоров', 
                          'Статус актов', 
                          'Дата отправки актов']
    ) -> nt.TypeFilledDataFrame:
        df = {'Действие': [], 
              'Номер договора': [], 
              'Спикер': [], 
              'Дата': [], 
              'Проект': [], 
              'Этап согласования': [], 
              'ПЭП: Договор': [], 
              'ПЭП: Акт': [], 
              'Статус: Отчет': []}

        match event:
            case 'Статус договоров':
                data = self.__get_contracts_data()
            case 'Статус актов':
                data = self.__get_acts_data()
            case 'Дата отправки актов':
                data = self.__get_send_acts_data()
        
        if len(data):
            for el in data:
                for k, v in el.items():
                    if el['Действие'] is not None:
                        df[k].append(v)
        
        return df

    def __get_contracts_data(self) -> list[dict[str, nt.Any]]:
        self.ws_title = 'Договоры'
        data = self.get_data_safe()
        filtered_data = []

        for el in data:
            if el[1] == 'ПЭП':
                current_date = datetime.strptime(el[3], '%d.%m.%Y')
                termination_optins = ('Согласуется', 'Бумага', 
                                      'Отправлено', 'Подписано')
                msg = None

                # Действие на проверку подписания договора в срок
                if el[7] == 'Отправлен' and self.dt_now() <= current_date:
                    msg = ('Проверить подписание договора спикером до ' + 
                           f'{current_date.strftime('%d.%m.%Y')}')
                # Действие на проверку подписания договора после срока
                elif el[7] == 'Отправлен' and self.dt_now() > current_date:
                    msg = 'Проверить, успел ли спикер подписать договор в срок'
                # Действие по отправке отчета на проверку
                elif (el[7] == 'Подписан' and el[8] == 'Подписан' and 
                      el[9] not in termination_optins and el[10] != 'Отправлен'):
                    msg = 'Необходимо загрузить отчет по договору'
                
                filtered_data.append({'Действие': msg, 
                                      'Номер договора': el[0], 
                                      'Спикер': el[2], 
                                      'Дата': el[3], 
                                      'Проект': el[4], 
                                      'Этап согласования': el[6], 
                                      'ПЭП: Договор': el[7], 
                                      'ПЭП: Акт': el[8], 
                                      'Статус: Отчет': el[10]})
        
        return filtered_data

    def __get_acts_data(self) -> list[dict[str, nt.Any]]:
        self.ws_title = 'Договоры'
        data = self.get_data_safe()
        filtered_data = []

        for el in data:
            if el[1] == 'ПЭП':
                current_date = datetime.strptime(el[3], '%d.%m.%Y')
                end_date = current_date + timedelta(days=14)
                msg = None

                # Действие на подписание акта в срок
                if (el[7] == 'Подписан' and el[8] == 'Отправлен' and 
                    self.dt_now() <= end_date):
                    msg = ('Проверить подписание акта спикером до ' + 
                           f'{end_date.strftime('%d.%m.%Y')}')
                
                filtered_data.append({'Действие': msg, 
                                        'Номер договора': el[0], 
                                        'Спикер': el[2], 
                                        'Дата': el[3], 
                                        'Проект': el[4], 
                                        'Этап согласования': el[6], 
                                        'ПЭП: Договор': el[7], 
                                        'ПЭП: Акт': el[8], 
                                        'Статус: Отчет': el[10]})
        
        return filtered_data

    def __get_send_acts_data(self) -> list[dict[str, nt.Any]]:
        self.ws_title = 'Договоры'
        data = self.get_data_safe()
        filtered_data = []
    
        for el in data:
            if el[1] == 'ПЭП':
                current_date = datetime.strptime(el[3], '%d.%m.%Y')
                act_optins = ('Отправлен', 'Подписан')
                msg = None

                # Действие на отправку договора после даты выступления
                if (el[7] == 'Подписан' and el[8] not in act_optins and
                    self.dt_now() >= current_date + timedelta(days=1)):
                    date = current_date + timedelta(days=1)
                    msg = ('Необходимо отправить акт на подписание, начиная с ' + 
                    f'{date.strftime('%d.%m.%Y')}')

                filtered_data.append({'Действие': msg, 
                                        'Номер договора': el[0], 
                                        'Спикер': el[2], 
                                        'Дата': el[3], 
                                        'Проект': el[4], 
                                        'Этап согласования': el[6], 
                                        'ПЭП: Договор': el[7], 
                                        'ПЭП: Акт': el[8], 
                                        'Статус: Отчет': el[10]})
        
        return filtered_data

    def __get_notes_data(self): pass
