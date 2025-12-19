students = []  
courses = []   
marks = {}     

print("Student Mark Management")

while True:
    print("\n==============================")
    print("1. Input list students")
    print("2. Input list courses")
    print("3. Select a course, input marks for students")
    print("4. List students")
    print("5. List course")
    print("6. Show student marks for a given course")
    print("0. Exit")
    print("==============================")

    choice = input("Choose: ").strip()

    # 1) Input students
    if choice == "1":
        while True:
            s = input("Input number of students in a class: ").strip()
            try:
                n = int(s)
                if n > 0:
                    break
                print("Please enter a POSITIVE integer .")
            except ValueError:
                print("Invalid integer. Try again.")

        students = []
        used_student_ids = set()

        print("\n=== Input student information: id, name, DoB ===")
        for i in range(1, n + 1):
            print(f"\nStudent #{i}")

            while True:
                sid = input("  ID: ").strip()
                if sid == "":
                    print("ID cannot be empty.")
                    continue
                if sid in used_student_ids:
                    print("ID already exists. Enter another.")
                    continue
                break

            while True:
                name = input("  Name: ").strip()
                if name != "":
                    break
                print("Name cannot be empty.")

            while True:
                dob = input("  DoB (e.g., 2004-10-21): ").strip()
                if dob != "":
                    break
                print("DoB cannot be empty.")

            students.append((sid, name, dob))
            used_student_ids.add(sid)

        print("Students saved.")

    # 2) Input courses
    elif choice == "2":
        while True:
            s = input("Input number of courses: ").strip()
            try:
                m = int(s)
                if m > 0:
                    break
                print("Please enter a POSITIVE integer .")
            except ValueError:
                print("Invalid integer. Try again.")

        courses = []
        used_course_ids = set()

        print("\n=== Input course information: id, name ===")
        for i in range(1, m + 1):
            print(f"\nCourse #{i}")

            while True:
                cid = input("  ID: ").strip()
                if cid == "":
                    print("ID cannot be empty.")
                    continue
                if cid in used_course_ids:
                    print("Course ID already exists. Enter another.")
                    continue
                break

            while True:
                cname = input("  Name: ").strip()
                if cname != "":
                    break
                print("Course name cannot be empty.")

            courses.append((cid, cname))
            used_course_ids.add(cid)

        print("Courses saved.")

    # 3) Select course & input marks
    elif choice == "3":
        if len(courses) == 0:
            print("No courses available. Please input courses first (option 2).")
            continue
        if len(students) == 0:
            print("No students available. Please input students first (option 1).")
            continue

        print("\n--- Courses ---")
        for i, c in enumerate(courses, start=1):
            print(f"{i}. {c[0]} - {c[1]}")

        while True:
            mode = input("Choose course by (1) index or (2) ID? Enter 1/2: ").strip()
            if mode == "1":
                while True:
                    s = input("Enter course index: ").strip()
                    try:
                        idx = int(s)
                        if 1 <= idx <= len(courses):
                            course_id = courses[idx - 1][0]
                            course_name = courses[idx - 1][1]
                            break
                        print("Index out of range.")
                    except ValueError:
                        print("Invalid integer.")
                break
            elif mode == "2":
                cid = input("Enter course ID: ").strip()
                found = False
                for c in courses:
                    if c[0] == cid:
                        course_id = c[0]
                        course_name = c[1]
                        found = True
                        break
                if found:
                    break
                print("Course ID not found. Try again.")
            else:
                print("Please enter 1 or 2.")

        min_mark = 0.0
        max_mark = 20.0
        print(f"\n=== Input marks for course: {course_id} - {course_name} ===")
        print(f"Mark range: [{min_mark}, {max_mark}]")

        if course_id not in marks:
            marks[course_id] = {}

        for s in students:
            sid, name, dob = s
            while True:
                raw = input(f"  Mark for {sid} - {name}: ").strip()
                try:
                    val = float(raw)
                    if min_mark <= val <= max_mark:
                        marks[course_id][sid] = val
                        break
                    print(f"Mark must be in range [{min_mark}, {max_mark}].")
                except ValueError:
                    print("Invalid number. Try again.")

        print("Marks updated.")

    # 4) List course
    elif choice == "4":
        print("\n--- Students ---")
        if len(students) == 0:
            print("(empty)")
        else:
            for i, s in enumerate(students, start=1):
                sid, name, dob = s
                print(f"{i}. {sid} | {name} | DoB: {dob}")

    # 5) List students
    elif choice == "5":
        print("\n--- Courses ---")
        if len(courses) == 0:
            print("(empty)")
        else:
            for i, c in enumerate(courses, start=1):
                print(f"{i}. {c[0]} - {c[1]}")


    # 6) Show marks for a course
    elif choice == "6":
        if len(courses) == 0:
            print("No courses available.")
            continue
        if len(students) == 0:
            print("No students available.")
            continue

        print("\n--- Courses ---")
        for i, c in enumerate(courses, start=1):
            print(f"{i}. {c[0]} - {c[1]}")

        # choose course
        while True:
            mode = input("Choose course by (1) index or (2) ID? Enter 1/2: ").strip()
            if mode == "1":
                while True:
                    s = input("Enter course index: ").strip()
                    try:
                        idx = int(s)
                        if 1 <= idx <= len(courses):
                            course_id = courses[idx - 1][0]
                            course_name = courses[idx - 1][1]
                            break
                        print("Index out of range.")
                    except ValueError:
                        print("Invalid integer.")
                break
            elif mode == "2":
                cid = input("Enter course ID: ").strip()
                found = False
                for c in courses:
                    if c[0] == cid:
                        course_id = c[0]
                        course_name = c[1]
                        found = True
                        break
                if found:
                    break
                print("Course ID not found. Try again.")
            else:
                print("Please enter 1 or 2.")

        print(f"\n=== Marks for course: {course_id} - {course_name} ===")
        course_marks = marks.get(course_id, {})

        for s in students:
            sid, name, dob = s
            if sid in course_marks:
                print(f"{sid} - {name}: {course_marks[sid]}")
            else:
                print(f"{sid} - {name}: N/A")

    # 0) Exit
    elif choice == "0":
        print("Exits")
        break

    else:
        print("Invalid choice. Please select 0..6.")
