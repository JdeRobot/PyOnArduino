import unittest
from . import ComplubotExamplesTests
from . import SergioRobotExampleTests
from . import MBotExamplesTest
from . import TranslatorTests

def Examples_tests():
	test_to_run=[ComplubotExamplesTests,SergioRobotExampleTests,MBotExamplesTest,TranslatorTests]
	loader = unittest.TestLoader()
	suite_list=[]
	for test in test_to_run:
		suite = loader.loadTestsFromModule(test)
		suite_list.append(suite)
	
	big_suite = unittest.TestSuite(suite_list)
	return big_suite	