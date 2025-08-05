import streamlit as st

from Nerta.Handlers.EventsH import EventsHandler


events_h = EventsHandler()
col1, col2, col3 = st.columns(3)

# договоры
contracts_df = events_h.get_event_status('Статус договоров')
contracts_pd_df = events_h.to_pandas(contracts_df)

col1.markdown(':red[Подписание договоров]')
col1.dataframe(contracts_pd_df)

# отправка актов
send_acts_df = events_h.get_event_status('Дата отправки актов')
send_acts_pd_df = events_h.to_pandas(send_acts_df)

col2.markdown(':red[Отправка актов]')
col2.dataframe(send_acts_pd_df)

# акты
acts_df = events_h.get_event_status('Статус актов')
acts_pd_df = events_h.to_pandas(acts_df)

col3.markdown(':red[Подписание актов]')
col3.dataframe(acts_pd_df)
