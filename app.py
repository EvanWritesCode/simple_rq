from flask import Flask,jsonify,request
from rq import Queue
from rq.job import Job
from worker import conn
import os
import time
from tasks import tasks
from models import training_task
from persistence import persistence
import datetime

#TODO remove this
import image_classification.training_models.train as trainer

app = Flask(__name__)
#app.config.from_object(os.environ['APP_SETTINGS'])

#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#db = SQLAlchemy(app)

q = Queue(connection=conn)


@app.route('/heartbeat', methods=['GET','POST'])
def heartbeat():    
    return "up and running.. " + str(datetime.datetime.now())


@app.route('/', methods=['POST']) #['GET','POST'])
def index():
    jobId = 0
    results = {}
    if request.method == "POST":
        postedJson = request.get_json()

        #get a blank instance of a task model object
        task = training_task.training_task()
        task.taskName=postedJson["name"] if "name" in postedJson else str(datetime.datetime.now())
        task.description=postedJson["description"] if "description" in postedJson else ""
        task.taskStart = datetime.datetime.now()
        task.trainingModelId= postedJson["trainingModel"] if "trainingModel" in postedJson else 1
        task.imageLocation=postedJson["imageLocation"] if "imageLocation" in postedJson else ""
        #insert task into db
        db = persistence.TaskDAO()
        result = db.createTrainingTask(task.__dict__)
        print("db create id: ");print(result.inserted_id)
        task.taskId = result.inserted_id
        #mongoID = "ObjectId(\'" + str(task.taskId)+ "\')"
                
        job = q.enqueue(tasks.testTask, 'https://www.gutenberg.org/files/2600/2600-h/2600-h.htm',task.taskId)
        #jobId is the redis queue id
        jobId = job.get_id()        
        print("queue job id: " + str(job.get_id())) 

        task.taskQueueId=jobId
        #TODO:  update record in mongodb to reflect rqID
        db.updateTask(task)

        #debugging
        print("task object: ");print(vars(task))
        print("task object dict: "); print(task.__dict__)


        # testing egates 
        job = q.enqueue(tasks.trainModel_scratch)

        #TODO delete this
        #Testing egates model training  inline for easier debugging
        trainer.main(image_dir=imageDir)


        
    return jobId

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        return str(job.result), 200
    else:
        return "job result: " + str(job.result) + ".   Not done.  Status: " + str(job.get_status), 202


# @app.route("/queue_status/", methods=['GET'])
# def get_queue_status():
       


if __name__ == '__main__':
    app.run()