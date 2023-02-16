class Student:

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __lt__(self, other):
        if not isinstance(other, Student):
            print('Not a Student.')
            return
        return self.avg_grade() < other.avg_grade()

    def __eq__(self, other):
        if not isinstance(other, Student):
            print('Not a Student.')
            return
        return self.avg_grade() == other.avg_grade()

    def __str__(self):
        actual_courses = ', '.join(self.courses_in_progress)
        finished_courses = ', '.join(self.finished_courses)
        return (f'Имя: {self.name}\nФамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {self.avg_grade()}\n'
                f'Курсы в процессе изучения: {actual_courses}\n'
                f'Завершенные курсы: {finished_courses}'
                )

    def avg_grade(self):
        all_grades_lst = [grade for course_grades in self.grades.values() for grade in course_grades]
        return round(sum(all_grades_lst) / len(all_grades_lst), 1) if len(all_grades_lst) > 0 else 0

    def add_course(self, course):
        if course not in self.courses_in_progress + self.finished_courses:
            self.courses_in_progress.append(course)

    def finish_course(self, course):
        if course in self.courses_in_progress:
            self.courses_in_progress.remove(course)
            self.finished_courses.append(course)

    def rate_lect(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer)
            and course in self.courses_in_progress + self.finished_courses
            and course in lecturer.courses_attached
            and grade in range(1, 11)
        ):

            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]

        else:
            return 'Ошибка'


class Mentor:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'

    def add_course(self, course):
        if course not in self.courses_attached:
            self.courses_attached.append(course)


class Lecturer(Mentor):

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            print('Not a Lecturer.')
            return
        return self.avg_grade() < other.avg_grade()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            print('Not a Lecturer.')
            return
        return self.avg_grade() == other.avg_grade()

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за лекции: {self.avg_grade()}')

    def avg_grade(self):
        all_grades_lst = [grade for course_grades in self.grades.values() for grade in course_grades]
        return round(sum(all_grades_lst) / len(all_grades_lst), 1) if len(all_grades_lst) > 0 else 0


class Reviewer(Mentor):

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'

    def rate_hw(self, student, course, grade):
        if (isinstance(student, Student)
            and course in self.courses_attached
            and course in student.courses_in_progress
            and grade in range(1, 11)
        ):

            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]

        else:
            return 'Ошибка'


def avg_course_grade(course, students):
    for student in students:
        if not isinstance(student, Student):
            return 'Not a Student in the list.'
    course_grades = [grade for student in students
                               for for_course, grades in student.grades.items() if for_course == course
                                   for grade in grades
                     ]
    return sum(course_grades) / len(course_grades) if len(course_grades) > 0 else 0


def avg_course_lecture_grade(course, lecturers):
    for lecturer in lecturers:
        if not isinstance(lecturer, Lecturer):
            return 'Not a Lecturer in the list.'
    course_grades = [grade for lecturer in lecturers
                               for for_course, grades in lecturer.grades.items() if for_course == course
                                   for grade in grades
                     ]
    return sum(course_grades) / len(course_grades) if len(course_grades) > 0 else 0


cool_student = Student('Студент', 'Вечный', 'Мужской')
cool_student.add_course('Python')
cool_student.add_course('Git')
cool_student.add_course('Спортивная стрельба сигарет')
cool_student.add_course('Художественный храп')
cool_student.finish_course('Спортивная стрельба сигарет')

lame_student = Student('Родион', 'Раскольников', 'Мужской')
lame_student.add_course('Спортивная нищета')
lame_student.add_course('Фехтование на топорах')
lame_student.add_course('Python')
lame_student.add_course('Flush')
lame_student.finish_course('Спортивная нищета')
lame_student.finish_course('Фехтование на топорах')

cool_mentor = Mentor('Аристарх', 'Менторской-Залихватский')
lame_mentor = Mentor('Альберт', 'Инструментор')

cool_lecturer = Lecturer('Ганнибал', 'Лектор')
cool_lecturer.add_course('Python')
cool_lecturer.add_course('Git')
cool_lecturer.add_course('Кулинария')

lame_lecturer = Lecturer('Степан', 'Выпускной-Коллектор')
lame_lecturer.add_course('Python')
lame_lecturer.add_course('Flush')

cool_reviewer = Reviewer('Хэл', 'Чеккер')
cool_reviewer.add_course('Python')
cool_reviewer.add_course('Git')
cool_reviewer.add_course('Художественный храп')

lame_reviewer = Reviewer('Гейко', 'Сабмитич')
lame_reviewer.add_course('Python')
lame_reviewer.add_course('Flush')

cool_student.rate_lect(cool_lecturer, 'Git', 9)
cool_student.rate_lect(cool_lecturer, 'Python', 10)

lame_student.rate_lect(lame_lecturer, 'Python', 3)
lame_student.rate_lect(lame_lecturer, 'Flush', 8)

cool_reviewer.rate_hw(cool_student, 'Git', 8)
cool_reviewer.rate_hw(cool_student, 'Python', 9)

lame_reviewer.rate_hw(lame_student, 'Python', 2)
lame_reviewer.rate_hw(lame_student, 'Flush', 4)

print(f'Студент:\n{lame_student}', end='\n\n')
print(f'Ментор:\n{cool_mentor}', end='\n\n')
print(f'Лектор:\n{cool_lecturer}', end='\n\n')
print(f'Проверяющий:\n{cool_reviewer}', end='\n\n')
print(lame_student < cool_student)
print(lame_lecturer == cool_lecturer, end='\n\n')
students = [cool_student, lame_student]
lecturers = [cool_lecturer, lame_lecturer]
print(f"Средняя оценка заданий по курсу Python: {avg_course_grade('Python', students)}")
print(f"Средняя оценка лекций по курсу Python: {avg_course_lecture_grade('Python', lecturers)}")
