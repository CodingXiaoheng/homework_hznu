class Student:
    def __init__(self, name: str, age: int):
        self.__name = name
        self.__age = age
        self.__grades = []

    def add_grade(self, grade: float):
        if not isinstance(grade, (int, float)):
            try:
                grade = float(grade)
            except ValueError:
                raise TypeError("Grade must be a number")
        if grade < 0:
            raise ValueError("Grade cannot be negative")
        self.__grades.append(grade)

    def get_average_grade(self):
        if not self.__grades:
            return 0
        return sum(self.__grades) / len(self.__grades)

    def get_details(self):
        return (self.__name, self.__age, round(self.get_average_grade(), 2))

    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        return self.__age

    @property
    def grades(self):
        return self.__grades.copy()

class StudentFeatureTest:
    def test_empty_grades(self):
        s = Student("Tom", 19)
        try:
            if isinstance(s.get_average_grade(),(int, float)):
                print("Test empty grades succeed!")
                return
            print("Test empty grades failed!")
        except:
            print("Test empty grades failed!")

    def test_invalid_input(self):
        s = Student("Tom", 19)
        s.add_grade(90)
        s.add_grade(80)
        s.add_grade("70")
        try:
            s.add_grade("abc")
            print("Test invalid input failed!")
        except:
            if s.grades == [90, 80, 70]:
                print("Test invalid input succeed!")
            else:
                print("Test invalid input failed!")

    def test_instance_independences(self):
        s1 = Student("Tom", 19)
        s2 = Student("Jerry", 20)
        s1.add_grade(90)
        s2.add_grade(80)
        s1.add_grade(80)
        s2.add_grade(70)
        if not s1.grades == [90, 80] and not s2.grades == [80, 70]:
            print("Test instance independences failed!")
        if not s1.name == "Tom" and not s2.name == "Jerry":
            print("Test instance independences failed!")
        if not s1.age == 19 and not s2.age == 20:
            print("Test instance independences failed!")
        print("Test instance independences succeed!")

if __name__ == "__main__":
    test = StudentFeatureTest()
    test.test_empty_grades()
    test.test_invalid_input()
    test.test_instance_independences()



    
    