import json
import luigi
import os
from luigi import LocalTarget
from luigi.util import requires
from process_s2_swath.BuildPyramid import BuildPyramid
from process_s2_swath.BuildStats import BuildStats
from process_s2_swath.ConvertToTif import ConvertToTif


@requires(ConvertToTif)
class BuildPyramidsAndStats(luigi.Task):
    pathRoots = luigi.DictParameter()

    def run(self):

        with self.input().open("r") as convertToTifFile:
            convertToTifJson = json.load(convertToTifFile)

            addoTasks = []
            statTasks = []

            for filename in convertToTifJson["convertedFiles"]:
                addoTasks.append(BuildPyramid(pathRoots=self.pathRoots, inputFile=filename))
                statTasks.append(BuildStats(pathRoots=self.pathRoots, inputFile=filename))

            yield addoTasks
            yield statTasks

        with self.output().open('w') as o:
            convertToTifJson["builtPyramids"] = True
            convertToTifJson["calculatedStats"] = True
            json.dump(convertToTifJson)

    def output(self):
        outFile = os.path.join(self.pathRoots['state'], 'BuildPyramidsAndStats.json')
        return LocalTarget(outFile)