from flask import Flask,request,g

app = Flask(__name__)

@app.route("/")
def hello_world(request):
    #data = request.json
    g.username = "liuhao"
    g.passworld = "123"
    return "hello world"

if __name__ == "__main__":
    app.run()