import streamlit as st
import time

from gspread.utils import rowcol_to_a1

from Nerta.Handlers.KpiH import KpiHandler


title = 'КПЭ_Q3'
kpi_h = KpiHandler(title)
gs_data = kpi_h.get_data_safe()
kpi_h.gs_data = gs_data
df = kpi_h.fill_df()
col_left, col_right = st.columns([0.3, 0.7])

# Сводка КПЭ
with col_left.expander('Сводка по КПЭ', icon=':material/analytics:'):
    pd_df = kpi_h.to_pandas(df).T
    pd_df.columns = ['План основной', 'План новый', 'Факт', '%']
    pd_df.index.name = 'ЦА'
    pd_df_s = pd_df.style.set_properties(**{'color': 'black', 'background-color': '#EADDCA'}, 
                                        subset=['План новый'])

    st.dataframe(pd_df_s)

# Формы для работы с КПЭ
with col_right.expander('Формы для работы с КПЭ', icon=':material/table:'):
    with st.form('Form_add_kpi_data', clear_on_submit=True):
        targets = {'ЦА Школьники': [7, 10], 
                   'ЦА Студенты': [13, 16], 
                   'ЦА Ветераны СВО': [19, 22], 
                   'ЦА Работающая молодежь': [25, 28],
                   'ЦА Родители': [31, 34], 
                   'ЦА Пожилые': [37, 40], 
                   'ФОИВ': [43, 46]}
        col1, col2 = st.columns(2)

        date = col1.date_input('Дата проведения', format='DD.MM.YYYY')
        number = col2.number_input('Кол-во check-in', min_value=0, step=1, 
                                   icon=':material/man_2:')
        target = st.selectbox('Выбор ЦА', options=targets.keys())

        if st.form_submit_button('Добавить', icon=':material/add:'):
            if number:
                col_a, col_b = targets[target]
                row = kpi_h.get_last_row(col_a) + 1
                date = date.strftime('%d.%m.%Y')
                updates = [{'range': rowcol_to_a1(row, col_a), 'values': [[date]]}, 
                           {'range': rowcol_to_a1(row, col_b), 'values': [[number]]}]
                
                kpi_h.upd_kpi_data(updates)
                kpi_h.upd_cache()

                with st.spinner('Данные были внесены', show_time=True):
                    time.sleep(3)

                st.rerun()
            else: st.warning('Нельзя выставить :red[0]', icon=':material/warning:')
