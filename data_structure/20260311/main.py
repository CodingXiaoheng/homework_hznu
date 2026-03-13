from student import Student
from sqrt import sqrt as sqrt

stu = Student("Tom", 19)

# stu.add_grade(80)
# stu.add_grade(90)
stu.add_grade("63.281")

stu2 = Student("Jerry", 20)

# stu.add_grade(80)
# stu.add_grade(90)
stu2.add_grade(72)

print(stu.get_details())

print(stu.grades)

print(stu2.get_details())

print(stu2.grades)

print(sqrt(4))