from typing import Optional
import db
import os
import shutil
from colorama import init
from colorama import Fore, Back, Style
init(autoreset=True)


class Notes:
    def __init__(self, user: str):
        self.__user_dir = db.Data().get_path_to_user_dir(user)

    def create_new_note(self, note_name: str, note_data: bytes) -> bool:
        if isinstance(note_data, bytes) and isinstance(note_name, str) is False:
            print(Fore.RED + "•Неверный тип данных!")
            return False
        if os.path.exists(self.__user_dir + '/Zapyski' + note_name + '.txt'):
            return False
        with open(self.__user_dir + f'/Zapyski/{note_name}.txt', 'wb') as file:
            file.write(note_data)
            return True

    def read_note(self, note_name: str) -> Optional[bytes]:
        if isinstance(note_name, str) is False:
            print(Fore.RED + "•Неверный тип данных!")
            return None
        if os.path.exists(self.__user_dir + f'/Zapyski/{note_name}.txt'):
            with open(self.__user_dir + f'/Zapyski/{note_name}.txt', 'rb') as file:
                data = file.read()
                return data
        else:
            print(Fore.RED + "•Не существует такой заметки!")
            return None

    def update_note(self, note_name: str, note_data: bytes) -> bool:
        if isinstance(note_data, bytes) and isinstance(note_name, str) is False:
            print(Fore.RED + "•Неверный тип данных!")
            return False
        if os.path.exists(self.__user_dir + f'/Zapyski/{note_name}.txt'):
            with open(self.__user_dir + f'/Zapyski/{note_name}.txt', 'wb') as file:
                file.seek(0)
                file.write(note_data)
                return True
        else:
            return False

    def delete_note(self, note_name: str) -> bool:
        if isinstance(note_name, str) is False:
            raise Exception(Fore.RED + "•Неверный тип данных!")
        if os.path.exists(self.__user_dir + f'/Zapyski/{note_name}.txt'):
            os.remove(self.__user_dir + f'/Zapyski/{note_name}.txt')
            return True
        else:
            return False

    def delete_all_notes(self, user: str) -> None:
        if isinstance(user, str) is False:
            raise Exception(Fore.RED + "•Неверный тип данных!")
        shutil.rmtree(self.__user_dir + f'/Zapyski')
        os.mkdir(self.__user_dir + f'/Zapyski')

    def notes_count(self) -> None:
        i = 1
        for filename in os.listdir(self.__user_dir + '/Zapyski'):
            file = filename.split('.')
            if file[len(file) - 1] == 'txt':
                print(f'{i}. {filename}')
                i += 1
