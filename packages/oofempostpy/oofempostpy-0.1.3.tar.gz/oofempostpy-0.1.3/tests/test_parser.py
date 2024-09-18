import unittest
from oofempostpy import parse_simulation_log, log2csv, hm2oofem

class TestParser(unittest.TestCase):
    def test_parse_simulation_log(self):
        log_data = """
        Solving [step number 1.0,
        EngngModel info: user time consumed by solution step 1: 0.001s
        Equilibrium reached in 2 iterations
        """
        with open('test.log', 'w') as f:
            f.write(log_data)

        result = parse_simulation_log('test.log')
        self.assertEqual(result['Solution Steps'], [1])
        self.assertEqual(result['User Times'], [0.001])
        self.assertEqual(result['Iterations'], [2])

    def test_log2csv(self):
        data = {
            'Solution Steps': [1],
            'User Times': [0.001],
            'Iterations': [2]
        }
        log2csv(data, 'test.csv')

        with open('test.csv', 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 2)  # Header + 1 data row

if __name__ == '__main__':
    unittest.main()
