import pandas as pd
import sqlite3

def menu():
    menu = ['Add.','Edit.','Delete.','Total of the month.','Export data.']
    print("Select one option:")
    for i in range(len(menu)):
        print(f'{i+1}. {menu[i]}')
    option = input("Option:")
    match option:
        case '1':
            add()
        case '2':
            edit()
        case '3':
            delete()
        case '4':
            total()
        case '5':
            export()
        case _:
            print("Invalid option")
            menu()