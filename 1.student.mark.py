student = []
course = []
mark = []

while True:
    n = input("Input number of student in class: ")

    if not n or not n.isdigit():
        print("Please enter the positive number of student in classs")
        continue

    n=int(n)
    if n < 1:
        print("Please enter number > 0")
        continue

    break
    
for i in range(n):
    print("\n=====Input infor student=====")
    id = input("ID: ")
    name = input("Name: ")
    Dob = input("Dob: ")

    stu = (id, name, Dob)

    student.append(stu)

print("======================")
while True:
    c = int(input("Input number of course: "))

    if not n or not n.isdigit():
        print("Please enter the positive number of student in classs")
        continue

    n=int(n)
    if n < 1:
        print("Please enter number > 0")
        continue

    break

for i in range(c):
    print("\n=====Input infor course=====")
    id = input("ID: ")
    name = input("Name: ")

    cr = (id, name)

    course.append(cr)

s = input("Select a course: ")

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