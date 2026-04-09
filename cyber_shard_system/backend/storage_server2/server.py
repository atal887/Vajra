from flask import Flask, request
import os

app = Flask(__name__)

os.makedirs("storage", exist_ok=True)

@app.route("/store", methods=["POST"])
def store():
    file = request.files["file"]
    file.save(os.path.join("storage", file.filename))
    return "Stored Successfully"

@app.route("/get/<filename>")
def get_file(filename):
    return open(os.path.join("storage", filename), "rb").read()

if __name__ == "__main__":
    app.run(port=5002)