import json
import luigi
import shutil
import os

def getFormattedJson(jsonString):
    return json.dumps(jsonString, indent=4)

def makePath(newPath):
    if not os.path.exists(newPath):
        os.makedirs(newPath)

def clearFolder(folder):
    for f in os.listdir(folder):
        path = os.path.join(folder, f)

        if os.path.isfile(path):
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

def createDirectory(path):
    if (os.path.exists(path)):
        clearFolder(path)
    makePath(path)

    if not (os.path.isdir(path)):
        raise RuntimeError("Could not create the directory: {}".format(path))

def checkFileExists(filePath):
    if not os.path.getsize(filePath) > 0:
        raise Exception("Something went wrong, file size is 0 for " + filePath)
    return filePath

def writeBinaryFile(filePath):
    with open(filePath, 'wb') as f:
        f.write(bytes([10]))