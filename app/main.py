from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # getting the url argument
        return "hello"
    else:
        return jsonify({'Error': "This is a GET API method"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
