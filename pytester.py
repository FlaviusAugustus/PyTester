from argparse import ArgumentParser
import time
import os
import subprocess
import tempfile
import typing
from typing import Tuple
from typing import Type

InputSuffix = ".in"
OutputSuffix = ".out"
    
def getInputFiles(dir: str) -> list[str]:
    return getFilesWithSuffix(dir, InputSuffix)

def getOutputFiles(dir: str) -> list[str]:
    return getFilesWithSuffix(dir, OutputSuffix)

def getFilesWithSuffix(dir: str, suffix: str) -> list[str]:
    testDirectory = os.fsencode(dir)
    files: list[str] = []
    try:
        for file in os.listdir(testDirectory):
            filename = os.path.join(dir, os.fsdecode(file))
            if filename.endswith(suffix) and os.path.isfile(filename):
                files.append(os.path.splitext(filename)[0])
    except FileNotFoundError:
        print(f"Directory {dir} doesn't exist.")
    return files

def executeTests(program: str, testFiles: list[str]) -> None:
    for testFile in testFiles:
        try:
            executeTest(program, testFile)
        except FileNotFoundError as e:
            print(f"Output File for test {os.path.basename(testFile)} not found")
            continue

def executeTest(program: str, testFile: str) -> None:
    with open(testFile+OutputSuffix) as outFile:
        testResult = getOutputForTest(program, testFile+InputSuffix)
        evaluateTestResut(outFile.read(), testResult, testFile)
 
def getOutputForTest(program: str, test: str) -> Tuple[str, float]:
    with open(test) as testfile:
        try:
            start = time.time()
            process = subprocess.check_output(program, stdin=testfile)
            end = time.time()
            return (process.decode('utf-8'), end-start)
        except subprocess.CalledProcessError: 
            print(f"subprocess error")
            exit(1)
        except FileNotFoundError:
            print(f"Program {program} does not exist")
            exit(1)
             

def evaluateTestResut(expected: str, testResult: Tuple[str, float], testFile: str) -> None:
    actual = testResult[0]
    executionTime = testResult[1]
    if expected != actual:
        print(f"test {os.path.basename(testFile)} failed :(")
    else:
        print(f"test {os.path.basename(testFile)} passed! Execution time: {executionTime:.4f} s")
        

    
def main():

    argParser = ArgumentParser()
    argParser.add_argument("program", help="specify the program to test", type=str)
    argParser.add_argument("fileDir", help="specify the file directory in which the tests are", type=str)
    argv = argParser.parse_args()

    inputFiles = getInputFiles(argv.fileDir)
    executeTests(argv.program, inputFiles)    
           
if __name__ == "__main__":
    main()
