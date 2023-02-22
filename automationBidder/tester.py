import os


# def __init__(self ,test):
#     self.test = test
#     self.ROOTDIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
#     self.resourcesPath = os.path.join(self.ROOTDIR, "resources")
#     self.testResults = open(os.path.join(self.resourcesPath, "testResults.txt") ,'a')
#     self.expectedResults = {}


def protoSer():
    ROOTDIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
    resourcesPath = os.path.join(ROOTDIR, "resources/proto/aug.proto")
    # FilePath = sys.argv[1]

    T = MyMessage.MyType()
    f = open(FilePath, 'rb')
    T.ParseFromString(f.read())
    f.close()

    print(T)