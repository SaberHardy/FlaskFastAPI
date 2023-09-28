import os
import csv
from flask import Flask, render_template, request, redirect, url_for, jsonify, json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'staticfiles/uploads'

# Ensure the uploads directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


# @app.route('/')
# def index():
#     return render_template('upload.html')


# @app.route('/upload', methods=['POST'])
# def upload():
#     file = request.files['file']
#     if file and file.filename.endswith('.csv'):
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
#         return redirect(url_for('display_api', filename=file.filename))
#     else:
#         return "Please upload a valid CSV file."

@app.route('/file/api-data', methods=['POST', 'GET'])
def display_api():
    api_data = []
    with open('staticfiles/uploads/homes.csv', 'r') as csvfile:
        # next(csv)
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            api_data.append(dict(row))

    # Pass the data to the template
    return jsonify(api_data)


if __name__ == '__main__':
    app.run(debug=True)
