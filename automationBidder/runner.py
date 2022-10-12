import os
import time
import json
from main import main
from Automation import *
import dataSetup
import sys
import config

class runner():
    def __init__(self):
        self.keyword = sys.argv[1]
        self.testcases = []
        self.ROOTDIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
        fix = ""
        if "bidder" in self.keyword.lower():
            fix = "fixtures_Bidder"
        elif "augmentor" in self.keyword.lower():
            fix = "fixtures_Augmentor"
        self.fixPath = os.path.join(self.ROOTDIR, "{}/testCases.txt".format(fix))
        self.testNames = open(self.fixPath,'r')
        for tests in self.testNames:
            if self.keyword in tests:
                self.testcases.append(tests.strip())


    def setup(self):
        dataSetup.dataset.setup(self.keyword)

    def teardown(self):
        dataSetup.dataset.teardown(self.keyword)


    def rerun(self):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        reruntests = []
        jsonFile = os.path.join(main(self.keyword).returnPaths().get("fixturesPath"), "testData.json")
        with open(jsonFile) as jFile:
            data = json.load(jFile)
        testResults = os.path.join(main(self.keyword).returnPaths().get("resourcePath"),"testResults.txt")
        for line in open(testResults):
            if ":Fail" in line:
                reruntests.append(line.split(":")[0])
        tests = [test.strip() for test in reruntests]
        if len(tests) > 0:
            time.sleep(30)
        for words in tests:
            print("waiting 30 seconds to rerun failed tests")
            print("rerunning failed test cases "+ words)
            expStat = int(data.get(words).get("expectedResult").get("statusCode"))
            if  expStat == 200 and len(words) > 0:
                print("re running "+words+" test again")
                dataTest = Automation(words)
                main(self.keyword).updateFile(dataTest)
                # main(self.keyword).runBeeswaxCommand()
                main(self.keyword).runCommand()
                status =main(self.keyword).readResults()[0]
                bidPrice =main(self.keyword).readResults()[2]
                if int(status) == int(data.get(words).get("expectedResult").get("statusCode")) and int(bidPrice) == int(data.get(words).get("expectedResult").get("price")):
                    passFail = "Pass"
                    main(self.keyword).readResults()
                    main(self.keyword).testResults.write(words + " , " + str(main(self.keyword).readResults()) + " , "+ passFail+ '\n')
                else:
                    passFail = "Fail"
                    main(self.keyword).readResults()
                    main(self.keyword).testResults.write(words + " , " + str(main(self.keyword).readResults()) + " , " + passFail + '\n')
        ROOTDIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
        resourcesPath = os.path.join(ROOTDIR, "resources")
        os.rename(f"{resourcesPath}/testResults.txt","{0}/testResults_{1}.txt".format(resourcesPath,timestamp))
        open(self.fixPath, 'w').close()

    def run(self):
        # time.sleep(20)
        passFail = ""
        getCurrentTS = time.time()
        main(self.keyword).createListOfTestCases()
        main(self.keyword).testResults.write("AutomationTestCaseId" + " , " + "TestResults  , " + " Pass/Fail" + '\n')
        fixPath = os.path.join(main(self.keyword).returnPaths().get("fixturesPath"), "testCases.txt")
        testCases = open(fixPath)
        tests = [test for test in testCases.read().split('\n')]
        if len(self.testcases) >= 1:
            tests = [test for test in tests if test in self.testcases]
            dataSetup.dataset.teardown(tests)
            dataSetup.dataset.setup(tests)
        else:
            dataSetup.dataset.teardown(tests)
            dataSetup.dataset.setup(tests)
        # time.sleep(40)
        jsonFile = os.path.join(main(self.keyword).returnPaths().get("fixturesPath"), "testData.json")

        with open(jsonFile) as jFile:
            result = json.load(jFile)
        for words in tests:
            if len(words) > 0:
                expRes = result[words]
                expectedResults = expRes["expectedResult"]
                data = Automation(words)
                main(self.keyword).updateFile(data)
                # time.sleep(60)
                main(self.keyword).runCommand()
                if "bidder" in self.keyword.lower():
                    status =main(self.keyword).readResults()[0]
                    bidPrice =main(self.keyword).readResults()[2]
                    print(str(status) + " " + str(bidPrice))
                    if int(bidPrice) == int(expectedResults["price"]) and int(status) == int(expectedResults["statusCode"]):
                        passFail = "Pass"
                    else:
                        passFail = "Fail"
                    main(self.keyword).testResults.write(
                        words + " , " + str(main(self.keyword).readResults()) + " , " + passFail + '\n')
                elif "augmentor" in self.keyword.lower():
                    status = main(self.keyword).readResults()[0]
                    ip = main(self.keyword).readResults()[1]
                    if int(status) == int(expectedResults["statusCode"]):
                        passFail = "Pass"
                    else:
                        passFail = "Fail"
                    main(self.keyword).testResults.write(words + " , " + str(main(self.keyword).readResults()) + " , " + passFail + '\n')
                    print(status)
                    print("running augmentor")
                    open(self.fixPath, 'w').close()

if __name__ == "__main__":
    runner().run()
    runner().rerun()


