from flask import Flask,abort,Response

app = Flask(__name__)

@app.errorhandler(404)
def handle_404_error(err):
    return "Sorry,raise 404 error errmsg = %s "% err

if __name__ == "__main__":
    app.run(debug = True)