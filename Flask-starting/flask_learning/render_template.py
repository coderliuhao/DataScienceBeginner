from flask import Flask,render_template

app = Flask(__name__)

@app.route("/index")
def index():
#    return render_template("index.html",name = "liuhao",age=25)

    data = {
        "name" : "liuhao",
        "age":25,
        "dict":{"city":"korla"},
        "list":[0,1,2,3],
        "int":1
    }
    return render_template("index.html",**data)

if __name__ == "__main__":
    app.run()