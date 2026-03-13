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