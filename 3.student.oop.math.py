from __future__ import annotations
from abc import ABC, abstractmethod
import curses
import curses.textpad
import math
from typing import Dict, List, Optional, Tuple

try:
    import numpy as np
except Exception:
    np = None


def s_add(stdscr, y: int, x: int, text: str, attr: int = 0):
    try:
        h, w = stdscr.getmaxyx()
        if y < 0 or y >= h:
            return
        if x < 0 or x >= w:
            return
        stdscr.addstr(y, x, text[: max(0, w - x - 1)], attr)
    except curses.error:
        pass


def center(stdscr, y: int, text: str, attr: int = 0):
    h, w = stdscr.getmaxyx()
    x = max(0, (w - len(text)) // 2)
    s_add(stdscr, y, x, text, attr)


def draw_frame(stdscr, title: str, subtitle: str = ""):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    center(stdscr, 1, title, curses.A_BOLD)
    if subtitle:
        center(stdscr, 2, subtitle, curses.A_DIM)
    s_add(stdscr, 3, 2, "-" * max(0, w - 4), curses.A_DIM)
    stdscr.refresh()


def message(stdscr, title: str, lines: List[str]):
    draw_frame(stdscr, title)
    h, w = stdscr.getmaxyx()
    top = 5
    max_lines = max(1, h - top - 3)
    for i in range(min(len(lines), max_lines)):
        s_add(stdscr, top + i, 2, lines[i][: max(0, w - 4)])
    s_add(stdscr, h - 2, 2, "Press any key...", curses.A_DIM)
    stdscr.refresh()
    stdscr.getch()


def input_box(stdscr, title: str, prompt: str) -> str:
    def validator(ch):
        if ch in (10, 13):      # Enter
            return 7            # Ctrl+G để kết thúc Textbox
        if ch in (curses.KEY_BACKSPACE, 127, 8):
            return 8            # Backspace
        return ch

    draw_frame(stdscr, title)
    h, w = stdscr.getmaxyx()

    s_add(stdscr, 5, 2, prompt[: max(0, w - 4)])
    s_add(stdscr, 7, 2, "> ")
    s_add(stdscr, h - 2, 2, "Enter: submit   Backspace: delete", curses.A_DIM)
    stdscr.refresh()

    box_w = max(10, min(60, w - 6))
    edit = curses.newwin(1, box_w, 7, 4)
    edit.bkgd(" ", curses.A_REVERSE)  # làm ô nhập nổi bật
    edit.keypad(True)
    edit.refresh()

    curses.curs_set(1)
    tb = curses.textpad.Textbox(edit)
    s = tb.edit(validator).strip()
    curses.curs_set(0)
    return s



def menu(stdscr, title: str, items: List[Tuple[str, str]]) -> str:
    idx = 0
    while True:
        draw_frame(stdscr, title, "Up/Down to move, Enter to select, q to quit")
        h, w = stdscr.getmaxyx()
        if h < 14 or w < 60:
            message(stdscr, "Resize Terminal", ["Please resize terminal (recommend >= 60x14)."])
            continue

        top = 6
        visible = h - top - 4
        start = 0
        if idx >= visible:
            start = idx - visible + 1

        for i in range(start, min(len(items), start + visible)):
            key, text = items[i]
            line = f"{key}. {text}"
            y = top + (i - start)
            if i == idx:
                s_add(stdscr, y, 4, line[: max(0, w - 8)], curses.A_REVERSE)
            else:
                s_add(stdscr, y, 4, line[: max(0, w - 8)])

        stdscr.refresh()
        k = stdscr.getch()
        if k in (ord("q"), 27):
            return "0"
        if k in (curses.KEY_UP, ord("k")):
            idx = (idx - 1) % len(items)
        elif k in (curses.KEY_DOWN, ord("j")):
            idx = (idx + 1) % len(items)
        elif k in (10, 13, curses.KEY_ENTER):
            return items[idx][0]


def viewer(stdscr, title: str, lines: List[str]):
    pos = 0
    while True:
        draw_frame(stdscr, title, "Up/Down scroll, PgUp/PgDn, q back")
        h, w = stdscr.getmaxyx()
        top = 5
        view_h = max(1, h - top - 3)

        pos = max(0, min(pos, max(0, len(lines) - view_h)))
        for i in range(view_h):
            if pos + i >= len(lines):
                break
            s_add(stdscr, top + i, 2, lines[pos + i][: max(0, w - 4)])

        footer = f"Lines {pos+1}-{min(len(lines), pos+view_h)}/{len(lines)}"
        s_add(stdscr, h - 2, 2, footer, curses.A_DIM)
        stdscr.refresh()

        k = stdscr.getch()
        if k in (ord("q"), 27):
            return
        if k in (curses.KEY_UP, ord("k")):
            pos = max(0, pos - 1)
        elif k in (curses.KEY_DOWN, ord("j")):
            pos = min(max(0, len(lines) - view_h), pos + 1)
        elif k == curses.KEY_NPAGE:
            pos = min(max(0, len(lines) - view_h), pos + view_h)
        elif k == curses.KEY_PPAGE:
            pos = max(0, pos - view_h)


def input_non_empty(stdscr, prompt: str) -> str:
    while True:
        s = input_box(stdscr, "Input", prompt).strip()
        if s:
            return s
        message(stdscr, "Error", ["Input cannot be empty."])


def input_positive_int(stdscr, prompt: str) -> int:
    while True:
        s = input_box(stdscr, "Input", prompt).strip()
        try:
            n = int(s)
            if n > 0:
                return n
            message(stdscr, "Error", ["Please enter a positive integer (>0)."])
        except ValueError:
            message(stdscr, "Error", ["Invalid integer."])


def input_int_in_range(stdscr, prompt: str, lo: int, hi: int) -> int:
    while True:
        s = input_box(stdscr, "Input", prompt).strip()
        try:
            x = int(s)
            if lo <= x <= hi:
                return x
            message(stdscr, "Error", [f"Please enter an integer in range [{lo}, {hi}]."])
        except ValueError:
            message(stdscr, "Error", ["Invalid integer."])


def input_float_in_range(stdscr, prompt: str, lo: float, hi: float) -> float:
    while True:
        s = input_box(stdscr, "Input", prompt).strip()
        try:
            v = float(s)
            if lo <= v <= hi:
                return v
            message(stdscr, "Error", [f"Please enter a value in range [{lo}, {hi}]."])
        except ValueError:
            message(stdscr, "Error", ["Invalid number."])


def input_unique_id(stdscr, prompt: str, used: set) -> str:
    while True:
        s = input_non_empty(stdscr, prompt)
        if s in used:
            message(stdscr, "Error", ["ID already exists."])
        else:
            return s


class Entity(ABC):
    @abstractmethod
    def key(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def input(self, stdscr) -> None:
        raise NotImplementedError

    @abstractmethod
    def display(self) -> str:
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

    def input(self, stdscr) -> None:
        self.__name = input_non_empty(stdscr, "Name: ")
        self.__dob = input_non_empty(stdscr, "DoB (e.g., 2004-10-21): ")

    def display(self) -> str:
        return f"{self.__id} | {self.__name} | DoB: {self.__dob}"


class Course(Entity):
    def __init__(self, course_id: str = "") -> None:
        self.__id = course_id
        self.__name = ""
        self.__credit = 0

    @property
    def course_id(self) -> str:
        return self.__id

    @property
    def credit(self) -> int:
        return self.__credit

    def key(self) -> str:
        return self.__id

    def input(self, stdscr) -> None:
        self.__name = input_non_empty(stdscr, "Course name: ")
        self.__credit = input_positive_int(stdscr, "Credit (positive int): ")

    def display(self) -> str:
        return f"{self.__id} - {self.__name} (credit={self.__credit})"


class MarkSystem:
    def __init__(self) -> None:
        self.__students: List[Student] = []
        self.__courses: List[Course] = []
        self.__marks: Dict[str, Dict[str, float]] = {}
        self.__min_mark = 0.0
        self.__max_mark = 20.0

    def floor_1_decimal(self, x: float) -> float:
        return math.floor(x * 10.0) / 10.0

    def calc_gpa(self, student_id: str) -> Optional[float]:
        credit_map = {c.course_id: c.credit for c in self.__courses}
        marks_list = []
        credits_list = []
        for course_id, st_marks in self.__marks.items():
            if student_id in st_marks and course_id in credit_map:
                marks_list.append(st_marks[student_id])
                credits_list.append(credit_map[course_id])
        if not marks_list:
            return None
        m = np.array(marks_list, dtype=float)
        c = np.array(credits_list, dtype=float)
        denom = float(c.sum())
        if denom <= 0:
            return None
        return float((m * c).sum() / denom)

    def sort_students_by_gpa_desc(self):
        def k(st: Student):
            g = self.calc_gpa(st.student_id)
            if g is None:
                return (1, 0.0)
            return (0, -g)
        self.__students.sort(key=k)

    def input_students(self, stdscr) -> None:
        n = input_positive_int(stdscr, "Number of students: ")
        self.__students = []
        used = set()
        for i in range(1, n + 1):
            message(stdscr, "Student", [f"Student #{i}"])
            sid = input_unique_id(stdscr, "ID: ", used)
            st = Student(sid)
            st.input(stdscr)
            self.__students.append(st)
            used.add(sid)
        message(stdscr, "Done", ["Students saved."])

    def input_courses(self, stdscr) -> None:
        m = input_positive_int(stdscr, "Number of courses: ")
        self.__courses = []
        used = set()
        for i in range(1, m + 1):
            message(stdscr, "Course", [f"Course #{i}"])
            cid = input_unique_id(stdscr, "ID: ", used)
            c = Course(cid)
            c.input(stdscr)
            self.__courses.append(c)
            used.add(cid)
        message(stdscr, "Done", ["Courses saved."])

    def list_courses(self, stdscr) -> None:
        lines = ["Courses:"]
        if not self.__courses:
            lines.append("(empty)")
        else:
            for i, c in enumerate(self.__courses, start=1):
                lines.append(f"{i}. {c.display()}")
        viewer(stdscr, "Courses", lines)

    def list_students(self, stdscr) -> None:
        lines = ["Students:"]
        if not self.__students:
            lines.append("(empty)")
        else:
            for i, st in enumerate(self.__students, start=1):
                g = self.calc_gpa(st.student_id)
                g_str = f"{g:.4f}" if g is not None else "N/A"
                lines.append(f"{i}. {st.display()} | GPA={g_str}")
        viewer(stdscr, "Students", lines)

    def select_course(self, stdscr) -> Optional[Course]:
        if not self.__courses:
            message(stdscr, "Error", ["No courses available."])
            return None

        lines = ["Courses:"]
        for i, c in enumerate(self.__courses, start=1):
            lines.append(f"{i}. {c.display()}")
        viewer(stdscr, "Select Course", lines + ["", "Tip: You can choose by index or by ID."])

        mode = input_non_empty(stdscr, "Choose by index (1) or ID (2): ")
        if mode == "1":
            idx = input_int_in_range(stdscr, "Course index: ", 1, len(self.__courses))
            return self.__courses[idx - 1]
        if mode == "2":
            cid = input_non_empty(stdscr, "Course ID: ")
            for c in self.__courses:
                if c.course_id == cid:
                    return c
            message(stdscr, "Error", ["Course ID not found."])
            return None

        message(stdscr, "Error", ["Invalid choice. Use 1 or 2."])
        return None

    def select_student(self, stdscr) -> Optional[Student]:
        if not self.__students:
            message(stdscr, "Error", ["No students available."])
            return None

        lines = ["Students:"]
        for i, st in enumerate(self.__students, start=1):
            lines.append(f"{i}. {st.display()}")
        viewer(stdscr, "Select Student", lines + ["", "Tip: You can choose by index or by ID."])

        mode = input_non_empty(stdscr, "Choose by index (1) or ID (2): ")
        if mode == "1":
            idx = input_int_in_range(stdscr, "Student index: ", 1, len(self.__students))
            return self.__students[idx - 1]
        if mode == "2":
            sid = input_non_empty(stdscr, "Student ID: ")
            for st in self.__students:
                if st.student_id == sid:
                    return st
            message(stdscr, "Error", ["Student ID not found."])
            return None

        message(stdscr, "Error", ["Invalid choice. Use 1 or 2."])
        return None

    def input_marks_for_course(self, stdscr) -> None:
        if not self.__students:
            message(stdscr, "Error", ["Input students first."])
            return
        if not self.__courses:
            message(stdscr, "Error", ["Input courses first."])
            return

        course = self.select_course(stdscr)
        if course is None:
            return

        cid = course.course_id
        if cid not in self.__marks:
            self.__marks[cid] = {}

        message(
            stdscr,
            "Input Marks",
            [
                f"Course: {course.display()}",
                f"Range: [{self.__min_mark}, {self.__max_mark}]",
                "Scores will be floor-rounded to 1 decimal."
            ]
        )

        for st in self.__students:
            raw = input_float_in_range(
                stdscr,
                f"Mark for {st.student_id} - {st.name}: ",
                self.__min_mark,
                self.__max_mark
            )
            self.__marks[cid][st.student_id] = self.floor_1_decimal(raw)

        message(stdscr, "Done", ["Marks updated."])

    def show_marks_for_course(self, stdscr) -> None:
        if not self.__students or not self.__courses:
            message(stdscr, "Error", ["Need students and courses first."])
            return

        course = self.select_course(stdscr)
        if course is None:
            return

        cid = course.course_id
        cm = self.__marks.get(cid, {})

        lines = [f"Marks for {course.display()}:"]
        for st in self.__students:
            if st.student_id in cm:
                lines.append(f"{st.student_id} - {st.name}: {cm[st.student_id]:.1f}")
            else:
                lines.append(f"{st.student_id} - {st.name}: N/A")

        viewer(stdscr, "Marks", lines)

    def show_gpa_for_student(self, stdscr) -> None:
        if not self.__students:
            message(stdscr, "Error", ["Input students first."])
            return

        st = self.select_student(stdscr)
        if st is None:
            return

        g = self.calc_gpa(st.student_id)
        if g is None:
            message(stdscr, "GPA", [f"{st.student_id} - {st.name}", "GPA: N/A (no marks yet)"])
        else:
            message(stdscr, "GPA", [f"{st.student_id} - {st.name}", f"GPA: {g:.4f}"])

    def run(self, stdscr) -> None:
        items = [
            ("1", "Input students"),
            ("2", "Input courses"),
            ("3", "Select a course, input marks (floor 1 decimal)"),
            ("4", "List courses"),
            ("5", "List students (with GPA)"),
            ("6", "Show student marks for a course"),
            ("7", "Show GPA for a student"),
            ("8", "Sort students by GPA descending"),
            ("0", "Exit"),
        ]

        while True:
            choice = menu(stdscr, "Practice 3 - Student Mark Management", items)
            if choice == "0":
                return
            if choice == "1":
                self.input_students(stdscr)
            elif choice == "2":
                self.input_courses(stdscr)
            elif choice == "3":
                self.input_marks_for_course(stdscr)
            elif choice == "4":
                self.list_courses(stdscr)
            elif choice == "5":
                self.list_students(stdscr)
            elif choice == "6":
                self.show_marks_for_course(stdscr)
            elif choice == "7":
                self.show_gpa_for_student(stdscr)
            elif choice == "8":
                self.sort_students_by_gpa_desc()
                message(stdscr, "Done", ["Students sorted by GPA descending."])
            else:
                message(stdscr, "Error", ["Invalid choice."])


def main(stdscr):
    if np is None:
        stdscr.clear()
        s_add(stdscr, 1, 2, "numpy is not installed.", curses.A_BOLD)
        s_add(stdscr, 3, 2, "Fix (Ubuntu): sudo apt install python3-numpy")
        s_add(stdscr, 4, 2, "or inside venv: pip install numpy")
        s_add(stdscr, 6, 2, "Press any key to exit...", curses.A_DIM)
        stdscr.refresh()
        stdscr.getch()
        return

    curses.curs_set(0)
    stdscr.keypad(True)
    MarkSystem().run(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
