from flask import Flask, render_template, send_from_directory
import cadquery as cq
import os

app = Flask(__name__)

@app.route("/")
def index():
    generate_model()
    return render_template("index.html")

def generate_model():
    result = cq.Workplane("XY").box(2, 2, 1)
    os.makedirs("static", exist_ok=True)
    result.export("static/model.stl")  # This works in your CadQuery setup

@app.route("/model")
def model():
    generate_model()
    return {"status": "Model exported"}

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    app.run(debug=True)
