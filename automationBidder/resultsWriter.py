import json

import pandas as pd


def readtestResults():
    returnObj = {}
    results = open("../resources/testResults_20220630-120953.txt")
    fileRead = open("../fixtures_Bidder/testData.json")
    jsonReader = json.load(fileRead)
    for lines in results.read().split('\n'):
        if len(lines) > 0:
            testCase = lines.split(":")[0]
            returnedStatusCode = lines.split(":")[1].split(",")[0]
            returnedprice = lines.split(":")[1].split(',')[2]
            status = returnedStatusCode[2:]
            price = returnedprice[:len(returnedprice) -2].strip()
            returnObj[testCase] = {"ReturnedStatusCode":status,"ReturnedbidPrice":price}
            expectedResults  = jsonReader[testCase.strip()].get('expectedResult')
            print(expectedResults.get('statusCode'))
            print(status)
            print(expectedResults.get('price'))
            print(price)
            # if int(status) == int(expectedResults.get('statusCode')) and int(price) == int(expectedResults.get('price')):
            #     print("pass")




            # jsonReader[lines.split(":")[0]] = {}
    # print(results.read())
    # jsonReader[""]
    # print(jsonReader)


    # df = pd.read_csv("../resources/BidderTests.xlsx")
    # df = pd.read_excel("../resources/BidderTests.xlsx")
    # testCaseName  = df.get("AutomationTestCaseId")
    # tests  = [tests for tests in testCaseName]
    # # file = open("../resources/testResults_20220630-120953.txt", 'r')
    # dfResults = pd.read_csv("../resources/testResults_20220703-141855.txt")
    # print(dfResults.keys())
    # mergedResults = pd.merge(df,dfResults,on="AutomationTestCaseId")
    # print(mergedResults)
    # results = [lines.split(":")[0] for lines in file]
    # print(results)
    # resultsVals = [lines.split(":")[2] for lines in file]
    # print(results)
    # print(resultsVals)


    # with open("../resources/testResults_20220630-120953.txt") as fileName:
    #     for lines in fileName:
    #         tests = [test for test in testCaseName if test in lines]
    #         print(tests)







readtestResults()