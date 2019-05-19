# Dependencies
from flask import Flask, request, jsonify, render_template
from sklearn.externals import joblib
import traceback, json
import pandas as pd
import numpy as np

# Your API definition
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about.html')


#@app.route('/predict', methods=['POST'])
#def predict():
#    if lr:
#        try:
#            json_ = request.json
#            print(json_)
#            query = pd.get_dummies(pd.DataFrame(json_))
#            query = query.reindex(columns=model_columns, fill_value=0)
#
#            prediction = list(lr.predict(query))
#
#            return jsonify({'prediction': str(prediction)})
#
#        except:
#
#            return jsonify({'trace': traceback.format_exc()})
#    else:
#        print ('Train the model first')
#        return ('No model here to use')
    

@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        if lr:
            try:
                comment = request.form['features']
                data = comment.split()
                d = {}
                d['Age'] = int(data[0])
                d['Sex'] = data[1]
                d['Embarked'] = data[2]
                json_ = [json.dumps(d)]
                query = pd.get_dummies(pd.DataFrame(json_))
                query = query.reindex(columns=model_columns, fill_value=0)
                
                my_prediction = lr.predict(query)
                
                #return jsonify({'prediction': str(my_prediction)})
                return render_template('result.html',prediction = my_prediction, s = json_)
                
            except:
            
                return jsonify({'trace': traceback.format_exc()})
        else:
            print ('Train the model first')
            return ('No model here to use')
        #return render_template('result.html',prediction = my_prediction)

if __name__ == '__main__':
    try:
        port = int(sys.argv[1]) # This is for a command-line input
    except:
        port = 12345 # If you don't provide any port the port will be set to 12345

    lr = joblib.load("model.pkl") # Load "model.pkl"
    print ('Model loaded')
    model_columns = joblib.load("model_columns.pkl") # Load "model_columns.pkl"
    print ('Model columns loaded')

    app.run(port=port, debug=True)