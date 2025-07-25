from collections import defaultdict
from functools import reduce
   

class GradeManager:
    def __init__(self):
        self.students = defaultdict(dict)

    def add_grade(self, student_name, subject, grade):
        self.students[student_name].update({subject: grade})
        """
        Add a grade for a student in a specific subject
        Args:
            student_name (str): Name of the student
            subject (str): Subject name
            grade (float): Grade value (0–100)
        """
        pass

    def get_student_average(self, student_name):
        """
        Calculate average grade for a student across all subjects
        Args:
            student_name (str): Name of the student
        Returns:
            float: Average grade or 0 if student not found
        """
        student = self.students.get(student_name)
        if not student:
            return 0.0
        total_grades = sum([grade for grade in student.values()])
        total_subjects = len(student)
        if total_subjects == 0:
            return 0.0 
        return total_grades / total_subjects
    
    def get_subject_statistics(self, subject):
        """
        Get statistics for a specific subject across all students
        Args:
            subject (str): Subject name
        Returns:
            dict: Contains 'average', 'highest', 'lowest', 'student_count'
        """
        subject_grades = [student[subject] for student in self.students.values() if subject in student]
        if not subject_grades:
            return {
                'average': 0.0,
                'highest': None,
                'lowest': None,
                'student_count': 0
            } 
        average = sum(subject_grades) / len(subject_grades)
        highest = max(subject_grades)
        lowest = min(subject_grades)
        student_count = len([student for student in self.students.values() if subject in student])
        return {
            'average': average,
            'highest': highest,
            'lowest': lowest,
            'student_count': student_count
        }

    def get_top_students(self, n=3):
        """
        Get top N students based on their overall average
        Args:
            n (int): Number of top students to return
        Returns:
            list: List of tuples (student_name, average_grade)
        """
        lst = []
        for student_name, student_detail in self.students.items():
            student_grades = [grade for grade in student_detail.values()]
            average_grade = sum(student_grades)/len(student_grades)
            lst.append((student_name, average_grade))
        return sorted(lst, key=lambda x: x[1], reverse=True)[:n]


    def get_failing_students(self, passing_grade=60):
        """
        Get students who are failing (average below passing grade)
        Args:
            passing_grade (float): Minimum grade to pass
        Returns:
            list: List of tuples (student_name, average_grade)
        """
        failing_students = []
        for student_name, student_detail in self.students.items():
            student_grades = [grade for grade in student_detail.values()]
            average_grade = sum(student_grades)/len(student_grades)
            if average_grade < passing_grade:
                failing_students.append((student_name, average_grade))
        return failing_students


# Test your implementation
manager = GradeManager()

# Add sample grades
grades_data = [
    ("Alice", "Math", 85), ("Alice", "Science", 92), ("Alice", "English", 78),
    ("Bob", "Math", 75), ("Bob", "Science", 68), ("Bob", "English", 82),
    ("Charlie", "Math", 95), ("Charlie", "Science", 88), ("Charlie", "History", 91),
    ("Diana", "Math", 55), ("Diana", "Science", 62), ("Diana", "English", 70),
    ("Eve", "Math", 88), ("Eve", "Science", 94), ("Eve", "English", 86), ("Eve", "History", 89)
]

for student, subject, grade in grades_data:
    manager.add_grade(student, subject, grade)

# Test all methods
print("Alice's average:", manager.get_student_average("Alice"))
print("Math statistics:", manager.get_subject_statistics("Math"))
print("Top 3 students:", manager.get_top_students(3))
print("Failing students:", manager.get_failing_students(75))
