import os
import db
import notes
import security
from colorama import init
from colorama import Fore, Back, Style
init(autoreset=True)


def main_menu() -> None:
    print('•Аутентифицироваться - 1')
    print('•Создать аккаунт - 2')
    print('•Выход - 3')
    return None


def account_edit() -> None:
    print('•Работа с заметками - 1')
    print('•Изменить ключ шифрования - 2')
    print('•Удалить аккаунт - 3')
    print('•Выход в главное меню - 4')
    return None


def notes_menu() -> None:
    print('•Создать заметку - 1')
    print('•Прочитать конкретную заметку - 2')
    print('•Изменить заметку - 3')
    print('•Удалить заметку - 4')
    print('•Удалить все заметки - 5')
    print('•Получить список заметок - 6')
    print('•Выход в меню управления аккаунтом - 7')
    return None


Data = db.Data()
Data.create_new_user_db()
os.chdir('Data_Base')
sec = security.Security()
auth_flag = False
secret_key = b''
while True:
    main_menu()
    main_menu_choice = security.Security().menu_choice_check()
    if main_menu_choice == 1:
        user = ''
        password = ''
        while True:
            user = security.Security().get_correct_str('логин')
            password = security.Security().get_password()
            if Data.authorized(user, password):
                print(Fore.GREEN + '•Авторизация прошла успешно')
                auth_flag = True
                master_key = sec.gen_master_key(password)
                secret_key = sec.decrypt(Data.get_secret_key(), master_key)
            else:
                auth_flag = False
            if auth_flag:
                print()
                break
        while True:
            account_edit()
            vibor = security.Security().menu_choice_check()
            print()
            if vibor == 1:
                note = notes.Notes(user)
                while True:
                    notes_menu()
                    notes_choice = security.Security().menu_choice_check()
                    print()
                    if notes_choice == 1:
                        note_name = security.Security().get_correct_str('название заметки')
                        note_message = security.Security().get_data_from_file()
                        if note.create_new_note(note_name,
                                                sec.encrypt(bytes(note_message, encoding='utf-8'), secret_key)):
                            print(Fore.GREEN + 'Заметка успешно создана')

                        else:
                            print(Fore.RED + 'Заметка с таким именем уже существует!')

                    elif notes_choice == 2:
                        note_name = security.Security().get_correct_str('название заметки')
                        data = note.read_note(note_name)
                        if data is not None:
                            data = sec.decrypt(data, secret_key)
                            print(data.decode())

                    elif notes_choice == 3:
                        note_name = security.Security().get_correct_str('название заметки')
                        note_message = security.Security().get_data_from_file()
                        if note.update_note(note_name, sec.encrypt(bytes(note_message, encoding='utf-8'), secret_key)):
                            print(Fore.GREEN + 'Заметка успешна изменена!')
                        else:
                            print(Fore.RED + "Не существует такой заметки!")

                    elif notes_choice == 4:
                        note_name = security.Security().get_correct_str('название заметки')
                        if note.delete_note(note_name):
                            print(Fore.GREEN + 'Заметка успешно удалена!')

                        else:
                            print(Fore.RED + "Не существует такой заметки!")
                    elif notes_choice == 5:
                        note.delete_all_notes(user)
                        print(Fore.GREEN + '•Заметки успешно удалены!')
                    elif notes_choice == 6:
                        print('Список заметок: ')
                        note.notes_count()

                    elif notes_choice == 7:
                        break

            elif vibor == 2:
                new_password = security.Security().get_password()
                Data.update(user, new_password)
                print(Fore.GREEN + 'Пароль успешно изменен!')
            elif vibor == 3:
                Data.delete(user)
                break
            elif vibor == 4:
                break
            else:
                print(Fore.RED + 'Неправильная команда!')

    elif main_menu_choice == 2:
        user = security.Security().get_correct_str('логин')
        password = security.Security().get_password()
        master_key = sec.gen_master_key(password)
        enc_key = sec.gen_secret_key()
        hash_pass = sec.gen_user_secret_key(password)
        encrypt_user = sec.encrypt(bytes(user, encoding='utf-8'), enc_key)
        Data.insert(user, hash_pass, sec.encrypt(enc_key, master_key), encrypt_user)
        print(Fore.RED + '•Пожалуйста, авторизуйтесь!')

    elif main_menu_choice == 3:
        break
    else:
        print(Fore.RED + '•Неправильная команда!')
