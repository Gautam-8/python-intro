class Course:
    total_enrollments = 0

    def __init__(self, course_id, name, instructor, credits, enrollment_limit):
        self.course_id = course_id
        self.name = name
        self.instructor = instructor
        self.credits = credits
        self.enrollment_limit = enrollment_limit
        self.enrolled_students = {}
        Course.total_enrollments += 0

    def enroll_student(self, student):
        if len(self.enrolled_students) < self.enrollment_limit:
            self.enrolled_students[student.student_id] = student
            Course.total_enrollments += 1
            return True
        else:
            return False

    def get_enrollment_count(self):
        return len(self.enrolled_students)

    def is_full(self):
        return len(self.enrolled_students) >= self.enrollment_limit

    def get_available_spots(self):
        return self.enrollment_limit - len(self.enrolled_students)
    
    def add_grade(self, student_id, grade):
        if student_id in self.enrolled_students:
            self.enrolled_students[student_id].add_grade(self.course_id, grade)

    def get_course_statistics(self):
        """
        Get statistics for the course
        Returns:
            dict: Contains 'average_grade', 'highest_grade', 'lowest_grade', 'student_count'
        """
        grades = [student.grades.get(self.course_id, 0) for student in self.enrolled_students.values()]
        if not grades:
            return {
                'average_grade': 0.0,
                'highest_grade': None,
                'lowest_grade': None,
                'student_count': 0
            }
        average_grade = sum(grades) / len(grades)
        highest_grade = max(grades)
        lowest_grade = min(grades)
        return {
            'average_grade': average_grade,
            'highest_grade': highest_grade,
            'lowest_grade': lowest_grade,
            'student_count': len(self.enrolled_students)
        }

    @classmethod
    def get_total_enrollments(cls):
        return cls.total_enrollments

    def __str__(self):
        return f"{self.name} ({self.course_id}) by {self.instructor}, Credits: {self.credits}, Enrollment Limit: {self.enrollment_limit}"
    

class Student:
    students_list = []

    def __init__(self, student_id, name, email, program):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.program = program
        self.enrolled_courses = {}
        self.grades = {}
        Student.students_list.append(self)

    def enroll_in_course(self, course: Course):
        if course.enroll_student(self):
            self.enrolled_courses[course.course_id] = course
            return True
        else:
            return False

    def add_grade(self, course_id, grade):
        if course_id in self.enrolled_courses:
            self.grades[course_id] = grade

    def calculate_gpa(self):
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)
    
    def get_transcript(self):
        return {course_id: self.grades.get(course_id, 'N/A') for course_id in self.enrolled_courses}
    
    def calculate_gpa(self):
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)
    
    @classmethod
    def get_average_gpa(cls):
        total_gpa = sum(student.calculate_gpa() for student in cls.total_students)
        return total_gpa / cls.total_students if cls.total_students > 0 else 0.0
    

    @classmethod
    def get_top_students(cls, n=10):
        lst = []
        for student in cls.total_students:
            student_grades = [grade for grade in student.grades.values()]
            average_grade = sum(student_grades) / len(student_grades) if student_grades else 0
            lst.append((student.name, average_grade))
        return sorted(lst, key=lambda x: x[1], reverse=True)[:n]
    
   
    @classmethod
    def get_total_students(cls):
        return cls.total_students


# Test Case 1: Creating courses with enrollment limits
math_course = Course("MATH101", "Calculus I", "Dr. Smith", 3, 30)
physics_course = Course("PHYS101", "Physics I", "Dr. Johnson", 4, 25)
cs_course = Course("CS101", "Programming Basics", "Prof. Brown", 3, 20)

print(f"Course: {math_course}")
print(f"Available spots in Math: {math_course.get_available_spots()}")

# Test Case 2: Creating students with different programs
student1 = Student("S001", "Alice Wilson", "alice@university.edu", "Computer Science")
student2 = Student("S002", "Bob Davis", "bob@university.edu", "Mathematics")
student3 = Student("S003", "Carol Lee", "carol@university.edu", "Physics")

print(f"Student: {student1}")
print(f"Total students: {Student.get_total_students()}")

# Test Case 3: Course enrollment
enrollment1 = student1.enroll_in_course(math_course)
enrollment2 = student1.enroll_in_course(cs_course)
enrollment3 = student2.enroll_in_course(math_course)

print(f"Alice's enrollment in Math: {enrollment1}")
print(f"Math course enrollment count: {math_course.get_enrollment_count()}")

# Test Case 4: Adding grades and calculating GPA
student1.add_grade("MATH101", 85.5)
student1.add_grade("CS101", 92.0)
student2.add_grade("MATH101", 78.3)

print(f"Alice's GPA: {student1.calculate_gpa()}")
print(f"Alice's transcript: {student1.get_transcript()}")

# Test Case 5: Course statistics
math_course.add_grade("S001", 85.5)
math_course.add_grade("S002", 78.3)

course_stats = math_course.get_course_statistics()
print(f"Math course statistics: {course_stats}")

# Test Case 6: University-wide analytics using class methods
total_enrollments = Course.get_total_enrollments()
print(f"Total enrollments across all courses: {total_enrollments}")

average_gpa = Student.get_average_gpa()
print(f"University average GPA: {average_gpa}")

top_students = Student.get_top_students(2)
print(f"Top 2 students: {top_students}")

# Test Case 7: Enrollment limits and waitlist
# Try to enroll more students than course capacity
for i in range(25):  # Assuming math course limit is 30
    temp_student = Student(f"S100{i}", f"Student {i}", f"student{i}@uni.edu", "General")
    result = temp_student.enroll_in_course(math_course)

print(f"Course full status: {math_course.is_full()}")
print(f"Waitlist size: {len(math_course.waitlist) if hasattr(math_course, 'waitlist') else 0}")
