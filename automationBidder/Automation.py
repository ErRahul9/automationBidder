import datetime
import json
import sys
import os
import time
from datetime import datetime
import enumerator
import re
import fileinput
from connectors import connectToCache

class Automation():


    def __init__(self,testCase):
        self.test = testCase

        self.ROOTDIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
        self.resourcesPath = os.path.join(self.ROOTDIR, "resources")
        fix = ""
        file = ""
        self.type = ""
        if "bidder" in testCase.lower():
            self.columnsToBeFixed = ["domain", "ip", "bundle"]
            fix = "fixtures_Bidder"
            file = "bidder_try_1.txt"
            self.type = "bidder"
        elif "augmentor" in testCase.lower():
            self.columnsToBeFixed = ["ip"]
            fix = "fixtures_Augmentor"
            file = "augmentor_sample_request_1.txt"
            self.type = "augmentor"
        self.fixturesPath = os.path.join(self.ROOTDIR, "{}".format(fix))
        self.jsonfile = os.path.join(self.fixturesPath, "testData.json")
        self.processFile = os.path.join(self.fixturesPath, "{}".format(file))
        self.metaPath = os.path.join(self.resourcesPath,"metadata.json")
        if "bidder" in self.type:
            self.enum = enumerator.bid
        elif "augmentor" in self.type:
            self.enum = enumerator.augment






    def setVariablesFromJsonFile(self):

        with open(self.jsonfile) as jsonFile:
            data = json.load(jsonFile)
            testData = data.get(self.test)

        for values in self.enum:
            if type(values.value) == list:
                for items in values.value:
                    regex = re.compile(r'\b' + str(items) + r'\b')
                    for line in fileinput.input(self.processFile, inplace=1):
                        if len(re.findall(regex, line)) > 0:
                            line = line.replace(line,re.findall(regex, line)[0] + " : "+str(testData.get(values.name)))
                            sys.stdout.write(" " * 6 + line + '\n')
                        else:
                            sys.stdout.write(line)
            else:
                regex = re.compile(r'\b' + str(values.value) + r'\b')

            for line in fileinput.input(self.processFile,inplace=1):
                if len(re.findall(regex, line)) > 0:
                    line = line.replace(line,re.findall(regex, line)[0] + " : " + str(testData.get(values.name)))
                    sys.stdout.write(" "*6+line+'\n')
                else:
                    sys.stdout.write(line)



    def insertMetadataCache(self):
        with open(self.metaPath) as meta:
            jMeta = json.load(meta)
        with open(self.jsonfile) as f:
            data = json.load(f)
            testData = data.get(self.test)
        createNewJsonObject  = {"mapping":{}}
        createNewJsonObject["mapping"] = jMeta.get("metadata")
        mapping = createNewJsonObject["mapping"]
        for values in self.enum:
            if type(values.value) == list:
                if values.value[1] in jMeta.get("metadata").keys():
                    mapping[values.value[1]] = testData.get(str(values).split(".")[1])
            elif values.value in jMeta.get("metadata").keys():
                mapping[values.value] = testData.get(str(values).split(".")[1])
        thresholds = [keys for keys in jMeta.get("metadata").keys() if "threshold" in keys]
        for thrash in thresholds:
            mapping[thrash] = testData.get("Thresholds").get(thrash.split("_")[0])
        key = "crid_"+str(testData.get("creativeId"))
        cache = "core-dev-bidder-metadata.pid24g.clustercfg.usw2.cache.amazonaws.com"
        print(key,createNewJsonObject,cache)
        return key,createNewJsonObject,cache



    def insertBidderObject(self):
        with open(self.metaPath) as meta:
            jMeta = json.load(meta)
        with open(self.jsonfile) as f:
            data = json.load(f)
            testData = data.get(self.test)
        createNewJsonObject  = {"mapping":{}}
        mapping = createNewJsonObject["mapping"]
        mapping[str(testData.get("width"))+":"+str(testData.get("height"))+"_avg_cpi"] = testData.get("cpi").get("avg_cpi")
        mapping[str(testData.get("width")) + ":" + str(testData.get("height")) + "_min_cpi"] = testData.get("cpi").get("min_cpi")
        mapping[str(testData.get("width")) + ":" + str(testData.get("height")) + "_max_cpi"] = testData.get("cpi").get("max_cpi")
        mapping["viewability_rate"] = testData.get("cpi").get("viewability_rate")
        key = testData.get("domainId")
        cache = "core-dev-bidder-price-optimize.pid24g.clustercfg.usw2.cache.amazonaws.com"
        # cache = "core-dev-bidder-price.pid24g.clustercfg.usw2.cache.amazonaws.com"
        print(key, createNewJsonObject, cache)
        return key,createNewJsonObject,cache

    def insertRecencyData(self):
        with open(self.metaPath) as meta:
            jMeta = json.load(meta)
        with open(self.jsonfile) as f:
            data = json.load(f)
            testData = data.get(self.test)
        createNewJsonObject = {"mapping": {}}
        dt = round(time.time()*1000) - 11*1000
        mapping = createNewJsonObject["mapping"]
        getChecks = testData.get("recency")
        for i in range(0,len(getChecks)):
            times =  getChecks[i]
            dt = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())*1000 - times *60000
            mapping[str(testData.get("advertiserId")+i)] = dt
        if testData.get("objectiveId") == 5:
            key = testData.get("ip")+"_vast"
        else:
            key = testData.get("ip")
        cache = "core-dev-recency.pid24g.clustercfg.usw2.cache.amazonaws.com"
        print(key, createNewJsonObject, cache)
        return key,createNewJsonObject,cache

    def insertHouseholdScore(self):
        with open(self.metaPath) as meta:
            jMeta = json.load(meta)
        with open(self.jsonfile) as f:
            data = json.load(f)
            testData = data.get(self.test)
        createNewJsonObject = {"mapping": {}}
        mapping = createNewJsonObject["mapping"]
        mapping["household_score"] = testData.get("scores").get("household_score")
        key = testData.get("ip")
        cache = "core-dev-household-score.pid24g.clustercfg.usw2.cache.amazonaws.com"
        print(key, createNewJsonObject, cache)
        return key,createNewJsonObject,cache




    def insertSegmentData(self):
        with open(self.jsonfile) as f:
            data = json.load(f)
            testData = data.get(self.test)
        key = testData.get("steelhouseId")
        value = testData.get("advertiserId")
        cache = "core-dev-segment-mapping.pid24g.clustercfg.usw2.cache.amazonaws.com"
        for items in key:
            createNewJsonObject = {"mapping": {}}
            mapping = createNewJsonObject["mapping"]
            mapping[items] = value
            connectToCache(cache, 6379, mapping, items, "insert")
        return key, createNewJsonObject,cache



    def insertMembershipData(self):
        with open(self.jsonfile) as f:
            data = json.load(f)
            testData = data.get(self.test)
        key = testData.get("ip")
        value = testData.get("steelhouseId")
        cache = "core-dev-membership.pid24g.clustercfg.usw2.cache.amazonaws.com"
        # cache = "core-dev-membership-opm.pid24g.clustercfg.usw2.cache.amazonaws.com"
        for items in value:
            createNewJsonObject = {"mapping": {}}
            mapping = createNewJsonObject["mapping"]
            mapping[key] = items
            connectToCache(cache,6379,mapping,items,"insert")
        return key, createNewJsonObject, cache



    def fixStringColumns(self):
        exp = {}
        for i, items in enumerate(self.columnsToBeFixed):
            exp["regex"+"_"+str(i)] = re.compile(r'\b' + str(items) + r'\b')
        for regex in exp.keys():
            for line in fileinput.input(self.processFile, inplace=1):
                if len(re.findall(exp.get(regex), line)) > 0:
                    key = line.strip().split(" :")[0].strip()
                    val = line.strip().split(":")[1].strip()
                    correctedString = key+':"'+val+'"'
                    line = line.replace(line, correctedString)
                    sys.stdout.write(" " * 6 + correctedString + '\n')
                else:
                    sys.stdout.write(line)


    def getExpectedResults(self,tests):
        with open(self.jsonfile) as f:
            data = json.load(f)
            testData = data.get(self.test)
        return testData[tests]


# Automation("AugmentorTestmultipleSegments").insertSegmentData()