import os
from main import main
import Automation




class dataset():

    def __init__(self,test):
        self.tests = test
        if "bidder" in self.test:
            self.fixturesPath = os.path.join(self.ROOTDIR, "fixtures_Bidder")
        elif "augmentor" in self.test:
            self.fixturesPath = os.path.join(self.ROOTDIR, "fixtures_Augmentor")

        main(self.test).createListOfTestCases()


    def setup(tests):
        for words in tests:
            if len(words) > 0:
                data = Automation.Automation(words)
                print(data)
                main(tests).loadData(data)

    def teardown(tests):
        for words in tests:
            if len(words) > 0:
                data = Automation.Automation(words)
                print(data)
                main(tests).teardown(data)


