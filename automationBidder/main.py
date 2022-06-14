import json
import sys

import enumerator
import re
import fileinput
class bidderAutomation():


    def __init__(self, jsonFileName, bidderFile,testCase):
        self.jsonfile = jsonFileName
        self.bidderfile = bidderFile
        self.test = testCase


    def setVariablesFromJsonFile(self):
        with open(self.jsonfile) as jsonFile:
            data = json.load(jsonFile)
            testData = data.get(self.test)
        for values in enumerator.enumerator:
            regex = re.compile(r'\b' + str(values.value) + r'\b')
            for line in fileinput.input(self.bidderfile,inplace=1):
                if len(re.findall(regex, line)) > 0:
                    line = line.replace(line,re.findall(regex, line)[0] + " : " + str(testData.get(values.name)))
                    sys.stdout.write(" "*6+line+'\n')
                else:
                    sys.stdout.write(line)





    def movingFiles(self):
        print("moving bidder file to the bidder folder")

    def runningBidderAPICode(self):
        print("run bidder API code ")

    def tearDown(self):
        print("code to teardown test data")



data = bidderAutomation("fixtures/testData.json","fixtures/bidder_try_1.txt","BidderTestPositiveWithBidAmount")
data.setVariablesFromJsonFile()

# print(bidderAutomation.updateBidderFileWithTestData("resources/testData.json"))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
#         print(updateBidderFileWithTestData("fixtures/testData.json"))

'''
read the json file pass the data to args
read the text file and look for specific text
update the line 3 spaces after the text
save the file

'''
