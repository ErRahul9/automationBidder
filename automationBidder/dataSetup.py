import os
from main import main
import bidderAutomation

main().createListOfTestCases()

fixPath = os.path.join(main().fixturesPath, "testCases.txt")
testCases = open(fixPath)
tests = [test for test in testCases.read().split('\n')]
ROOTDIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
resourcesPath = os.path.join(ROOTDIR, "resources")
fixturesPath = os.path.join(ROOTDIR, "fixtures")
fixPath = os.path.join(fixturesPath, "testCases.txt")
testCases = open(fixPath)

def setup(tests):
    for words in tests:
        if len(words) > 0:
            data = bidderAutomation.bidderAutomation(words)
            loadData = main().loadData(data)

def teardown(tests):
    for words in tests:
        if len(words) > 0:
            data = bidderAutomation.bidderAutomation(words)
            main().teardown(data)


# print(setup())
# print(teardown())