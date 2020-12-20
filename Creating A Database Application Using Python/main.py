import sqlite3

# If value is 1, user wants to create table, else user doesn't want to create table
firstInput = 0

class DBOperations:
  # SQL queries to be used
  # '?' symbol represents input data in query
  sql_create_table_firsttime = "CREATE TABLE IF NOT EXISTS"
  sql_create_table = "CREATE TABLE"
  sql_insert = "INSERT INTO EmployeeUoB VALUES (?, ?, ?, ?, ?, ?)"
  sql_select_all = "SELECT * FROM EmployeeUoB"
  sql_search = "SELECT * FROM EmployeeUoB WHERE employeeID = ?"
  sql_update_data = "UPDATE EmployeeUoB SET employeeID = ?, empTitle = ?, forename = ?, surname = ?, email = ?, salary = ?"
  sql_delete_data = "DELETE FROM EmployeeUoB WHERE employeeID = ?"
  sql_drop_table = "DROP TABLE IF EXISTS EmployeeUoB"

  # Run before any other function in class
  # Creates table, only if table doesn't exist and user doesn't try to create table first
  def __init__(self):
    try:
      self.get_connection()
      # Tries to find table within database file. Returns 1 if found, 0 if not
      findTable = self.cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='EmployeeUoB'")
      exists = 0

      # Sets 'exists' variable to determine if table exists
      for i in findTable:
        exists = i[0]

      # Runs only if table doesn't exist AND if user's 1st input isn't to create table
      if(exists == 0 and firstInput != 1):
        print("\nTable does not exist")
        # Executes SQL query to create 'EmployeeUoB' table
        self.cur.execute(self.sql_create_table_firsttime + " 'EmployeeUoB' (employeeID SMALLINT UNSIGNED, empTitle VARCHAR(20), forename VARCHAR(20), surname VARCHAR(20), email CHAR(50), salary INTEGER UNSIGNED, PRIMARY KEY (employeeID), CHECK(empTitle != '' AND forename != '' AND surname != '' AND (email LIKE '%@%' OR email == '')))")
        print("Table created")
        # Saves changes made to database
        self.conn.commit()

    except Exception as e:
      print(e)
    finally:
      # Closes connection to database
      self.conn.close()

  # 'connect()' creates file for database, 'cursor()' allows processing of individual rows
  def get_connection(self):
    self.conn = sqlite3.connect("DBName.db")
    self.cur = self.conn.cursor()

  # Creates table, only if table doesn't exist and user tries to create table first
  def create_table(self):
    try:
      self.get_connection()

      # Executes SQL query to create 'EmployeeUoB' table, if table doesn't exist
      self.cur.execute(self.sql_create_table + " 'EmployeeUoB' (employeeID SMALLINT UNSIGNED, empTitle VARCHAR(20), forename VARCHAR(20), surname VARCHAR(20), email CHAR(50), salary INTEGER UNSIGNED, PRIMARY KEY (employeeID), CHECK(empTitle != '' AND forename != '' AND surname != '' AND (email LIKE '%@%' OR email == '')))")
      self.conn.commit()
      print("\nTable created successfully")

    # Error message if table already exists
    except Exception:
      print("\nThis table is already created")
    finally:
      self.conn.close()

  # Inserts new row of data into table
  def insert_data(self):
    try:
      self.get_connection()

      # New 'Employee' object to set data values of employee
      emp = Employee()

      # 'setter' functions of 'Employee' class and input used to set values for columns
      emp.set_employee_id(int(input("\nEnter Employee ID: ")))
      emp.set_employee_title(input("Enter Employee Title: "))
      emp.set_forename(input("Enter Employee Forename: "))
      emp.set_surname(input("Enter Employee Surname: "))
      emp.set_email(input("Enter Employee Email: "))
      emp.set_salary(int(input("Enter Employee Salary: ")))

      # Executes SQL query to insert row of data into table
      # 'emp' converted to string, delimited by new line character and inserted into tuple
      self.cur.execute(self.sql_insert, tuple(str(emp).split("\n")))
      self.conn.commit()
      print("\nInserted data successfully")

    # Error message if input values cannot be accepted
    except Exception:
      print("\nInvalid input!")
      print("Please enter valid values!")
    finally:
      self.conn.close()

  # Selects and prints all rows within 'EmployeeUoB' table
  def select_all(self):
    try:
      self.get_connection()
      # Executes SQL query to select all rows within table
      self.cur.execute(self.sql_select_all)
      # Fetches all query results and returns a tuple with all rows from table
      results = self.cur.fetchall()

      # Data from table printed only if data exists in table
      if(len(results) != 0):
        # Column values printed for each row returned by query
        for row in results:
          print ("\nEmployee ID: "+ str(row[0]))
          print ("Title: "+ row[1])
          print ("Forename: "+ row[2])
          print ("Surname: "+ row[3])
          print ("Email: "+ row[4])
          print ("Salary: £"+ str(row[5]))
      else:
        print("\nThis table is empty!")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  # Selects and prints specific row based on inputted Employee ID
  def search_data(self):
    try:
      self.get_connection()
      # Employee ID input for employee being searched for
      employeeID = int(input("\nEnter Employee ID: "))
      # Executes SQL query to retrieve row of data for employee
      self.cur.execute(self.sql_search, str(employeeID))
      # Returns the single result from the query
      result = self.cur.fetchone()

      # Column values printed for employee returned by query
      for index, detail in enumerate(result):
        if index == 0:
          print("\nEmployee ID: " + str(detail))
        elif index == 1:
          print("Title: " + detail)
        elif index == 2:
          print("Forename: " + detail)
        elif index == 3:
          print("Surname: " + detail)
        elif index == 4:
          print("Email: " + detail)
        else:
          print("Salary: £"+ str(detail))

    # If query returns 'None', then record doesn't exist in table
    except Exception:
      print("\nCannot find this record in the database")
    finally:
      self.conn.close()

  # Updates columns of specific row within table
  def update_data(self):
    try:
      self.get_connection()
      # Employee ID input for employee data being updated
      employeeID = int(input("\nEnter Employee ID: "))
      # Executes SQL query to retrieve row of data for employee
      self.cur.execute(self.sql_search, tuple(str(employeeID)))
      # Returns the single result from the query
      result = self.cur.fetchone()

      # 'rows' will be how many rows are updated
      # 'column' identifies the column being updated
      rows = 0
      column = 0

      # New 'Employee' object to set new data values of employee
      emp = Employee()

      # Data updated only if employee exists within table
      if(result != None):
        while(column < 6):
          # Current column value printed before new input
          print("\nCurrent information: ", result[column])
          # New column values inputted into 'Employee' object
          if(column == 0):
            emp.set_employee_id(int(input("Enter NEW Employee ID: ")))
          elif(column == 1):
            emp.set_employee_title(input("Enter NEW Employee Title: "))
          elif(column == 2):
            emp.set_forename(input("Enter NEW Employee Forename: "))
          elif(column == 3):
            emp.set_surname(input("Enter NEW Employee Surname: "))
          elif(column == 4):
            emp.set_email(input("Enter NEW Employee Email: "))
          elif(column == 5):
            emp.set_salary(int(input(" Enter NEW Employee Salary: ")))
          column += 1 # To iterate through each column

        # SQL query formulated as it has both 'SET' and 'WHERE'
        sql = self.sql_update_data + " WHERE employeeID = '" + str(employeeID) + "'"

        # Executes SQL query to update row within table
        # 'emp' converted to string, delimited by new line character and inserted into tuple
        self.cur.execute(sql, tuple(str(emp).split("\n")))
        self.conn.commit()

        # 'total_changes' gives how many rows were updated
        rows = self.conn.total_changes
      else:
        rows = 0

      # Gives number of rows affected only if rows were updated
      if rows != 0:
        print ("\n"+str(rows)+" Row(s) affected.")
      else:
        print ("\nCannot find this record in the database")

    # Error message if input values cannot be accepted
    except Exception:
      print("\nInvalid input!")
      print("Please enter valid values!")
    finally:
      self.conn.close()

  # Deletes data from table based on inputted Employee ID
  def delete_data(self):
    try:
      self.get_connection()
      # Employee ID input for employee data being deleted
      employeeID = int(input("\nEnter Employee ID: "))
      # Executes SQL query to retrieve row of data for employee
      self.cur.execute(self.sql_search, tuple(str(employeeID)))
      # Returns the single result from the query
      result = self.cur.fetchone()

      # 'rows' will be how many rows are deleted
      rows = 0

      # Row deleted only if it exists in table
      if(result != None):
        # Executes SQL query to delete specific row within table
        self.cur.execute(self.sql_delete_data, str(employeeID))
        self.conn.commit()

        # 'rows' gives how many rows were deleted
        rows = self.conn.total_changes
      else:
        rows = 0

      # Gives number of rows affected only if rows were deleted
      if rows != 0:
        print ("\n"+str(rows)+ " Row(s) affected.")
      else:
        print ("\nCannot find this record in the database")

    # Error message if input values cannot be accepted
    except Exception:
      print("\nInvalid input!")
      print("Please enter valid values!")
    finally: 
      self.conn.close()

  # Deletes entire table, only if confirmation is given (Extra function)
  def delete_table(self):
    try:
      self.get_connection()
      print("\nAre you sure you want to delete the table?")
      print ("If Yes, please enter 'yes'")
      print ("If No, please enter 'no'")
      # Confirmation must be given before table can be deleted
      confirm = input("\nEnter your choice: ")

      # Executes SQL query to delete entire table if confirmation given
      if(confirm == "yes"):
        self.cur.execute(self.sql_drop_table)
        print("\nTable deleted!")
      elif(confirm == "no"):
        pass
      # Error message if invalid input is given
      else:
        print("\nInvalid choice!")
    except Exception as e:
      print(e)
    finally: 
      self.conn.close()

# Allows creation of 'Employee' object to store employee data
class Employee:
  def __init__(self):
    self.employeeID = 0
    self.empTitle = ''
    self.forename = ''
    self.surname = ''
    self.email = ''
    self.salary = 0.0

  # Following functions set employee column values
  def set_employee_id(self, employeeID):
    self.employeeID = employeeID

  def set_employee_title(self, empTitle):
    self.empTitle = empTitle

  def set_forename(self,forename):
   self.forename = forename
  
  def set_surname(self,surname):
    self.surname = surname

  def set_email(self,email):
    self.email = email
  
  def set_salary(self,salary):
    self.salary = salary

  def __str__(self):
    return str(self.employeeID)+"\n"+self.empTitle+"\n"+ self.forename+"\n"+self.surname+"\n"+self.email+"\n"+str(self.salary)


# Inputs defined by user on console
# User will select choice from menu to interact with database
print ("EmployeeUoB Database")
while True:
  print ("\n Menu:")
  print ("**********")
  print (" 1. Create table EmployeeUoB")
  print (" 2. Insert data into EmployeeUoB")
  print (" 3. Select all data into EmployeeUoB")
  print (" 4. Search an employee")
  print (" 5. Update data some records")
  print (" 6. Delete data some records")
  print (" 7. Delete table EmployeeUoB")
  print (" 8. Exit\n")

  # Input to choose option from menu
  __choose_menu = int(input("Enter your choice: "))

  # If-Else ensures table is always created before carrying out any functions
  # If 'firstInput' does equal 1, then table created by 'create_table()'
  if(__choose_menu == 1):
    firstInput = 1
  # If 'firstInput' doesn't equal 1 and table doesn't exist, then table created by '__init__()'
  else:
    firstInput = 0

  # Function run depending on which option chosen from menu
  db_ops = DBOperations()
  if __choose_menu == 1:
    db_ops.create_table()
  elif __choose_menu == 2:
    db_ops.insert_data()
  elif __choose_menu == 3:
    db_ops.select_all()
  elif __choose_menu == 4:
    db_ops.search_data()
  elif __choose_menu == 5:
    db_ops.update_data()
  elif __choose_menu == 6:
    db_ops.delete_data()
  elif __choose_menu == 7:
    db_ops.delete_table()
  elif __choose_menu == 8:
    exit(0)
  else:
    print ("\nInvalid Choice")