from datetime import datetime, timedelta

class Employee:
    company_name = "TechCorp Inc."
    tax_rates = {"USA": 0.22, "India": 0.18, "UK": 0.25}
    departments = {"Engineering": 0, "Sales": 0, "HR": 0, "Marketing": 0}
    total_employees = 0
    employee_list = []

    def __init__(self, name, department, salary, country, email):
        self.name = name
        self.department = department
        self.salary = salary
        self.country = country
        self.email = email
        self.hire_date = datetime.now()
        self.performance_ratings = []
        self.employee_id = f"EMP-{datetime.now().year}-{Employee.total_employees + 1:04d}"
        Employee.total_employees += 1
        Employee.departments[department] += 1
        Employee.employee_list.append(self)

    @staticmethod
    def validate_email(email):
        return "@" in email and "." in email.split("@")[-1]

    @staticmethod
    def is_valid_department(department):
        return department in Employee.departments

    @staticmethod
    def calculate_tax(salary, country):
        return salary * Employee.tax_rates.get(country, 0)

    @classmethod
    def from_csv_data(cls, csv_data):
        name, department, salary, country, email = csv_data.split(',')
        return cls(name.strip(), department.strip(), float(salary.strip()), country.strip(), email.strip())

    @classmethod
    def hire_bulk_employees(cls, bulk_data):
        for data in bulk_data:
            cls.from_csv_data(data)

    def add_performance_rating(self, rating):
        self.performance_ratings.append(rating)

    def get_average_performance(self):
        return sum(self.performance_ratings) / len(self.performance_ratings) if self.performance_ratings else 0

    def get_years_of_service(self):
        return (datetime.now() - self.hire_date).days // 365

    def is_eligible_for_bonus(self):
        return self.get_years_of_service() >= 2 and self.get_average_performance() >= 4.0

    def calculate_net_salary(self):
        tax = Employee.calculate_tax(self.salary, self.country)
        return self.salary - tax
    
    @classmethod
    def get_department_stats(cls):
        stats = {}
        for dept, count in cls.departments.items():
            stats[dept] = {
                "count": count,
                "average_salary": sum(emp.salary for emp in cls.employee_list if emp.department == dept) / count if count > 0 else 0
            }
        return stats

# Test Case 1: Class setup and basic functionality
Employee.company_name = "GlobalTech Solutions"
Employee.tax_rates = {"USA": 0.22, "India": 0.18, "UK": 0.25}
Employee.departments = {"Engineering": 0, "Sales": 0, "HR": 0, "Marketing": 0}

emp1 = Employee("John Smith", "Engineering", 85000, "USA", "john.smith@globaltech.com")
assert emp1.employee_id.startswith("EMP-2025-")
assert Employee.total_employees == 1
assert Employee.departments["Engineering"] == 1

# Test Case 2: Static method validations
assert Employee.validate_email("test@company.com") == True
assert Employee.validate_email("invalid.email") == False
assert Employee.is_valid_department("Engineering") == True
assert Employee.is_valid_department("InvalidDept") == False
assert abs(Employee.calculate_tax(100000, "USA") - 22000) < 0.01

# Test Case 3: Class methods and bulk operations
emp2 = Employee.from_csv_data("Sarah Johnson,Sales,75000,UK,sarah.j@globaltech.com")
assert emp2.name == "Sarah Johnson"
assert emp2.department == "Sales"
assert Employee.departments["Sales"] == 1

bulk_data = [
    "Mike Wilson,Marketing,65000,India,mike.w@globaltech.com",
    "Lisa Chen,HR,70000,USA,lisa.chen@globaltech.com"
]
Employee.hire_bulk_employees(bulk_data)
assert Employee.total_employees == 4

stats = Employee.get_department_stats()
assert stats["Engineering"]["count"] == 1
assert stats["Sales"]["count"] == 1

# Test Case 4: Performance and bonus calculations
emp1.add_performance_rating(4.2)
emp1.add_performance_rating(3.8)
emp1.add_performance_rating(4.5)
assert abs(emp1.get_average_performance() - 4.17) < 0.01

# Simulate employee with 2 years of service
emp1.hire_date = datetime.now() - timedelta(days=800)
assert emp1.get_years_of_service() >= 2
assert emp1.is_eligible_for_bonus() == True

# Test Case 5: Salary calculations
net_salary = emp1.calculate_net_salary()
expected_net = 85000 - (85000 * 0.22)
assert abs(net_salary - expected_net) < 0.01
