# Sakash Khanna
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   # <-- this fixes CORS fully

def calculate(text):
    print(text)
    return "scam"

@app.route("/getEmail", methods=["POST"])
def getEmail():
    data = request.get_json()
    if not data or "email" not in data:
        return jsonify({"error": "Invalid JSON"}), 400

    email_text = data["email"]
    result = calculate(email_text)

    return jsonify({"classification": result})

if __name__ == "__main__":
    app.run(debug=True)
