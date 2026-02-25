# Employee Management System....

from decimal import Decimal
import mysql.connector

try:
    conn = mysql.connector.connect(user='root',
        password='manish8630',
        host='localhost',
        database='my_project',
        port=3306
        )
    if(conn.is_connected()):
        print("Connected to database!!")

    else:
        print("Connection failed!!")
    
except:
    print("Unable to Connect Database")


cursor = conn.cursor()


def check_employee(employee_id):
    try:
        query = "SELECT * FROM employee WHERE id = %s"
        cursor.execute(query, (employee_id,))  # ✅ note the comma
        result = cursor.fetchone()
        return result is not None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False


def add_employee():
    id = input("Enter Student Id:- ")
    if check_employee(id):
        print("Student Already Exists. Please Try Again!!")
        return
    
    Name = input("Enter the employee name:- ")
    Post = input("Enter the employee post:- ")
    Salary = float(input("Enter the employee salary:- "))
    
    num = "insert into employee(id, name, post, salary) values(%s, %s, %s, %s)"
    data = (id, Name, Post, Salary)

    try:
        cursor.execute(num, data)
        conn.commit()
        print("Student Data Saved Successfully!!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()


def remove_employee():
    id = input("Enter the student id: ")
    if not check_employee(id):
        print()
        print("Student Already Exists. Please Try Again!!")
        return
    
    num = "delete from employee where id=%s"
    data = (id,)

    try:
        cursor.execute(num, data)
        conn.commit()
        print("Student Data Removed Successfully!!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()


def promote_employee():
    id = input("Enter the student id: ")

    if not check_employee(id):
        print("Student Already Exists. Please Try Again!!")
        return

    try:
        Amount = Decimal(input("Enter Increase Salary:- ").strip())

        num_select = "SELECT salary FROM employee WHERE id=%s"
        cursor.execute(num_select, (id,))
        current_salary = cursor.fetchone()[0]   # this is already Decimal

        new_salary = current_salary + Amount

        num_update = "UPDATE employee SET salary=%s WHERE id=%s"
        cursor.execute(num_update, (new_salary, id))
        conn.commit()

        print("Employee Promoted Successfully!!")

    except (ValueError, mysql.connector.Error) as e:
        print(f"Error: {e}")
        conn.rollback()


def display_employee():
    try:
        query = "SELECT id, name, post, salary FROM employee"
        cursor.execute(query)

        employees = cursor.fetchall()

        if not employees:
            print("No employees found.")
            return

        for employee in employees:
            print("Employee Id:- ", employee[0])
            print("Employee Name:- ", employee[1])
            print("Employee Post:- ", employee[2])
            print("Employee Salary:- ", employee[3])
            print("---------------------------")

    except mysql.connector.Error as err:
        print(f"Error: {err}")


def menu():
    while True:
        print("\nWelcome to Employee Management Record!!")
        print("Press: ")
        print("1 to Check Employee")
        print("2 to Add Employee")
        print("3 to Remove Employee")
        print("4 to Promote Employee")
        print("5 to Display Employees")
        print("6 to Exit")

        choice = input("Enter Your Choice:- ")
        
        if choice == '1':
            emp_id = input("Enter Employee ID to check: ")
            if check_employee(emp_id):
                print("Employee exists.")
            else:
                print("Employee does not exist.")

        if choice == '2':
            add_employee()

        elif choice == '3':
            remove_employee()

        elif choice == '4':
            promote_employee()

        elif choice == '5':
            display_employee()

        elif choice == '6':
            print("Existing the program. Good Byee!!")
            break
        else:
            print("Invalid Choice. Please Try Again!!")

if __name__ == "__main__":
    menu()
