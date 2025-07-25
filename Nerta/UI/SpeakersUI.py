import streamlit as st
import time

from gspread.utils import rowcol_to_a1

from Nerta.Handlers.SpeakersH import SpeakersHandler
from Nerta.DBModule import DatabaseModule


def chage_flag():
    current_flag = st.session_state['UserSettings']['speakers_flag']
    st.session_state['UserSettings']['speakers_flag'] = not current_flag

    db = DatabaseModule()
    db.upd_user_settings('user_settings', st.session_state['UserSettings']['login'], 
                         {'speakers_flag': not current_flag})


title = 'Спикеры'
speakers_h = SpeakersHandler(title)
gs_data = speakers_h.get_data_safe()
speakers_h.gs_data = gs_data
speakers_h.speakers_data = speakers_h.get_speakers_data()
df = speakers_h.fill_df()

col1, col2 = st.columns([0.15, 0.85])

# Сводка по спикерам
with col1.expander('Сводка по спикерам', icon=':material/person_check:'):
    deep_scan = st.toggle('Отсеять спикеров без документов?', 
                          value=st.session_state['UserSettings']['speakers_flag'], 
                          on_change=chage_flag)

    totals_df = {'Всего': len(gs_data), 
                 'Без анкеты': speakers_h.get_count_no_form(deep_scan, df), 
                 'Без карточки': speakers_h.get_count_no_card(deep_scan, df), 
                 'Без соглашения': speakers_h.get_count_no_agree(deep_scan, df)}
    totals_df = speakers_h.to_pandas([totals_df]).T
    totals_df.columns = ['Значение']
    totals_df.index.name = 'Спикеров'

    st.dataframe(totals_df)

# Таблица документов спикеров
with col2.expander('Таблица документов спикеров', icon=':material/dataset:'):
    pd_df = speakers_h.to_pandas(df)
    pd_df.index.name = 'Строка'
    pd_df.index += 2
    st.dataframe(pd_df)

# Формы для работы с таблицей
with st.expander('Формы для работы с таблицей', icon=':material/checkbook:'):
    with st.form('Form_add_speaker', clear_on_submit=True):
        st.markdown(':red[Добавление спикера в БД]')
        name = st.text_input('Спикер', placeholder='Иванов Иван Иванович')
        flag = st.toggle('Спикер без фамилии')

        if st.form_submit_button('Добавить', icon=':material/add:'):
            try:
                if not flag:
                    l_name, f_name, m_name = name.strip().split(' ')
                else:
                    l_name, f_name = name.strip().split(' ')
            except ValueError:
                st.warning('Поле неверно заполнено!', 
                            icon=':material/warning:')
                st.stop()

            if not speakers_h.validate_speaker(name, df):
                speakers_h.add_speaker(name)
                speakers_h.upd_cache()
                
                with st.spinner('Спикер успешно добавлен', show_time=True):
                    time.sleep(3)
                
                st.rerun()
            else: st.error(f'Не вышло добавить спикера! {name} ' + 
                           'уже есть в таблице', icon='🚨')
    
    with st.form('Form_edit_speaker_data', clear_on_submit=True):
        st.markdown(':red[Изменение наличия документов у спикера]')
        name = st.selectbox('Спикер', options=df['Спикер'])
        types = ('Без изменений', 'Есть', 'Нет')
        col_1, col_2, col_3, col_4 = st.columns(4)

        with col_1:
            form = st.selectbox('Анкета', options=types)
            card = st.selectbox('Карточка', options=types)
        
        with col_2:
            id_ = st.selectbox('Паспорт', options=types)
            visa = st.selectbox('Прописка', options=types)
        
        with col_3:
            inn = st.selectbox('ИНН', options=types)
            snils = st.selectbox('СНИЛС', options=types)
        
        with col_4:
            details = st.selectbox('Реквизиты', options=types)
            agreement = st.selectbox('Соглашение', options=types)
        
        if st.form_submit_button('Изменить', icon=':material/edit:'):
            cell = speakers_h.find_name(name)
            fields = [(2, form), (3, card), (4, id_), (5, visa), 
                      (6, inn), (7, snils), (8, details), (9, agreement)]
            updates = []
            
            for col, val in fields:
                if val != 'Без изменений':
                    updates.append({'range': f'{rowcol_to_a1(cell.row, col)}', 
                                    'values': [[val]]})
            
            if updates:
                speakers_h.upd_speaker_data(updates)
                speakers_h.upd_cache()

                with st.spinner('Изменения были применены', show_time=True):
                    time.sleep(3)
                
                st.rerun()
            else: st.warning('Внести изменения не удалось', icon=':material/warning:')
