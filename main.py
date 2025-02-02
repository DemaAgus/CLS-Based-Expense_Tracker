import pandas as pd
import sqlite3

def add(conn):
    data = {
        'cost': [],
        'date': [],
        'kind': []
    }
    flag = True
    while flag:
        print("Add a new expense:\n")
        cost = input("Cost:")
        date = input("Date:")
        kind = input("Kind:")
        data['cost'].append(cost)
        data['date'].append(date)
        data['kind'].append(kind)
        flag = input("Do you want to add another cost? (y/n):") == 'y'
    df_data = pd.DataFrame(data)
    df_data.to_sql(name='expenses', con=conn, if_exists='append', index=False)
    return True    

def menu(database):
    menu = ['Add.','Edit.','Delete.','Total of the month.','Export data.']
    print("Select one option:")
    for i in range(len(menu)):
        print(f'{i+1}. {menu[i]}')
    option = input("Option:")
    match option:
        case '1':
            if add(database) == True:
                print("Expenses added successfully.")
            else:
                print("Error: adding expenses.")
        case '2':
            edit(database)
        case '3':
            delete(database)
        case '4':
            total(database)
        case '5':
            export(database)
        case _:
            print("Invalid option")
            menu(database)
            
if __name__ == '__main__':
    with sqlite3.connect('expenses.db') as conn:
        menu(conn)