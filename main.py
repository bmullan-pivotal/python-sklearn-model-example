import os
import pickle
import flask
from flask import request
from flask import Flask

app = Flask(__name__)

#getting our trained model from a file we created earlier
model = pickle.load(open("model.pkl","rb"))

# set the port dynamically with a default of 3000 for local development
cf_port = int(os.getenv('PORT', '3000'))

print("Starting application .................................................!\n")

print("port:",cf_port)

# start the app
#if __name__ == "__main__":

@app.route('/')
def home():
    return "predict-demo"

@app.route('/isAlive')
def index():
    return "true"

@app.route('/coef', methods=['GET'])
def coef():
    return flask.jsonify(model.coef_.tolist())

@app.route('/instance')
def instance():
    return "{" + " guid : " + os.environ.get('CF_INSTANCE_GUID') + ", ip:"+ os.environ.get('CF_INSTANCE_IP') + "}"

@app.route('/predict', methods=['POST'])
def predict():
    #grabbing a set of wine features from the request's body
    feature_array = request.get_json()['feature_array']

    # print(len(feature_array))    
    #our model rates the wine based on the input array
    prediction = model.predict([feature_array]).tolist()
    
    #preparing a response object and storing the model's predictions
    response = {}
    response['predictions'] = prediction
    
    #sending our response object back as json
    return flask.jsonify(response)

# app.run(host='0.0.0.0', port=port)
app.debug=True

if __name__ == '__main__':
  app.run(port=cf_port,host='0.0.0.0')
