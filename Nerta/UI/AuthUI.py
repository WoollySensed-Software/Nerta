import streamlit as st

from string import digits, ascii_uppercase

from Nerta.DBModule import DatabaseModule
from Nerta.Encryption import Encryption


class AuthUI(DatabaseModule):

    def __init__(self):
        super().__init__()

    def sign_in(self):
        st.subheader(':red[Авторизация]')

        login = st.text_input('Логин', max_chars=100, autocomplete='email', 
                              placeholder='Введите почту от аккаунта', 
                              icon=':material/mail:')
        password = st.text_input('Пароль', max_chars=100, type='password', 
                                 autocomplete='current-password', 
                                 placeholder='Введите пароль от аккаунта', 
                                 icon=':material/password:')
        
        login_is_valid = self.__login_validator(login)
        password_is_valid = self.__password_validator(password)

        submit = st.button('Войти', icon=':material/account_circle:')
        
        if submit:
            if login_is_valid and password_is_valid:
                if self.__sign_in_check(login.strip(), password.strip()):
                    st.success('Вы успешно авторизовались')
                    st.session_state['AuthStatus'] = True
                    st.rerun()
                else: st.warning('Введенные данные не соответствуют данным аккаунта')
            else: st.warning('Что-то не так...')

    def sign_up(self):
        st.subheader(':red[Создание аккаунта]')

        login = st.text_input('Логин', max_chars=100, autocomplete='email', 
                              placeholder='Введите почту example@mail.com', 
                              icon=':material/mail:')
        password = st.text_input('Пароль', max_chars=100, type='password', 
                                 autocomplete='new-password', 
                                 placeholder='Не используйте простой пароль', 
                                 icon=':material/password:')
        
        login_is_valid = self.__login_validator(login)
        password_is_valid = self.__password_validator(password)

        st.markdown(':material/lock: Условия для пароля:\n\n' + 
                    ':green[:material/priority:] Должен содержать ' + 
                    'спец. символы :orange-badge[!#$%&*.:;?@^_~]\n\n' + 
                    ':green[:material/priority:] Должен содержать ' + 
                    'цифры :orange-badge[0-9]\n\n' + 
                    ':green[:material/priority:] Должен содержать ' + 
                    ':orange-badge[заглавные] буквы\n\n' + 
                    ':green[:material/priority:] Длина должна быть ' + 
                    'не менее :orange-badge[8] символов')
        st.markdown(':grey[:material/error: Чтобы получить полный доступ к ' + 
                    'сайту, администратор должен выдать его]')
        submit = st.button('Создать аккаунт', icon=':material/person_add:')

        if submit:
            if login_is_valid and password_is_valid:
                self.__create_account(login.strip(), password.strip())
                st.success('Аккаунт был успешно создан. Чтобы войти в свой ' + 
                           'аккаунт перейдите во вкладку с авторизацией', 
                           icon=':material/verified:')
    
    def __login_validator(self, login: str):
        if login == '':
            return False
        elif '@' not in login:
            st.warning('Попробуйте указать корректную почту для логина')
            return False
        elif len(login) <= 5:
            st.warning('Логин слишком короткий')
            return False
        elif '@' in login:
            return True
    
    def __password_validator(self, password: str):
        special_chars = set('!#$%&*.:;?@^_~')
        upper_case = set(ascii_uppercase)
        digits_ = set(digits)

        if password == '':
            return False
        elif not any(char in upper_case for char in password):
            st.warning('Пароль должен содержать заглавные буквы')
            return False
        elif not any(char in special_chars for char in password):
            st.warning('Пароль должен содержать спец. символы')
            return False
        elif not any(char in digits_ for char in password):
            st.warning('Пароль должен содержать цифры')
            return False
        elif len(password) < 8:
            st.warning('Длина пароля не соответствует условию')
            return False
        else: return True
    
    def __create_account(self, login: str, password: str):
        self.insert('users', {'login': login, 
                              'password': Encryption.hash_pw(password), 
                              'access_status': False})
        self.insert('user_settings', {'login': login})
    
    def __sign_in_check(self, login: str, password: str):
        data = self.get_auth_data('users', login).data[0]

        if data['login'] == login and Encryption.check_pw(data['password'], password):
            user_settings = self.get_user_settings('user_settings', login).data[0]
            st.session_state['AccessStatus'] = data['access_status']

            st.session_state['UserSettings'] = {
                'login': login, 
                'homep_links_long': user_settings['homep_links_long'], 
                'homep_contracts_long': user_settings['homep_contracts_long'], 
                'speakers_flag': user_settings['speakers_flag']}
            return True
        else: return False
