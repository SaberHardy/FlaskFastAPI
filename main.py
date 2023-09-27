from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/api/data', methods=['GET'])
def get_all_data():
    data = [{'title': 'data 1'}, {'title2': 'data 2'}]
    return jsonify({'data': data})


@app.route('/api/data/<int:data_id>', methods=['GET'])
def get_data(data_id):
    data = {'title': f'Data {data_id}'}
    return jsonify({'book': data})


if __name__ == '__main__':
    app.run(debug=True)
