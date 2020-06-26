import hashlib
import random
import os
from Crypto import Random
from Crypto.Cipher import AES
from colorama import init
from colorama import Fore, Back, Style
init(autoreset=True)


class Security:
    def __init__(self) -> None:
        self._SALT = b'8_TuDUK9IpJKaM7NWkpSQcMlVh0ZoEmYdeIOjvItOSk='
        self._BLOCK_SIZE = 16
        self._IV456 = b'yo_esK1DOHg2x-3L'

    def gen_user_secret_key(self, password: str) -> str:
        if isinstance(password, str) is False:
            raise TypeError(Fore.RED + "•Неверный тип данных!")
        salt_s = '8_TuDUK9IpJKaM7NWkpSQcMlVh0ZoEmYdeIOjvItOSk='
        salt_b = self._SALT
        hash_pass = hashlib.sha256(salt_b + password.encode()).hexdigest() + '|' + salt_s
        return hash_pass

    def gen_master_key(self, password: str) -> bytes:
        if isinstance(password, str) is False:
            raise TypeError(Fore.RED + "Неверный тип данных!")
        master_key = hashlib.pbkdf2_hmac('sha256', password.encode(), self._SALT, 100000)
        return master_key

    def gen_secret_key(self) -> bytes:
        return Random.new().read(32)

    def __fill_random_bytes(self, text: bytes, length: int) -> bytes:
        while len(text) % length != 0:  # кратно 16 байт
            symbol = bytes()
            if len(text) > 0:
                pos = random.randint(0, len(text))
                symbol = text[pos: pos + 1]
            text += symbol
        return text

    def encrypt(self, message: bytes, secret_key: bytes) -> bytes:
        if isinstance(message, bytes) is False:
            raise TypeError(Fore.RED + "•Неверный тип текста")
        if isinstance(secret_key, bytes) is False:
            raise TypeError(Fore.RED + "•Неверный тип ключа")
        len_block = len(message).to_bytes(length=self._BLOCK_SIZE, byteorder='big')
        message = len_block + message
        message_byte = self.__fill_random_bytes(message, self._BLOCK_SIZE)
        object = AES.new(secret_key, AES.MODE_CBC, self._IV456)
        cipher_text = object.encrypt(message_byte)
        return cipher_text

    def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        if isinstance(ciphertext, bytes) is False:
            raise TypeError(Fore.RED + "•Неверный тип текста")
        if isinstance(key, bytes) is False:
            raise TypeError(Fore.RED + "•Неверный тип ключа")
        if len(ciphertext) % self._BLOCK_SIZE != 0:
            raise ValueError(Fore.RED + "•Длина шифротекста не кратна блоку")
        object = AES.new(key, AES.MODE_CBC, self._IV456)
        text = object.decrypt(ciphertext)
        size = int.from_bytes(text[:self._BLOCK_SIZE], byteorder='big')
        text = text[self._BLOCK_SIZE:size + self._BLOCK_SIZE]
        return text

    def get_correct_str(self, type: str) -> str:
        wrong_simbols = ["\\", "/", ":", "*", "?", "\"", "|", "<", ">"]
        while True:
            flag = True
            user = str(input(f'Введите {type}: '))
            if len(user) == 0:
                print(Fore.RED + '•Недопустимая длина!')
                flag = False
            else:
                for i in range(len(user)):
                    for j in range(len(wrong_simbols)):
                        if user[i] == wrong_simbols[j]:
                            print(Fore.RED + '•Недопустимые символы!')
                            flag = False
            if flag:
                return user

    def get_password(self) -> str:
        while True:
            password = str(input('•Введите пароль: '))
            if len(password) == 0:
                print(Fore.RED + '•Недопустимая длина!')
            else:
                break
        return password

    def get_data_from_file(self) -> str:
        while True:
            file_way = str(input('•Введите путь к заметке, которую надо зашифровать (формат заметки ".txt"): '))
            file_expansion = file_way.split('.')
            if file_expansion[len(file_expansion) - 1] == 'txt':
                if os.path.exists(file_way):
                    break
                else:
                    print(Fore.RED + '•Такого файла не существует!')
            else:
                print(Fore.RED + '•Неверный тип расширения')
        with open(file_way, 'r') as file:
            return file.read()

    def check_password(self, hashed_password: str, user_pass: str) -> bool:
        if isinstance(hashed_password, str) is False:
            raise TypeError(Fore.RED + "•Тип хеш-пароля не подходит")
        if isinstance(user_pass, str) is False:
            raise TypeError(Fore.RED + "•Тип пользовательского пароля не подходит")
        hash_password = hashed_password.split('|')
        password = hash_password[0]
        salt = hash_password[1]
        check_password = hashlib.sha256(salt.encode() + user_pass.encode()).hexdigest()
        return password == check_password

    def menu_choice_check(self) -> int:
        while True:
            try:
                choice = int(input('•Ваш выбор: '))
            except ValueError:
                print(Fore.RED + '•Неправильная команда!')
            else:
                break
        return choice
