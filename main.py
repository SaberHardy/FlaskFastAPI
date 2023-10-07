import os
import csv
import json
from flask import Flask, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'staticfiles/uploads'
app.config['BATCH_SIZE'] = 5

# Ensure the uploads directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Global variables to hold the current batch of data and metadata
current_batch = []
batch_index = 0  # Keep track of the batch index
total_rows = 0  # Total number of rows in the CSV


def is_csv_empty():
    with open('fraudDataCopy.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        return not any(csv_reader)  # Check if there are any rows


# Load the CSV data initially
def load_csv_data():
    global current_batch, batch_index, total_rows

    if is_csv_empty():
        return  # If CSV is empty, don't load any data

    with open('FraudAnalysis.csv', 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        rows = list(csv_reader)
        total_rows = len(rows)

        start_idx = batch_index * app.config['BATCH_SIZE']
        end_idx = start_idx + app.config['BATCH_SIZE']
        current_batch = [dict(row) for row in rows[start_idx:end_idx]]
        current_batch.append(rows)
        batch_index += 1

        # Check if all data has been served, if so, stop the scheduler
        if start_idx >= total_rows:
            try:
                scheduler.shutdown()
            except RuntimeError:
                pass  # Ignore the error if the scheduler is already shut down


load_csv_data()


def reload_data():
    try:
        load_csv_data()
    except RuntimeError:
        pass


scheduler = BackgroundScheduler()
scheduler.add_job(func=reload_data, trigger='interval', seconds=5)
scheduler.start()


@app.route('/api/data', methods=['GET'])
def render_html():
    global current_batch

    # Assuming current_batch is a list of dictionaries containing the data
    return render_template('index.html', json_data=current_batch)


# ...

@app.route('/', methods=['GET'])
def get_data():
    global current_batch, total_rows

    if len(current_batch) == 0:
        if batch_index * app.config['BATCH_SIZE'] >= total_rows:
            return jsonify(message='All data has been served.')

    formatted_json_data = '\n'.join([f'    "{key}": {json.dumps(value)}' for key, value in current_batch[0].items()])
    pretty_json_data = '{\n' + formatted_json_data + '\n}'


    # Return the pretty-printed JSON response
    response = app.response_class(
        response=pretty_json_data,
        status=200,
        mimetype='application/json')
    return response


# ...


if __name__ == '__main__':
    app.run(debug=True)
