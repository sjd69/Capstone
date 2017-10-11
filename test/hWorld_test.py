import unittest
from hWorld import hello


class testing(unittest.TestCase):
	def test_case(self):
		test1 = hello("Heidi")
		self.assertEqual(test1, 'Hello World: Heidi')
		
if __name__ == '__main__':
    unittest.main()