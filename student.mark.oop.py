from abc import ABC, abstractmethod

def read_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter an integer!")


def read_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a number!")

class Student:
    def __init__(self):
        self.__id = ""
        self.__name = ""
        self.__dob = ""  

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def dob(self) -> str:
        return self.__dob

    def input(self):
        """Input information for ONE student"""
        print("Input student information:")
        self.__id = input("  ID: ")
        self.__name = input("  Name: ")
        self.__dob = input("  Date of birth (dd/mm/yyyy): ")

    def show(self):
        """Show information for ONE student"""
        print(f"ID: {self.__id}, Name: {self.__name}, DoB: {self.__dob}")

class Course:
    def __init__(self):
        self.__id = ""
        self.__name = ""

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    def input(self):
        """Input information for ONE course"""
        print("Input course information:")
        self.__id = input("  Course ID: ")
        self.__name = input("  Course name: ")

    def show(self):
        """Show information for ONE course"""
        print(f"Course ID: {self.__id}, Name: {self.__name}")

class BaseManager(ABC):
    @abstractmethod
    def input(self):
        """Input the whole list (students or courses)"""
        pass

    @abstractmethod
    def list(self):
        """List all objects (students or courses)"""
        pass

class StudentManager(BaseManager):
    def __init__(self):
        self.__students: list[Student] = []

    def input(self):
        """Input number of students and their info"""
        n = read_int("Input number of students: ")
        self.__students = []  # reset
        for i in range(n):
            print(f"\n-- Student {i + 1} --")
            s = Student()
            s.input()
            self.__students.append(s)

    def list(self):
        """List all students"""
        print("\n=== STUDENT LIST ===")
        if not self.__students:
            print("  (No students)")
            return
        for idx, s in enumerate(self.__students):
            print(f"[{idx}] ", end="")
            s.show()

    def get_students(self) -> list[Student]:
        return list(self.__students)

class CourseManager(BaseManager):
    def __init__(self):
        self.__courses: list[Course] = []

    def input(self):
        """Input number of courses and their info"""
        n = read_int("Input number of courses: ")
        self.__courses = []
        for i in range(n):
            print(f"\n-- Course {i + 1} --")
            c = Course()
            c.input()
            self.__courses.append(c)

    def list(self):
        """List all courses"""
        print("\n=== COURSE LIST ===")
        if not self.__courses:
            print("  (No courses)")
            return
        for idx, c in enumerate(self.__courses):
            print(f"[{idx}] ", end="")
            c.show()

    def get_courses(self) -> list[Course]:
        return list(self.__courses)

class MarkManager:
    def __init__(self):
        self.__marks: dict[tuple[str, str], float] = {}

    def input(self, course_manager: CourseManager, student_manager: StudentManager):
        """
        Select a course, input marks for all students in this course.
        Same name 'input' as other managers, but logic khác -> polymorphism by name
        """
        courses = course_manager.get_courses()
        students = student_manager.get_students()

        if not courses:
            print("No courses to input marks.")
            return
        if not students:
            print("No students to input marks.")
            return

        course_manager.list()
        idx = read_int(f"Select course index (0..{len(courses)-1}): ")

        if idx < 0 or idx >= len(courses):
            print("Invalid index.")
            return

        course = courses[idx]
        print(f"\nInput marks for course: {course.name} (ID: {course.id})")

        for s in students:
            mark = read_float(f"  Mark for student {s.id} - {s.name}: ")
            self.__marks[(course.id, s.id)] = mark

    def list(self, course_manager: CourseManager, student_manager: StudentManager):
        """
        Show student marks for a given course.
        Same function name 'list', nhưng ý nghĩa: list marks
        """
        courses = course_manager.get_courses()
        students = student_manager.get_students()

        if not courses:
            print("No courses.")
            return
        if not students:
            print("No students.")
            return

        course_manager.list()
        idx = read_int(f"Select course index to show marks (0..{len(courses)-1}): ")

        if idx < 0 or idx >= len(courses):
            print("Invalid index.")
            return

        course = courses[idx]
        print(f"\n=== MARKS FOR COURSE: {course.name} (ID: {course.id}) ===")

        for s in students:
            key = (course.id, s.id)
            if key in self.__marks:
                print(f"Student {s.id} - {s.name}: {self.__marks[key]}")
            else:
                print(f"Student {s.id} - {s.name}: No mark yet")

class StudentMarkSystem:
    def __init__(self):
        # Encapsulation: các manager là private
        self.__student_manager = StudentManager()
        self.__course_manager = CourseManager()
        self.__mark_manager = MarkManager()

    def run(self):
        while True:
            print("\n===== STUDENT MARK MANAGEMENT =====")
            print("1. Input students")
            print("2. Input courses")
            print("3. List students")
            print("4. List courses")
            print("5. Select a course and input marks")
            print("6. Show student marks for a given course")
            print("0. Exit")

            choice = read_int("Your choice: ")

            if choice == 1:
                self.__student_manager.input()
            elif choice == 2:
                self.__course_manager.input()
            elif choice == 3:
                self.__student_manager.list()
            elif choice == 4:
                self.__course_manager.list()
            elif choice == 5:
                self.__mark_manager.input(self.__course_manager, self.__student_manager)
            elif choice == 6:
                self.__mark_manager.list(self.__course_manager, self.__student_manager)
            elif choice == 0:
                print("Bye!")
                break
            else:
                print("Invalid choice!")

if __name__ == "__main__":
    system = StudentMarkSystem()
    system.run()
