import math
import numpy as np

def floor(a):
    b = a*10
    c = math.floor(b)
    return c/10

class Student():
    def __init__(self):
        self.id = ""
        self.name = ""
        self.dob = ""
    
    def input(self):
        self.id = input("ID: ")
        self.name = input("Name: ")
        self.dob = input("Dob: ")

    def display(self):
        print(f"ID: {self.id}, Name: {self.name}, Dob: {self.dob}")
    
class Course():
    def __init__(self):
        self.id = ""
        self.name = ""
        self.credit = ""

    def input(self):
        self.id = input("ID: ")
        self.name =input("Name: ")
        self.credit = input("Credit: ")

    def display(self):
        print(f"ID: {self.id}, Name: {self.name}, Credit: {self.credit}")

class Mark():
    def __init__(self,student_id="", course_id="", mark=0):
        self.student_id = student_id
        self.course_id = course_id
        self.mark = mark

    def display(self):
        print(f"Student ID: {self.student_id}, Course ID: {self.course_id}, Mark: {self.mark}")

class SudentManagement():
    def __init__(self):
        self.Student = []
        self.Course = []
        self.mark = []

    def inputStudent(self):
        n = int(input("Input number of student: "))
        for i in range(n):
            print("Input Information Student")
            s = Student()
            s.input()
            self.Student.append(s)
    def inputCourse(self):
        c = int(input("Input number of course: "))
        for i in range(c):
            print("Input Infor Course")
            cr = Course()
            cr.input()
            self.Course.append(cr)

    def displayStudent(self):
        print("\n==List Student:==")
        for s in self.Student:
            s.display()

    def displayCousre(self):
        print("\n==List Course:==")
        for c in self.Course:
            c.display()
    
    def MarkForStudent(self):
        cid = input("Select a course: ")
        course = None
        for c in self.Course:
            if c.id == cid:
                course = c
                break

        if course is None:
            print("Not Found")
            return
        print(f"\nInput mark for {course.name} ({course.id})")

        for s in self.Student:
            kq = float(input(f"Score for {s.name} ({s.id}):"))
            self.mark.append(Mark(s.id, course.id, floor(kq)))

    def show_mark(self):
        if not self.Course:
            print("No courses")
            return
        
        cid = input("Show marks for course ID: ")

        course_name = None
        for c in self.Course:
            if c.id == cid:
                course_name = c.name
                break
        
        if course_name is None:
            print("Course not found!")
            return

        print(f"\n== Marks for {course_name} ({cid}) ==")

        has_any = False
        for m in self.mark:
            if m.course_id == cid:
                print(f"{m.student_id} -> {m.mark}")
                has_any = True

        if not has_any:
            print("No marks for this course yet.")

    def GPA(self):
        if not self.Student:
            print("No student then calculate GPA")
            return
        
        sid = input("Choose one student in list student: ")

        a = np.array([])
        b = 0

        for m in self.mark:
            if sid == m.student_id:
                a = np.append(a,m.mark)

        print(a)

sm = SudentManagement()
sm.inputStudent()
sm.inputCourse()
sm.displayStudent()
sm.displayCousre()
sm.MarkForStudent()
sm.show_mark()
sm.GPA()