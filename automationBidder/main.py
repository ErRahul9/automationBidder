# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import json

class bidderAutomation():
    def __init__(self):
        jsonObject = self.jsonObject

    def setUp(self):
        print("setting up data in caches and postgres database")


    def readJson(self,jsonFileName):
        with open(jsonFileName) as f:
            jsonObject = json.dumps(f.read())
        return jsonObject

    def updateBidderFileWithTestData(self):
        print("updating bidder file")

    def movingFiles(self):
        print("moving bidder file to the bidder folder")

    def runningBidderAPICode(self):
        print("run bidder API code ")

    def tesrDown(self):
        print("code to teardown test data")







    # Press the green button in the gutter to run the script.
    if __name__ == '__main__':
        print(readJson("resources/testData.json"))


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
