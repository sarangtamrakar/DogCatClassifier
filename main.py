from flask import Flask,request,Response,jsonify
from flask_cors import CORS,cross_origin
from predict import prediction_class


app = Flask(__name__)

CORS(app)

@app.route("/predict",methods=["POST"])
@cross_origin()
def predictRoute():
    if request.method == "POST":
        bucket_name = request.json["bucket"]

        # calling predict api
        obj = prediction_class()
        obj.predict_from_model(bucket_name)

    return Response("prediction Completed")


if __name__ == "__main__":
    app.run(debug=True)


