n = int(input("Input number of student in class: "))

student = []

for i in range(n):
    print("==========================\nInput infor student")
    id = input("ID: ")
    name = input("Name: ")
    Dob = input("Dob: ")

    stu = (id, name, Dob)

    student.append(stu)

print("======================")
c = int(input("Input number of course: "))

course = []

for i in range(c):
    print("==========================\nInput infor course")
    id = input("ID: ")
    name = input("Name: ")

    cr = (id, name)

    course.append(cr)

s = input("Select a course: ")

mark = []

d = [cr[0] for cr in course]
if s not in d:
    print("course not found")
else:
    for id, name, dob in student:
        m = float(input(f"input mark for {name} in course {s}: "))
        mark.append((s, id,name, m))

print("=======================\nList Course")
for cr in course:
    print(f"ID: {cr[0]},\n Name: {cr[1]}\n")

print("=======================\nList Student")
for stu in student:
    print(f"ID: {stu[0]},\n Name: {stu[1]},\n Dob: {stu[2]}\n")

print("=======================\nMark")
for m in mark:
    print(f"\nCourse ID: {m[0]},\n Student ID: {m[1]},\n Name: {m[2]}, Mark: {m[3]}\n")