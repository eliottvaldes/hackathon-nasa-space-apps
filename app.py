from flask import Flask, request

app = Flask(__name__)

# @app.route("/query")
# def query():
#     data = request.args.get('data', '')
#     print("GOT")
#     print(data)
#     return data

@app.route("/")
def hello_world():
    return "<p>Hola universo!</p>"

if __name__ == '__main__':
    app.debug = True
    app.run()

