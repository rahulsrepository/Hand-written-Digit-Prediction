from flask import Flask, render_template, request, jsonify
from model import DigitPredictor

app = Flask(__name__)
predictor = DigitPredictor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    image_data = request.json['image']
    predicted_digit = predictor.predict(image_data)
    return jsonify({'prediction': int(predicted_digit)})

if __name__ == '__main__':
    app.run(debug=True)