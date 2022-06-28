# import automationBidder
# import datetime
import os
import time
import json
from datetime import datetime, timezone
import timestamp as timestamp

from main import main
from automationBidder.bidderAutomation import bidderAutomation
import dataSetup
import sys




def readArgs():
    keyword = sys.argv[1]
    testcases = []
    ROOTDIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
    fixPath = os.path.join(ROOTDIR, "fixtures/testCases.txt")
    testNames = open(fixPath,'r')
    print(sys.argv[1])
    for tests in testNames:
        if keyword in tests:
            testcases.append(tests.strip())
    return testcases


def setup(testCases):
    dataSetup.setup(testCases)

def teardown(testCases):
    dataSetup.teardown(testCases)


def rerun():
    print("rerunning failed test cases.")
    print("waiting 30 sec..")
    # time.sleep(30)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    reruntests = []
    jsonFile = os.path.join(main().fixturesPath, "testData.json")
    with open(jsonFile) as jFile:
        data = json.load(jFile)
    testResults = os.path.join(main().resourcesPath,"testResults.txt")
    for line in open(testResults):
        if ":Fail" in line:
            reruntests.append(line.split(":")[0])
    tests = [test.strip() for test in reruntests]
    for words in tests:
        expStat = int(data.get(words).get("expectedResult").get("statusCode"))
        if  expStat == 200 and len(words) > 0:
            print("re running "+words+" test again")
            dataTest = bidderAutomation(words)
            main().updateFile(dataTest)
            main().runBeeswaxCommand()
            status = main().readResults()[0]
            bidPrice = main().readResults()[2]
            if int(status) == int(data.get(words).get("expectedResult").get("statusCode")) and int(bidPrice) == int(data.get(words).get("expectedResult").get("statusCode")):
                passFail = "Pass"
                main().readResults()
                main().testResults.write(words + " : " + str(main().readResults()) + " : "+"Pass/Fail :"+passFail+ '\n')
            else:
                passFail = "Fail"
                main().readResults()
                main().testResults.write(words + " : " + str(main().readResults()) + " : " + "Pass/Fail :" + passFail + '\n')
    ROOTDIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
    resourcesPath = os.path.join(ROOTDIR, "resources")
    os.rename(f"{resourcesPath}/testResults.txt","{0}/testResults_{1}.txt".format(resourcesPath,timestamp))
    # dataSetup.teardown(tests)



if __name__ == "__main__":


    readArgs()
    testCase = readArgs()
    # print(testCase.strip())
    passFail = ""
    getCurrentTS = time.time()
    test = main().createListOfTestCases()
    fixPath = os.path.join(main().fixturesPath, "testCases.txt")
    testCases = open(fixPath)
    tests = [test for test in testCases.read().split('\n')]
    # print(tests)
    print(len(testCase))
    if len(testCase) > 1:
        tests = [test for test in tests if test in testCase]
        teardown(tests)
        setup(tests)
    else:
        teardown(tests)
        setup(tests)
    time.sleep(40)
    jsonFile = os.path.join(main().fixturesPath, "testData.json")
    with open(jsonFile) as jFile:
        result = json.load(jFile)
    for words in tests:
        if len(words) > 0 :
            expRes = result[words]
            expectedResults = expRes["expectedResult"]
            data = bidderAutomation(words)
            updateFile = main().updateFile(data)
            main().runBeeswaxCommand()
            status = main().readResults()[0]
            bidPrice = main().readResults()[2]
            if int(bidPrice) ==  int(expectedResults["price"]) and int(status) == int(expectedResults["statusCode"]):
                passFail = "Pass"
            else:
                passFail = "Fail"
            main().testResults.write(words + " : " + str(main().readResults()) + " : "+"Pass/Fail :"+passFail+ '\n')
    rerun()

