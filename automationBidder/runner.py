import os
import time
import json
from main import main
from bidderAutomation import *
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
        # print(self.testcases)


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
                dataTest = bidderAutomation(words)
                main(self.keyword).updateFile(dataTest)
                main(self.keyword).runBeeswaxCommand()
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


    def run(self):
        # testCase = self.readArgs()
        passFail = ""
        getCurrentTS = time.time()
        main(self.keyword).createListOfTestCases()
        fixPath = os.path.join(main(self.keyword).returnPaths().get("fixturesPath"), "testCases.txt")
        testCases = open(fixPath)
        tests = [test for test in testCases.read().split('\n')]
        # print(tests)
        # print(len(self.testcases))
        if len(self.testcases) >= 1:
            tests = [test for test in tests if test in self.testcases]
            # print(tests)
            dataSetup.dataset.teardown(tests)
            dataSetup.dataset.setup(tests)
        else:
            dataSetup.dataset.teardown(tests)
            dataSetup.dataset.setup(tests)
        # time.sleep(40)
        jsonFile = os.path.join(main(self.keyword).returnPaths().get("fixturesPath"), "testData.json")
        main(self.keyword).testResults.write("AutomationTestCaseId" + " , " + "TestResults  , " + " Pass/Fail" +'\n')
        with open(jsonFile) as jFile:
            result = json.load(jFile)
        for words in tests:
            if len(words) > 0:
                expRes = result[words]
                expectedResults = expRes["expectedResult"]
                data = bidderAutomation(words)
                main(self.keyword).updateFile(data)
                main(self.keyword).runBeeswaxCommand()
                status =main(self.keyword).readResults()[0]
                bidPrice =main(self.keyword).readResults()[2]
                print(str(status) + " " + str(bidPrice))
                if int(bidPrice) == int(expectedResults["price"]) and int(status) == int(expectedResults["statusCode"]):
                    passFail = "Pass"
                else:
                    passFail = "Fail"
                main(self.keyword).testResults.write(
                    words + " , " + str(main(self.keyword).readResults()) + " , " + passFail + '\n')


if __name__ == "__main__":
    runner().run()
    # readArgs()
    # testCase = readArgs()
    # passFail = ""
    # getCurrentTS = time.time()
    # test = main(keyword).createListOfTestCases()
    # fixPath = os.path.join(main(keyword).fixturesPath, "testCases.txt")
    # testCases = open(fixPath)
    # tests = [test for test in testCases.read().split('\n')]
    # # print(tests)
    # print(len(testCase))
    # if len(testCase) >= 1:
    #     tests = [test for test in tests if test in testCase]
    #     print(tests)
    #     teardown(tests)
    #     setup(tests)
    # else:
    #     teardown(tests)
    #     setup(tests)
    # # time.sleep(40)
    # jsonFile = os.path.join(main(keyword).fixturesPath, "testData.json")
    # main(keyword).testResults.write("AutomationTestCaseId" + " , " + "TestResults          " + "             Pass/Fail" + '\n')
    # with open(jsonFile) as jFile:
    #     result = json.load(jFile)
    # for words in tests:
    #     if len(words) > 0 :
    #         expRes = result[words]
    #         expectedResults = expRes["expectedResult"]
    #         data = bidderAutomation(words)
    #         main(keyword).updateFile(data)
    #         main(keyword).runBeeswaxCommand()
    #         status = main(keyword).readResults()[0]
    #         bidPrice = main(keyword).readResults()[2]
    #         print(str(status)+" "+str(bidPrice))
    #         if int(bidPrice) ==  int(expectedResults["price"]) and int(status) == int(expectedResults["statusCode"]):
    #             passFail = "Pass"
    #         else:
    #             passFail = "Fail"
    #
    #         main(keyword).testResults.write(words + " , " + str(main(keyword).readResults()) + " , "+passFail+ '\n')
    runner().rerun()

