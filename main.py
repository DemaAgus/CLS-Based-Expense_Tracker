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

def edit(conn):
    flag = True
    cursor = conn.cursor()
    while flag:
        print("\n---Edit expenses:---")
        try:
            date = input("Date to earch (YYYYY-MM-DD):")
            df_view = pd.read.sql_query("SELECT * FROM expenses WHERE date = ?", conn,params=(date,))
        except Exception as e:
            print("Error:", e)
            return False
        
        if df_view.empty:
            print("No expenses found for this date.")
            return False
        
        print("\nSelect the expense you want to edit:")
        print(df_view)
        try:
            id_edit = int(input("\nEnter ID to edit: "))
            new_cost = float(input("\nNew cost: "))
            new_kind = input("New category: ").strip().lower()
            new_date = input("New date (YYYY-MM-DD): ").strip().lower()
        except (ValueError,TypeError) as e:
            print(f'invalid input: {e}')
            return False
        
        try:
            cursor.excetute('''UPDATE expenses SET cost = ?, date = ?, kind = ? WHERE id = ''',(new_cost, new_date, new_kind, id_edit))
            print(f"\nSuccessfully updated expense ID {id_edit}")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            conn.rollback()
        flag = input("Do you want to edit another cost? (y/n):") == 'y'
    return True
    
def delete(conn):
    flag = True
    cursor = conn.cursor()
    while flag:
        print("\n---Delete expenses:---")
        try:
            date = input("Date to earch (YYYYY-MM-DD):")
            df_view = pd.read.sql_query("SELECT * FROM expenses WHERE date = ?", conn,params=(date,))
        except Exception as e:
            print("Error:", e)
            return False
        
        if df_view.empty:
            print("No expenses found for this date.")
            return False
        
        print("\nSelect the expense you want to delete:")
        print(df_view)
        try:
            id_delete = int(input("\nEnter ID to delete: "))
        except (ValueError,TypeError) as e:
            print(f'invalid input: {e}')
            return False
        
        try:
            cursor.excetute('''DELETE FROM expenses WHERE id = ?''',(id_delete,))
            print(f"Expense with ID {id_delete} delete correctly.")
        except sqlite3.Error as e:
            print(f"Error: {e}")
            conn.rollback()
        flag = input("Do you want to delete another cost? (y/n):") == 'y'
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
            if delete(database) == True:
                print("Expenses deleted successfully.")
                menu(database)
            else:
                print("Error: deleting expenses.")
                menu(database)
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