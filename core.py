import streamlit as st

from Nerta.UI.AuthUI import AuthUI
from Nerta.CoreProcessor import CoreProcessor


core = CoreProcessor()

core.set_basic_states()
core.set_site_cfg('Nerta | Дашборд', 
                  icon='Nerta/Resources/NERTA_icon_logo.png', 
                  logo='Nerta/Resources/NERTA_icon_logo.png')

if not st.session_state['AuthStatus']:
    auth_ui = AuthUI()
    tab_sign_in, tab_sign_up = st.tabs(['Авторизация', 'Создание аккаунта'])

    with tab_sign_in:
        auth_ui.sign_in()

    with tab_sign_up:
        auth_ui.sign_up()
else:
    if st.session_state['AccessStatus']:
        navigation = st.navigation(core.get_pages_struct(), position='top')
        navigation.run()
    else:
        st.header(':red[:material/sentiment_dissatisfied: ' + 
                    'Вы не имеете доступ к сайту. ' + 
                    'За подробностями обратитесь к администратору]')
