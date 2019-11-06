import unittest

from HW9.HW09_yu_zhou import Repository, file_reading_gen


class TestRepository(unittest.TestCase):
    def test_student_table(self):
        sit = Repository(dir_path=r'/Users/joeyiszy/PycharmProjects/810/HW9/TestCase')
        sit.read_student()
        sit.read_instructor()
        sit.read_grade()

        lst = list()
        for cwid, stu in sit.student_container.items():
            lst.append((cwid, stu.name, list(stu.get_course_grade().keys())))

        self.assertEqual(lst, [('10103', 'Yu, Z', ['SSW 567'])])

    def test_instructor_table(self):
        sit = Repository(dir_path=r'/Users/joeyiszy/PycharmProjects/810/HW9/TestCase')
        sit.read_student()
        sit.read_instructor()
        sit.read_grade()

        lst = list()
        for cwid, ins in sit.instructor_container.items():
            for course, students in ins.get_course_student_num().items():
                lst.append((cwid, ins.name, ins.department, course, students))

        self.assertEqual(lst, [('98765', 'Rowland, J', 'SFEN', 'SSW 567', 1)])


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
