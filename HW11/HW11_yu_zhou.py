"""@Author: JoeyIsZY
"""
import sqlite3
import os
from collections import defaultdict
from prettytable import PrettyTable


def file_reading_gen(path, fields, sep=',', header=False):
    # This function is to read field-separated text files and yield a tuple with all of the values from
    # a single line in the file.

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
            if grade in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']:
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


class Major:
    __slots__ = {'major', 'required', 'elective'}

    def __init__(self, major):
        self.major = major
        self.required = set()
        self.elective = set()

    def add_required(self, course):
        self.required = self.required.union(set(course))

    def add_elective(self, course):
        self.elective = self.elective.union(set(course))


class Repository:
    __slots__ = {'student_container', 'instructor_container', 'file_path', 'course_container', 'major_container'}

    def __init__(self, dir_path=os.getcwd, ptables=True):
        self.student_container = dict()
        self.instructor_container = dict()
        self.file_path = dir_path
        self.course_container = list()
        self.major_container = dict()

        # connect the database
        DB_FILE = '/Applications/DataGrip.app/Contents/bin/810_starup.db'
        db = sqlite3.connect(DB_FILE)

        try:
            self.read_student()
            self.read_instructor()
            self.read_major()
            self.read_grade()
        except ValueError as ve:
            print(ve)
        except FileNotFoundError as fnfe:
            print(fnfe)
        if ptables:
            self.student_table()
            self.instructor_table()
            self.major_table()

    def read_student(self):
        student_path = os.path.join(self.file_path, 'students.txt')
        reading_gen = file_reading_gen(student_path, 3, '\t', header=False)
        for cwid, name, major in reading_gen:
            new_student = Student(cwid=cwid, name=name, major=major)
            self.student_container[new_student.cwid] = new_student

    def read_instructor(self):
        instructor_path = os.path.join(self.file_path, 'instructors.txt')
        reading_gen = file_reading_gen(instructor_path, 3, sep='|', header=True)
        for cwid, name, department in reading_gen:
            new_instructor = Instructor(cwid=cwid, name=name, department=department)
            self.instructor_container[new_instructor.cwid] = new_instructor

    def read_grade(self):
        grade_path = os.path.join(self.file_path, 'grades.txt')
        reading_gen = file_reading_gen(grade_path, 4, sep='|', header=True)

        for student_cwid, course, grade, instructor_cwid in reading_gen:
            for stu in self.student_container.values():
                if student_cwid == stu.cwid:
                    stu.add_course_grade(student_cwid, course, grade)

            for ins in self.instructor_container.values():
                if instructor_cwid == ins.cwid:
                    ins.add_course_student_num(instructor_cwid, course)

            self.course_container.append({'student_cwid': student_cwid, 'course': course, 'grade': grade,
                                          'instructor_id': instructor_cwid})

    def read_major(self):
        major_path = os.path.join(self.file_path, 'majors.txt')
        reading_gen = file_reading_gen(major_path, 3, sep='\t', header=False)
        tmp_dict = defaultdict(lambda: defaultdict(set))

        for dept, flag, courses in reading_gen:
            tmp_dict[dept][flag].add(courses)

        for dept, courses in tmp_dict.items():
            new_major = Major(major=dept)

            for flag, course in courses.items():
                if flag == 'R':
                    new_major.add_required(course)
                elif flag == 'E':
                    new_major.add_elective(course)
            self.major_container[dept] = new_major

    def student_table(self):
        field_name = ['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Elective']
        pt = PrettyTable(field_names=field_name)

        for cwid, stu in self.student_container.items():
            remain_required = self.major_container[stu.major].required.difference(stu.get_course_grade().keys())
            remain_elective = sorted(self.major_container[stu.major].elective.intersection(stu.get_course_grade().keys()))

            if len(remain_elective) == 0:
                remain_elective = sorted(self.major_container[stu.major].elective)
            else:
                remain_elective = None
            pt.add_row([cwid, stu.name, stu.major, list(sorted(stu.get_course_grade().keys())),
                        sorted(remain_required), remain_elective])

        print(pt.get_string(sortby='CWID'))

        # prepare for test
        # lst = list()
        # for cwid, stu in self.student_container.items():
        #     lst.append((cwid, stu.name, stu.major, list(sorted(stu.get_course_grade().keys())), sorted(remain_required),
        #                 remain_elective))
        # return lst

    def instructor_table(self):
        field_name = ['CWID', 'Name', 'Dept', 'Course', 'Students']
        pt = PrettyTable(field_names=field_name)
        for cwid, ins in self.instructor_container.items():
            for course, students in ins.get_course_student_num().items():
                pt.add_row([cwid, ins.name, ins.department, course, students])

        print(pt.get_string(sortby='CWID'))

        # prepare for test
        # lst = list()
        # for cwid, ins in self.instructor_container.items():
        #     for course, students in ins.get_course_student_num().items():
        #         lst.append((cwid, ins.name, ins.department, course, students))
        # print(lst)

    def major_table(self):
        field_name = ['Dept', 'Required', 'Elective']
        pt = PrettyTable(field_names=field_name)

        for dept, major in self.major_container.items():
            pt.add_row([dept, sorted(major.required), sorted(major.elective)])

        print(pt)

        # prepare for test
        # lst = list()
        # for dept, major in self.major_container.items():
        #     lst.append([dept, major.required, major.elective])
        # return lst

    def instructor_table_db(self, db_path):
        db = sqlite3.connect(db_path)
        field_name = ['CWID', 'Name', 'Dept', 'Course', 'Students']
        pt = PrettyTable(field_names=field_name)
        lst = list()

        for row in db.execute("select CWID, Name, Dept, course, stuNum from instructors_summary"):
            pt.add_row(list(row))
            lst.append(list(row))
        print('Instructor summary from Database')
        print(pt)

        return lst


def main():
    sit = Repository(dir_path=r'/Users/joeyiszy/PycharmProjects/810/HW10')
    DB_FILE = '/Applications/DataGrip.app/Contents/bin/810_starup.db'
    sit.instructor_table_db(DB_FILE)


if __name__ == '__main__':
    main()