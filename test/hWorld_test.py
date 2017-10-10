import unittest
from hWorld import hello


class testing(unittest.TestCase):
    
    def test_string(self):
        arr = ['Jordan','Heidi','Alex','Mama','Tyree','Tim','Paul']
        for x in arr:
            print(x)
            self.assertEqual(hello(x), 'Hello World: '+x)

if __name__ == '__main__':
    unittest.main()
