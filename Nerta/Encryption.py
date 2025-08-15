import os
import hashlib


class Encryption:
    """
    Класс для шифрования и проверки паролей и ключей.
    """

    @staticmethod
    def hash_pw(_password: str) -> str:
        """
        Хэширует строку переданную в качестве аргумента.

        Параметры:
        - _password: str, принимает строку.

        Возвращает:
        - строку с последовательностью символов + соль.
        """
        
        salt = os.urandom(32).hex()
        return hashlib.sha256(
            salt.encode() + _password.encode()
        ).hexdigest() + ':' + salt

    @staticmethod
    def check_pw(_hash: str, _password: str) -> bool:
        """
        Сравнивает хэш со строкой переданной в качестве аргумента.

        Параметры:
        - _hash: str, принимает хэш-строку;
        - _password: str, принимает строку.
        
        Возвращает:
        - True, если переданный аргумент совпадает;
        - False, если переданный аргумент не совпадает.
        """

        password, salt = _hash.split(':')
        return password == hashlib.sha256(
            salt.encode() + _password.encode()
        ).hexdigest()
