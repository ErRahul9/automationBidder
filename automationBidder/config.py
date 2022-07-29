import os
import sys

def setPath(test):

    ROOTDIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
    resourcesPath = os.path.join(ROOTDIR, "resources")
    fix = ""
    if "bidder" in test.lower():
        fix = "fixtures_Bidder"
    elif "augmentor" in test.lower():
        fix = "fixtures_Augmentor"
    fixPath = os.path.join(ROOTDIR, "{}/testCases.txt".format(fix))
    testResults = open(os.path.join(resourcesPath, "testResults.txt"), 'a')
    # sys.path.append(ROOTDIR)
    # sys.path.append(resourcesPath)
    # sys.path.append(fixPath)
    # sys.path.append(testResults)

