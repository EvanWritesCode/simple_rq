from pymongo import MongoClient
import datetime


class TaskDAO:
    
    mongoServer = "localhost"
    mongoPort = 27017
    dbName="maestro"
    client = MongoClient(mongoServer,mongoPort)
    db = client[dbName]
    coll = db.trainingTasks
    
    # def __init__(self,mongoServer="localhost",mongoPort=27017,dbName="xaas"):
    #     self.client = MongoClient(mongoServer,mongoPort)
    #     self.db = client[dbName]

    def createTrainingTask(self,taskDetails):
        result = self.coll.insert_one(taskDetails)
        return result

    def markTaskAsDone(self,dbId):
        print("marking task as done "); print(str(dbId))
        
        task = self.coll.find_one({'_id': dbId})
        if task is not None:
            self.coll.update_one(
                {'_id':dbId},
                {'$set':
                    {'taskEnd': datetime.datetime.now()}
                }
            )

        else:
            # TODO bubble message up and real logging
            print("ERROR: Can not update doc.  DbID not found.  " + str(dbId))


    def updateTask(self, task):
        t = self.coll.find_one({'_id': task.taskId})
        if t is not None:
            self.coll.replace_one({'_id':task.taskId},task.__dict__)
#res = createTrainingTask()

