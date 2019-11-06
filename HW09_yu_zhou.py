"""@Author: JoeyIsZY"""
import os
from prettytable import PrettyTable


def file_reading_gen(path, fields, sep=',', header=False):
    """ This function is to read field-separated text files and yield a tuple with all of the values from a single line
    in the file """
    try:
        fp = open(path, 'r')
    except FileNotFoundError:
        raise ValueError(f" Can't open {path}")
    else:
        with fp:
            lines = fp.readlines()
            for offset, line in enumerate(lines):
                ln = line.strip()
                item = ln.split(sep)
                if len(item) == fields:
                    if header == True:
                        header = False
                        continue
                    else:
                        yield tuple(item)
                else:
                    raise ValueError(f'Excepted {fields} fields is not {len(item)}.')


class Student:
    __slots__ = {'cwid', 'name', 'major', 'letter_grade'}

    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.letter_grade = dict()

    def add_course_grade(self, cwid, course, grade):
        if cwid == self.cwid:
            self.letter_grade[course] = grade

    def get_course_grade(self):
        return self.letter_grade


class Instructor:
    __slots__ = {'cwid', 'name', 'department', 'course_student_num'}

    def __init__(self, cwid, name, department):
        self.cwid = cwid
        self.name = name
        self.department = department
        self.course_student_num = dict()

    def add_course_student_num(self, cwid, course,):
        if cwid == self.cwid:
            self.course_student_num.setdefault(course, 0)
            self.course_student_num[course] += 1

    def get_course_student_num(self):
        return self.course_student_num


class Repository:
    __slots__ = {'student_container', 'instructor_container', 'file_path', 'course_container'}

    def __init__(self, dir_path=os.getcwd):
        self.student_container = dict()
        self.instructor_container = dict()
        self.file_path = dir_path
        self.course_container = list()

    def read_student(self):
        student_path = os.path.join(self.file_path, 'students.txt')
        reading_gen = file_reading_gen(student_path, 3, '\t', False)
        for cwid, name, major in reading_gen:
            new_student = Student(cwid=cwid, name=name, major=major)
            self.student_container[new_student.cwid] = new_student

    def read_instructor(self):
        instructor_path = os.path.join(self.file_path, 'instructors.txt')
        reading_gen = file_reading_gen(instructor_path, 3, '\t', False)
        for cwid, name, department in reading_gen:
            new_instructor = Instructor(cwid=cwid, name=name, department=department)
            self.instructor_container[new_instructor.cwid] = new_instructor

    def read_grade(self):
        grade_path = os.path.join(self.file_path, 'grades.txt')
        reading_gen = file_reading_gen(grade_path, 4, '\t', False)
        for student_cwid, course, grade, instructor_cwid in reading_gen:
            for stu in self.student_container.values():
                if student_cwid == stu.cwid:
                    stu.add_course_grade(student_cwid, course, grade)

            for ins in self.instructor_container.values():
                if instructor_cwid == ins.cwid:
                    ins.add_course_student_num(instructor_cwid, course)

            self.course_container.append({'student_cwid': student_cwid, 'course': course, 'grade': grade,
                                          'instructor_id': instructor_cwid})

    def student_table(self):
        field_name = ['CWID', 'Name', 'Completed Courses']
        pt = PrettyTable(field_names=field_name)
        for cwid, stu in self.student_container.items():
            pt.add_row([cwid, stu.name, list(sorted(stu.get_course_grade().keys()))])

        print(pt.get_string(sortby='CWID'))
        return pt.get_string(sortby='CWID')

    def instructor_table(self):
        field_name = ['CWID', 'Name', 'Dept', 'Course', 'Students']
        pt = PrettyTable(field_names=field_name)
        for cwid, ins in self.instructor_container.items():
            for course, students in ins.get_course_student_num().items():
                pt.add_row([cwid, ins.name, ins.department, course, students])

        print(pt.get_string(sortby='CWID'))
        return pt.get_string(sortby='CWID')


def main():
    sit = Repository(dir_path=r'/Users/joeyiszy/PycharmProjects/810/HW9')
    sit.read_student()
    sit.read_instructor()
    sit.read_grade()
    sit.instructor_table()
    sit.student_table()


if __name__ == '__main__':
    main()




