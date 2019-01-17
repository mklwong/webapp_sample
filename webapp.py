from flask import Flask, render_template, request, jsonify
from webapp_tools import web_api

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_filter',methods=['POST'])
def get_filter():
    data = request.get_json()
    result = jsonify(web_api.extract_options(**data))
    return result

@app.route('/get_data',methods=['POST'])
def get_data():
    data = request.get_json()
    return web_api.return_data(**data)

@app.route('/download_data',methods=['POST'])
def download_data():
    data = request.get_json()
    return web_api.return_excel_output(**data)

@app.route('/test_api',methods=['GET','POST'])
def test_api():
    return 'hello world'

if __name__ == "__main__":
    app.run(port=8000,debug=True)
