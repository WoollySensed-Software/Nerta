import streamlit as st

from Nerta.Handlers.ContractsH import ContractsHandler


title = 'Договоры'
contracts_h = ContractsHandler(title)
gs_data = contracts_h.get_data_safe()
contracts_h.gs_data = gs_data
df = contracts_h.fill_df()
pd_df = contracts_h.to_pandas(df)
pd_df.index.name = 'Строка'
pd_df.index += 2

st.dataframe(pd_df)
