import os
import flask
import pickle
from flask import jsonify, request
import pandas as pd

MODEL = os.getenv('MODEL')
# MODEL = 'model.pkl'
with open(MODEL, 'rb') as f:
    lr = pickle.load(f)

# Initialize server
app = flask.Flask(__name__)


@app.route('/prediction', methods=['POST'])
def prediction():
    try:
        feature_vector = request.json['feature_vector'].split(",")
        feature_vector = pd.DataFrame(
            [int(x) for x in feature_vector]).T.to_numpy()
        pred = lr.predict(feature_vector)
        predicted_class = ""

        if (pred[0] == 0):
            predicted_class = "On Time"

        elif (pred[0] == 1):
            predicted_class = "Delay"

        return jsonify({'prediction': int(pred[0]),
                        'predicted_class': predicted_class}), 200

    except ValueError as e:
        return f"Error: {e}"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
