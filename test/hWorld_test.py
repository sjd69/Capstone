import unittest
from DeployApp.src import hWorld
from pyVim import connect
import ssl


class testing(unittest.TestCase):
	def test_case(self):
		s = ssl._create_unverified_context()

		my_cluster = connect.Connect(host='127.0.0.1',
		user = 'user',
		pwd = 'pass',
		port=8989,
		sslContext=s)
		
		if not my_cluster:
			print('didn\'t work')
		else:
			test1 = hello("Heidi")
			self.assertEqual(test1, 'Hello World: Heidi')
		
		connect.Disconnect(my_cluster)
if __name__ == '__main__':
    unittest.main()
	
