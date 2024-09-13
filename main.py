from flask import render_template, Flask

app = Flask(__name__,template_folder="/templates")

@app.get("/")
def index():
    return render_template("index.html")