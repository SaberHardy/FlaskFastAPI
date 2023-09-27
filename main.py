from distutils.log import debug
import pandas as pd

from fileinput import filename
import pandas as pd
from flask import *
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')

# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)

# Configure upload file path flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'This is your secret key to utilize session in Flask'


@app.route('/', methods=['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':
        # upload file flask
        f = request.files.get('file')

        # Extracting uploaded file name
        data_filename = secure_filename(f.filename)

        f.save(os.path.join(app.config['UPLOAD_FOLDER'],
                            data_filename))

        session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], data_filename)

        return render_template('index2.html')
    return render_template("index.html")


@app.route('/show_data')
def showData():
    # Uploaded File Path
    data_file_path = session.get('uploaded_data_file_path', None)
    # read csv
    uploaded_df = pd.read_csv(data_file_path,
                              encoding='unicode_escape')
    # Converting to html Table
    uploaded_df_html = uploaded_df.to_html()
    return render_template('show_csv_data.html',
                           data_var=uploaded_df_html)


@app.route('/get_csv_data/<filename>', methods=['GET'])
def get_csv_data(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404

    # Read the CSV file using Pandas
    data = pd.read_csv(file_path)

    # Convert the CSV data to JSON
    json_data = data.to_json(orient='records')

    return {'data': json_data}, 200


if __name__ == '__main__':
    app.run(debug=True)
