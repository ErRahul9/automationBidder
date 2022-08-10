import time

# from automationBidder.runner import runner
from connectors import connectToCache
from Automation import *
import subprocess
import shutil
import os
import config


class main():

    def __init__(self,test):
        self.test = test
        self.ROOTDIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
        self.resourcesPath = os.path.join(self.ROOTDIR, "resources")
        self.testResults = open(os.path.join(self.resourcesPath, "testResults.txt"),'a')
        self.expectedResults = {}


    def returnPaths(self):
        retObj ={}
        ROOTDIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
        resourcesPath = os.path.join(ROOTDIR, "resources")
        testResults = open(os.path.join(resourcesPath, "testResults.txt"),'a')
        fix = ""
        if "bidder" in self.test.lower():
            fix = "fixtures_Bidder"
        elif "augmentor" in self.test.lower():
            fix = "fixtures_Augmentor"
        fixturesPath = os.path.join(ROOTDIR, "{}".format(fix))
        fixPath = os.path.join(ROOTDIR, "{}/testCases.txt".format(fix))
        retObj["rootDir"] = ROOTDIR
        retObj["resourcePath"] = resourcesPath
        retObj["fixturesPath"] = fixturesPath
        retObj["testResults"] = testResults
        retObj["fixPath"] = fixPath
        return retObj



    def createListOfTestCases(self):
        jsonPath = os.path.join(self.returnPaths().get("fixturesPath"), "testData.json")
        with open(jsonPath) as jFile:
            data = json.load(jFile)
            testPath = os.path.join(self.returnPaths().get("fixturesPath"),"testCases.txt")
            with open(testPath,"w+") as f:
                for keys in data.keys():
                    if self.test in keys:
                        f.write(keys+'\n')
            f.close()
        jFile.close()



    def loadData(self, data):
        retArr =[]
        caches = []
        for tests in self.test:

            if "bidder" in tests.lower():
                caches = ["insertMetadataCache", "insertBidderObject", "insertRecencyData", "insertHouseholdScore"]
            elif "augmentor" in tests.lower():
                caches = ["insertSegmentData","insertMembershipData"]
        for funcs in caches:
            if "Segment" in funcs or "Membership" in funcs:
                method = getattr(data, funcs)
                methodCall = method()
                retArr.append(methodCall)
            else:
                method = getattr(data, funcs)
                methodCall = method()
                key = methodCall[0]
                metadata = methodCall[1]
                cache = methodCall[2]
                retVal = connectToCache(cache, 6379, metadata.get("mapping"), key, "insert")
                retArr.append(retVal)
        return retArr


    def updateFile(self, data):
        print("updating from json file")
        data.setVariablesFromJsonFile()
        print("fixing string column types")
        data.fixStringColumns()

    def runCommand(self):
        src = os.path.join(self.returnPaths().get("fixturesPath"))
        retData = ""
        trg = ""
        rootdir = self.returnPaths().get("rootDir")
        if "bidder" in src.lower():
            trg = os.path.join(rootdir,'beeswaxCode/beeswax/tools/bid/bid')
        elif "augmentor" in src.lower():
            trg = os.path.join(rootdir, 'beeswaxCode/beeswax/tools/augmentor/augmentor')
        files = os.listdir(src)
        for file in files:
            if "bidder" in file or "augmentor" in file:
                shutil.copy2(os.path.join(src, file), trg)
        change = os.chdir(trg)
        print(file)
        if "bidder" in src.lower():
            retData = subprocess.run(['./bidding_agent_requests_generator', 'bidder_try_1.txt',
                                  'http://bidder.coredev.west2.steelhouse.com/beeswax/bidder',
                                  '--path-to-responses-file', '../../../../../resources/output.txt'])
            return retData.returncode
        elif "augmentor" in src.lower():
            retData = subprocess.run(['./augmentor_requests_generator', 'augmentor_sample_request_1.txt',
                                      'http://augmentor.coredev.west2.steelhouse.com/beeswax/augmentor',
                                      '--path-to-responses-file', '../../../../../resources/outputAugmentor.txt'])
            return retData.returncode





    def teardown(self,data):
        caches = []
        for vals in self.test:
            if "bidder" in vals.lower():
                caches = ["insertMetadataCache", "insertBidderObject", "insertRecencyData", "insertHouseholdScore"]
            elif "augmentor" in vals.lower():
                caches = ["insertSegmentData","insertMembershipData"]
        retData = []
        for funcs in caches:
            method = getattr(data, funcs)
            methodCall = method()
            key = "methodCall[0]"
            metadata = "methodCall[1]"
            cache = methodCall[2]
            retVal = connectToCache(cache, 6379, metadata, key, "delete")
            retData.append("deleted :  " + key[0] + "   :" + str(retVal))
        return retData

    def readResults(self):
        retStatus = 0
        lineitem = 0
        retPrice = 0
        resourcePath = self.returnPaths().get("resourcePath")
        outPath = ""
        print(self.test)
        if "bidder" in self.test.lower():
            outPath = os.path.join(resourcePath, "output.txt")
        elif "augmentor" in self.test.lower():
            outPath = os.path.join(resourcePath, "outputAugmentor.txt")

        with open(outPath) as f_results:
            for line in f_results.read().split("\n"):
                if "Error" in line or "204" in line:
                    retStatus = 204
                    lineItem = 0
                    retPrice = 0
                elif "bidder" in self.test.lower():
                    if "Status" in line and "200" in line:
                        retStatus = 200
                    if "line_item_id" in line:
                        lineitem = int(line.split(":")[1].strip())
                    if "bid_price_micros" in line:
                        retPrice = int(line.split(":")[1].strip())
                elif "augmentor" in self.test.lower():
                    if "Status" in line and "200" in line:
                        retStatus = 200
                    if "id" in line:
                        lineitem = line.split(":")[1].strip()
                        retPrice = 0


        return retStatus, lineitem, retPrice



