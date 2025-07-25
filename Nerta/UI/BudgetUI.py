import streamlit as st

from Nerta.Handlers.BudgetH import BudgetHandler


title = 'Бюджет_Q3'
budget_h = BudgetHandler(title)
gs_data = budget_h.get_data_safe()
budget_h.gs_data = gs_data
df = budget_h.fill_df()

pd_df = budget_h.to_pandas(df).T
pd_df.index.name = 'Проект'
pd_df.columns = ['Бюджет', 'Остаток']
pd_df_s = pd_df.style.set_properties(**{'color': 'black', 'background-color': '#EADDCA'}, 
                                        subset=['Остаток'])

st.dataframe(pd_df_s)
