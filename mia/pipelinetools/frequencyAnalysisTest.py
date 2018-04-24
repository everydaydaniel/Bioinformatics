import unittest
import frequencyAnalysis


class frequencyAnalysisTest(unittest.TestCase):

    def setUp(self):
        self.getFilePaths = frequencyAnalysis.getFilePaths

    def test_get_file_paths(self):
        result = self.getFilePaths("testFiles/testDir")
        self.assertEqual(result, ["testFiles/testDir/B.txt", "testFiles/testDir/A.txt"])

    def test_fa_wa(self):
        weighted_average = frequencyAnalysis.weighted_std_dev


if __name__ == '__main__':
    unittest.main()
