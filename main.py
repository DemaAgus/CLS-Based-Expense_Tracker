import pandas as pd
import sqlite3
from datetime import datetime

def add(conn):
    """
    Adds new expenses to the SQLite database through user input.
    
    Parameters:
    conn (sqlite3.Connection): Active database connection object
    
    Returns:
    bool: True if operation completed successfully, False if errors occurred
    
    Features:
    - Input validation for numeric cost
    - Basic date format validation (YYYY-MM-DD)
    - Transaction safety with rollback on error
    - SQL injection prevention through parameterization
    """
    data = {'cost': [],'date': [],'kind': []}
    
    flag = True
    while flag:
        print("\n--- Add New Expense ---")
        
        # Cost validation
        while True:
            cost = input("Cost (numeric value): ").strip()
            try:
                cost_val = float(cost)
                if cost_val <= 0:
                    raise ValueError("Cost must be positive")
                break
            except ValueError:
                print("Invalid input. Please enter a positive numeric value.")
        
        # Date validation
        while True:
            date = input("Date (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(date, '%Y-%m-%d')
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD format.")
        
        # Category input
        kind = input("Expense category: ").strip()
        
        # Store validated values
        data['cost'].append(cost_val)
        data['date'].append(date)
        data['kind'].append(kind)
        
        # Continue prompt
        while True:
            cont = input("\nAdd another expense? (y/n): ").strip().lower()
            if cont in ('y', 'n'):
                flag = (cont == 'y')
                break
            print("Invalid input. Please enter 'y' or 'n'.")
    
    try:
        # Create DataFrame from validated data
        df_data = pd.DataFrame(data)
        
        # Insert into database with explicit transaction
        with conn:
            df_data.to_sql(
                name='expenses',
                con=conn,
                if_exists='append',
                index=False
            )
        print("\nSuccessfully added expenses to database.")
        return True
        
    except Exception as e:
        print(f"\nError saving to database: {str(e)}")
        conn.rollback()
        return False    

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

def total(conn):
    """
    Displays expense details and summary totals for a specific month.
    
    Parameters:
    conn (sqlite3.Connection): Active database connection object
    
    Returns:
    bool: True if operation completed successfully, False if critical error occurred
    
    Features:
    - Month validation (01-12 format)
    - Detailed expense listing
    - Categorized expense summary
    - Grand total calculation
    - Error handling with transaction safety
    - Multiple month analysis capability
    """
    flag = True
    while flag:
        try:
            # Get and validate month input
            month = input("\nEnter the month to calculate totals (MM): ").strip().zfill(2)
            
            if not (1 <= int(month) <= 12):
                print("Invalid month. Please enter 01-12.")
                continue

            print(f"\n--- Total expenses for month {month} ---")
            
            # Execute database query
            df_view = pd.read_sql_query(
                "SELECT date, kind, cost FROM expenses WHERE strftime('%m', date) = ?",
                conn,
                params=(month,)
            )

            if df_view.empty:
                print("\nNo expenses found for this month.")
            else:
                # Display detailed expenses
                print("\n--- Detailed Expenses ---")
                print(df_view.to_string(index=False))
                
                # Calculate category totals
                print("\n--- Category Totals ---")
                category_totals = df_view.groupby('kind', as_index=False)['cost'].sum()
                category_totals.columns = ['Category', 'Total']
                print(category_totals.to_string(index=False))
                
                # Calculate grand total
                grand_total = df_view['cost'].sum()
                print(f"\nGRAND TOTAL FOR MONTH {month}: ${grand_total:.2f}")

        except ValueError:
            print("Invalid month format. Please use numeric format (01-12).")
        except sqlite3.Error as e:
            print(f"\nDatabase error: {str(e)}")
            return False
        except Exception as e:
            print(f"\nUnexpected error: {str(e)}")
            return False

        # Handle continuation prompt
        while True:
            cont = input("\nView another month? (y/n): ").strip().lower()
            if cont in ('y', 'n'):
                flag = (cont == 'y')
                break
            print("Invalid input. Please enter 'y' or 'n'.")

    return True

def export(conn):
    """
    Exports all expense data from the database to a timestamped CSV file.
    
    Parameters:
    conn (sqlite3.Connection): Active database connection object
    
    Returns:
    bool: True if operation completed successfully, False if any error occurred
    
    Features:
    - Automatic CSV file naming with timestamp
    - Full database table export
    - Comprehensive error handling (database and file I/O)
    - Empty dataset validation
    - User feedback messages
    """
    try:
        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"expenses_export_{timestamp}.csv"
        
        # Retrieve all expense data
        df_view = pd.read_sql_query("SELECT * FROM expenses", conn)
        
        if df_view.empty:
            print("\nNo data available to export.")
            return False
            
        # Export to CSV
        df_view.to_csv(filename, index=False)
        print(f"\nSuccessfully exported {len(df_view)} records to {filename}")
        return True
        
    except sqlite3.Error as e:
        print(f"\nDatabase operation failed: {str(e)}")
        return False
    except PermissionError:
        print("\nFile write error: Permission denied. Check file access rights.")
        return False
    except Exception as e:
        print(f"\nUnexpected error during export: {str(e)}")
        return False

def menu(database):
    menu = ['Add.','Edit.','Delete.','Total of the month.','Export data.','Exit.']
    print("Select one option:")
    for i in range(len(menu)):
        print(f'{i+1}. {menu[i]}')
    option = input("Option:")
    match option:
        case '1':
            if add(database) == True:
                print("\nExpenses added successfully.")
                menu(database)
            else:
                print("\nError: adding expenses.")
                menu(database)
        case '2':
            if edit(database) == True:
                print("\nExpenses edited successfully.")
                menu(database)
            else:
                print("\nError: editing expenses.")
                menu(database)
        case '3':
            if delete(database) == True:
                print("\nExpenses deleted successfully.")
                menu(database)
            else:
                print("\nError: deleting expenses.")
                menu(database)
        case '4':
            if total(database) == True:
                print("\nTotal calculated successfully.")
                menu(database)
            else:
                print("\nError: calculating total.")
                menu(database)
        case '5':
            if export(database) == True:
                print("\nSuccessfully exported data.")
                menu(database)
            else:
                print("\nError: exporting data.")
                menu(database)
        case '6':
            print("Goodbye!")
            database.close()
            exit()
        case _:
            print("Invalid option")
            menu(database)
            
if __name__ == '__main__':
    with sqlite3.connect('expenses.db') as conn:
        menu(conn)