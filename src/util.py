# Miscellanious utility functions
import oead
import pathlib
from platform import system
import os
from wildbits._sarc import *
from pymsyt import Msbt
import time
import UnityPy
import json
import string

# Checks if a directory exists and makes it if not
def findMKDir(checkDir):
    if isinstance(checkDir, pathlib.Path):
        checkDir = checkDir
    else:
        try:
            checkDir = pathlib.Path(checkDir)
        except:
            print('Failed to make the pathlib instance :(')
            return
    if checkDir.exists():
        return checkDir
    else:
        if ("." in pathlib.PurePath(checkDir).name):
            checkFile = checkDir
            checkDir = checkDir.parents[0]
            checkDir.mkdir(parents=True, exist_ok=True)
            checkFile.touch()
            return checkFile
        checkDir.mkdir(parents=True, exist_ok=True)
        return checkDir

def get_data_dir() -> Path:
    if system() == "Windows":
        data_dir = pathlib.Path(os.path.expandvars("%LOCALAPPDATA%")) / "AiTextGen"
    else:
        data_dir = pathlib.Path.home() / ".config" / "AiTextGen"
    if not data_dir.exists():
        data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

def getConfigData():
    dataDir = get_data_dir()
    configPath = dataDir / 'config.json'
    with open(configPath, 'rt') as readConfig:
        config = json.loads(readConfig.read())
    return config
