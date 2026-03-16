from student import Student,StudentFeatureTest
from sqrt import sqrt

test = StudentFeatureTest()
test.test_empty_grades()
test.test_invalid_input()
test.test_instance_independences()

# 第一个学生
stu = Student("Tom", 19)
# 空分数测试
print(stu.get_average_grade())
# 输入转换测试
stu.add_grade("63.281")

# 第二个学生
stu2 = Student("Jerry", 20)
stu2.add_grade(80)
stu2.add_grade(90)
stu2.add_grade(72)

#封装测试
stu.grades.clear()
print(stu.grades)
print(stu2.grades)


# 独立性测试
print(stu.get_details())
print(stu2.get_details())

# 扩展题
print(sqrt(4))