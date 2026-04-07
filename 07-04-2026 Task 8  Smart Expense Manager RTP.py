import mysql.connector
from functools import reduce
from abc import ABC, abstractmethod


#                                               DATABASE CONNECTION 
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2001",
    database="expense_manager"
)
cursor = conn.cursor()


#                                               ABSTRACT CLASS 
class Person(ABC):
    @abstractmethod
    def show_details(self):
        pass


#                                                USER CLASS 
class User(Person):
    def __init__(self, name):
        self.__name = name

    def add_user(self):
        sql = "INSERT INTO users(name) VALUES(%s)"
        cursor.execute(sql, (self.__name,))
        conn.commit()
        print("User added successfully")

    def get_name(self):
        return self.__name

    def show_details(self):
        print("User Name:", self.__name)


#                                            EXPENSE CLASS 
class Expense(User):
    def __init__(self, name, user_id, amount=0, category="", description="", date=""):
        super().__init__(name)
        self.__user_id = user_id
        self.__amount = amount
        self.__category = category
        self.__description = description
        self.__date = date

    def add_expense(self):
        sql = """
        INSERT INTO expenses(user_id, amount, category, description, date)
        VALUES(%s, %s, %s, %s, %s)
        """
        values = (self.__user_id, self.__amount, self.__category, self.__description, self.__date)
        cursor.execute(sql, values)
        conn.commit()
        print("Expense added successfully")

    def show_details(self):
        print("Expense Details:")
        print("Name:", self.get_name())
        print("User ID:", self.__user_id)
        print("Amount:", self.__amount)
        print("Category:", self.__category)
        print("Description:", self.__description)
        print("Date:", self.__date)

    def get_expenses(self):
        sql = """
        SELECT u.user_id, u.name, e.exp_id, e.amount, e.category, e.description, e.date
        FROM users u
        JOIN expenses e ON u.user_id = e.user_id
        WHERE u.user_id = %s
        """
        cursor.execute(sql, (self.__user_id,))
        return cursor.fetchall()

    def view_expenses(self):
        records = self.get_expenses()

        print("\n--- All Expenses ---")
        if records:
            for row in records:
                print(row)
        else:
            print("No expenses found")
        return records

    def filter_by_category(self, category_name):
        records = self.get_expenses()
        filtered = list(filter(lambda x: x[4].lower() == category_name.lower(), records))

        print("\n--- Filter By Category ---")
        if filtered:
            for row in filtered:
                print(row)
        else:
            print("No matching category found")
        return filtered

    def filter_by_date(self, expense_date):
        records = self.get_expenses()
        filtered = [row for row in records if str(row[6]) == expense_date]

        print("\n--- Filter By Date ---")
        if filtered:
            for row in filtered:
                print(row)
        else:
            print("No matching date found")
        return filtered

    def total_expense(self):
        records = self.get_expenses()
        amounts = list(map(lambda x: x[3], records))
        total = reduce(lambda a, b: a + b, amounts, 0)

        print("\nTotal Expense:", total)
        return total

    def category_wise_spending(self):
        records = self.get_expenses()
        categories = {row[4]: 0 for row in records}

        for row in records:
            categories[row[4]] += row[3]

        print("\n--- Category Wise Spending ---")
        if categories:
            for key, value in categories.items():
                print(key, ":", value)
        else:
            print("No expense records")
        return categories

    def update_expense(self, exp_id, new_amount, new_category, new_description, new_date):
        sql = """
        UPDATE expenses
        SET amount=%s, category=%s, description=%s, date=%s
        WHERE exp_id=%s
        """
        values = (new_amount, new_category, new_description, new_date, exp_id)
        cursor.execute(sql, values)
        conn.commit()
        print("Expense updated successfully")

    def delete_expense(self, exp_id):
        sql = "DELETE FROM expenses WHERE exp_id=%s"
        cursor.execute(sql, (exp_id,))
        conn.commit()
        print("Expense deleted successfully")

    def monthly_report(self):
        records = self.get_expenses()
        report = {}

        for row in records:
            month = str(row[6])[:7]
            report[month] = report.get(month, 0) + row[3]

        print("\n--- Monthly Report ---")
        if report:
            for month, total in report.items():
                print(month, ":", total)
        else:
            print("No expense records")
        return report

    def highest_expense(self):
        records = self.get_expenses()

        print("\n--- Highest Expense ---")
        if records:
            highest = reduce(lambda a, b: a if a[3] > b[3] else b, records)
            print(highest)
            return highest
        else:
            print("No expense records")
            return None

    def smart_insight(self):
        records = self.get_expenses()
        monthly_category = {}

        for row in records:
            month = str(row[6])[:7]
            key = (month, row[4])
            monthly_category[key] = monthly_category.get(key, 0) + row[3]

        print("\n--- Smart Insight ---")
        if monthly_category:
            max_key = max(monthly_category, key=monthly_category.get)
            month, category = max_key
            amount = monthly_category[max_key]
            print(f"You are spending too much on {category} in {month}. Total = {amount}")
        else:
            print("No expense data for insight")


#                                                EXAMPLE USAGE 

u1 = User("Ibrahim")
u1.add_user()
u1.show_details()

e1 = Expense("Ibrahim", 1, 200, "Food", "Lunch", "2026-04-01")
e1.add_expense()

e2 = Expense("Ibrahim", 1, 500, "Travel", "Bus Ticket", "2026-04-02")
e2.add_expense()

e3 = Expense("Ibrahim", 1, 1000, "Shopping", "Shoes", "2026-04-03")
e3.add_expense()

e4 = Expense("Ibrahim", 1, 300, "Food", "Dinner", "2026-04-05")
e4.add_expense()

e1.view_expenses()
e1.filter_by_category("Food")
e1.filter_by_date("2026-04-02")
e1.total_expense()
e1.category_wise_spending()
e1.update_expense(1, 250, "Food", "Lunch Updated", "2026-04-01")
#e1.delete_expense(2)
e1.view_expenses()
e1.monthly_report()
e1.highest_expense()
e1.smart_insight()


#                                          CLOSE CONNECTION
cursor.close()
conn.close()