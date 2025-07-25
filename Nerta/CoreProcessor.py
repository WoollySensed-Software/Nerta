import streamlit as st

from Nerta.custom_types import (
    TypeNothing
)


class CoreProcessor:

    def is_mobile(self) -> bool:
        try:
            user_agent = st.context.headers.get('User-Agent', '').lower()
            return any(m in user_agent for m in {'mobi', 'android', 'iphone'})
        except AttributeError:
            return False

    def set_site_cfg(self, title: str, *, icon: str, logo: str) -> TypeNothing:
        layout = 'centered' if st.session_state['IsMobile'] else 'wide'
        st.set_page_config(page_title=title, 
                           page_icon=icon, 
                           initial_sidebar_state='collapsed', 
                           layout=layout)
        st.logo(image=logo, size='large')
        st.markdown('<style>[data-testid="stDecoration"]' + 
                    '{display: none !important;}</style>', 
                    unsafe_allow_html=True)

    def set_basic_states(self) -> TypeNothing:
        if 'Cache' not in st.session_state:
            st.session_state['Cache'] = dict()
        if 'IsMobile' not in st.session_state:
            st.session_state['IsMobile'] = self.is_mobile()
        if 'AuthStatus' not in st.session_state:
            st.session_state['AuthStatus'] = False
        if 'AccessStatus' not in st.session_state:
            st.session_state['AccessStatus'] = False
        if 'UserSettings' not in st.session_state:
            st.session_state['UserSettings'] = {'login': None, 
                                                'homep_links_long': 5, 
                                                'homep_contracts_long': 5, 
                                                'speakers_flag': False}

    def get_pages_struct(self) -> dict:
        pages = {'Главная': [st.Page(page='Nerta/UI/HomepageUI.py', 
                                     title='Главная страница', 
                                     icon=None)], 
                 'КПЭ': [st.Page(page='Nerta/UI/KpiUI.py', 
                                 title='КПЭ', 
                                 icon=None)], 
                 'Бюджет': [st.Page(page='Nerta/UI/BudgetUI.py', 
                                    title='Бюджет', 
                                    icon=None)], 
                 'Таблицы': [st.Page(page='Nerta/UI/AuditLogUI.py', 
                                     title='Журнал', 
                                     icon=None), 
                             st.Page(page='Nerta/UI/LinksUI.py', 
                                     title='Ссылки', 
                                     icon=None), 
                             st.Page(page='Nerta/UI/ContractsUI.py', 
                                     title='Договоры', 
                                     icon=None), 
                             st.Page(page='Nerta/UI/SpeakersUI.py', 
                                     title='Спикеры', 
                                     icon=None)]}
        return pages

    def exp_clear_cache(self) -> TypeNothing:
        st.session_state['Cache'] = dict()
