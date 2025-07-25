import streamlit as st

from Nerta.Handlers.LinksH import LinksHandler


title = 'Ссылки'
links_h = LinksHandler(title)
gs_data = links_h.get_data_safe()
links_h.gs_data = gs_data
df = links_h.fill_df()
pd_df = links_h.to_pandas(df)
pd_df.index.name = 'Строка'
pd_df.index += 2

st.dataframe(pd_df)
