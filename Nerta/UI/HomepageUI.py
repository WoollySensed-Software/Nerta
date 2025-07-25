import streamlit as st

from Nerta.Handlers.LinksH import LinksHandler
from Nerta.Handlers.ContractsH import ContractsHandler
from Nerta.Handlers.KpiH import KpiHandler
from Nerta.Handlers.BudgetH import BudgetHandler
from Nerta.DBModule import DatabaseModule

db = DatabaseModule()
links_h = LinksHandler('Ссылки')
links_h.gs_data = links_h.get_data_safe()
contracts_h = ContractsHandler('Договоры')
contracts_h.gs_data = contracts_h.get_data_safe()
kpi_h = KpiHandler('КПЭ_Q3')
kpi_h.gs_data = kpi_h.get_data_safe()
budget_h = BudgetHandler('Бюджет_Q3')
budget_h.gs_data = budget_h.get_data_safe()

with st.sidebar.form('Form_edit_metrics'):
    links_long = st.slider('Кол-во отображаемых строк в :red[ссылках]', 
                           min_value=3, max_value=15, step=1, 
                           value=st.session_state['UserSettings']['homep_links_long'])
    contracts_long = st.slider('Кол-во отображаемых строк в :red[договорах]', 
                               min_value=3, max_value=15, step=1, 
                               value=st.session_state['UserSettings']['homep_contracts_long'])
    
    if st.form_submit_button('Применить изменения'):
        st.session_state['UserSettings'].update({'homep_links_long': links_long, 
                                                 'homep_contracts_long': contracts_long})
        db.upd_user_settings('user_settings', st.session_state['UserSettings']['login'], 
                             {'homep_links_long': links_long, 
                              'homep_contracts_long': contracts_long})

with st.sidebar.form('Form_update_cache'):
    options = ('КПЭ_Q3', 'Бюджет_Q3', 'Ссылки', 'Договоры')
    option = st.selectbox('Обновить данные для', options=options, 
                          accept_new_options=True)
    
    if st.form_submit_button('Обновить'):
        st.session_state['Cache'].pop(option, None)
        st.rerun()

col_1, col_2 = st.columns(2)

with col_1.expander('КПЭ', expanded=not st.session_state['IsMobile'], icon=':material/analytics:'):
    kpi_df = kpi_h.fill_df()
    kpi_pd_df = kpi_h.to_pandas(kpi_df).T
    kpi_pd_df.columns = ['План основной', 'План новый', 'Факт', '%']
    kpi_pd_df.index.name = 'ЦА'
    pd_df_s = kpi_pd_df.style.set_properties(**{'color': 'black', 
                                                'background-color': "#B19C7D"}, 
                                             subset=['План новый'])

    st.dataframe(pd_df_s)

with col_2.expander('Бюджет', expanded=not st.session_state['IsMobile'], icon=':material/currency_ruble:'):
    budget_df = budget_h.fill_df()
    budget_pd_df = budget_h.to_pandas(budget_df).T
    budget_pd_df.index.name = 'Проект'
    budget_pd_df.columns = ['Бюджет', 'Остаток']
    pd_df_s = budget_pd_df.style.set_properties(**{'color': 'black', 
                                                   'background-color': '#B19C7D'}, 
                                                subset=['Остаток'])

    st.dataframe(pd_df_s)

with st.expander('Последние операции из таблиц', expanded=not st.session_state['IsMobile'], icon=':material/history:'):
    links_long_ = st.session_state['UserSettings']['homep_links_long']
    st.markdown(f':red[Последние {links_long_} операций из таблицы с ссылками]')
    links_df = links_h.fill_df(links_long_)
    links_pd_df = links_h.to_pandas(links_df)
    links_pd_df.index.name = 'Строка'
    links_pd_df.index += len(links_h.gs_data) - (links_long_ - 4) - 2
    
    st.dataframe(links_pd_df)

    contracts_long_ = st.session_state['UserSettings']['homep_contracts_long']
    st.markdown(f':red[Последние {contracts_long_} операций из таблицы с договорами]')
    contracts_df = contracts_h.fill_df(contracts_long_)
    contracts_pd_df = contracts_h.to_pandas(contracts_df)
    contracts_pd_df.index.name = 'Строка'
    contracts_pd_df.index += len(contracts_h.gs_data) - (contracts_long_ - 4) - 2
    
    st.dataframe(contracts_pd_df)
