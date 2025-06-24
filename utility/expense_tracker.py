import csv
from datetime import datetime

FILENAME = "dir/expense_tracker.csv"

def add_expense(date, category, amount):
    with open(FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount])
    print("✅ Expense recorded.")

def view_expenses():
    print("\n📊 Expense Summary:")
    with open(FILENAME, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(f"{row[0]} | {row[1]} | ${row[2]}")

def main():
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Exit")
        choice = input("Choose: ")

        if choice == '1':
            date = input("Enter date (YYYY-MM-DD) or leave blank for today: ") 
            if date:
                date = datetime.strptime(date_input, "%Y-%m-%d")
            else:
                date = datetime.now()
            formatted_date = date.strftime("%d/%m/%Y %H:%M:%S")

            category = input("Category: ")

            amount = input("Amount: ")
            add_expense(formatted_date, category, amount)
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
