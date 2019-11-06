import unittest
from HW10.HW10_yu_zhou import Repository


class TestRepository(unittest.TestCase):

    def test_students_table(self):
        calculated = Repository(dir_path=r'/Users/joeyiszy/PycharmProjects/810/HW10')
        calculated.read_student()
        calculated.read_instructor()
        calculated.read_grade()
        calculated.read_major()

        expected = [('10103', 'Baldwin, C', 'SFEN', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], ['SYS 612', 'SYS 671', 'SYS 800'], None),
                    ('10115', 'Wyatt, X', 'SFEN', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], ['SYS 612', 'SYS 671', 'SYS 800'], None),
                    ('10172', 'Forbes, I', 'SFEN', ['SSW 555', 'SSW 567'], ['SYS 612', 'SYS 671', 'SYS 800'], None),
                    ('10175', 'Erickson, D', 'SFEN', ['SSW 564', 'SSW 567', 'SSW 687'], ['SYS 612', 'SYS 671', 'SYS 800'], None),
                    ('10183', 'Chapman, O', 'SFEN', ['SSW 689'], ['SYS 612', 'SYS 671', 'SYS 800'], None),
                    ('11399', 'Cordova, I', 'SYEN', ['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], None),
                    ('11461', 'Wright, U', 'SYEN', ['SYS 611', 'SYS 750', 'SYS 800'], ['SYS 612', 'SYS 671', 'SYS 800'], None),
                    ('11658', 'Kelly, P', 'SYEN', [], ['SYS 612', 'SYS 671', 'SYS 800'], None),
                    ('11714', 'Morton, A', 'SYEN', ['SYS 611', 'SYS 645'], ['SYS 612', 'SYS 671', 'SYS 800'], None),
                    ('11788', 'Fuller, E', 'SYEN', ['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], None)]

        self.assertEqual(calculated.student_table(), expected)

    def test_instructor_table(self):
        calculated = Repository(dir_path=r'/Users/joeyiszy/PycharmProjects/810/HW10')
        calculated.read_student()
        calculated.read_instructor()
        calculated.read_grade()
        calculated.read_major()

        expected = [('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4),
                    ('98765', 'Einstein, A', 'SFEN', 'SSW 540', 3),
                    ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 3),
                    ('98764', 'Feynman, R', 'SFEN', 'SSW 687', 3),
                    ('98764', 'Feynman, R', 'SFEN', 'CS 501', 1),
                    ('98764', 'Feynman, R', 'SFEN', 'CS 545', 1),
                    ('98763', 'Newton, I', 'SFEN', 'SSW 555', 1),
                    ('98763', 'Newton, I', 'SFEN', 'SSW 689', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 800', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 750', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 611', 2),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 645', 1)]

        self.assertEqual(calculated.instructor_table(), expected)

    def test_major_table(self):
        calculated = Repository(dir_path=r'/Users/joeyiszy/PycharmProjects/810/HW10')
        calculated.read_student()
        calculated.read_instructor()
        calculated.read_grade()
        calculated.read_major()

        expected = [['SFEN', {'SSW 564', 'SSW 555', 'SSW 540', 'SSW 567'}, {'CS 513', 'CS 501', 'CS 545'}],
                    ['SYEN', {'SYS 612', 'SYS 800', 'SYS 671'}, {'SSW 565', 'SSW 540', 'SSW 810'}]]

        self.assertEqual(calculated.major_table(), expected)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
