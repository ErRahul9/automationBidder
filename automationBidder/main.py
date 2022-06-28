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
        self.expectedResults = {}


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

        # return data.getExpectedResults()


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
        return retData.returncode

    def teardown(self,data):
        caches = ["insertMetadataCache", "insertBidderObject", "insertRecencyData", "insertHouseholdScore"]
        retData = []
        for funcs in caches:
            method = getattr(data, funcs)
            methodCall = method()
            key = methodCall[0]
            metadata = methodCall[1]
            cache = methodCall[2]
            retVal = connectToCache(cache, 6379, metadata.get("mapping"), key, "delete")
            retData.append("deleted :  " + key + "   :" + str(retVal))
        print(retData)
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
                    lineItem = 0
                    retPrice = 0
                else:
                    if "Status" in line and "200" in line:
                        retStatus = 200
                    if "line_item_id" in line:
                        lineitem = line.split(":")[1].strip()
                    if "bid_price_micros" in line:
                        retPrice = line.split(":")[1].strip()

        return retStatus, lineitem, retPrice



