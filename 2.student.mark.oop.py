from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class Entity(ABC):
    @abstractmethod
    def key(self) -> str:
        """Unique ID"""
        raise NotImplementedError

    @abstractmethod
    def input(self) -> None:
        """Read info from keyboard"""
        raise NotImplementedError

    @abstractmethod
    def display(self) -> str:
        """String for listing"""
        raise NotImplementedError


class Student(Entity):
    def __init__(self, student_id: str = "") -> None:
        self.__id = student_id
        self.__name = ""
        self.__dob = ""

    @property
    def student_id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    def key(self) -> str:
        return self.__id

    def input(self) -> None:
        self.__name = input("  Name: ").strip()
        while self.__name == "":
            print("Name cannot be empty.")
            self.__name = input("  Name: ").strip()

        self.__dob = input("  DoB: ").strip()
        while self.__dob == "":
            print("DoB cannot be empty.")
            self.__dob = input("  DoB: ").strip()

    def display(self) -> str:
        return f"{self.__id} | {self.__name} | DoB: {self.__dob}"


class Course(Entity):
    def __init__(self, course_id: str = "") -> None:
        self.__id = course_id
        self.__name = ""

    @property
    def course_id(self) -> str:
        return self.__id

    def key(self) -> str:
        return self.__id

    def input(self) -> None:
        self.__name = input("  Name: ").strip()
        while self.__name == "":
            print("Course name cannot be empty.")
            self.__name = input("  Name: ").strip()

    def display(self) -> str:
        return f"{self.__id} - {self.__name}"


class MarkSystem:
    def __init__(self) -> None:
        self.__students: List[Student] = []
        self.__courses: List[Course] = []
        self.__marks: Dict[str, Dict[str, float]] = {}  
        self.__min_mark = 0.0
        self.__max_mark = 20.0

    def __input_positive_int(self, prompt: str) -> int:
        while True:
            s = input(prompt).strip()
            try:
                n = int(s)
                if n > 0:
                    return n
                print("Please enter a POSITIVE integer.")
            except ValueError:
                print("Invalid integer. Try again.")

    def __input_int_in_range(self, prompt: str, lo: int, hi: int) -> int:
        while True:
            s = input(prompt).strip()
            try:
                x = int(s)
                if lo <= x <= hi:
                    return x
                print(f"Please enter an integer in range [{lo}, {hi}].")
            except ValueError:
                print("Invalid integer. Try again.")

    def __input_float_in_range(self, prompt: str, lo: float, hi: float) -> float:
        while True:
            s = input(prompt).strip()
            try:
                v = float(s)
                if lo <= v <= hi:
                    return v
                print(f"Mark must be in range [{lo}, {hi}].")
            except ValueError:
                print("Invalid number. Try again.")

    def __list_entities(self, items: List[Entity]) -> None:
        for i, it in enumerate(items, start=1):
            print(f"{i}. {it.display()}")

    def __select_course(self) -> Optional[Course]:
        if not self.__courses:
            print("No courses available.")
            return None

        print("\n--- Courses ---")
        self.__list_entities(self.__courses)

        while True:
            mode = input("Choose course by (1) index or (2) ID? Enter 1/2: ").strip()
            if mode == "1":
                idx = self.__input_int_in_range("Enter course index: ", 1, len(self.__courses))
                return self.__courses[idx - 1]
            elif mode == "2":
                cid = input("Enter course ID: ").strip()
                for c in self.__courses:
                    if c.course_id == cid:
                        return c
                print("Course ID not found. Try again.")
            else:
                print("Please enter 1 or 2.")

    def input_students(self) -> None:
        n = self.__input_positive_int("Input number of students in a class: ")
        self.__students = []
        used = set()

        print("\n=== Input student information: id, name, DoB ===")
        for i in range(1, n + 1):
            print(f"\nStudent #{i}")

            sid = input("  ID: ").strip()
            while sid == "" or sid in used:
                if sid == "":
                    print("ID cannot be empty.")
                else:
                    print("ID already exists. Enter another.")
                sid = input("  ID: ").strip()

            st = Student(sid)
            st.input()
            self.__students.append(st)
            used.add(sid)

        print("Students saved.")

    def input_courses(self) -> None:
        m = self.__input_positive_int("Input number of courses: ")
        self.__courses = []
        used = set()

        print("\n=== Input course information: id, name ===")
        for i in range(1, m + 1):
            print(f"\nCourse #{i}")

            cid = input("  ID: ").strip()
            while cid == "" or cid in used:
                if cid == "":
                    print("ID cannot be empty.")
                else:
                    print("Course ID already exists. Enter another.")
                cid = input("  ID: ").strip()

            c = Course(cid)
            c.input()
            self.__courses.append(c)
            used.add(cid)

        print("Courses saved.")

    def input_marks_for_course(self) -> None:
        if not self.__students:
            print("No students available. Please input students first (option 1).")
            return
        course = self.__select_course()
        if course is None:
            return

        cid = course.course_id
        print(f"\n=== Input marks for course: {course.display()} ===")
        print(f"Mark range: [{self.__min_mark}, {self.__max_mark}]")

        if cid not in self.__marks:
            self.__marks[cid] = {}

        for st in self.__students:
            val = self.__input_float_in_range(
                f"  Mark for {st.student_id} - {st.name}: ",
                self.__min_mark,
                self.__max_mark
            )
            self.__marks[cid][st.student_id] = val

        print("Marks updated.")

    def list_students(self) -> None:
        print("\n--- Students ---")
        if not self.__students:
            print("(empty)")
            return
        self.__list_entities(self.__students)

    def list_courses(self) -> None:
        print("\n--- Courses ---")
        if not self.__courses:
            print("(empty)")
            return
        self.__list_entities(self.__courses)

    def show_marks_for_course(self) -> None:
        if not self.__students:
            print("No students available.")
            return
        course = self.__select_course()
        if course is None:
            return

        cid = course.course_id
        print(f"\n=== Marks for course: {course.display()} ===")
        cm = self.__marks.get(cid, {})

        for st in self.__students:
            if st.student_id in cm:
                print(f"{st.student_id} - {st.name}: {cm[st.student_id]}")
            else:
                print(f"{st.student_id} - {st.name}: N/A")

    def run(self) -> None:
        while True:
            print("\n==============================")
            print(" Student Mark Management")
            print("==============================")
            print("1. Input number of students + student info")
            print("2. Input number of courses + course info")
            print("3. Select a course, input marks for students")
            print("4. List students")
            print("5. List courses")
            print("6. Show student marks for a given course")
            print("0. Exit")

            choice = input("Choose: ").strip()

            if choice == "1":
                self.input_students()
            elif choice == "2":
                self.input_courses()
            elif choice == "3":
                self.input_marks_for_course()
            elif choice == "4":
                self.list_students()
            elif choice == "5":
                self.list_courses()
            elif choice == "6":
                self.show_marks_for_course()
            elif choice == "0":
                print("Exit!")
                break
            else:
                print("Invalid choice. Please select 0..6.")


if __name__ == "__main__":
    MarkSystem().run()
