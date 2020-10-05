################################################################################
# process.py

# Copyright (C) 2016-2017 Yoonsang Lee

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
import fnmatch
from global_const import *
from unicode import *
from submission import *

############################################
# main functions
def collectAllProjInfosInAllSubmissions(submissionTitles, assignmentDir, exclude_patterns=[], std_input=[], cmd_args=[], destDir=None, deco2unicoMap=None, user_dict=None):
    allProjInfos = []

    # process each submission
    for j in range(len(submissionTitles)):
        submissionTitle = submissionTitles[j]
        submissionType = detectSubmissionType(opjoin(assignmentDir, submissionTitle))

        # set submissionDir, projNames, projSrcFileNames for each project
        # ex)
        # projNames : ['proj1', 'proj2']
        # projSrcFileNames: [['proj1.c','proj1.h'], ['proj2.c','proj2.h']]
        if submissionType==SINGLE_SOURCE_FILE or submissionType==SOURCE_FILES:
            if destDir!=None:
                # unidecode destSubmissionDir
                decodeDestSubmissionDirPathRecursive(destDir, submissionTitle, deco2unicoMap)

            if submissionType==SINGLE_SOURCE_FILE:
                if destDir!=None:
                    submissionDir = destDir 
                    # [[u'student01.c']]
                    projSrcFileNames = [[unico2decoPath(submissionTitle, deco2unicoMap)]]
                    # [u'student01']
                    projNames = [os.path.splitext(unico2decoPath(submissionTitle, deco2unicoMap))[0]]
                else:
                    submissionDir = assignmentDir
                    projSrcFileNames = [[submissionTitle]]
                    projNames = [os.path.splitext(submissionTitle)[0]]

            elif submissionType==SOURCE_FILES:
                if destDir!=None:
                    submissionDir = opjoin(destDir, unico2decoPath(submissionTitle, deco2unicoMap))
                else:
                    submissionDir = opjoin(assignmentDir, submissionTitle)

                # [[u'prob1.c'], [u'prob2.c']]
                projSrcFileNames = []

                # Convert paths for os.walk to byte string only for posix os (due to python bug?)
                if os.name=='posix':
                    tempSubDir = toString(submissionDir)
                else:
                    tempSubDir = submissionDir
                for root, dirs, files in os.walk(tempSubDir):
                    if gBuildDirPrefix not in root:
                        for name in files:
                            # Convert paths for os.walk to byte string only for posix os (due to python bug?)
                            if os.name=='posix':
                                root = toUnicode(root)
                                name = toUnicode(name)
                            fileName = opjoin(root, name).replace(submissionDir+os.sep, '')
                            isSrcFile = True
                            for pattern in exclude_patterns:
                                if fnmatch.fnmatch(fileName, pattern):
                                    isSrcFile = False
                                    break
                            if isSrcFile:
                                projSrcFileNames.append([fileName])

                # [u'prob1', u'prob2']
                projNames = [os.path.splitext(srcFileNamesInProj[0])[0] for srcFileNamesInProj in projSrcFileNames]

        elif submissionType==CMAKE_PROJECT or submissionType==MAKE_PROJECT or submissionType==VISUAL_CPP_PROJECT:

            if submissionType==CMAKE_PROJECT or submissionType==MAKE_PROJECT:
                if destDir!=None:
                    decodeDestSubmissionDirPathRecursive(destDir, submissionTitle, deco2unicoMap)
                    submissionDir = opjoin(destDir, unico2decoPath(submissionTitle, deco2unicoMap))
                    projNames = [unico2decoPath(submissionTitle, deco2unicoMap)]    # ['student01']
                else:
                    submissionDir = opjoin(assignmentDir, submissionTitle)
                    projNames = [submissionTitle]

            elif submissionType==VISUAL_CPP_PROJECT:
                # No need of decodeDestSubmissionDirPathRecursive(), 
                # and VISUAL_CPP_PROJECT can include multibyte characters as MSVC compiler supports it.
                if destDir!=None:
                    submissionDir = opjoin(destDir, submissionTitle)
                else:
                    submissionDir = opjoin(assignmentDir, submissionTitle)
                projNames = [submissionTitle]

            # [[u'CMakeLists.txt', u'student01.c', u'utility.c', u'utility.h']]
            projSrcFileNames = [[]]
            
            # Convert paths for os.walk to byte string only for posix os (due to python bug?)
            if os.name=='posix':
                tempSubDir = toString(submissionDir)
            else:
                tempSubDir = submissionDir
            for root, dirs, files in os.walk(tempSubDir):
                if gBuildDirPrefix not in root:
                    for name in files:
                        # Convert paths for os.walk to byte string only for posix os (due to python bug?)
                        if os.name=='posix':
                            root = toUnicode(root)
                            name = toUnicode(name)
                        fileName = opjoin(root, name).replace(submissionDir+os.sep, '')
                        isSrcFile = True
                        for pattern in exclude_patterns:
                            if fnmatch.fnmatch(fileName, pattern):
                                isSrcFile = False
                                break
                        if isSrcFile:
                            projSrcFileNames[0].append(fileName)

        else:
            print '%s%s: Submission type %s is not supported.'%(gLogPrefix, submissionTitle, gSubmissionTypeName[submissionType])
            continue

        # collect info
        for i in range(len(projNames)):
            projInfo = {}
            projInfo['submissionIndex'] = j
            projInfo['submissionTitle'] = submissionTitle
            projInfo['submissionType'] = submissionType
            projInfo['numSubmission'] = len(submissionTitles)
            projInfo['projIndex'] = i
            projInfo['numProjInSubmission'] = len(projNames)
            projInfo['projName'] = projNames[i]
            projInfo['submissionDir'] = submissionDir
            projInfo['filesInProj'] = projSrcFileNames[i]

            # set stdInputs
            if user_dict!=None:
                stdInputs = getStdInputsFromUserDict(user_dict, projNames[i])
                projInfo['stdInputs'] = stdInputs
            else:
                stdInputs = std_input
                projInfo['stdInputs'] = stdInputs

            projInfo['cmdArgss'] = cmd_args

            allProjInfos.append(projInfo)

    return allProjInfos

def generateReportDataForAllProjs(allProjInfos, buildResults, runResults, destDir, args, deco2unicoMap):
    submittedFileNames = []
    srcFileLists = []
    buildRetCodes = []
    buildLogs = []
    exitTypeLists = []
    stdoutStrLists = []
    stdInputLists = []
    cmdArgsLists = []
    submissionTypes = []
    buildVersionSet = set()

    for i in range(len(allProjInfos)):
        projInfo = allProjInfos[i]
        submissionTitle = projInfo['submissionTitle']
        submissionDir = projInfo['submissionDir']
        filesInProj = projInfo['filesInProj']
        submissionType = projInfo['submissionType']

        buildRetCode, buildLog, buildVersion = buildResults[i]

        exitTypeList, stdoutStrList, stdInputList, cmdArgsList = runResults[i]

        # add report data
        submittedFileNames.append(submissionTitle)

        # full path -> \hagsaeng01\munje2\munje2.c
        projOrigSrcFilePathsAfterAssignDir = []
        for srcFileName in filesInProj:
            destSrcFilePath = opjoin(submissionDir, srcFileName)
            destSrcFilePathAfterDestDir = destSrcFilePath.replace(destDir+os.sep, '')

            if args.run_only:
                projOrigSrcFilePathsAfterAssignDir.append(opjoin(destDir, destSrcFilePathAfterDestDir))
            else:
                if submissionType==SINGLE_SOURCE_FILE or submissionType==SOURCE_FILES or submissionType==CMAKE_PROJECT or submissionType==MAKE_PROJECT:
                    # deco2unico src file paths to properly display in the report
                    origSrcFilePathAfterAssignDir = deco2unicoPath(destSrcFilePathAfterDestDir, deco2unicoMap)
                else:
                    origSrcFilePathAfterAssignDir = destSrcFilePathAfterDestDir
                projOrigSrcFilePathsAfterAssignDir.append(opjoin(args.assignment_dir, origSrcFilePathAfterAssignDir))

        srcFileLists.append(projOrigSrcFilePathsAfterAssignDir)
        buildRetCodes.append(buildRetCode)
        buildLogs.append(buildLog)
        exitTypeLists.append(exitTypeList)
        stdoutStrLists.append(stdoutStrList)
        stdInputLists.append(stdInputList)
        cmdArgsLists.append(cmdArgsList)
        submissionTypes.append(submissionType)
        buildVersionSet.add(buildVersion)

    return submittedFileNames, srcFileLists, buildRetCodes, buildLogs, exitTypeLists, stdoutStrLists, stdInputLists, cmdArgsLists, submissionTypes, buildVersionSet

############################################
# project type detection
def decodeDestSubmissionDirPathRecursive(destDir, submissionTitle, deco2unicoMap):
    origSubDir = opjoin(destDir, submissionTitle)
    newSubDir = opjoin(destDir, unico2decoPath(submissionTitle, deco2unicoMap))

    # if --run-only mode, os.rename() will throw an exception, which is expected behavior.
    try:
        os.rename(origSubDir, newSubDir)
    except:
        pass

    # Convert paths for os.walk to byte string only for posix os (due to python bug?)
    if os.name=='posix':
        newSubDir = toString(newSubDir)

    for root, dirs, files in os.walk(newSubDir, topdown=False):
        for name in dirs:

            if os.name=='posix':
                name = toUnicode(name)

            decoName = unico2decoPath(name, deco2unicoMap)
            try:
                os.rename(opjoin(root, name), opjoin(root, decoName))
            except:
                pass

        for name in files:
            
            if os.name=='posix':
                name = toUnicode(name)

            decoName = unico2decoPath(name, deco2unicoMap)
            try:
                os.rename(opjoin(root, name), opjoin(root, decoName))
            except:
                pass

def getStdInputsFromUserDict(userDict, projName):
    stdInputs = None
    for key in userDict:
        if projName.endswith(key):
            stdInputs = userDict[key] 
            break
    if stdInputs == None:
        stdInputs = []
        for key in userDict:
            stdInputs.extend(userDict[key])
    return stdInputs


