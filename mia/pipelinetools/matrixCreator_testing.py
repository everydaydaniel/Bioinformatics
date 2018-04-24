import unittest
from matrix_creator import Matrix


row1 = "Probe1-1	1	10	NS500358:107:H75GCBGXY:1:13307:22748:15645/1	37	+".split()
row2 = "Probe1-1	1	5	NS500358:107:H75GCBGXY:1:23111:19558:3009/2	25	-".split()
row3 = "Probe1-1	3	5	NS500358:107:H75GCBGXY:1:13307:22748:15645/1	37	+".split()
row4 = "Probe1-1	15	20	NS500358:107:H75GCBGXY:1:13307:22748:15645/1	37	+".split()
row5 = "Probe1-2	1	5	NS500358:107:H75GCBGXY:1:13307:22748:15645/1	37	+".split()
row6 = "Probe1-1	20	21	NS500358:107:H75GCBGXY:1:13307:22748:15645/1	37	+".split()
row7 = "Probe1-2	1	2	NS500358:107:H75GCBGXY:1:13307:22748:15645/1	37	+".split()


class TestMatrix(unittest.TestCase):

    def setUp(self):
        # create the matrix
        self.matrix = Matrix()

    def test_rows(self):
        m = self.matrix
        # check that the matrix is being created
        self.assertEqual(m.matrix, {})
        # adding to the rows
        m.add(row1)
        self.assertEqual(m.matrix, {"Probe1-1": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})
        m.add(row2)
        self.assertEqual(m.matrix, {"Probe1-1": [2, 2, 2, 2, 2, 1, 1, 1, 1, 1]})
        m.add(row3)
        self.assertEqual(m.matrix, {"Probe1-1": [2, 2, 3, 3, 3, 1, 1, 1, 1, 1]})
        m.add(row4)
        self.assertEqual(
            m.matrix,
            {"Probe1-1": [2, 2, 3, 3, 3, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]}
        )
        m.add(row5)
        # check that the new row added has the max length
        self.assertEqual(
            m.matrix,
            {
                "Probe1-1": [2, 2, 3, 3, 3, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                "Probe1-2": [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            }
        )
        m.add(row6)
        self.assertEqual(
            m.matrix,
            {
                "Probe1-1": [2, 2, 3, 3, 3, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 1],
                "Probe1-2": [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            }
        )
        # check that vector gets extended
        m.add(row7)
        self.assertEqual(
            m.matrix,
            {
                "Probe1-1": [2, 2, 3, 3, 3, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 1],
                "Probe1-2": [2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            }
        )

    def testAddEnds(self):
        m = Matrix(ends=True)
        # check that the matrix is being created
        self.assertEqual(m.matrix, {})
        self.assertEqual(m.ends, True)
        m.add(row1)
        self.assertEqual(m.ends, True)
        self.assertEqual(m.matrix, {"Probe1-1": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]})
        m.add(row2)
        self.assertEqual(m.matrix, {"Probe1-1": [0, 0, 0, 0, 1, 0, 0, 0, 0, 1]})
        m.add(row3)
        self.assertEqual(m.matrix, {"Probe1-1": [0, 0, 0, 0, 2, 0, 0, 0, 0, 1]})
        m.add(row3)
        self.assertEqual(m.matrix, {"Probe1-1": [0, 0, 0, 0, 3, 0, 0, 0, 0, 1]})
        m.add(row4)
        self.assertEqual(
            m.matrix, {"Probe1-1": [0, 0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}
        )
        m.add(row5)
        self.assertEqual(
            m.matrix, {
                "Probe1-1": [0, 0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                "Probe1-2": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            }
        )
        m.add(row6)
        self.assertEqual(
            m.matrix, {
                "Probe1-1": [0, 0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                "Probe1-2": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            }
        )
        m.normalizeMatrixRow(m.matrix["Probe1-2"])
        self.assertEqual(
            m.matrix, {
                "Probe1-1": [0, 0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                "Probe1-2": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            }
        )
        m.add(row7)
        self.assertEqual(
            m.matrix, {
                "Probe1-1": [0, 0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                "Probe1-2": [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            }
        )


if __name__ == '__main__':
    unittest.main()
