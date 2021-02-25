from tensorflow import keras
import tensorflow as tf
import warnings
warnings.filterwarnings("ignore")
from tensorflow.keras.preprocessing.image import ImageDataGenerator,img_to_array,array_to_img,save_img,load_img
from tensorflow.keras.models import load_model
from s3_operation import s3_class
from mongdb_operation import mongo_class
import numpy as np
import boto3




class prediction_class:
    def __init__(self):
        self.s3 = s3_class()
        self.db = mongo_class()
        self.region = "us-east-2"
        self.db_name = "predictDB"
        self.collection_name = "col1"




    def predict_from_model(self,image_path):
        try:
            # loading the trained model from directory
            model = load_model("model/inception_resnet.h5")

            # bucket
            bucket = image_path
            size = (224,224) # same size as training time taken

            # get the list of object in bucket
            lis = self.s3.getting_list_of_objs_from_buckets(self.region,bucket)

            for key in lis:
                img = self.s3.read_img_from_s3_in_RAM(self.region,bucket,key,size)

                # convert img to array
                im_array = np.array(img)

                # expend dimension
                expended_img = np.expand_dims(im_array,axis=0)

                result = np.argmax(model.predict(expended_img),axis=1)

                if result[0] == 1:
                    predict = "DOG"
                else:
                    predict = "CAT"


                record = {
                    "Imagename":key,
                    "Prediction" : predict
                }

                # insert the result into db
                self.db.insert_one_record(record,self.db_name,self.collection_name)

            # delete the all images from the bucket after push the prediction to the mongodb
            self.s3.delete_all_objects_in_bucket(self.region,bucket)


        except Exception as e:
            raise e






