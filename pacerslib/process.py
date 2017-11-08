import fnmatch, glob
from unicode import *
from global_const import *

############################################
# main functions
def collectAllProjInfosInAllSubmissions(submissionTitles, assignmentDir, destDir, deco2unicoMap, args):
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
            # unidecode destSubmissionDir
            decodeDestSubmissionDirPathRecursive(destDir, submissionTitle, deco2unicoMap)

            if submissionType==SINGLE_SOURCE_FILE:
                submissionDir = destDir

                # [[u'student01.c']]
                projSrcFileNames = [[unico2decoPath(submissionTitle, deco2unicoMap)]]

                # [u'student01']
                projNames = [os.path.splitext(unico2decoPath(submissionTitle, deco2unicoMap))[0]]

            elif submissionType==SOURCE_FILES:
                submissionDir = opjoin(destDir, unico2decoPath(submissionTitle, deco2unicoMap))

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
                            for pattern in args.exclude_patterns:
                                if fnmatch.fnmatch(fileName, pattern):
                                    isSrcFile = False
                                    break
                            if isSrcFile:
                                projSrcFileNames.append([fileName])

                # [u'prob1', u'prob2']
                projNames = [os.path.splitext(srcFileNamesInProj[0])[0] for srcFileNamesInProj in projSrcFileNames]

        elif submissionType==CMAKE_PROJECT or submissionType==VISUAL_CPP_PROJECT:
            if submissionType==CMAKE_PROJECT:
                decodeDestSubmissionDirPathRecursive(destDir, submissionTitle, deco2unicoMap)
                submissionDir = opjoin(destDir, unico2decoPath(submissionTitle, deco2unicoMap))
                projNames = [unico2decoPath(submissionTitle, deco2unicoMap)]    # ['student01']

            elif submissionType==VISUAL_CPP_PROJECT:
                # No need of decodeDestSubmissionDirPathRecursive(), 
                # and VISUAL_CPP_PROJECT can include multibyte characters as MSVC compiler supports it.
                submissionDir = opjoin(destDir, submissionTitle)
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
                        for pattern in args.exclude_patterns:
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

            # set userInputs
            if args.user_dict!=None:
                userInputs = getUserInputsFromUserDict(args.user_dict, projNames[i])
            else:
                userInputs = args.user_input
            projInfo['userInputs'] = userInputs

            allProjInfos.append(projInfo)

    return allProjInfos

def generateReportDataForAllProjs(allProjInfos, buildResults, runResults, destDir, args, deco2unicoMap):
    submittedFileNames = []
    srcFileLists = []
    buildRetCodes = []
    buildLogs = []
    exitTypeLists = []
    stdoutStrLists = []
    userInputLists = []
    submissionTypes = []
    buildVersionSet = set()

    for i in range(len(allProjInfos)):
        projInfo = allProjInfos[i]
        submissionTitle = projInfo['submissionTitle']
        submissionDir = projInfo['submissionDir']
        filesInProj = projInfo['filesInProj']
        submissionType = projInfo['submissionType']

        buildRetCode, buildLog, buildVersion = buildResults[i]

        exitTypeList, stdoutStrList, userInputList = runResults[i]

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
                if submissionType==SINGLE_SOURCE_FILE or submissionType==SOURCE_FILES or submissionType==CMAKE_PROJECT:
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
        userInputLists.append(userInputList)
        submissionTypes.append(submissionType)
        buildVersionSet.add(buildVersion)

    return submittedFileNames, srcFileLists, buildRetCodes, buildLogs, exitTypeLists, stdoutStrLists, userInputLists, submissionTypes, buildVersionSet

############################################
# project type detection
def detectSubmissionType(submissionPath):
    if os.path.isdir(submissionPath):
        # print 'dir'
        for submissionType in range(BEGIN_SUBMISSION_TYPE+1, END_SUBMISSION_TYPE):
            for pattern in gSubmissionPatterns[submissionType]:
                # Convert paths for glob to byte string only for posix os (due to python bug?)
                if os.name=='posix':
                    if len(glob.glob(toString(opjoin(submissionPath, pattern)))) > 0:
                        return submissionType
                else:
                    if len(glob.glob(opjoin(submissionPath, pattern))) > 0:
                        return submissionType
        return SOURCE_FILES
    else:
        # print 'file'
        return SINGLE_SOURCE_FILE

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

def getUserInputsFromUserDict(userDict, projName):
    userInputs = None
    for key in userDict:
        if projName.endswith(key):
            userInputs = userDict[key] 
            break
    if userInputs == None:
        userInputs = []
        for key in userDict:
            userInputs.extend(userDict[key])
    return userInputs

