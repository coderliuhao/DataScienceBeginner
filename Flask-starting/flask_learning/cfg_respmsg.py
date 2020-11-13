from flask import Flask,make_response

app = Flask(__name__)

@app.route("/index")
def index():
#    return ("index page",400,[("itcast","python"),("city","korla")])
#    return ("index page",666,[("itcast","python"),("city","korla")])
    resp = make_response("index page")
    resp.status = "666"
    resp.headers["city"] = "korla"
    return resp


if __name__ == "__main__":
    app.run(debug = True)