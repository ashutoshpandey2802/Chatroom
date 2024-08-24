import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('employee_database.db')
cursor = conn.cursor()

# Create the Employees table
create_table_query = """
CREATE TABLE IF NOT EXISTS Employees (
    EmployeeID INT PRIMARY KEY,
    FirstName TEXT,
    LastName TEXT,
    Email TEXT,
    PhoneNumber TEXT,
    HireDate DATE,
    JobTitle TEXT,
    Salary REAL,
    Department TEXT
);
"""
cursor.execute(create_table_query)

# Clear existing data from the table
cursor.execute("DELETE FROM Employees")

# Insert dummy data with unique EmployeeID values
insert_data_query = """
INSERT INTO Employees (EmployeeID, FirstName, LastName, Email, PhoneNumber, HireDate, JobTitle, Salary, Department) VALUES
(1, 'John', 'Doe', 'john.doe@example.com', '555-1234', '2021-01-15', 'Software Engineer', 80000.00, 'IT'),
(2, 'Jane', 'Smith', 'jane.smith@example.com', '555-2345', '2021-02-20', 'Data Analyst', 70000.00, 'IT'),
(3, 'Michael', 'Johnson', 'michael.johnson@example.com', '555-3456', '2021-03-25', 'Project Manager', 90000.00, 'IT'),
(4, 'Emily', 'Davis', 'emily.davis@example.com', '555-4567', '2021-04-30', 'HR Manager', 85000.00, 'HR'),
(5, 'Matthew', 'Wilson', 'matthew.wilson@example.com', '555-5678', '2021-05-10', 'Accountant', 60000.00, 'Finance'),
(6, 'Sophia', 'Moore', 'sophia.moore@example.com', '555-6789', '2021-06-15', 'Marketing Specialist', 65000.00, 'Marketing'),
(7, 'James', 'Brown', 'james.brown@example.com', '555-7890', '2021-07-20', 'Sales Manager', 75000.00, 'Sales'),
(8, 'Isabella', 'Taylor', 'isabella.taylor@example.com', '555-8901', '2021-08-25', 'Customer Support', 55000.00, 'Support'),
(9, 'Oliver', 'Anderson', 'oliver.anderson@example.com', '555-9012', '2021-09-30', 'DevOps Engineer', 85000.00, 'IT'),
(10, 'Ava', 'Thomas', 'ava.thomas@example.com', '555-1235', '2021-10-15', 'Product Manager', 95000.00, 'Product'),
(11, 'William', 'Jackson', 'william.jackson@example.com', '555-2346', '2021-11-20', 'QA Engineer', 70000.00, 'IT'),
(12, 'Mia', 'White', 'mia.white@example.com', '555-3457', '2021-12-25', 'UI/UX Designer', 75000.00, 'Design'),
(13, 'Benjamin', 'Harris', 'benjamin.harris@example.com', '555-4568', '2022-01-30', 'System Administrator', 80000.00, 'IT'),
(14, 'Charlotte', 'Martin', 'charlotte.martin@example.com', '555-5679', '2022-02-10', 'Business Analyst', 72000.00, 'Business'),
(15, 'Elijah', 'Thompson', 'elijah.thompson@example.com', '555-6780', '2022-03-15', 'Network Engineer', 77000.00, 'IT'),
(16, 'Amelia', 'Garcia', 'amelia.garcia@example.com', '555-7891', '2022-04-20', 'Content Writer', 60000.00, 'Marketing'),
(17, 'Lucas', 'Martinez', 'lucas.martinez@example.com', '555-8902', '2022-05-25', 'Legal Advisor', 90000.00, 'Legal'),
(18, 'Harper', 'Robinson', 'harper.robinson@example.com', '555-9013', '2022-06-30', 'Research Scientist', 95000.00, 'R&D'),
(19, 'Henry', 'Clark', 'henry.clark@example.com', '555-1236', '2022-07-15', 'Procurement Specialist', 65000.00, 'Operations'),
(20, 'Evelyn', 'Rodriguez', 'evelyn.rodriguez@example.com', '555-2347', '2022-08-20', 'Operations Manager', 80000.00, 'Operations');
"""

cursor.executescript(insert_data_query)

# Commit the changes and close the connection
conn.commit()
conn.close()
