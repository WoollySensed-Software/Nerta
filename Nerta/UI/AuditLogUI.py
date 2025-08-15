import streamlit as st

from Nerta.Handlers.AuditLogH import AuditLogHandler


title = 'Журнал'
audit_log_h = AuditLogHandler(title)
gs_data = audit_log_h.get_data_safe()
audit_log_h.gs_data = gs_data
df = audit_log_h.fill_df()
pd_df = audit_log_h.to_pandas(df)
pd_df.index.name = 'Строка'
pd_df.index += 2

st.dataframe(pd_df)