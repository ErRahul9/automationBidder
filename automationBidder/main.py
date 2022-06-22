import time
from connectors import connectToCache
from bidderAutomation import *
import subprocess
import shutil
import os


class main():

    def __init__(self):
        self.ROOTDIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
        self.resourcesPath = os.path.join(self.ROOTDIR, "resources")
        self.fixturesPath = os.path.join(self.ROOTDIR, "fixtures")
        self.testResults = open(os.path.join(self.resourcesPath, "testResults.txt"),'a')


    def createListOfTestCases(self):
        jsonPath = os.path.join(self.fixturesPath,"testData.json")
        with open(jsonPath) as jFile:
            data = json.load(jFile)
            testPath = os.path.join(self.fixturesPath,"testCases.txt")
            with open(testPath,"w+") as f:
                for keys in data.keys():
                    f.write(keys+'\n')
            f.close()
        jFile.close()
    def loadData(self, data):
        retArr =[]
        caches = ["insertMetadataCache", "insertBidderObject", "insertRecencyData", "insertHouseholdScore"]
        for funcs in caches:
            method = getattr(data, funcs)
            methodCall = method()
            key = methodCall[0]
            metadata = methodCall[1]
            cache = methodCall[2]
            retVal = connectToCache(cache, 6379, metadata.get("mapping"), key, "insert")
            retArr.append(retVal)
        return retArr


    def updateFile(self, data):
        # data = bidderAutomation("../fixtures/testData.json", "../fixtures/bidder_try_1.txt","BidderTestPositiveWithBidAmount")

        print("updating from json file")
        data.setVariablesFromJsonFile()
        print("fixing string column types")
        data.fixStringColumns()


    def runBeeswaxCommand(self):

        src = os.path.join(self.fixturesPath)

        trg = os.path.join(self.ROOTDIR,'beeswaxCode/beeswax/tools/bid/bid')
        files = os.listdir(src)
        for file in files:
            if "bidder" in file:
                shutil.copy2(os.path.join(src, file), trg)
        change = os.chdir(trg)
        retData = subprocess.run(['./bidding_agent_requests_generator', 'bidder_try_1.txt',
                                  'http://bidder.coredev.west2.steelhouse.com/beeswax/bidder',
                                  '--path-to-responses-file', '../../../../../resources/output.txt'])
        print(retData.returncode)
        return retData.returncode

    def teardown(self, data):
        caches = ["insertMetadataCache", "insertBidderObject", "insertRecencyData", "insertHouseholdScore"]
        retData = []
        # caches = ["insertMetadataCache"]
        for funcs in caches:
            method = getattr(data, funcs)
            methodCall = method()
            key = methodCall[0]
            metadata = methodCall[1]
            cache = methodCall[2]
            retVal = connectToCache(cache, 6379, metadata.get("mapping"), key, "delete")
            retData.append("deleted :  " + key + "   :" + str(retVal))

        return retData

    def readResults(self):
        retStatus = 0
        lineitem = 0
        retPrice = 0
        outPath = os.path.join(self.resourcesPath, "output.txt")

        with open(outPath) as f_results:
            for line in f_results.read().split("\n"):
                if "Error" in line or "204" in line:
                    retStatus = 204
                    lineItem = "fail"
                    retPrice = 0
                else:
                    if "Status" in line and "200" in line:
                        retStatus = 200
                    if "line_item_id" in line:
                        lineitem = line.split(":")[1].strip()
                    if "bid_price_micros" in line:
                        retPrice = line.split(":")[1].strip()

        return retStatus, lineitem, retPrice




if __name__ == "__main__":
    temp = 2
    getCurrentTS = time.time()
    main().createListOfTestCases()
    fixPath = os.path.join(main().fixturesPath, "testCases.txt")
    testCases = open(fixPath)
    tests = [test for test in testCases.read().split('\n')]

    for words in tests:
        if len(words) > 0:
            data = bidderAutomation(words)
            # print(data)
            teardown = main().teardown(data)
            updateFile = main().updateFile(data)
            loadData = main().loadData(data)
            time.sleep(20)
            main().runBeeswaxCommand()
            status = main().readResults()[0]
            main().testResults.write(words+"_"+str(getCurrentTS) +" : "+ str(main().readResults())+'\n')
        if "200" not in str(status):
            while temp > 0:
                print("returned 204 running the same test again "+str(temp)+" times")
                time.sleep(30)
                main().runBeeswaxCommand()
                status = main().readResults()[0]
                if status == 200:
                    main().readResults()
                    main().testResults.write(words + "_" + str(getCurrentTS) + " : " + str(main().readResults())+'\n')
                    break
                temp = temp - 1

        else:
            print(main().readResults())
