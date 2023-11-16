from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load the initial data from the CSV file
data = pd.read_csv('data/Fraud500.csv')
batch_size = 10  # Adjust the batch size as needed


@app.route('/file-api/data', methods=['GET'])
def get_data():
    global data
    current_data = data.head(batch_size).to_dict(orient='records')

    data = data[batch_size:]  # Move to the next batch
    if data.empty:
        # Reload the data from the CSV file when the end is reached
        data = pd.read_csv('data/Fraud500.csv')
    return jsonify(current_data), 200


if __name__ == '__main__':
    # Update the data every 3 seconds
    app.run(host='0.0.0.0', debug=True)
