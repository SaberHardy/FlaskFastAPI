import time
import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)

# Load the initial data from the CSV file
data = pd.read_csv('staticfiles/uploads/homes.csv')
batch_size = 10  # Adjust the batch size as needed


@app.route('/file-api/data', methods=['GET'])
def get_data():
    global data
    current_data = data.head(batch_size).to_dict(orient='records')
    data = data[batch_size:]  # Move to the next batch
    if data.empty:
        # Reload the data from the CSV file when the end is reached
        data = pd.read_csv('staticfiles/uploads/homes.csv')
    return jsonify(current_data)


if __name__ == '__main__':
    # Update the data every 3 seconds
    app.run(debug=True)