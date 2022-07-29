import os
from main import main
import bidderAutomation




class dataset():

    def __init__(self,test):
        self.tests = test
        if "bidder" in self.test:
            self.fixturesPath = os.path.join(self.ROOTDIR, "fixtures_Bidder")
        elif "augmentor" in self.test:
            self.fixturesPath = os.path.join(self.ROOTDIR, "fixtures_Augmentor")

        main(self.test).createListOfTestCases()

    # fixPath = os.path.join(main().fixturesPath, "testCases.txt")
    # testCases = open(fixPath)
    # tests = [test for test in testCases.read().split('\n')]
    #     resourcesPath = os.path.join(main(self.test).ROOTDIR, "resources")

    # if "bidder" in tests:
    #     fixturesPath = os.path.join(ROOTDIR, "fixtures_Bidder")
    # elif "augment" in tests:
    #     fixturesPath = os.path.join(ROOTDIR, "fixtures_Augmentor")
    # def setFixturePath(tests):
    #

    # fixturesPath = os.path.join(ROOTDIR, "fixtures_Bidder")
    #     fixPath = os.path.join(main(self.test).fixturesPath, "testCases.txt")
        # testCases = open(fixPath)

    def setup(tests):
        for words in tests:
            if len(words) > 0:
                data = bidderAutomation.bidderAutomation(words)
                print(data)
                main(tests).loadData(data)

    def teardown(tests):
        for words in tests:
            if len(words) > 0:
                data = bidderAutomation.bidderAutomation(words)
                print(data)
                main(tests).teardown(data)


# print(setup())
# print(teardown())