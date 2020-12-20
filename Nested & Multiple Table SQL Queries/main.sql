.header ON
.mode column
.width 28

CREATE TABLE Item (ItemName VARCHAR (30) NOT NULL, ItemType CHAR(1) NOT NULL, ItemColour VARCHAR(10), PRIMARY KEY (ItemName));

CREATE TABLE Employee (EmployeeNumber SMALLINT UNSIGNED NOT NULL, EmployeeName VARCHAR(10) NOT NULL, EmployeeSalary INTEGER UNSIGNED NOT NULL, DepartmentName VARCHAR(10) NOT NULL REFERENCES Department, BossNumber SMALLINT UNSIGNED NOT NULL REFERENCES Employee, PRIMARY KEY (EmployeeNumber));

CREATE TABLE Department (DepartmentName VARCHAR(10) NOT NULL, DepartmentFloor SMALLINT UNSIGNED NOT NULL, DepartmentPhone SMALLINT UNSIGNED NOT NULL, EmployeeNumber SMALLINT UNSIGNED NOT NULL REFERENCES Employee, PRIMARY KEY (DepartmentName));

CREATE TABLE Sale (SaleNumber INTEGER UNSIGNED NOT NULL, SaleQuantity SMALLINT UNSIGNED NOT NULL DEFAULT 1, ItemName VARCHAR(30) NOT NULL REFERENCES Item, DepartmentName VARCHAR(10) NOT NULL REFERENCES Department, PRIMARY KEY (SaleNumber));

CREATE TABLE Supplier (SupplierNumber INTEGER UNSIGNED NOT NULL, SupplierName VARCHAR(30) NOT NULL, PRIMARY KEY (SupplierNumber));

CREATE TABLE Delivery (DeliveryNumber INTEGER UNSIGNED NOT NULL, DeliveryQuantity SMALLINT UNSIGNED NOT NULL DEFAULT 1, ItemName VARCHAR(30) NOT NULL REFERENCES Item, DepartmentName VARCHAR(10) NOT NULL REFERENCES Department, SupplierNumber INTEGER UNSIGNED NOT NULL REFERENCES Supplier, PRIMARY KEY (DeliveryNumber));

.separator "\t"
.import item.txt Item
.import employee.txt Employee
.import department.txt Department
.import sale.txt Sale
.import supplier.txt Supplier
.import delivery.txt Delivery

.print "Databases Lab 2 - Multiple Table Queries"
.print
.print "Q1-1: List the green items of type 'C'"
SELECT ItemName FROM Item WHERE ItemType = 'C' AND ItemColour = 'Green' ORDER BY ItemName;

.print
.print "Q1-2: What are the names of brown items sold by the Recreation Department?"
SELECT Item.ItemName FROM Sale, Item WHERE Item.ItemName = Sale.ItemName AND ItemColour = 'Brown' AND DepartmentName = 'Recreation' ORDER BY Item.ItemName;

.print
.print "Q1-3: Which suppliers deliver compasses?"
SELECT DISTINCT SupplierName FROM Supplier, Delivery WHERE Supplier.SupplierNumber = Delivery.SupplierNumber AND Delivery.ItemName = 'Compass' ORDER BY Supplier.SupplierName;

.print
.print "Q1-4: What items are delivered to the Books department?"
SELECT ItemName FROM Delivery WHERE DepartmentName = 'Books' ORDER BY ItemName;

.print
.print "Q1-5: What are the numbers and names of those employees who earn more than their managers?"
SELECT Worker.EmployeeNumber, Worker.EmployeeName FROM Employee AS Worker, Employee AS Boss WHERE Worker.BossNumber = Boss.EmployeeNumber AND Worker.EmployeeSalary > Boss.EmployeeSalary;

.print
.print "Q1-6: What are the names of employees who are in the same department as their manager (as an employee), reporting the name of the employee, the department and the manager?"
SELECT Worker.EmployeeName, Worker.DepartmentName, Boss.EmployeeName AS 'Manager' FROM Employee AS Worker, Employee AS Boss WHERE Worker.BossNumber = Boss.EmployeeNumber AND Worker.DepartmentName = Boss.DepartmentName ORDER BY Worker.EmployeeName;

.print
.print "Q1-7: List the departments having an average salary of over £25000"
SELECT DepartmentName, AVG(EmployeeSalary) AS 'AverageSalary' FROM Employee GROUP BY DepartmentName HAVING AVG(EmployeeSalary) > 25000 ORDER BY DepartmentName;

.print
.print "Q1-8: List the name, salary and manager of the employees of the Marketing department who have a salary of over £25000"
SELECT Worker.EmployeeName, Worker.EmployeeSalary, Boss.EmployeeName AS 'Manager' FROM Employee AS Worker, Employee AS Boss WHERE Worker.BossNumber = Boss.EmployeeNumber AND Worker.DepartmentName = 'Marketing' AND Worker.EmployeeSalary > 25000;

.print
.print "Q1-9: For each item, give its type, the departments that sell the item and the floor location of these departments"
SELECT Item.ItemName, Item.ItemType, Department.DepartmentName, Department.DepartmentFloor FROM Item, Sale, Department WHERE Sale.DepartmentName = Department.DepartmentName AND Sale.ItemName = Item.ItemName ORDER BY Item.ItemName, Department.DepartmentName;

.print
.print "Q1-10: What suppliers deliver a total quantity of items of types 'C' and 'N' that is altogether greater than 100?"
SELECT Supplier.SupplierName FROM Supplier, Delivery, Item WHERE Supplier.SupplierNumber = Delivery.SupplierNumber AND Delivery.ItemName = Item.ItemName AND (Item.ItemType = 'C' OR Item.ItemType = 'N') GROUP BY Supplier.SupplierName HAVING SUM(Delivery.DeliveryQuantity) > 100;

.print
.print "Q2-1: Find the suppliers that do not deliver compasses"
SELECT DISTINCT SupplierName FROM Supplier WHERE SupplierNumber NOT IN (SELECT DISTINCT SupplierNumber FROM Delivery WHERE Delivery.ItemName = 'Compass') ORDER BY SupplierName;

.print
.print "Q2-2: Find the name of the highest-paid employee in the Marketing Department"
SELECT EmployeeName, EmployeeSalary FROM Employee WHERE EmployeeSalary IN (SELECT MAX(EmployeeSalary) FROM Employee WHERE DepartmentName = 'Marketing');

.print
.print "Q2-3: Find the names of the suppliers that do not supply compasses or geo-positioning systems"
SELECT DISTINCT SupplierName FROM Supplier WHERE SupplierNumber NOT IN (SELECT DISTINCT SupplierNumber FROM Delivery WHERE Delivery.ItemName = 'Geo positioning system' OR Delivery.ItemName = 'Compass') ORDER BY SupplierName;

.print
.print "Q2-4: Find the number of employees with a salary under £10000"
SELECT COUNT(*) AS 'No. With Salary Under £10k' FROM Employee WHERE EmployeeName IN (SELECT EmployeeName FROM Employee WHERE EmployeeSalary < 10000);

.print
.print "Q2-5: List the departments on the second floor that contain more than one employee"
SELECT DepartmentName, COUNT(EmployeeName) AS 'Number Of Employees' FROM Employee WHERE DepartmentName IN (SELECT DepartmentName FROM Department WHERE DepartmentFloor = 2) GROUP BY DepartmentName HAVING COUNT(EmployeeName) > 1;