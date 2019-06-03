
import requests
from pymongo import MongoClient
from persistence import persistence
import time

#from bxingest.egate_classifier.egate import Egate
#from image_classification.training_models.train import 
import image_classification.training_models.train as trainer
import tensorflow as tf
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

def trainMNIST_scratch():
    pass

def trainModel_scratch(imageDir="../image_classification/images"):
    # python tensorflow/examples/image_retraining/retrain.py  --image_dir ~/flower_photos
    #trainer.main(image_dir=imageDir)
    outdir = "image_classification/output"
    flip_left_right = False #default= False
    how_many_training_steps = 4000  #default = 4000
    learning_rate = .01 #default = .01
    model_dir = '/tmp/imagenet' #default =/tmp/imagenet
    random_crop = 0 #default = 0
    architecture = 'inception_v3'  #default = inception_v3
    
    #set the argparser flags since we are not calling from command line
    flags = Namespace(architecture=architecture,
                     bottleneck_dir="{}/bottlenecks".format(outdir),
                     eval_step_interval=10,
                     final_tensor_name='final_result',
                     flip_left_right=flip_left_right,
                     how_many_training_steps=how_many_training_steps,
                     image_dir=imageDir,
                     intermediate_output_graphs_dir='/tmp/intermediate_graph/',  
                     intermediate_store_frequency=0,
                     learning_rate=learning_rate,
                     model_dir=model_dir,
                     output_graph='{}/retrained_graph.pb'.format(outdir),
                     output_labels='{}/retrained_labels.txt'.format(outdir),
                     print_misclassified_test_images=False,
                     random_brightness=0,
                     random_crop=random_crop,
                     random_scale=0,
                     summaries_dir='{}/training_summaries/{}'.format(outdir,architecture),
                     test_batch_size=-1,
                     testing_percentage=10,
                     train_batch_size=100,
                     validation_batch_size=100,
                     validation_percentage=10)
    
    trainer.invoke(flags_ = flags,unparsed_=[])

    #tf.app.run(main=trainer.main, argv=[sys.argv[0]] + unparsed)