import unittest
from HW11.HW11_yu_zhou import Repository


class DataBaseTestCase(unittest.TestCase):
    def test_instructor_table(self):
        calculated = Repository(dir_path=r'/Users/joeyiszy/PycharmProjects/810/HW10')
        DB_FILE = '/Applications/DataGrip.app/Contents/bin/810_starup.db'

        expected = [['98760', 'Darwin, C', 'SYEN', 'SYS 611', '2'],
                    ['98760', 'Darwin, C', 'SYEN', 'SYS 645', '1'],
                    ['98760', 'Darwin, C', 'SYEN', 'SYS 750', '1'],
                    ['98760', 'Darwin, C', 'SYEN', 'SYS 800', '1'],
                    ['98763', 'Newton, I', 'SFEN', 'SSW 555', '1'],
                    ['98763', 'Newton, I', 'SFEN', 'SSW 689', '1'],
                    ['98764', 'Feynman, R', 'SFEN', 'CS 501', '1'],
                    ['98764', 'Feynman, R', 'SFEN', 'CS 545', '1'],
                    ['98764', 'Feynman, R', 'SFEN', 'SSW 564', '3'],
                    ['98764', 'Feynman, R', 'SFEN', 'SSW 687', '3'],
                    ['98765', 'Einstein, A', 'SFEN', 'SSW 540', '3'],
                    ['98765', 'Einstein, A', 'SFEN', 'SSW 567', '4']]

        self.assertEqual(expected, calculated.instructor_table_db(DB_FILE))


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
