from flask import Flask,make_response,request

app = Flask(__name__)

@app.route("/get_cookie")
def getting_cookie():
    c = request.cookies.get("name")
    return c

if __name__ == "__main__":
    app.run(debug = True)