from flask import Flask


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def inference() :
    return "Songdong Myoung Real DengSin Seki - Fuck you"