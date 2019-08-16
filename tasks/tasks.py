
import requests
from pymongo import MongoClient
from persistence import persistence
import time

from argparse import Namespace

def trainModel(modelKey,imageLocation):
    pass

def testTask(p,dbId):
    print("running task testTask with param " + str(p))
    resp = requests.get(p)
    numWords = len(resp.text.split())

    #make it take longer
    time.sleep(10)

    #write finished to db
    db = persistence.TaskDAO()
    db.markTaskAsDone(dbId)

    return numWords
